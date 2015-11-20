# Back up on May 5, 2015 #

# !/usr/local/bin/python
import itertools, glob, os, sys
from genCS import *
from generate_intersects import *
"""For each segment, extract scu's associated with their n-grams, generate it's permutations, & select that scu - list with the highest score"""

#####################################################################################################################

# Step 1 : Generate SCU dictionary for that pyramid/document name
# Eg : "scu" document sentence := 
# 12_10_09_MATTER.pyr	100	5	Chemical properties are observed when matter changes into a new type of matter with different properties.

#####################################################################################################################

scu_dict = {}

def getSCU(pyr_name, scu_doc_path):
	""" <scu_id> : <weight> """
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
			# The second condition indicates that, scu has been completed for that pyramid in 'scu - doc' and
			# new pyramid lines have started. Hence, we can break out of the loop now 
			break
	print "SCU generation complete"
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
	""" For a given <list of n-grams> broken from a unique set/segments, return the scu combo with the max score """
	scus_list, cos_list = [], [] # List of scu lists #
	for each_ng in seg_ng:
		if each_ng.strip() in ng_dict:
			scus_list.append(ng_dict[each_ng.strip()][0])

			# #
			cos_list.append(ng_dict[each_ng.strip()][1])
			# #
	scus = list(itertools.product(*scus_list))

	# #
	cos_sim = list(itertools.product(*cos_list))

	scu_cs = {}
	for i in xrange(len(scus)):
		if (scus[i] not in scu_cs):
			scu_cs[scus[i]] = [cos_sim[i]]
		elif ((scus[i] in scu_cs) and (cos_sim[i] not in scu_cs[scus[i]])):
			scu_cs[scus[i]].append[cos_sim[i]]
			print "there"
		elif ((scus[i] in scu_cs) and (cos_sim[i] in scu_cs[scus[i]])):
			print "there"

	print "scu_cs", scu_cs
	# #
	scu_uel = [list(set(each_el)) for each_el in scus]
	uq_list = [(list(x), compute_score(list(x))) for x in set(tuple(x) for x in scu_uel)]
	# print "MAX ------- ", max(uq_list, key = (lambda x : x[1]))
	return max(uq_list, key = (lambda x : x[1]))


doc_id, peer_id = "12_10_09_MATTER.pyr", 1
# sen_id = 1
path = "~/Unique_Sets/"+str(doc_id)+"/"+str(peer_id)
scu_set = {}  #{<Sen_id> : [<unique hashset of all scu>]}#

# For each sentence within a pyr-peer directory --> for each unique set .. #

# Init the scu_set # HARDCODING #
for i in xrange(1,10):
	scu_set[i] = []

scu_sen = {} # This is a dictionary of the <scu_id:[sen_id]>

for filename in glob.glob(os.path.join(path, '*.dat')):
	sen_id = filename[len(path)+1:filename.find('.dat')]
	rfile_path = path + "/" + str(sen_id) + ".dat"
	wfile_path = path + "/" + str(sen_id) + ".best.scu"
	bestscu_file = open(wfile_path, 'w')
	print "Starting sentence : "+ str(sen_id)
	with open(rfile_path) as segments_file:
		for unique_set_i in segments_file:
			seg_sentence = unique_set_i.split('\t')
			uq_id = seg_sentence[0].strip()
			seg_ng = unique_set_i.split(",")
			max_scus = max_scu_list(seg_ng)[0]
			max_scu_score = max_scu_list(seg_ng)[1]

			for each_scu in max_scus:
				if each_scu not in scu_sen:
					scu_sen[each_scu] = [sen_id]
				elif ((each_scu in scu_sen) and (sen_id not in scu_sen[each_scu])):
					scu_sen[each_scu].append(sen_id)

			scu_set[int(sen_id)].extend(max_scus)
			bestscu_file.write(uq_id + "\t"+ ", \t".join(map(str, (max_scus))) + "\t|\t"+ str(max_scu_score) +'\n')
for each_key in scu_set:
	scu_set[each_key] = set(scu_set[each_key])
print "scu_set : ",scu_set
print "scu_sen : ", scu_sen

# 2 things added: 1) scu_sen 2) each's score

#####################################################################################################################
#Pass no of sentences as arguments, create a square matrix of intersection sets | nrow = ncol = no_sen + 1

# no_sen = len(scu_set) + 1 #(2 + 1)
intersect_mat = getIntersections(10, scu_set)
print "intersect_mat"
for i in range(10):
	for j in range(10):
		sys.stdout.write(str(intersect_mat[i][j]) + '\t')
	sys.stdout.write('\n') 


#####################################################################################################################


