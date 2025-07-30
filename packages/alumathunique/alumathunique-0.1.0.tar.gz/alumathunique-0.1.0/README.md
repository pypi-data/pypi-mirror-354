# Group27MatrixMultiplier

A fun and educational Python package for matrix multiplication, featuring custom error messages with personality from each group member!

## Features

- Matrix class for 2D array operations
- Matrix multiplication with detailed, humorous error messages
- Easy-to-use API
- Custom exceptions for invalid operations

## Installation

```bash
pip install .
```

## Usage

```python
from alumathunique.matrix_multiply import create_matrix, multiply_matrices

A = create_matrix([[1, 2], [3, 4]])
B = create_matrix([[5, 6], [7, 8]])
C = multiply_matrices(A, B)
print(C)
```

## Running Tests

```bash
pytest
```

## Project Structure

- `alumathunique/` - Main package code
- `tests/` - Unit tests
- `setup.py` - Packaging script
- `README.md` - This file

## Authors

- Belyse, Elyse, Bella (ALU Math Vanguard)