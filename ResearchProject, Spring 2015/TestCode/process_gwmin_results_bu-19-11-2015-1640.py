# Call get inputs for each peer_id
# get gwmin for each peer id
import os, glob
import config
from gwmin import get_results
from get_top_scus import get_best_scus, flatten_lists
from get_ngram import get_ngram
import numpy

pan_peer_map = {
1: "881197544.pan",
2: "881520246.pan",
3: "881745597.pan",
4: "883076719.pan",
5: "883178560.pan",
6: "883690042.pan",
7: "883707584.pan",
8: "884203758.pan",
9: "885640486.pan",
10: "885925399.pan",
11: "887016576.pan",
12: "887051477.pan",
13: "887582679.pan",
14: "887645490.pan",
15: "887897589.pan",
16: "887898669.pan",
17: "888277107.pan",
18: "888717500.pan",
19: "889198081.pan",
20: "889920032.pan"
}
cmd = "perl process-pans.pl '/export/projects/nlp/pyramid/backup/pyramids/pan/WhatIsMatter/12_10_09_Matter/881745597.pan' > '/export/projects/nlp/pyramid/backup/pyramids/pan/parsed/op_881745597.pan'"

pan_file_path = config.pan_file_path


def generate_pan_map():
	global pan_peer_map
	pan_file_path = config.pan_file_path
	pan_peer_map = {}
	peer_id = 1
	for file_path in glob.glob(os.path.join(pan_file_path, '*.pan')):
		pan_file_name = file_path[len(pan_file_path)+1:]
		# print 'pfn,' pan_file_name
		pan_peer_map[peer_id] = pan_file_name
		peer_id = peer_id + 1
		parsed_pan_file = config.pan_file_path_parsed+"/op_" + pan_file_name
		if not os.path.exists(config.pan_file_path_parsed):
		    os.makedirs(config.pan_file_path_parsed)
		    print "Creating directory", config.pan_file_path_parsed

		cmd = "perl process-pans.pl '"+ file_path + "' > '"+parsed_pan_file+"'"
		print cmd
		os.system(cmd)
	for k,v in pan_peer_map.iteritems():
		print k,v
	return pan_peer_map

# generate_pan_map()


def get_unique_values(d):
	val_list = []
	for value in d.values():
		val_list.extend(value[0])
	return set(val_list)


def get_stats(val_list):
	"""Get mean, SD & variance of the list values"""
	mean = numpy.mean(val_list)
	std = numpy.std(val_list)
	var = numpy.var(val_list)
	print "==>  MEAN:", mean
	print  "==> STD:" , std
	print  "==> VAR:" , var
	return [mean, std, var]


def compute_recall(orig_uq, d_comp):
	"""Compute recall between two dictionaries, original & computed"""
	# orig_uq = get_unique_values(d_orig)
	# orig_uq = get_orig_pan_scores(peer_id)
	comp_uq = get_unique_values(d_comp)
	intersection_set = orig_uq.intersection(comp_uq)
	return float(len(intersection_set))/float(len(orig_uq))



def generate_gwmin_input(best_scus):
	Y_dict = {}
	key_int = 1
	for k,v in best_scus.iteritems():
		for scu_set in v:
			scu_set.append(-1 * k)
			# print 'k,v ', key_int, scu_set, k
			Y_dict[key_int] = scu_set
			key_int = key_int + 1
	for k,v in Y_dict.iteritems():
		print str(k) + ":",  v
		print ","
	return Y_dict


def process_results(result):
	sen_result = {} # Our allocation of scu_id to sen_id
	for value in result.values():
		for scu in reversed(value):
			if int(scu) < 0:
				sen_id = scu*-1
				break
		value.remove(scu)
		sen_result[sen_id] = value
	print '---Our results--'
	for k,v in sen_result.iteritems():
		print k,v
	print '-----'
	return sen_result



