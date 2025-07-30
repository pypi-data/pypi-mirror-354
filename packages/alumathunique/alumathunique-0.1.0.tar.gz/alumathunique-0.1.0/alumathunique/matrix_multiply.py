"""
Matrix Multiply Module
Handles matrix multiplication
"""

import random
from typing import List, Union


class Matrix:
    """A matrix class that stores 2D arrays and provides basic operations."""

    def __init__(self, data: List[List[Union[int, float]]]):
        """
        Initialize a matrix with 2D list data.

        Args:
            data: 2D list representing the matrix
        """
        if not data or not data[0]:
            raise ValueError("Matrix cannot be empty!")

        # Check if all rows have the same length
        row_length = len(data[0])
        for i, row in enumerate(data):
            if len(row) != row_length:
                raise ValueError(
                    f"All rows must have the same length! Row {i} has length {len(row)}, expected {row_length}"
                )

        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def __str__(self):
        """String representation of the matrix."""
        result = []
        for row in self.data:
            result.append("[" + " ".join(f"{x:8.2f}" for x in row) + "]")
        return "\n".join(result)

    def __repr__(self):
        return f"Matrix({self.rows}x{self.cols})"

    def get_dimensions(self):
        """Return matrix dimensions as (rows, cols)."""
        return (self.rows, self.cols)


class MatrixMultiplicationError(Exception):
    """Custom exception for matrix multiplication errors with personality!"""

    def __init__(self, message, error_type="general"):
        self.error_type = error_type
        super().__init__(message)


class MatrixMultiplier:
    """
    The main matrix multiplication class with personality-driven error messages.
    Each group member has their own style of preventing invalid operations!
    """

    # Funny error messages for each group member
    ERROR_MESSAGES = {
        "belyse": [
            "Belyse can't allow you to do that because he's too busy debugging his own code to fix your matrix dimensions.",
            "Belyse says: 'Nope! These matrices are more incompatible than Windows and stability.'",
            "Belyse is blocking this operation because he knows it'll crash harder than his laptop during finals week.",
            "Belyse refuses because he's seen enough mathematical disasters for one lifetime.",
            "Belyse can't let you do that because he's seen what happens when dimensions don't match - chaos.",
            "Belyse declares: 'I'd rather debug recursive functions than deal with these incompatible matrices.'"
        ],
        "elyse": [
            "Elyse (the group leader) can't permit this because she has standards, and your matrices don't meet them.",
            "Elyse says: 'As group leader, I hereby veto this mathematical catastrophe.'",
            "Elyse is stopping you because she's responsible for everyone's grades and this isn't it.",
            "Elyse declares: 'My leadership skills include preventing linear algebra disasters like this one.'",
            "Elyse says: 'These matrices are more misaligned than my sleep schedule during exam week.'"
        ],
        "bella": [
            "Bella can't allow this because he's too busy solving actual solvable problems.",
            "Bella says: 'Even my calculator is laughing at these dimension mismatches.'",
            "Bella is blocking this operation because he values his mathematical sanity.",
            "Bella refuses because he's already traumatized by enough matrix errors this semester.",
            "Bella is preventing this because he believes in mathematical harmony, not dimension discord."
        ]
    }

    @staticmethod
    def _get_funny_error(matrix1_dims, matrix2_dims):
        """Generate error message from a random group member."""
        members = list(MatrixMultiplier.ERROR_MESSAGES.keys())
        chosen_member = random.choice(members)
        error_template = random.choice(MatrixMultiplier.ERROR_MESSAGES[chosen_member])

        detailed_error = (
            f"MATRIX MULTIPLICATION DENIED!\n\n{error_template}\n\n"
            f"Technical Details:\n"
            f"   • Matrix A dimensions: {matrix1_dims[0]}×{matrix1_dims[1]}\n"
            f"   • Matrix B dimensions: {matrix2_dims[0]}×{matrix2_dims[1]}\n"
            f"   • Problem: Matrix A has {matrix1_dims[1]} columns, but Matrix B has {matrix2_dims[0]} rows\n"
            f"   • For multiplication A×B, columns of A must equal rows of B!\n"
            f"\nSuggestion: Try transposing one of your matrices or check your data.\n"
            f"   (Blocked by: {chosen_member.title()} from ALU Math Unique)\n"
        )

        return detailed_error

    @staticmethod
    def multiply(matrix1: Union[Matrix, List[List]], matrix2: Union[Matrix, List[List]]) -> Matrix:
        """
        Multiply two matrices with style and personality!

        Args:
            matrix1: First matrix (Matrix object or 2D list)
            matrix2: Second matrix (Matrix object or 2D list)

        Returns:
            Matrix: Result of matrix multiplication

        Raises:
            MatrixMultiplicationError: When matrices can't be multiplied (with personality!)
        """
        # Convert to Matrix objects if needed
        if not isinstance(matrix1, Matrix):
            matrix1 = Matrix(matrix1)
        if not isinstance(matrix2, Matrix):
            matrix2 = Matrix(matrix2)

        # Check if multiplication is possible
        if matrix1.cols != matrix2.rows:
            funny_error = MatrixMultiplier._get_funny_error(
                matrix1.get_dimensions(),
                matrix2.get_dimensions()
            )
            raise MatrixMultiplicationError(funny_error, "dimension_mismatch")

        # Perform matrix multiplication
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
        """
        Check if two matrices can be multiplied.

        Args:
            matrix1: First matrix
            matrix2: Second matrix

        Returns:
            bool: True if matrices can be multiplied, False otherwise
        """
        if not isinstance(matrix1, Matrix):
            matrix1 = Matrix(matrix1)
        if not isinstance(matrix2, Matrix):
            matrix2 = Matrix(matrix2)

        return matrix1.cols == matrix2.rows

    @staticmethod
    def get_result_dimensions(matrix1: Union[Matrix, List[List]], matrix2: Union[Matrix, List[List]]) -> tuple:
        """
        Get the dimensions of the result matrix if multiplication is possible.

        Args:
            matrix1: First matrix
            matrix2: Second matrix

        Returns:
            tuple: (rows, cols) of result matrix

        Raises:
            MatrixMultiplicationError: If matrices can't be multiplied
        """
        if not isinstance(matrix1, Matrix):
            matrix1 = Matrix(matrix1)
        if not isinstance(matrix2, Matrix):
            matrix2 = Matrix(matrix2)

        if not MatrixMultiplier.can_multiply(matrix1, matrix2):
            funny_error = MatrixMultiplier._get_funny_error(
                matrix1.get_dimensions(),
                matrix2.get_dimensions()
            )
            raise MatrixMultiplicationError(funny_error, "dimension_mismatch")

        return (matrix1.rows, matrix2.cols)


# Convenience functions for easy access
def multiply_matrices(matrix1, matrix2):
    """Convenience function for matrix multiplication."""
    return MatrixMultiplier.multiply(matrix1, matrix2)


def create_matrix(data):
    """Convenience function to create a Matrix object."""
    return Matrix(data)
