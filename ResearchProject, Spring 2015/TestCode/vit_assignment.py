# This is an attempt in the viterbi-modified method


""" Rembr : scu should be string | ', '.join should be followed """
scu_dict = dict()
pi = dict() ## This is the main dictionary holding all the scoree i.e sum of scores ##

## u_dict -> <k,v> : [list of u's valid for the combination of k,v] i.e list of prev scu-ids not in v
no_sen = 4 # Init #
u_dict = dict() # This is the computed 'u' #
for i in xrange(1, no_sen):
	u_dict[i] = {}

def getSCU(pyr_name, scu_doc_path):
	""" <scu_id> : <weight> """
	# print "Starting SCU generation "
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
	# print "SCU generation complete"
	# pretty_print_dict(scu_dict) 
	return scu_dict


def pretty_print_dict(hmap):
	if not isinstance(hmap, dict):
		return None
	for k,v in hmap.iteritems():
		print "Key : "+ str(k) + " | "+ str(v) 


def compute_score(list_scu):
	""" Computes the sum of scu scores for a [list of scu] """
	sum_scu = 0
	for scu in list_scu:
		sum_scu += scu_dict[scu]
	return sum_scu


def get_v(sen_id):
	""" Currently this is a hard coded function. But this will change into a function that extracts the top scu's per sentence from the files
	i.e <Sen_id : [List of lists i.e set of scu's it matches best]> a = {1:[100,101], 2:[[101], [100,105]]}. As per Viterbi, it is the 
	K(k), K(k-1) etc. """
	best_scu_sen = {0:['*'], 1:[['103, 105'], ['100']], 2:[['105'], ['110'], ['105, 110']], 3:[['105'], ['121, 105']]} 
	if sen_id in best_scu_sen: # If key prsent in dictionary
		return best_scu_sen[sen_id]
	return None


def get_u(sen_id, v):
	""" append 'current' v with 'previous' u | k=sen_id 
	compute_u for a given [k,v] """ # u+v #
	global u_dict
	list_u = []
	str_v = ', '.join(v)
	if sen_id == 1:
		# For any v, it will be => '*' + v #
		u_dict[sen_id][str_v] = ', '.join(get_v(sen_id-1)) + ', ' + str_v
		print u_dict
		# list_u.append(u_dict[sen_id, v])
	else:
		# list_v_prevk = get_v(sen_id-1) | # u_dict['sen_id, '+'v']
		# loop over each v from list_v_prevk for sen_id, get val = u_dict[sen_id-1,v] for each, store only those val which do not contain the provided v i.e v for sen_id
		# Store only those for u_dict['sen_id' + ', v']
		print "Sen id + [v's]", sen_id, str_v
		list_u = [each_u for each_u in get_v(sen_id-1) if any(v.split(', ')) not in each_u]
		# print list_u
	return list_u

a = get_u(1, ['103, 105'])
# print a
get_u(1, ['100'])
print get_u(2, ['103, 105'])
print get_u(2, ['110'])


""" Do hard-coded 'u' generation for now? it is not the hardest part """

def vit_comp(no_sen = 3):
	# no_sen = 3
	for k in xrange(no_sen):
		for v in get_v(k): # use ' '.join(v) => will convert list to string #
			for u in get_u(k, v):
				temp = pi[k-1, u] + compute_score(v)
				# pi[k, v] = 
				return None



# Step 1 # Function call | ** -- PYRAMID ID as input -- **
# scu_dict = getSCU("12_10_09_MATTER.pyr", "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/scu_YINGHUI/scu") ## Uncomment this 