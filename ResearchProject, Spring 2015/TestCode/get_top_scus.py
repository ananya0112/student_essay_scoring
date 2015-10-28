"""This will read the <sen_no>.best.scu.wtd.new.st.unique
Format of file:
unique_set_id '|', {scu_set} '|',new wtd score ,'|', avg wtd score,'|', ng_len, '| ', cos_sim_mean, ' | ', sd, ' | ', cos_sim
  lines_seen is used to maintain unique files
16	|	103	|	13.0823210974	|	2.61646421949	|	5	| 	0.654116054871	 | 	0.0	 | 	0.654116054871
"""

import os.path
import sys
import dln

""" Set these parameters """ 
best_scu_path = 'Sentences/Unique_Sets/12_10_09_MATTER.pyr/1/new_wtd_files/'
no_sen = 3 # Actual no. of sentences
top_scu_dict = dict() # <sen_id : {[], []} set of scu's>
# n = 3

def extract_scu_set(file_line):
	""" Takes the sentence format specified above, extracts scu's and returns a list """
	scu_list = []
	segment_info = file_line.split("\t|\t")
	scu_str = segment_info[1].strip()
	if scu_str.strip():
		scu_list = scu_str.split(", \t")
		scu_list = [int(element) for element in scu_list]
	return scu_list


def extract_top_n_scus(file_pth, n):
	""" Traverses only over the top 'n' sentences, and returns top 'n' best scu sets """
	counter = 0
	top_scu_list = []
	with open(file_pth) as sen_scu_file:
		head = [next(sen_scu_file) for x in xrange(n)]
	# top_scu_list = [extract_scu_set(line) for line in head]
	for line in head:
		if len(extract_scu_set(line)) > 0:
			top_scu_list.append(extract_scu_set(line))
	return top_scu_list

# get top scu's for each sentence
# sen_id convert into matrix format
# Call dln.py as with input as X and Y


def get_best_scus(n):
	""" Set no_sen (global parameter) on top """
	for sen_id in xrange(1, no_sen+1):
	# for sen_id in xrange(2, 3):
		file_path = best_scu_path + str(sen_id) + '.best.scu.wtd.new.st.unique'
		if not (os.path.exists(file_path)):
			# raise ValueError("File " + file_path + " does not exist")
			continue
		else:
			top_scu_dict[sen_id] = extract_top_n_scus(file_path, n)
	print '----Best SCUs----'
	for k,v in top_scu_dict.iteritems():
		print k, v
	print '----------------'
	return top_scu_dict


# generate inputs for Algo X

def flatten_lists(lists):
	"""[[['103'], ['100']], [['105'], ['110'], ['100', '110']],
	[['105'], ['100', '105'], ['121', '105']], [['138'], ['137']], [['136'],
	['136', '119'], ['119']], [['100'], ['100', '136'], ['100', '119']], [['100'], ['136', '100']]]
	"""
	output_list = []
	for element in lists:
		if isinstance(element, list):
			output_list.extend(flatten_lists(element))
		else:
			output_list.append(element)
	return output_list


def get_Y(best_scus):
	""" All elements in matrix/DL as rows | set-names + sets """
	Y_dict = {}
	key_int = 1
	for k,v in best_scus.iteritems():
		for scu_set in v:
			scu_set.append(-1 * k)
			# print 'k,v ', key_int, scu_set, k
			Y_dict[key_int] = scu_set
			key_int = key_int + 1
	for k,v in Y_dict.iteritems():
		print k, v
	return Y_dict



def get_X(best_scus):
	""" All element-names in matrix/DL as columns """
	list_X = flatten_lists(best_scus.values())
	# for k,v in best_scus.iteritems():
	# 	list_X.append(-1 * k) # This represents the sentence id's # 
	print sorted(list(set(list_X)))
	return sorted(list(set(list_X)))


"""
best_scu's : 

1 [['103'], ['100']]
2 [['105'], ['110'], ['100', '110']]
3 [['105'], ['100', '105'], ['121', '105']]
4 [['138'], ['137']]
7 [['136'], ['136', '119'], ['119']]
8 [['100'], ['100', '136'], ['100', '119']]
9 [['100'], ['136', '100']]


new X : set([100, 103, 136, 105, 138, 119, 110, -7, -1, 137, -8, 121, -4, -3, -2, -9])
"""


""" Here n represents the 'n' best scu's to be extracted from each 'best scu' file """
def generate_inputs(n):
	best_scus = get_best_scus(int(n))
	print '-----Y-----'
	Y = get_Y(best_scus)
	print '----original X-----'
	X = get_X(best_scus)
	print '----modified X-----'
	X = {j: set() for j in X}
	for i in Y:
	    for j in Y[i]:
	        X[j].add(i)
	
	for k,v in X.iteritems():
		print k,v
	print '-----------'
	return X, Y


def usage():
	print """ This file is used to get the top scu's for each sentence. 
	Specify file as 'python get_top_scus.py n' where n is an integer, indicating the top n scu's required """


if __name__ == "__main__": 
	if len(sys.argv) != 2:
		usage()
		sys.exit(-1)
	n = sys.argv[1]
	X, Y = generate_inputs(n)
	a = dln.solve(X, Y)
	print '---Solution :---'
	for i in a:
		print(i)
	print '-----------'

"""
from get_top_scus import *
a = generate_inputs(3)
"""
	