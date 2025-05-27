"""
Example showing how to use custom classes other than TreeNode/ListNode in Pyleet.
"""

from pyleet import register_deserializer, register_serializer

# Step 1: Define Your Custom Classes

# Example: Matrix/Grid


class Matrix:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        return self.grid == other.grid

    def __repr__(self):
        return f"Matrix({self.grid})"

# Step 2: Define Deserializer Functions


def list_to_matrix(data):
    """
    Convert 2D list to Matrix.
    Format: [[row1], [row2], ...]
    Example: [[1, 2, 3], [4, 5, 6]]
    """
    return Matrix(data)

# Step 3: Define Serializer Functions (reverse of deserializers)


def matrix_to_list(matrix):
    """
    Convert Matrix to 2D list.
    """
    if not matrix:
        return []
    return matrix.grid


# Step 4: Register Your Deserializers and Serializers

register_deserializer("Matrix", list_to_matrix)

register_serializer("Matrix", matrix_to_list)

# Step 5: Your Solution Class


class Solution:
    def processMatrix(self, matrix):
        """Example function that processes a matrix"""
        if not matrix or not matrix.grid:
            return Matrix([])
        # Simple example: transpose the matrix
        transposed = list(zip(*matrix.grid))
        return Matrix([list(row) for row in transposed])
