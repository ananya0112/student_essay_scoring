"""Implementation of Munkres Kuhn algorithm for 'scu assignment to sentences'
"""

from munkres import Munkres, print_matrix

matrix = [[80, 40, 50, 46],
          [40, 70, 20, 25],
          [30, 10, 20, 30],
          [35, 20, 25, 30]
        ]
m = Munkres()
indexes = m.compute(matrix)
print_matrix(matrix, msg='Lowest cost through this matrix:')
total = 0
for row, column in indexes:
    value = matrix[row][column]
    total += value
    print '(%d, %d) -> %d' % (row, column, value)
print 'total cost: %d' % total