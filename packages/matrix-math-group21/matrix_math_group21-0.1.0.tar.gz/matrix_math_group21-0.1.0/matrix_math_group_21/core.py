def add_matrices(a, b):
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("Marvin you know how matrixes work please try again, make sure they are the same dimensions this time")
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def multiply_matrices(a, b):
    if len(a[0]) != len(b):
        raise ValueError("You're not a quality tester please make sure the number of columns match the rows, Marvin")
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b)))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]
