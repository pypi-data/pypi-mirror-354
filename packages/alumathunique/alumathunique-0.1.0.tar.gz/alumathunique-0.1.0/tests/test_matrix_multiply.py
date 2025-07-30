import pytest
from alumathunique.matrix_multiply import (
    Matrix,
    MatrixMultiplier,
    MatrixMultiplicationError,
    multiply_matrices,
    create_matrix,
)

def test_matrix_creation_valid():
    m = create_matrix([[1, 2], [3, 4]])
    assert m.rows == 2
    assert m.cols == 2
    assert m.data == [[1, 2], [3, 4]]

def test_matrix_creation_empty():
    with pytest.raises(ValueError):
        create_matrix([])

def test_matrix_creation_irregular_rows():
    with pytest.raises(ValueError):
        create_matrix([[1, 2], [3]])

def test_matrix_str_and_repr():
    m = create_matrix([[1, 2], [3, 4]])
    s = str(m)
    assert "[" in s and "]" in s
    assert "1.00" in s
    assert repr(m) == "Matrix(2x2)"

def test_get_dimensions():
    m = create_matrix([[1, 2, 3], [4, 5, 6]])
    assert m.get_dimensions() == (2, 3)

def test_matrix_multiplication_valid():
    A = create_matrix([[1, 2], [3, 4]])
    B = create_matrix([[5, 6], [7, 8]])
    C = multiply_matrices(A, B)
    assert C.data == [[19, 22], [43, 50]]

def test_matrix_multiplication_invalid_dimensions():
    A = create_matrix([[1, 2, 3], [4, 5, 6]])
    B = create_matrix([[7, 8], [9, 10]])
    with pytest.raises(MatrixMultiplicationError) as excinfo:
        multiply_matrices(A, B)
    assert "MATRIX MULTIPLICATION DENIED!" in str(excinfo.value)

def test_can_multiply_true():
    A = create_matrix([[1, 2], [3, 4]])
    B = create_matrix([[5, 6], [7, 8]])
    assert MatrixMultiplier.can_multiply(A, B) is True

def test_can_multiply_false():
    A = create_matrix([[1, 2, 3], [4, 5, 6]])
    B = create_matrix([[7, 8], [9, 10]])
    assert MatrixMultiplier.can_multiply(A, B) is False

def test_get_result_dimensions_valid():
    A = create_matrix([[1, 2], [3, 4]])
    B = create_matrix([[5, 6], [7, 8]])
    assert MatrixMultiplier.get_result_dimensions(A, B) == (2, 2)

def test_get_result_dimensions_invalid():
    A = create_matrix([[1, 2, 3], [4, 5, 6]])
    B = create_matrix([[7, 8], [9, 10]])
    with pytest.raises(MatrixMultiplicationError) as excinfo:
        MatrixMultiplier.get_result_dimensions(A, B)
    assert "MATRIX MULTIPLICATION DENIED!" in str(excinfo.value)