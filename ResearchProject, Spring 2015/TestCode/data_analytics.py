""" This file is used for Data Analytics on best scu's generated per sentence | to generate supporting data for histograms."""

from get_top_scus import get_best_scus, flatten_lists

n = 3
# Histogram: How many scus occur once per sentence, twice per sentence, etc.
# Average size of all the sets in a sentence 
# Average number of sets per sentence 
# Average weight of SCUs that occur once per sentence, twice per sentence, etc.
# Histogram: How many SCUs occur in n sentences, for n=1 to number of sentences? 
# Average weight of SCUs that occur in n sentences?


# Get best scu's:

scu_dict = {}

def getSCU(pyr_name, scu_doc_path):
	""" <scu_id> : <weight> """
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
			break
	print scu_dict
	return scu_dict


# Step 1 # Function call | ** -- PYRAMID ID as input -- **
scu_dict = getSCU("12_10_09_MATTER.pyr", "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/scu_YINGHUI/scu")

best_scus = {}
n = 3
for peer_id in xrange(1,20):
	adder = len(best_scus)
	temp_scus = get_best_scus(int(n), peer_id)
	for k,v in temp_scus.iteritems():
		best_scus[int(k)+adder] = v
for k,v in best_scus.iteritems():
	print k,v


"""
Output : The sentences considered are 7 sentences from 1-9:
----Best SCUs----
1 [[103], [100]]
2 [[105], [110], [100, 110]]
3 [[105], [100, 105], [121, 105]]
4 [[138], [137]]
7 [[136], [136, 119], [119]]
8 [[100], [100, 136], [100, 119]]
9 [[100], [136, 100]]
----------------
"""

# 2. Average size of all the sets in a sentence

def get_avg_size_sets():
	""" Avg_size = total size of sets / no. of sets """
	no_of_sets = 0
	total_sets_size = 0
	for k,v in best_scus.iteritems():
		for scu_set in v:
			no_of_sets = no_of_sets + 1
			total_sets_size = total_sets_size + len(scu_set)
	return float(total_sets_size)/float(no_of_sets)

# print 'Avg size of sets:'
# avg_size = get_avg_size_sets()
# print avg_size

# 3. Average number of sets per sentence

def get_avg_no_sets():
	""" Avg_no_sets per sentence = total no. of sets / no. of sentences """
	no_of_sen = len(best_scus)
	no_of_sets = 0
	for k,v in best_scus.iteritems():
		for scu_set in v:
			no_of_sets = no_of_sets + 1
	# print no_of_sets, no_of_sen
	return float(no_of_sets)/float(no_of_sen)

# print 'Avg no of sets per sen_id:'
# avg_no = get_avg_no_sets()
# print avg_no

"""
Output : The sentences considered are 7 sentences from 1-9:
----Best SCUs----
1 [[103], [100]]
2 [[105], [110], [100, 110]]
3 [[105], [100, 105], [121, 105]]
4 [[138], [137]]
7 [[136], [136, 119], [119]]
8 [[100], [100, 136], [100, 119]]
9 [[100], [136, 100]]

Flattened lists : 
1 [103, 100]
2 [105, 110, 100, 110]
3 [105, 100, 105, 121, 105]
4 [138, 137]
7 [136, 136, 119, 119]
8 [100, 100, 136, 100, 119]
9 [100, 136, 100]
----------------
"""

# 4. No. of scu's that occur 1ce, 2ce etc 'within' a sentence

def compute_scu_freq(flat_list):
	"""[105, 110, 100, 110]
	<scu_id : frequency>"""
	scu_freq = {}
	for scu in flat_list:
		if scu not in scu_freq:
			scu_freq[scu] = 1
		else:
			scu_freq[scu] = scu_freq[scu] + 1
	return scu_freq


