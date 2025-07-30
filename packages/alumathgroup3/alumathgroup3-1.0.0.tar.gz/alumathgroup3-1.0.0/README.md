# ALUMatrixMath

A simple Python library for matrix multiplication with proper validation.

## Installation

```bash
pip install alumathgroup3
```
## QuickStart

```
from alumathgroup3 import Matrix, matrix_multiply

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

## More example using alumath
```
    from alumath import Matrix, matrix_multiply

    # Example 1: Compatible matrices
    print("Example 1: 2x3 × 3x2 matrices")
    m1 = Matrix([[1, 2, 3], [4, 5, 6]])
    m2 = Matrix([[7, 8], [9, 10], [11, 12]])

    print(f"Matrix A {m1.shape()}:")
    print(m1)
    print(f"\nMatrix B {m2.shape()}:")
    print(m2)

    result = m1 * m2
    print(f"\nA × B = {result.shape()}:")
    print(result)
    print()

    # Example 2: Different dimensions
    print("Example 2: 3x2 × 2x4 matrices")
    m3 = Matrix([[1, 2], [3, 4], [5, 6]])
    m4 = Matrix([[1, 0, 1, 2], [2, 1, 0, 1]])

    print(f"Matrix C {m3.shape()}:")
    print(m3)
    print(f"\nMatrix D {m4.shape()}:")
    print(m4)

    result2 = matrix_multiply(m3, m4)
    print(f"\nC × D = {result2.shape()}:")
    print(result2)
    print()

    # Example 3: Error case
    print("Example 3: Incompatible matrices (will show error)")
    try:
        m5 = Matrix([[1, 2]])  # 1x2
        m6 = Matrix([[1], [2], [3]])  # 3x1
        print(f"Trying to multiply {m5.shape()} × {m6.shape()}")
        result3 = m5 * m6
    except ValueError as e:
        print(f"Error: {e}")
```

## License
MIT License

### `LICENSE`
