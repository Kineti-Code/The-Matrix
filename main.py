from classes import Matrix
import config

def get_matrix_initialization():
    num_rows = 0
    num_columns = 0

    while True:
        try:
            num_rows = int(input("How many rows in this matrix? "))
            num_columns = int(input("How many columns in a row of this matrix? "))
            Matrix._validate_construction(num_rows, num_columns)
            break

        except ValueError as error:
            print(f"Error occured while initializing {num_rows}x{num_columns} matrix. Please re-initialize matrix. {error}")

    print(f"Successfully configured {num_rows}x{num_columns} matrix!")
    return num_rows, num_columns


def get_populated_matrix(num_rows, num_columns):
    values = [[0 for _ in range(num_columns)] for _ in range(num_rows)]
    current_row = 0
    current_column = 0

    print(f"Please input values for a {num_rows}x{num_columns} matrix!")
    
    while True:
        if current_row == num_rows:
            break

        try:
            values[current_row][current_column] = float(input(f"R{current_row+1} C{current_column+1}: "))

            current_column = (current_column + 1) % num_columns
            if current_column == 0:
                current_row += 1
        except ValueError as error:
            print(f"Ensure input is a valid float: {error}\n")

    matrix = Matrix(num_rows, num_columns, values)

    print(f"{num_rows}x{num_columns} matrix successfully initialized!")
    print(matrix)

    return matrix


def run():
    if config.INITIAL_MATRIX is not None:
        matrix = Matrix(2, 3, [[2, 5, 12], [1, 2, 5]])
        print(matrix)
    else:
        num_rows, num_columns = get_matrix_initialization()
        matrix = get_populated_matrix(num_rows, num_columns)

    while True:
        try:
            operation = input("Please input a row operation to perform on the matrix: ")
            matrix.parse_text(operation)
            print(matrix)
        except SyntaxError as error:
            print(f"Error occured while performing operation '{operation}'. Please re-input operation. {error}")


if __name__ == "__main__":
    run()