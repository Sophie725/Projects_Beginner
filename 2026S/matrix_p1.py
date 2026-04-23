# Drop data
# Don't use other libraries for this assignment such as numpy or pandas.

def drop_first_row(matrix: list[list]) -> list[list]:
    # This function should drop the first row of the matrix 
    # and return the modified matrix.
    # Fill in the code here

    return matrix

def drop_last_row(matrix: list[list]) -> list[list]:
    # This function should drop the last row of the matrix
    # and return the modified matrix.
    # Fill in the code here

    return matrix

def drop_row(matrix: list[list], i: int) -> list[list]:
    # This function should drop the row at index i of the matrix
    # and return the modified matrix. 
    # Your code should be able to handle errors, 
    # such as i being out of bounds or the matrix being empty.
    # Fill in the code here

    return matrix

def drop_rows_range(matrix: list[list], start: int, end: int) -> list[list]:
    # This function should drop the rows from index start to end (inclusive) of the matrix
    # and return the modified matrix.
    # Your code should be able to handle errors, 
    # such as start or end being out of bounds or the matrix being empty.
    # Fill in the code here

    return matrix

def drop_row_if_value(matrix: list[list], value) -> list[list]:
    # This function should drop all rows that contain the value
    # and return the modified matrix.
    # Fill in the code here

    return matrix

def drop_row_threshold(matrix: list[list], threshold: int) -> list[list]:
    # This function should drop all rows that contain a value greater than the threshold
    # and return the modified matrix.
    # Fill in the code here

    return matrix

def drop_first_col(matrix: list[list]) -> list[list]:
    # This function should drop the first column of the matrix 
    # and return the modified matrix.
    # Fill in the code here

    return matrix

def drop_last_col(matrix: list[list]) -> list[list]:
    # This function should drop the last column of the matrix
    # and return the modified matrix.
    # Fill in the code here

    return matrix

def drop_col(matrix: list[list], j: int) -> list[list]:
    # This function should drop the column at index j of the matrix
    # and return the modified matrix.
    # Your code should be able to handle errors,
    # such as j being out of bounds or the matrix being empty.
    # Fill in the code here
    
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

    return matrix

def drop_col_threshold(matrix: list[list], threshold: int) -> list[list]:
    # This function should drop all columns that contain a value greater than the threshold
    # and return the modified matrix.
    # Fill in the code here

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