def get_orig_scores(peer_id):
	"""For a given peer id, returns original scores from pan-files pr.st which contains sen_id mapping"""
	pan_file_path = "pan-files/parsed/op_"+pan_peer_map[peer_id].strip()+".pr.st"
	# print pan_file_path
	with open(pan_file_path) as pan_file:
		orig_score = {}
		for line in pan_file:
			line_sp = line.split("\t")
			sen_id, scu_id = line_sp[1], int(line_sp[2])
			if sen_id in orig_score:
				orig_score[sen_id].append(scu_id)
			else:
				orig_score[sen_id] = [scu_id]
		print '--orig-- : '+str(peer_id)
		for k,v in orig_score.iteritems():
			print k,v
	return orig_score


def get_orig_pan_scores(peer_id):
	""" Retrieves the scores from Becky's script output files : 'op_*.pan'
	Eg sen: 105	4	You can be sure that everything in the world has matter
	"""
	generate_pan_map()
	pan_file_path = os.path.join(config.pan_file_path_parsed, "op_"+pan_peer_map[peer_id].strip())
	print pan_file_path
	with open(pan_file_path) as pan_file:
		orig_score = []
		for line in pan_file:
			line_sp = line.split("\t")
			if line_sp[0].isdigit():
				scu_id = int(line_sp[0])
				if scu_id not in orig_score:
					orig_score.append(scu_id)
	print orig_score		
	return set(orig_score)

# get_orig_pan_scores(1)


def compute_precision(orig_uq, d_comp):
	"""Compute recall between two dictionaries, original & computed"""
	# orig_uq = get_unique_values(d_orig)
	comp_uq = get_unique_values(d_comp)
	intersection_set = orig_uq.intersection(comp_uq)
	return float(len(intersection_set))/float(len(comp_uq))


def compute_fmeasure(recall, precision):
	""" F-measure = 2 * ((precision * recall)/(precision + recall)) """
	f_measure = 2 * ((precision * recall)/(precision + recall))
	return f_measure


def generate_all_best_scus(pyr_id, scu_fp, n, best_scu_path_base=""):
	"""
	n : The max no. of candidate scu-sets to be extracted from the files | 
	best_scu_path :  path to the candidate-scu's generated. This is processed as an input to the 
	'pyr, peer' : scu - > sen allocation function
	"""
	# n = 3
	if best_scu_path_base == "":
		best_scu_path_base = 'Sentences/Unique_Sets_new/12_10_09_MATTER.pyr/'
	all_scus = {}
	for peer_id in xrange(1,21):
		all_scus[peer_id] = {}
	p, r, f = [], [], []
	for peer_id in xrange(1,21):
		wtd_files_path = str(peer_id)+'/new_wtd_files/'
		best_scu_path =  os.path.join(best_scu_path_base, wtd_files_path)
		our_results, peer_scus = compute_gwmin_scores(pyr_id, scu_fp, peer_id, n, best_scu_path)
		all_scus[peer_id] = peer_scus
		# orig_results = get_orig_scores(peer_id)
		orig_results = get_orig_pan_scores(peer_id)
		recall = compute_recall(orig_results, our_results)
		precision = compute_precision(orig_results, our_results)
		fm = compute_fmeasure(recall, precision)
		print "==>Recall : ", recall
		print "==>Precision : ", precision
		print "==> F-measure", fm
		p.append(precision)
		r.append(recall)
		f.append(fm)
	print 'Final results =>'
	print 'precision:', get_stats(p)
	print 'recall:', get_stats(r)
	print 'f-measure', get_stats(f)


def get_analytics(peer_id, our_results):
	orig_results = get_orig_pan_scores(peer_id)
	recall = compute_recall(orig_results, our_results)
	precision = compute_precision(orig_results, our_results)
	fm = compute_fmeasure(recall, precision)
	print "==>Recall : ", recall
	print "==>Precision : ", precision
	print "==> F-measure", fm
	return recall, precision, fm



"""
--our peer-id:--2
---Our results--
1 [145]
3 [101, 102]
5 [103, 120]
6 [146, 119]
7 [108, 100]
8 [109]
"""

