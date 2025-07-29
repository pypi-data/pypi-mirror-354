"""
Matrix Operations Module
Handles matrix multiplication with detailed error messages.
"""

from typing import List, Union


class Matrix:
    """A matrix class that stores 2D arrays and provides basic operations."""

    def __init__(self, data: List[List[Union[int, float]]]):
        if not data or not data[0]:
            raise ValueError("Matrix cannot be empty!")

        row_length = len(data[0])
        for i, row in enumerate(data):
            if len(row) != row_length:
                raise ValueError(f"All rows must have the same length. Row {i} has length {len(row)}, expected {row_length}")

        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def __str__(self):
        result = []
        for row in self.data:
            result.append("[" + " ".join(f"{x:8.2f}" for x in row) + "]")
        return "\n".join(result)

    def __repr__(self):
        return f"Matrix({self.rows}x{self.cols})"

    def get_dimensions(self):
        return (self.rows, self.cols)


class MatrixMultiplicationError(Exception):
    def __init__(self, message, error_type="general"):
        self.error_type = error_type
        super().__init__(message)


class MatrixMultiplier:
    @staticmethod
    def _get_detailed_error(matrix1_dims, matrix2_dims):
        """Generate a detailed technical error message for invalid multiplication."""
        message = "\n❌ Matrix Multiplication Error ❌\n\n"
        message += "Matrix dimensions are not compatible for multiplication.\n\n"
        message += f"📊 Matrix A dimensions: {matrix1_dims[0]} x {matrix1_dims[1]}\n"
        message += f"📊 Matrix B dimensions: {matrix2_dims[0]} x {matrix2_dims[1]}\n"
        message += "\n📌 Rule: The number of columns in Matrix A must equal the number of rows in Matrix B.\n"
        message += "💡 Tip: Check the shape of your matrices before multiplying.\n"
        return message

    @staticmethod
    def multiply(matrix1: Union[Matrix, List[List]], matrix2: Union[Matrix, List[List]]) -> Matrix:
        if not isinstance(matrix1, Matrix):
            matrix1 = Matrix(matrix1)
        if not isinstance(matrix2, Matrix):
            matrix2 = Matrix(matrix2)

        if matrix1.cols != matrix2.rows:
            detailed_error = MatrixMultiplier._get_detailed_error(
                matrix1.get_dimensions(), 
                matrix2.get_dimensions()
            )
            raise MatrixMultiplicationError(detailed_error, "dimension_mismatch")

        result_rows = matrix1.rows
        result_cols = matrix2.cols
        result = [[0 for _ in range(result_cols)] for _ in range(result_rows)]

        for i in range(result_rows):
            for j in range(result_cols):
                for k in range(matrix1.cols):
                    result[i][j] += matrix1.data[i][k] * matrix2.data[k][j]

        return Matrix(result)

    @staticmethod
    def can_multiply(matrix1: Union[Matrix, List[List]], matrix2: Union[Matrix, List[List]]) -> bool:
        if not isinstance(matrix1, Matrix):
            matrix1 = Matrix(matrix1)
        if not isinstance(matrix2, Matrix):
            matrix2 = Matrix(matrix2)

        return matrix1.cols == matrix2.rows

    @staticmethod
    def get_result_dimensions(matrix1: Union[Matrix, List[List]], matrix2: Union[Matrix, List[List]]) -> tuple:
        if not isinstance(matrix1, Matrix):
            matrix1 = Matrix(matrix1)
        if not isinstance(matrix2, Matrix):
            matrix2 = Matrix(matrix2)

        if not MatrixMultiplier.can_multiply(matrix1, matrix2):
            detailed_error = MatrixMultiplier._get_detailed_error(
                matrix1.get_dimensions(), 
                matrix2.get_dimensions()
            )
            raise MatrixMultiplicationError(detailed_error, "dimension_mismatch")

        return (matrix1.rows, matrix2.cols)


def multiply_matrices(matrix1, matrix2):
    return MatrixMultiplier.multiply(matrix1, matrix2)


def create_matrix(data):
    return Matrix(data)
