# !/usr/local/bin/python
import itertools, glob, os, sys, numpy
from genCS_stats import *
"""For each segment, extract scu's associated with their n-grams, generate it's permutations, & select that scu - list with the highest score"""

scu_dict = {}

def getSCU(pyr_name, scu_doc_path):
	""" <scu_id> : <weight> 
	The condition (1) indicates that, scu has been completed for that pyramid in 'scu - doc' and
	new pyramid lines have started. Hence, we can break out of the loop now """
	print "Starting SCU generation "
	rfile = open(scu_doc_path)
	rf_lines = rfile.readlines()
	started_pyr = False
	for each_line in rf_lines:
		line_arr = each_line.split('\t')
		scu_pyr_name, scu_id, scu_score, scu_text = line_arr[0].strip(), int(line_arr[1]), int(line_arr[2]), line_arr[3].strip()
		if(scu_pyr_name.strip() == pyr_name.strip()): # i.e if required pyramid's scu's found #
			started_pyr = True # Started reading scu's for that pyramid
			if(scu_id not in scu_dict):
				scu_dict[scu_id] = scu_score
		elif ((scu_pyr_name.strip() != pyr_name.strip()) and (started_pyr)):
			# (1 )
			break
	print 'SCU Dict generation complete'
	return scu_dict


# # Step 1 # Function call | ** -- PYRAMID ID as input -- **
# scu_dict = getSCU("12_10_09_MATTER.pyr", "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/scu_YINGHUI/scu") ## Uncomment this 

#####################################################################################################################

# Step 2 : Extract ng_dict for that (doc_id, peer_id) from genCS.py | ** -- PYRAMID ID, PEER_ID as input -- ** 
# ng_dict = gen_cos_sim("12_10_09_MATTER.pyr", 1, 1)  # Example call!

#####################################################################################################################

# Step 3: For each unique segment, extract best scu's associated with their n-grams #

def compute_score(list_scu_ids):
	""" Given the list of unique scu_id's of the form [134, 1], return the sum of their scores """
	sum_scu = 0
	for scu_id in list_scu_ids:
		sum_scu += scu_dict[scu_id]
	return sum_scu


def get_mean(arr):
	""" Computes mean/average of elements of the list """
	if len(arr)>0:
		return float(sum(arr))/float(len(arr))
	return 0


def compute_wtd_score(list_scu_ids, cos_sim_values, ng_len_list):
	""" Given the list of unique scu_id's of the form [134, 1], retrieve their individual scu scores - [2,3]
	Passed their cos_sim_values - [0.7, 0.67] and their ng_len_list (i.e the length of the ngrams the scu-id's matched), get the avg-ng-length
	return the sum of their scores """
	list_scu_weights = [scu_dict[scu_id] for scu_id in list_scu_ids]
	wtd_scores_list = [a*b for a,b in zip(list_scu_weights, cos_sim_values)]
	if len(wtd_scores_list)>0:
		return sum(wtd_scores_list)/len(wtd_scores_list)
	return 0


def max_scu_list(seg_ng):
	""" For a given <list of n-grams> broken from a unique set/segments, return the scu combo with the max score 
	Adding cosine similarity ###print as well.."""
	scus_list, cos_list, nglen_list = [], [], []
	for each_ng in seg_ng:
		if each_ng.strip() in ng_dict:
			scus_list.append(ng_dict[each_ng.strip()][0])
			cos_list.append(ng_dict[each_ng.strip()][1])
			nglen_rep = list(itertools.repeat(len(each_ng.strip().split(" ")), len(ng_dict[each_ng.strip()][0])))
			nglen_list.append(nglen_rep)
	
	scus = list(itertools.product(*scus_list))
	cos_sim = list(itertools.product(*cos_list))
	ng_len = list(itertools.product(*nglen_list))
	scu_cs = {}
	for i in xrange(len(scus)): # {scu_id_combo : [(cos_sim_combo), (ng_len_combo)]} 
		scu_cs[scus[i]] = [cos_sim[i], ng_len[i]]

	scu_uel = [each_el for each_el in scus if len(set(each_el)) == len(each_el)] # This removes any scu_id combos with repeated scu_id's
	uq_list = [(scu_uel_i, compute_wtd_score(scu_uel_i, cos_sim[scus.index(scu_uel_i)], ng_len[scus.index(scu_uel_i)])) for scu_uel_i in scu_uel]

	if len(scu_uel) == 0:
		return [[(),0], {}]

	max_value = max(uq_list, key = (lambda x : x[1]))
	max_key = max_value[0] # This is a 'set' of unique scu id's
	# Will look thru scu_cs, look for dictionary keys having same (&only these el)
	new_d = {} # {scu_id_combo : cos_sim_combo, len_ng_combo}
	for each_key in scu_cs:
		if ((len(set(each_key)) == len(set(max_key)) == len(set(each_key).intersection(set(max_key))))):
			for i in xrange(len(each_key)): 
				if each_key[i] not in new_d:
					# {scu_id_combo 	: 	cos_sim_combo, len_ng_combo}
					new_d[each_key[i]] = [[scu_cs[each_key][0][i]], [scu_cs[each_key][1][i]]]
				elif ((each_key[i] in new_d) and (scu_cs[each_key][0][i] not in new_d[each_key[i]][0])):
					new_d[each_key[i]][0].append(scu_cs[each_key][0][i])
					new_d[each_key[i]][1].append(scu_cs[each_key][1][i])			
	return [max_value, new_d]


