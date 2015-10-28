""" Dancing links implementation using a dictionary """

# X = {1, 2, 3, 4, 5, 6, 7, -1, -2, -3}
# # # S => -1, -2, -3 | Sentence-id's | 

# Y = {
#     'A': [1, 4, 7, -1],
#     'B': [1, 4, -1],
#     'C': [4, 5, 7, -1],
#     'D': [3, 5, 6, -2],
#     'E': [2, 3, 6, 7, -2],
#     'F': [2, 7, -3]}


# X = {j: set() for j in X}
# for i in Y:
#     for j in Y[i]:
#         X[j].add(i)

X = {1,2,3,4,5}

Y = {
'A' : [1, 5],
'B' : [2, 4],
'C' : [2, 3],
'D' : [3],
'E' : [1, 4, 5]
}

X = {j: set() for j in X}
for i in Y:
    for j in Y[i]:
        X[j].add(i)

 # - See more at: http://www.ams.org/samplings/feature-column/fcarc-kanoodle#sthash.9shmNcVB.dpuf

"""
X to be transformed into:
X = {
    1: {'A', 'B'},
    2: {'E', 'F'},
    3: {'D', 'E'},
    4: {'A', 'B', 'C'},
    5: {'C', 'D'},
    6: {'D', 'E'},
    7: {'A', 'C', 'E', 'F'}}
"""


def solve(X, Y, solution=[]):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        print "Choosing column : ", c
        for r in list(X[c]):
            print "For c : " + c + " | Row considered is "
            solution.append(r)
            cols = select(X, Y, r)
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

# for k,v in X.iteritems():
#     print k, v 
# for k,v in Y.iteritems():
#     print k, v

a = solve(X, Y)
for i in a:
    print(i)
