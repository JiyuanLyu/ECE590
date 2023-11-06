# This function takes 2 matricies (as lists of lists)
# and performs matrix multiplication on them.
# Note: you may not use any matrix multiplication libraries.
# You need to do the multiplication yourself.
# For example, if you have
#     a=[[1,2,3],
#        [4,5,6],
#        [7,8,9],
#        [4,0,7]]
#     b=[[1,2],
#        [3,4],
#        [5,6]]
#  Then a has 4 rows and 3 columns.
#  b has 3 rows and 2 columns.
#  Multiplying a * b results in a 4 row, 2 column matrix:
#  [[22, 28],
#   [49, 64],
#   [76, 100],
#   [39, 50]]
def matrix_mul(a,b):
    # Write me

    # let A * B = C
    c = []
    # For all rows in a
    for i in range(len(a)):
        # multiply with the columns in b
        row = []
        for j in range(len(b[0])):
            element = 0
            # add all the multiplications
            for k in range(len(b)):
                element += a[i][k] * b[k][j]
            # append this element to the row
            row.append(element)
        # append this row to the c matrix
        c.append(row)

    return c