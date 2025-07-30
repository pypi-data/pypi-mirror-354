# alumathblackout

A Python library for advanced matrix operations, specifically designed for efficient matrix multiplication with support for matrices of different dimensions.

## Installation

You can install `alumathblackout` directly from PyPI using pip:

```bash
pip install alumathblackout
```

### Alternative Installation Methods

If you encounter any issues with the standard installation, try:

```bash
# Install with user permissions
pip install --user alumathblackout

# Upgrade to latest version
pip install --upgrade alumathblackout

# Install specific version
pip install alumathblackout==1.0.0
```

## Quick Start

```python
import alumathblackout as amb

# Create matrices
matrix_a = amb.matrix([[1, 2], [3, 4]])
matrix_b = amb.matrix([[5, 6], [7, 8]])

# Perform matrix multiplication
result = amb.matrix_multiply(matrix_a, matrix_b)
print(result)

# Or use matrix multiplication operator @
result = matrix_a @ matrix_b
print(result)
```

## Features

- **Matrix Multiplication**: Efficient matrix multiplication for compatible dimensions
- **Dimension Validation**: Automatic validation of matrix dimensions for multiplication
- **Error Handling**: Clear error messages for incompatible operations
- **Multiple Data Types**: Support for integers, floats, and mixed numeric types
- **Flexible Input**: Accepts nested lists and numpy arrays

## Usage Examples

### Basic Matrix Multiplication

```python
import alumathblackout as amb

# 2x2 matrices
A = amb.matrix(
     [[1, 2], 
     [3, 4]])

B = amb.matrix(
     [[5, 6], 
     [7, 8]])

result = amb.matrix_multiply(A, B)
# Output: [[19, 22], [43, 50]]
```

### Different Dimensions

```python
import alumathblackout as amb

# 2x3 matrix
A = amb.matrix(
     [[1, 2, 3], 
     [4, 5, 6]])

# 3x2 matrix  
B = amb.matrix(
     [[7, 8], 
     [9, 10], 
     [11, 12]])

result = amb.matrix_multiply(A, B)
# Output: [[58, 64], [139, 154]]
```

### With Floating Point Numbers

```python
import alumathblackout as amb

A = amb.matrix(
     [[1.5, 2.5], 
     [3.5, 4.5]])

B = amb.matrix(
     [[0.5, 1.5], 
     [2.5, 3.5]])

result = amb.matrix_multiply(A, B)
# Output: [[7.0, 11.0], [13.0, 21.0]]
```

## API Reference

### `matrix_multiply(matrix_a, matrix_b)`

Performs matrix multiplication of two matrices.

**Parameters:**
- `matrix_a` (list of lists): First matrix (m×n dimensions)
- `matrix_b` (list of lists): Second matrix (n×p dimensions)

**Returns:**
- `list of lists`: Resulting matrix (m×p dimensions)

**Raises:**
- `ValueError`: If matrices have incompatible dimensions
- `TypeError`: If input is not a valid matrix format

**Example:**
```python
result = amb.matrix_multiply(amb.matrix([[1, 2]]), amb.matrix([[3], [4]]))
# Returns: [[11]]
```

## Requirements

- Python 3.6 or higher
- No external dependencies required

## Error Handling

The library provides clear error messages for common issues:

```python
import alumathblackout as amb

# Incompatible dimensions
A = amb.matrix([[1, 2]])      # 1x2
B = amb.matrix([[3, 4, 5]])   # 1x3

try:
    result = amb.matrix_multiply(A, B)
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Cannot multiply matrices: columns of first matrix (2) must equal rows of second matrix (1)
```

## Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup

1. Clone the repository
2. Install development dependencies
3. Run tests before submitting changes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the documentation above
2. Search existing issues on GitHub
3. Create a new issue with detailed information about your problem

## Changelog

### Version 1.0.0
- Initial release
- Basic matrix multiplication functionality
- Dimension validation
- Error handling

## Authors

- **Blackout Team** - *Initial work*

## Acknowledgments

- Thanks to the ALU community for support and feedback
- Inspired by linear algebra principles and efficient computation methods
