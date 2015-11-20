#Set scu values
scu_tbl = {1:4, 2:3, 3:3, 4:3, 5:2, 6:2, 7:2, 8:1, 9:1, 10:1}

#Each ngram with scu: #Key : (sen_id, ngram) : #Value [scu1, scu2]
ng_scu = {
	(1,"word1"):[1,2],
	(1,"word1 word2"):[4],
	(1,"word1 word2 word3"):[3,5],
	(1,"word2"):[2],
	(1,"word2 word3"):[2,4],
	(1,"word3"):[3],
	(2,"word4"):[1,4,7],
	(2,"word4 word5"):[4,5],
	(2,"word4 word5 word6"):[3,6,9],
	(2,"word5"):[1,5,9],
	(2,"word5 word6"):[6,7],
	(2,"word6"):[8,9],
	(3,"word4"):[1,4,7],
	(3,"word4 word5"):[4,5],
	(3,"word4 word5 word6"):[3,6,9],
	(3,"word5"):[1,5,9],
	(3,"word5 word6"):[6,7],
	(3,"word6"):[8,9]
	}


######################## Creates 2D Matrix of sentence id's ####################################
def alloc_matrix2d(W, H):
	""" Pre-allocate a 2D matrix of empty lists. """
	intersect_mat = [ [ [] for i in range(W) ] for j in range(H) ]
	for i in range(W):
		for j in range(H):
			if i==0 or j == 0:
				intersect_mat[i][j] = 0
			elif i ==j :
				intersect_mat[i][j] = 1
	return intersect_mat


#Pass no of sentences as arguments, create a square matrix of intersection sets | nrow = ncol = no_sen + 1

no_sen = 3 #(2 + 1)
intersect_mat = alloc_matrix2d(no_sen, no_sen)


######################## Creates unique scu sets for each sen_id ####################################

scu_set = {}
 # idea : do this during ng_dict creation #
def create_scu_sets(ng_scu):
	""" Will go through dictionary, creating unique hashsets for each sentence no. | {<Sen_id> : [<unique hashset of all scu>]}"""
	for each_key in ng_scu:
		sen_id = each_key[0]
		if sen_id in scu_set:
			scu_set[sen_id].extend(ng_scu[each_key])
		else:
			scu_set[sen_id] = ng_scu[each_key]
	for e_key in scu_set:
		scu_set[e_key] = set(scu_set[e_key])
	return scu_set


######################## Creates intersection scu sets for each pair of sen_id ####################################

def getIntersections(ng_scu):
	""" Creating intersect sets b/w unique sets of each sentence """
	#i,j are sen_ids
	for i in xrange(1,3):
		for j in xrange((i+1),3):
			set1 = scu_set[i]
			set2 = scu_set[j]
			intersect_mat[i][j] = intersect_mat[j][i] = set1.intersection(set2)
	return intersect_mat


######################## Creates matrix containing intersection set size ####################################

def updateIntersectionSize(H, no_scu):
	""" Holds sizes of intersection set size length """
	insize_mat = [ [ [] for i in range(no_scu) ] for j in range(H) ]
	#i,j are sen_ids
	for i in xrange(1,H):
		for j in xrange((i+1),H):
			intersect_mat[i][j] = intersect_mat[j][i] = set1.intersection(set2)
	return intersect_mat


######################## DRIVER : Function calls ####################################

some_val = create_scu_sets(ng_scu)
print "Calling create scu sets"
print some_val

some_int = getIntersections(ng_scu)
print "Calling get intersections"
print some_int

for i in range(3):
	for j in range(3):
		print some_int[i][j]
	print '\n'


########################################################################################

# def alloc_matrix2d(W, H):
#     """ Pre-allocate a 2D matrix of empty lists. """
#     return [ [ [] for i in range(W) ] for j in range(H) ]