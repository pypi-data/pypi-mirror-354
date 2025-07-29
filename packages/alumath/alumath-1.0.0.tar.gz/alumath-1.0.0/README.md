# AlumMath

A simple Python library for matrix multiplication with proper validation.

## Installation

```bash
pip install alumath
```
## QuickStart

```
from alumath import Matrix, matrix_multiply

# Create matrices
A = Matrix([[1, 2, 3], [4, 5, 6]])      # 2×3 matrix  
B = Matrix([[7, 8], [9, 10], [11, 12]]) # 3×2 matrix

# Multiply matrices
result = A * B
print(result)
print(f"Result shape: {result.shape()}")  # (2, 2)
```

## Features

✅ Matrix multiplication with dimension validation
✅ Clear error messages for incompatible matrices
✅ Clean display formatting
✅ Support for different matrix dimensions

## License
MIT License

### `LICENSE`

