
# checking the contraints
def multiplication_constraint_checking(a,b):
    row = len(b)
    col = len(a[0])
    if row == col:
        return True
    else:
        return False

def add_sub_constraint_checking(a,b):
    a_rows = len(a)
    b_rows = len(b)
    a_cols = len(a[0])
    b_cols = len(b[0])
    if a_rows == b_rows and a_cols == b_cols:
        return True
    else:
        return False

#Matrix-Addition
def matrix_addition(a,b):
    results_a = []
    if not add_sub_constraint_checking(a,b):
       raise AssertionError("matrix addition is allowed only when rows and cols are equal")
    else:
        results_a = [[0 for _ in range(len(a[0]))] for _ in range(len(a))]
    for i in range(len(a)):
      for j in range(len(a[0])):
          results_a[i][j] = a[i][j]+b[i][j]
    return results_a

#matrix-subtraction

def matrix_substraction(a, b):
  results_s = []
  if not add_sub_constraint_checking(a, b):
    raise AssertionError("Matrix substraction is allowed only when rows and cols are equal")
  else:
    results_s   = [[0 for _ in range(len(a[0]))] for _ in range(len(a))]

  for i in range(len(a)):
    for j in range(len(a[0])):
     results_s[i][j] = a[i][j] - b[i][j]
  return results_s
#matrix-multiplication

def matrix_multiplication(a, b):
    a_rows = len(a)
    b_cols = len(b[0])
    results_m = []

    if not multiplication_constraint_checking(a,b):
      raise AssertionError("demision must be equal. plead try again")
    else:
        results_m = [[0 for _ in range(b_cols)] for _ in range(a_rows)]
    print(a,b)
    for i in range(a_rows):
      for j in range(b_cols):
        for k in range(b_cols):
            results_m[i][j] += a[i][k] * b[k][j]
    return results_m
  
for i in matrix_multiplication(a,b):
    print(i) 
