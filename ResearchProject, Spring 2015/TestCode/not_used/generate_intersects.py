"""Generates an intersection set of scu_set for each sen_id"""


######################## Creates 2D Matrix of sentence id's ####################################
def alloc_matrix2d(W, H):
	""" Pre-allocate a 2D matrix of empty lists. """
	intersect_mat = [ [ [] for i in range(W) ] for j in range(H) ]
	for i in range(W):
		for j in range(H):
			if i==0 and j == 0:
				intersect_mat[i][j] = 0
			elif i==0 :
				intersect_mat[i][j] = j
			elif j == 0 :
				intersect_mat[i][j] = i
			elif i ==j :
				intersect_mat[i][j] = 1
	return intersect_mat


#Pass no of sentences as arguments, create a square matrix of intersection sets | nrow = ncol = no_sen + 1

no_sen = 3 #(2 + 1)
intersect_mat = alloc_matrix2d(no_sen, no_sen)

######################## Creates intersection scu sets for each pair of sen_id ####################################

def getIntersections(no_sen, scu_set):
	""" Creating intersect sets b/w scu's of unique sets of each sentence """
	intersect_mat = alloc_matrix2d(no_sen, no_sen)

	#i,j are sen_ids
	for i in xrange(1,no_sen):
		for j in xrange((i+1),no_sen):
			set1 = scu_set[i]
			set2 = scu_set[j]
			# print "sets for ",i,j
			# print set1, set2, set1.intersection(set2)
			if isinstance(set1, set) and isinstance(set2, set):
				intersect_mat[i][j] = intersect_mat[j][i] = set1.intersection(set2)
	return intersect_mat

####################################################################################################################