def get_freq_intra_scus():
	""" Create a dictionary of <'sen_id' : {frequency_x : count, total_wt}>
	freq_table = {1:{1:[5, wt], 2:[4, wt], 3:[6, wt]}, 2:{1:[3, wt],2:[3, wt]}}"""
	freq_table = {}
	for sen_id,v in best_scus.iteritems():
		freq_table[sen_id] = {}
		scus_list = flatten_lists(v)
		scu_freq = compute_scu_freq(scus_list)
		for scu, freq in scu_freq.iteritems():
			if freq not in freq_table[sen_id]:
				freq_table[sen_id][freq] = [1, scu_dict[scu]]
			else:
				freq_table[sen_id][freq][0] = freq_table[sen_id][freq][0] + 1
				freq_table[sen_id][freq][1] = freq_table[sen_id][freq][1] + scu_dict[scu]
	return freq_table

# print "How many scus occur once per sentence, twice per sentence, etc."
# f = get_freq_intra_scus()
# for k,v in f.iteritems():
# 	print k,v

"""
Output of get_freq_intra_scus():
sen_id | freq | count | total-weight
1 	{1: [2, 9]}
2 	{1: [2, 9], 2: [1, 3]}
3 	{1: [2, 8], 3: [1, 4]}
4 	{1: [2, 3]}
7 	{2: [2, 4]}
8 	{1: [2, 4], 3: [1, 5]}
9 	{1: [1, 1], 2: [1, 5]}
"""


def get_avg_wt_intra_scus():
	""" total-wt scu's - that occur x times / no. of scu's that occur x times |
	<freq-intra-scu-occurence : [count, total-wt]>"""
	avg_wt_intra_scus = {1: [0, 0, 0], 2: [0, 0, 0], 3: [0, 0, 0]} # 'n' no. will be max frequency
	f_table = get_freq_intra_scus()
	for sen_id,v in f_table.iteritems(): # Sentences
		for freq, cw in v.iteritems(): # <freq : [count, weight]>
			avg_wt_intra_scus[freq][0] = avg_wt_intra_scus[freq][0] + cw[0]
			avg_wt_intra_scus[freq][1] = avg_wt_intra_scus[freq][1] + cw[1]
			avg_wt_intra_scus[freq][2] = float(avg_wt_intra_scus[freq][1])/float(avg_wt_intra_scus[freq][0])
	return avg_wt_intra_scus

# print 'intra-scus |\n freq-x, count, weight, wt-avg'
# for k,v in get_avg_wt_intra_scus().iteritems():
# 	print k, v

"""
Output : The sentences considered are 7 sentences from 1-9:
----Best SCUs----
1 [[103], [100]]
2 [[105], [110], [100, 110]]
3 [[105], [100, 105], [121, 105]]
4 [[138], [137]]
7 [[136], [136, 119], [119]]
8 [[100], [100, 136], [100, 119]]
9 [[100], [136, 100]]

Flattened lists : 
1 [103, 100]
2 [105, 110, 100, 110]
3 [105, 100, 105, 121, 105]
4 [138, 137]
7 [136, 136, 119, 119]
8 [100, 100, 136, 100, 119]
9 [100, 136, 100]
----------------
"""
def get_freq_inter_scus():
	"""Create a dictionary of  <frequency_x : [count, total_wt]>"""
	freq_table = {}
	inter_scus = []
	for sen_id, v in best_scus.iteritems():
		scus_list = flatten_lists(v)
		inter_scus.extend(list(set(scus_list)))
	scu_freq = compute_scu_freq(inter_scus)
	for scu, freq in scu_freq.iteritems():
		# print scu, freq
		if freq not in freq_table:
			freq_table[freq] = [1, scu_dict[scu], scu_dict[scu]]
		else:
			freq_table[freq][0] = freq_table[freq][0] + 1
			freq_table[freq][1] = freq_table[freq][1] + scu_dict[scu]
			freq_table[freq][2] = float(freq_table[freq][1]) / float(freq_table[freq][0])
	return freq_table

print 'inter-scus |\n freq-x, count, weight, wt-avg'
f_table = get_freq_inter_scus()
# for k,v in f_table.iteritems():
# 	print k,v

keys_ordered = sorted(f_table.keys())
for k in keys_ordered:
	print k, f_table[k]

"""
Output of get_freq_inter_scus():
1 [5, 13]
2 [2, 7]
3 [1, 1]
5 [1, 5]
"""

