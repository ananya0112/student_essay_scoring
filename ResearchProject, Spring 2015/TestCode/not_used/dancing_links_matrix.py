
# Matrix implementation Input:
# X = {1, 2, 3, 4, 5, 6, 7}  | Originally X only held column names
# Y = {
#     'A': [1, 4, 7],
#     'B': [1, 4],
#     'C': [4, 5, 7],
#     'D': [3, 5, 6],
#     'E': [2, 3, 6, 7],
#     'F': [2, 7]}


# Dancing Links Input:
# X holds column -> row mapping
X = {
    1: {'A', 'B'},
    2: {'E', 'F'},
    3: {'D', 'E'},
    4: {'A', 'B', 'C'},
    5: {'C', 'D'},
    6: {'D', 'E'},
    7: {'A', 'C', 'E', 'F'}}

# Y hold rows -> columns mapping
Y = {
    'A': [1, 4, 7],
    'B': [1, 4],
    'C': [4, 5, 7],
    'D': [3, 5, 6],
    'E': [2, 3, 6, 7],
    'F': [2, 7]}


def solve(X, Y, solution=[]):
	if not X:
    	# If matrix has no columns, found solution. Stop.
		yield list(solution)
	else:
		c = min(X, key=lambda c: len(X[c])) # Select matrix with minimum no. of non-zero rows.
		for r in list(X[c]): # Consider each row with entry in c
			solution.append(r) # Include r as a possible solution
			cols = select(X, Y, r) # Consider each c' with an entry in r
			for s in solve(X, Y, solution):
				yield s
			deselect(X, Y, r, cols)
			solution.pop()


def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols


def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)



# # print "this is the file, calling solve now"
# # solve(X, Y, [])


# def main():
# 	print 'main'
# 	global X
# 	global Y
# 	print "X : "
# 	for k,v in X.iteritems():
# 		print k, v 
# 	for k,v in Y.iteritems():
# 		print k, v

# 	solve(X, Y)

# from dancing_links_matrix import *