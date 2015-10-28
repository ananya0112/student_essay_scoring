# !/usr/local/bin/python
import itertools, glob, os, sys, numpy
from genCS import *
# from generate_intersects import *
"""For each segment, extract scu's associated with their n-grams, generate it's permutations, & select that scu - list with the highest score"""

#####################################################################################################################

# Step 1 : Generate SCU dictionary for that pyramid/document name
# Eg : "scu" document sentence := 
# 12_10_09_MATTER.pyr	100	5	Chemical properties are observed when matter changes into a new type of matter with different properties.

#####################################################################################################################

scu_dict = {}

def getSCU(pyr_name, scu_doc_path):
	""" <scu_id> : <weight> """
	###print "Starting SCU generation "
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
			# The second condition indicates that, scu has been completed for that pyramid in 'scu - doc' and
			# new pyramid lines have started. Hence, we can break out of the loop now 
			break
	###print "SCU generation complete"
	print scu_dict
	return scu_dict


# Step 1 # Function call | ** -- PYRAMID ID as input -- **
scu_dict = getSCU("12_10_09_MATTER.pyr", "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/scu_YINGHUI/scu") ## Uncomment this 

#####################################################################################################################

# Step 2 : Extract ng_dict for that (doc_id, peer_id) from genCS.py | ** -- PYRAMID ID, PEER_ID as input -- ** 
ng_dict = gen_cos_sim("12_10_09_MATTER.pyr", 1)  # Example call!

#####################################################################################################################

# Step 3: For each unique segment, extract best scu's associated with their n-grams #

def compute_score(list_scu_ids):
	""" Given the list of unique scu_id's of the form [134, 1], return the sum of their scores """
	sum_scu = 0
	for scu_id in list_scu_ids:
		sum_scu += scu_dict[scu_id]
	return sum_scu


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

	scu_uel = [list(set(each_el)) for each_el in scus]
	uq_list = [(list(x), compute_score(list(x))) for x in set(tuple(x) for x in scu_uel)]
	# print "MAX ------- ", max(uq_list, key = (lambda x : x[1]))

	max_value = max(uq_list, key = (lambda x : x[1]))
	max_key = max_value[0] # This is a 'set' of unique scu id's
	# Will look thru scu_cs, look for dictionary keys having same (&only these el)
	new_d = {}
	for each_key in scu_cs:
		if ((len(set(each_key)) == len(set(max_key)) == len(set(each_key).intersection(set(max_key))))):
			# print "Matching : ",each_key, max_key
			for i in xrange(len(each_key)): # {scu_id_combo : cos_sim_combo, len_ng_combo}
				if each_key[i] not in new_d:
					# {scu_id_combo 	: 	cos_sim_combo, len_ng_combo}
					new_d[each_key[i]] = [[scu_cs[each_key][0][i]], [scu_cs[each_key][1][i]]]
				elif ((each_key[i] in new_d) and (scu_cs[each_key][0][i] not in new_d[each_key[i]][0])):
					new_d[each_key[i]][0].append(scu_cs[each_key][0][i])
					new_d[each_key[i]][1].append(scu_cs[each_key][1][i])
	# print "new_d", new_d				
	return [max(uq_list, key = (lambda x : x[1])), new_d]
	# [unique scu id's with scores, cosine similarities for those scu's (not unique)]


def get_stats(new_d):
	"""Get mean & SD of the cosine similarity list values"""
	val_list = []
	for k,v in new_d.iteritems():
		val_list.extend(v[0])
	# print "v list ", val_list
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


doc_id, peer_id = "12_10_09_MATTER.pyr", 1
# sen_id = 1
path = "Sentences/Unique_Sets/"+str(doc_id)+"/"+str(peer_id)
scu_set = {}  #{<Sen_id> : [<unique hashset of all scu>]}#

# For each sentence within a pyr-peer directory --> for each unique set .. #
# Init the scu_set # HARDCODING #
for i in xrange(1,10):
	scu_set[i] = []

scu_sen = {} # This is a dictionary of the <scu_id:[sen_id]>

##

for filename in glob.glob(os.path.join(path, '*.dat')):
	sen_id = filename[len(path)+1:filename.find('.dat')]
	rfile_path = path + "/" + str(sen_id) + ".dat"
	wfile_path = path + "/" + str(sen_id) + ".best.scu.new1"
	bestscu_file = open(wfile_path, 'w')
	print "Starting sentence : "+ str(sen_id)
	with open(rfile_path) as segments_file:
		for unique_set_i in segments_file:
			seg_sentence = unique_set_i.split('\t')
			uq_id = seg_sentence[0].strip()
			seg_ng = unique_set_i.split(",")
			max_scul = max_scu_list(seg_ng)
			# [max(uq_list, key = (lambda x : x[1])), new_d]
			max_scus = max_scul[0][0]
			max_scu_score = max_scul[0][1]
			max_cosine_sim = max_scul[1]
			# print "----------->>>>", max_scus, max_scu_score, max_cosine_sim

			##
			for each_scu in max_scus:
				if each_scu not in scu_sen:
					scu_sen[each_scu] = [sen_id]
				elif ((each_scu in scu_sen) and (sen_id not in scu_sen[each_scu])):
					scu_sen[each_scu].append(sen_id)

			cos_sim_str = gen_cos_sim_str(max_scus, max_cosine_sim) 
			scu_set[int(sen_id)].extend(max_scus)
			bestscu_file.write(uq_id + "\t|\t"+ ", \t".join(map(str, (max_scus))) + "\t|\t"+ str(max_scu_score) +"\t|\t"+ cos_sim_str +'\n')
for each_key in scu_set:
	scu_set[each_key] = set(scu_set[each_key])

##


#####################################################################################################################
#Pass no of sentences as arguments, create a square matrix of intersection sets | nrow = ncol = no_sen + 1

# no_sen = len(scu_set) + 1 #(2 + 1)

##
# intersect_mat = getIntersections(10, scu_set)
# # print "intersect_mat"
# for i in range(10):
# 	for j in range(10):
# 		sys.stdout.write(str(intersect_mat[i][j]) + '\t')
# 	sys.stdout.write('\n') 
##


#####################################################################################################################


