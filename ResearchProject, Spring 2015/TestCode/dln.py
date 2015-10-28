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

# Added only for logging purposes:
from time import gmtime, strftime
#

# Toy data
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
count = 0
si = 0

def solve(X, Y, solution=[]):
    global si
    global count

    si = si+1
    # print '\n * calling solve - iteration : ', si
    print '\n-----X----'
    for k,v in X.iteritems():
        print k,v
    print '-----Y----'
    for k,v in Y.iteritems():
        print k,v
    print '-----------\n'

    if not X:
        count = count + 1
        print '->>Found solution!'
        yield list(solution)
        print '->>!\n'
    else:
        c = min(X, key=lambda c: len(X[c]))
        print "Choosing column : ", c
        for r in list(X[c]):
            print "For column : ", str(c) + " taking row : " + str(r)
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            # print '\n-----X before deselect----'
            # for k,v in X.iteritems():
            #     print k,v
            deselect(X, Y, r, cols)
            # print '-----X after deselect----'
            # for k,v in X.iteritems():
            #     print k,v
            v = solution.pop()


def select(X, Y, r):
    global count
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    print "COUNT : " + str(count) +" | For set : " + str(r) + " | Due to it's element j : "+ str(j) +"  | removing j's set : "+ str(i) +" from it's element k " + str(k) + " where "+str(k)+" is a member of set "+str(i)
                    X[k].remove(i)
        print "\n X : ", X
        cols.append(X.pop(j))
        # print "X with popped X[j] -> X[" + str(j) + "] : ", X
    # print '\nCOUNT : ' + str(count) +' returning cols : '
    # for e in cols:
    #     if len(list(e))>0:
    #         print e
    # print 'Done returning cols\n'
    return cols


def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)


a = solve(X, Y)
# print "Performing dancing links operation at time : " + strftime("%Y-%m-%d %H:%M:%S")
for i in a:
    print(i)