def get_write_format(values):
	"""
	1 [[105, 129], ['are what all objects', 'and substances are'], [4, 2]]
	"""
	final_str = ""
	for i in xrange(len(values)):
		print values[i]
		list_str = [str(each).rstrip('\n') for each in values[i]]
		res_str = ', '.join(list_str)
		final_str = final_str + res_str + "\t|\t"
	return final_str


def write_results(pyr_id, peer_id, results_dict, results_path = ""):
	"""
	Given a results dictionary, print it in the results file
	1 [[105, 129], ['are what all objects', 'and substances are'], [4, 2]]
	"""
	if results_path == "":
		print "Setting default result path"
		results_path = os.path.join("Results", str(pyr_id), str(peer_id))
	final_sum = 0

	with open(results_path, 'w') as results:
		for sen_id, scus in results_dict.iteritems():
			final_sum = final_sum + sum(scus[2])
			write_line = str(sen_id) + " : " + get_write_format(scus)
			results.write(write_line + "\n")
		results.write("TOTAL SCORE:" + str(final_sum))


def compute_gwmin_scores(pyr_id, scu_file_path, peer_id, n, segmentations_file_path, best_scu_path=""):
	"""Gets all the candidate scus for that peer & processes it into required input format | 
	Passes that as input to gwmin and obtains output"""
	n = 3
	peer_scus = {}
	if best_scu_path == "":
		best_scu_path = 'Sentences/Unique_Sets_new/12_10_09_MATTER.pyr/'+str(peer_id)+'/new_wtd_files/'
	temp_scus = get_best_scus(int(n), peer_id, best_scu_path)
	for k,v in temp_scus.iteritems():
		peer_scus[int(k)] = v
	gr = generate_gwmin_input(peer_scus)
	max_set = get_results(2, gr, scu_file_path, pyr_id)
	print "--our--"+str(peer_id)
	our_results = process_results(max_set)
	modified_results = get_ngram(segmentations_file_path, best_scu_path, our_results, scu_file_path, pyr_id)
	for k,v in modified_results.iteritems():
		print k,v 
	
	results_path = os.path.join(config.results_path, str(pyr_id))
	if not os.path.exists(results_path):
		os.makedirs(results_path)
		print "Creating directory", results_path
	write_results(pyr_id, peer_id, modified_results, os.path.join(results_path, str(peer_id)+".output"))
	return our_results, peer_scus




## -- ##
# import os, config
# scu_file_path = os.path.join(config.scu_path, "scu")
output_filtered_score_path = 'Sentences/Unique_Sets_new/12_10_09_MATTER.pyr/5/new_wtd_files/'
segmentations_file_path = 'Sentences/Unique_Sets_new/12_10_09_MATTER.pyr/5/'
# pyr_id = '12_10_09_MATTER.pyr'
scu_file_path = os.path.join(config.scu_path, 'scu')
compute_gwmin_scores('12_10_09_MATTER.pyr', scu_file_path, 6, 3, segmentations_file_path)
# generate_all_best_scus('12_10_09_MATTER.pyr', scu_file_path, 3)
## -- ##
# Once recvd in this form:
"""
15 [136, -7]
9 [138, -4]
26 [113, -12]
5 [134, 110, -2]
29 [107, 116, -13]
11 [159, 137, -5]
20 [109, 120, -10]
7 [106, -3]
1 [105, -1]
25 [115, 103, -11]
18 [119, -8]
14 [100, -6]
"""
#process it.



"""
Final op:
1 [105]
2 [134, 110]
3 [106]
4 [138]
5 [159, 137]
6 [100]
7 [136]
8 [119]
10 [109, 120]
11 [115, 103]
12 [113]
13 [107, 116]
"""

# rs = process_results(a)
# for k,v in rs.iteritems():
# 	print k,v




"""
for k,v in all_scus.iteritems():
	for ky, val in v.iteritems():
		print k, ky, val

	# print 'Avg recall =>', float(tr)/float(20)
	# print 'Avg precision =>', float(tp)/float(20)
	# print 'Avg f-measure =>', float(tf)/float(20)
"""