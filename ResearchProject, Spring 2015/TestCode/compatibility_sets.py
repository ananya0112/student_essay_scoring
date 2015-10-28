import filter_scu_new_wtd as filtered
from generate_intersects import *
import itertools
from score_scu_segment import getSCU, compute_score


#####################################################################################################################

class Scu_node(object):
	def __init__(self, scu_id):
		self.id = scu_id
		self.visited = False
		self.assignedTo = None

	def visit(self):
		self.visited = True

	def assign(self, sen_id):
		self.assignedTo = sen_id

#####################################################################################################################

print "SCU SET represents all the (<sen_id> : scu): ", filtered.scu_set
print "SCU SEN represents (<scu_id>, sen_id): ", filtered.scu_sen

#####################################################################################################################
#Pass no of sentences as arguments, create a square matrix of intersection sets | nrow = ncol = no_sen + 1
##

intersect_mat = getIntersections(10, filtered.scu_set)
intersect_scu = {}


def gen_intersect_scu():
	global intersect_scu
	for i in range(1, 10):
		for j in range((i+1), 10):
			for each_scu in intersect_mat[i][j]:
				if each_scu not in intersect_scu:
					intersect_scu[int(each_scu)] = [i, j]
				elif each_scu in intersect_scu:
					if i not in intersect_scu[each_scu]:
						intersect_scu[int(each_scu)].append(i)
					if j not in intersect_scu[each_scu]:
						intersect_scu[int(each_scu)].append(j)
	print "INTERSECT SCU represents each sen_id THAT scu_id is present in (<scu_id> : [sen_id]): ", intersect_scu

gen_intersect_scu()


"""
SCU SET represents all the (<sen_id> : scu):  {1: set([100, 103]), 2: set([105, 100, 110]), 3: set([105, 100, 121]), 
4: set([137, 138]), 5: [], 6: [], 7: set([136, 119]), 8: set([136, 100, 119]), 9: set([136, 100])}

SCU SEN represents (<scu_id>, sen_id):  {100: ['1', '2', '3', '8', '9'], 103: ['1'], 136: ['7', '8', '9'], 105: ['2', '3'], 
138: ['4'], 119: ['7', '8'], 110: ['2'], 137: ['4'], 121: ['3']}

INTERSECT SCU represents each sen_id THAT scu_id is present in (<scu_id> : [sen_id]):  {136: [7, 8, 9], 105: [2, 3], 
100: [1, 2, 3, 8, 9], 119: [7, 8]}

"""

def restore_list(old_list):
	""" To overcome the issue of referential data type list """
	new_list = []
	for i in range(len(old_list)):
		new_list.append(list(old_list[i]))
	return new_list


def gen_comp_sets(list_scu_set, scu_id):
	# Case 1 : remove from all
	new_list_scu_set = restore_list(list_scu_set)
	list_comp_sets = []
	for i in range(0, len(list_scu_set)):
		new_list_scu_set[i].remove(scu_id)
	if [] in new_list_scu_set:
		new_list_scu_set.remove([]) # To avoid the issue of an empty list giving empty comp_sets
	comp_sets = list(itertools.product(*new_list_scu_set))
	print "case 1 : ", comp_sets
	# print "Compatibility sets : ", comp_sets

	# Case 2 : Remove from 1 in turn
	for i in range(0, len(list_scu_set)):
		new_list_scu_set = restore_list(list_scu_set) # Restoring back to the original list
		# print "restored list ", new_list_scu_set

		if scu_id in new_list_scu_set[i]:
			new_list_scu_set[i].remove(scu_id)
			if [] in new_list_scu_set:
				new_list_scu_set.remove([]) # To avoid the issue of an empty list giving empty comp_sets
			# print "new list : ", new_list_scu_set 
			comp_sets.extend(list(itertools.product(*new_list_scu_set)))
			print "case 2 : ", list(itertools.product(*new_list_scu_set))
	print "Compatibility sets : ", comp_sets

	comp_uel = [list(set(each_combo)) for each_combo in comp_sets]
	uq_list = [(list(x), compute_score(list(x))) for x in set(tuple(x) for x in comp_uel)]
	print uq_list
	best_comp_set = max(uq_list, key = (lambda x: x[1]))
	print "BEST SET : ", best_comp_set


def traverse_intersect_scu():
	global intersect_scu
	for scu_id in intersect_scu:
	# 	print "STARTING THIS"
		list_scu_set = []
		for sen_id in intersect_scu[scu_id]:
			list_scu_set.append(list(filtered.scu_set[int(sen_id)]))
		print "Starting generation for scu_id "+ str(scu_id) +" | ",intersect_scu[scu_id]
		gen_comp_sets(list_scu_set, scu_id)
		print "--------------------------------------------------------------------------"

traverse_intersect_scu()

# Display intersection matrix #
def display_intersection():
	global intersect_mat
	for i in range(10):
		for j in range(10):
			sys.stdout.write(str(intersect_mat[i][j]) + '\t')
		sys.stdout.write('\n') 

# display_intersection()

#####################################################################################################################
# list(itertools.product(*scus_list))

# from compatibility_sets import *