def get_stats(new_d):
	"""Get mean & SD of the cosine similarity list values"""
	val_list = []
	for k,v in new_d.iteritems():
		val_list.extend(v[0])
	mean = numpy.mean(val_list)
	std = numpy.std(val_list)
	return [mean, std]


def gen_cos_sim_str(max_scus, new_d):
	"""Given the max_scu_id's list & a dictionary of those <scu_ids : cos_sim>, generate the string"""
	""" mean | std | cos_sim values """
	# max_scus [104, 100, 101, 102, 103]
	# new_d {104: [[0.78], [1]], 100: [[0.687, 0.89], [3, 2]], 101: [[0.82], [1]], 102: [[0.69, 0.6069], [2, 3]], 103: [[0.72], [1]]}
	mean, std = 0.0, 0.0
	if not bool(new_d):
		scu_ngl = 0.0
	if bool(new_d): # Check if dict empty
		mean, std = get_stats(new_d)[0], get_stats(new_d)[1]
	stats_str =  str(mean)+ '\t | \t' + str(std) + '\t | \t'

	cos_str, scu_ngl = "", ""
	for scu in max_scus:
		scu_cos_str, scu_ng_len = "", ""
		for each_cos_val in new_d[scu][0]:
			scu_cos_str += str(each_cos_val) + ", "
		for each_ng_len in new_d[scu][1]:
			scu_ng_len += str(each_ng_len) + ", "
		scu_cos_str, scu_ng_len = scu_cos_str[:-2], scu_ng_len[:-2]
		cos_str += scu_cos_str + '\t'
		scu_ngl += scu_ng_len + '\t'
	return scu_ngl + '| \t' + stats_str + cos_str[:-1]



def score_sentences(doc_id, peer_id, path = ""):
	if path == "":
		path = "Sentences/Unique_Sets_new/"+str(doc_id)+"/"+str(peer_id)
	for filename in glob.glob(os.path.join(path, '10.dat')):
		sen_id = filename[len(path)+1:filename.find('.dat')]
		rfile_path = path + "/" + str(sen_id) + ".dat"
		wfile_path = path + "/" + str(sen_id) + ".best.scu.wtd.new2610" 
		bestscu_file = open(wfile_path, 'w')
		print "Starting sentence : "+ str(sen_id)
		with open(rfile_path) as segments_file:
			for unique_set_i in segments_file:
				seg_sentence = unique_set_i.split('\t')
				uq_id = seg_sentence[0].strip()
				seg_ng = unique_set_i.split(",")
				max_scul = max_scu_list(seg_ng)
				# Output format : [max(uq_list, key = (lambda x : x[1])), new_d]
				max_scus = max_scul[0][0]
				max_scu_score = max_scul[0][1]
				max_cosine_sim = max_scul[1] # This is new_d
				scu_len = [max_cosine_sim[scu_id][1][0] for scu_id in max_cosine_sim]
				avg_ng_len = get_mean(scu_len)
				wtd_score = max_scu_score * avg_ng_len # ** #
				#print "----------->>>>", max_scus, max_scu_score, max_cosine_sim, avg_ng_len, wtd_score
				cos_sim_str = gen_cos_sim_str(max_scus, max_cosine_sim) 
				bestscu_file.write(uq_id + "\t|\t"+ ", \t".join(map(str, (max_scus))) + "\t|\t"+ str(wtd_score)+ "\t|\t"+ str(max_scu_score) +"\t|\t"+ cos_sim_str +'\n')
		print "Completed sentence : "+str(sen_id)


def main(doc_id, peer_id, ng_parameter, scu_file = ""):
	# Step 1 # Function call | ** -- PYRAMID ID as input -- **
	# scu_dict = getSCU("12_10_09_MATTER.pyr", "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/scu_YINGHUI/scu")
	scu_dict = getSCU(doc_id, scu_file)
	# Step 2 : Extract ng_dict for that (doc_id, peer_id) from genCS.py | ** -- PYRAMID ID, PEER_ID, Mean/Median/Mode parameter as input -- ** 
	# ng_dict = gen_cos_sim("12_10_09_MATTER.pyr", 1, 1)  # Example call!
	ng_dict = gen_cos_sim(doc_id, peer_id, ng_parameter)
	score_sentences(doc_id, peer_id)



# def usage():
# 	print """ Error in usage. \n This script is used to generate the:
# 	(1)sen_file for segment generation (2)corrected summary.st (3)text.tok files for n-gram file generation. \n
# 	Correct usage : 'script-name.py text.tok summary.st action-number output-filename' """



if __name__ == '__main__':
	# doc_id = sys.argv[1]
	# peer_id = int(sys.argv[2])
	# scu_file = sys.argv[3]
	# ng_parameter = int(sys.argv[4])
	doc_id, peer_id = "12_10_09_MATTER.pyr", 1
	scu_file = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/scu_YINGHUI/scu"
	ng_parameter = 1
	main(doc_id, peer_id, ng_parameter, scu_file)


