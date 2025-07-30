def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("You can't multiply these matrices")
    
    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            sum_val = 0
            for k in range(len(B)):
                sum_val += A[i][k] * B[k][j]
            row.append(sum_val)
        result.append(row)
    return result
