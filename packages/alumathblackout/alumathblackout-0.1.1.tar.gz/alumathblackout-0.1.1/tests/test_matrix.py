import unittest
from alumathblackout import matrix

class TestMatrixOperations(unittest.TestCase):

    def test_create_matrix(self):
        """Test creating a matrix from a list of lists."""
        data = [[1, 2], [4, 5]]
        m = matrix(data)
        self.assertEqual(m.data, data)
        self.assertEqual(m.rows, 2)
        self.assertEqual(m.cols, 2)

    def test_matrix_multiplication(self):
        """Test matrix multiplication using the @ operator."""
        a = matrix([[1, 2], [3, 4]])
        b = matrix([[5, 6], [7, 8]])
        result = a @ b
        expected = matrix([[19, 22], [43, 50]])
        self.assertEqual(result.data, expected.data)

if __name__ == "__main__":
    unittest.main()