import numpy as np


def swap_diagonals(matrix):
    size = matrix.shape[0]

    for row in range(size):
        other_col = size - row - 1

        matrix[row, row], matrix[row, other_col] = (
            matrix[row, other_col],
            matrix[row, row],
        )


def main():
    size_text = input("Enter the size of the square matrix: ")
    size = int(size_text)

    if size < 1:
        raise ValueError("Matrix size must be at least 1.")

    rows = []

    for row_number in range(size):
        row_text = input(f"Enter row {row_number + 1}: ")
        pieces = row_text.split()
        row_values = [int(piece) for piece in pieces]

        if len(row_values) != size:
            raise ValueError(f"Each row must contain exactly {size} integers.")

        rows.append(row_values)

    matrix = np.array(rows)

    print("\nOriginal matrix:")
    print(matrix)

    swap_diagonals(matrix)

    print("\nMatrix after swapping diagonals:")
    print(matrix)


if __name__ == "__main__":
    main()