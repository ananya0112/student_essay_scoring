import itertools	

	## Hard Coding ##

# unique_set_i = "All, living, things man, made or from, mother nature itself, are made out of matter"

unique_set_i = "Gov Bill Owens, formed around, that, high, school"
ng_dict = {
	"Gov Bill Owens" : [[100,102], [0.687, 0.6069]],
	"formed around" : [[102, 100], [0.69, 0.89]],
	"that" :[[101,103], [0.85, 0.72]],
	"high" : [[104], [0.78]],
	"school" : [[101], [0.82]]
}

scu_dict = {100: 5, 101:4, 102:3, 103:6, 104:5, 105:8}


"""Debugging these functions"""

def compute_score(list_scu_ids):
	""" Given the list of unique scu_id's of the form [134, 1], return the sum of their scores """
	sum_scu = 0
	for scu_id in list_scu_ids:
		sum_scu += scu_dict[scu_id]
	return sum_scu


def max_scu_list(seg_ng):
	""" For a given <list of n-grams> broken from a unique set/segments, return the scu combo with the max score """
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

	print "new_d", new_d				
	return [max(uq_list, key = (lambda x : x[1])), new_d]

seg_ng = unique_set_i.split(', ')
max_scul = max_scu_list(seg_ng)
print max_scul

max_scus = max_scul[0][0]
max_scu_score = max_scul[0][1]
max_cosine_sim = max_scul[1]
print "max - scus", max_scus, max_scu_score
print "new_d", max_cosine_sim

############## STOP HERE ###############

# def gen_cos_sim_str(max_scus, new_d):
# 	"""Given the max_scu_id's list & a dictionary of those <scu_ids : cos_sim>, generate the string"""
# 	# max_scus [100, 101]
# 	# new_d {100: [0.64466145858385004, 0.72], 101: [0.63850029254043461]}
# 	cos_str = ""
# 	for scu in max_scus:
# 		scu_cos_str = ""
# 		for each_cos_val in new_d[scu]:
# 			scu_cos_str += str(each_cos_val) + ", " 
# 		scu_cos_str = scu_cos_str[:-2]
# 		cos_str += scu_cos_str + '\t'
# 	return cos_str[:-1]

# val = gen_cos_sim_str([100, 101],{100: [0.64466145858385004, 0.72], 101: [0.63850029254043461]})
# print val
# {107: ['8'], 
# 100: ['1', '2', '3', '7', '8', '9'],
# 102: ['7', '8'], 
# 134: ['2', '3'], 
# 103: ['1', '2', '3', '8'], 
# 136: ['7'], 
# 105: ['1', '2', '3', '7', '8'], 
# 106: ['2', '3', '8'], 
# 119: ['7', '8'], 
# 108: ['8', '9'], 
# 110: ['2', '3'], 
# 144: ['2', '3'], 
# 137: ['4'], 
# 121: ['3', '7'], 
# 138: ['4'], 
# 101: ['7', '8', '9']}

# {(100, 102, 101, 104, 101): [(0.687, 0.69, 0.85, 0.78, 0.82)], 
# (102, 102, 101, 104, 101): [(0.6069, 0.69, 0.85, 0.78, 0.82)], 
# (100, 100, 103, 104, 101): [(0.687, 0.89, 0.72, 0.78, 0.82)], 
# (102, 102, 103, 104, 101): [(0.6069, 0.69, 0.72, 0.78, 0.82)],
#  (100, 102, 103, 104, 101): [(0.687, 0.69, 0.72, 0.78, 0.82)], 
#  (102, 100, 101, 104, 101): [(0.6069, 0.89, 0.85, 0.78, 0.82)],
#   (100, 100, 101, 104, 101): [(0.687, 0.89, 0.85, 0.78, 0.82)],
#    (102, 100, 103, 104, 101): [(0.6069, 0.89, 0.72, 0.78, 0.82)]}