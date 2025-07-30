class Matrix:
    def __init__(self, data: list[list[float]]):
        """Initialize a matrix from a list of lists."""
        self.data = [row[:] for row in data]  # Create a deep copy
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0

    def __matmul__(self, other: "Matrix") -> "Matrix":
        """Implement @ operator for matrix multiplication."""
        if not isinstance(other, Matrix):
            raise ValueError("Can only multiply with another Matrix object")
        if self.cols != other.rows:
            raise ValueError("Number of columns in first matrix must equal number of rows in second matrix")
        
        result = [[0 for _ in range(other.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result[i][j] += self.data[i][k] * other.data[k][j]
        return Matrix(result)


    def __repr__(self):
        """String representation of the matrix."""
        return str(self.data)
    

def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    """
    Multiply two matrices using the @ operator.
    
    Args:
        a (Matrix): First matrix.
        b (Matrix): Second matrix.
    
    Returns:
        Matrix: Resulting matrix after multiplication.
    """
    return a @ b


def matrix(data: list[list[float]]) -> Matrix:
    """
    Create a matrix from a 2D list representing the matrix data.
    
    Args:
        data (list[list[float]]): 2D list representing the matrix data.
    
    Returns:
        Matrix: Matrix object
    """
    return Matrix(data)

# Export the matrix functions for external use
__all__ = ["matrix", "matrix_multiply"]
