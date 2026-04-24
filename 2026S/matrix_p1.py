# Drop data
# Don't use other libraries for this assignment such as numpy or pandas.

def drop_first_row(matrix: list[list]) -> list[list]:
    # This function should drop the first row of the matrix 
    # and return the modified matrix.
    # Fill in the code here
    if matrix: # to check whether a matrix is empty or not
        matrix.pop(0)

    return matrix

def drop_last_row(matrix: list[list]) -> list[list]:
    # This function should drop the last row of the matrix
    # and return the modified matrix.
    # Fill in the code here
    if matrix:
        matrix.pop(-1)

    return matrix

def drop_row(matrix: list[list], i: int) -> list[list]:
    # This function should drop the row at index i of the matrix
    # and return the modified matrix. 
    # Your code should be able to handle errors, 
    # such as i being out of bounds or the matrix being empty.
    # Fill in the code here
    if (not matrix) or (i < 0) or (i >= len(matrix)):
        print("Error")
    else:
        matrix.pop(i)
    
    return matrix

def drop_rows_range(matrix: list[list], start: int, end: int) -> list[list]:
    # This function should drop the rows from index start to end (inclusive) of the matrix
    # and return the modified matrix.
    # Your code should be able to handle errors, 
    # such as start or end being out of bounds or the matrix being empty.
    # Fill in the code here
    if (not matrix) or (start < 0) or (end >= len(matrix)) or (start > end):
        print("Error")
    else:
        del matrix[start:end+1]

    return matrix

def drop_row_if_value(matrix: list[list], value) -> list[list]:
    # This function should drop all rows that contain the value
    # and return the modified matrix.
    # Fill in the code here
    i = 0
    while i < len(matrix):
        if value in matrix[i]:
            matrix.pop(i)
        else:
            i += 1

    return matrix

def drop_row_threshold(matrix: list[list], threshold: int) -> list[list]:
    # This function should drop all rows that contain a value greater than the threshold
    # and return the modified matrix.
    # Fill in the code here
    i = 0
   ....don't know

    return matrix

def drop_first_col(matrix: list[list]) -> list[list]:
    # This function should drop the first column of the matrix 
    # and return the modified matrix.
    # Fill in the code here
    for i in range (len(matrix)):
        matrix[i] = matrix[i][1:]

    return matrix

def drop_last_col(matrix: list[list]) -> list[list]:
    # This function should drop the last column of the matrix
    # and return the modified matrix.
    # Fill in the code here
    for i in range(len(matrix)):
        matrix[i] = matrix[i][:-1]

    return matrix

def drop_col(matrix: list[list], j: int) -> list[list]:
    # This function should drop the column at index j of the matrix
    # and return the modified matrix.
    # Your code should be able to handle errors,
    # such as j being out of bounds or the matrix being empty.
    # Fill in the code here
    if not matrix or j < 0 or j >= len(matrix[0]):
        return matrix
        
    for i in range(len(matrix)):
        # j번째 값만 쏙 빼고 다시 합치기
        left = matrix[i][:j]
        right = matrix[i][j+1:]
        matrix[i] = left + right
    
    return matrix

def drop_cols_range(matrix: list[list], start: int, end: int) -> list[list]:
    # This function should drop the columns from index start to end (inclusive) of the matrix
    # and return the modified matrix.
    # Your code should be able to handle errors,
    # such as start or end being out of bounds or the matrix being empty.
    # Fill in the code here

    return matrix

def drop_col_if_value(matrix: list[list], value) -> list[list]:
    # This function should drop all columns that contain the value
    # and return the modified matrix.
    # Fill in the code here
    if not matrix:
        return matrix
    
    # 1. 먼저 어떤 열을 지워야 할지 인덱스 번호를 수집
    cols_to_delete = []
    num_cols = len(matrix[0])
    for j in range(num_cols):
        for i in range(len(matrix)):
            if matrix[i][j] == value:
                cols_to_delete.append(j)
                break # 해당 열에 값이 하나라도 있으면 다음 열로
    
    # 2. 수집된 인덱스를 제외하고 새로운 행 구성 (역순 삭제 권장하나 새 리스트가 안전)
    for i in range(len(matrix)):
        new_row = []
        for j in range(num_cols):
            if j not in cols_to_delete:
                new_row.append(matrix[i][j])
        matrix[i] = new_row
        
    return matrix

def drop_col_threshold(matrix: list[list], threshold: int) -> list[list]:
    # This function should drop all columns that contain a value greater than the threshold
    # and return the modified matrix.
    # Fill in the code here
    if not matrix:
        return matrix
    
    cols_to_delete = []
    num_cols = len(matrix[0])
    for j in range(num_cols):
        for i in range(len(matrix)):
            if matrix[i][j] > threshold:
                cols_to_delete.append(j)
                break
                
    for i in range(len(matrix)):
        new_row = []
        for j in range(num_cols):
            if j not in cols_to_delete:
                new_row.append(matrix[i][j])
        matrix[i] = new_row

    return matrix

def main():
    i = 1
    matrix = [[1, 2, 3], 
              [4, 5, 6], 
              [7, 8, 9]]
    # drop_first_row(matrix)
    # drop_last_row(matrix)
    # drop_row(matrix, i)
    # drop_rows_range(matrix, 0, i)
    # drop_row_if_value(matrix, 5)
    # drop_row_threshold(matrix, 5)

    # drop_first_col(matrix)
    # drop_last_col(matrix)
    # drop_col(matrix, i)
    # drop_cols_range(matrix, 0, i)
    # drop_col_if_value(matrix, 5)
    # drop_col_threshold(matrix, 5)


if __name__ == "__main__":
    main()
