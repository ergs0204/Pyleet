"""
Example showing how to use custom classes other than TreeNode/ListNode in Pyleet.
"""

from pyleet import register_deserializer, register_serializer

# Example 1: Graph Node


class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def __eq__(self, other):
        if not isinstance(other, GraphNode):
            return False
        return self.val == other.val and len(self.neighbors) == len(other.neighbors)

    def __repr__(self):
        neighbor_vals = [n.val for n in self.neighbors]
        return f"GraphNode(val={self.val}, neighbors={neighbor_vals})"

# Example 2: Matrix/Grid


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

# Example 3: Interval


class Interval:
    def __init__(self, start=0, end=0):
        self.start = start
        self.end = end

    def __eq__(self, other):
        if not isinstance(other, Interval):
            return False
        return self.start == other.start and self.end == other.end

    def __repr__(self):
        return f"Interval({self.start}, {self.end})"

# Example 4: Point/Coordinate


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# Step 2: Define Deserializer Functions


def list_to_graphnode(data):
    """
    Convert adjacency list to GraphNode.
    Format: [[node_val, [neighbor_vals]], ...]
    Example: [[1, [2, 3]], [2, [1]], [3, [1]]]
    """
    if not data:
        return None

    # Create nodes first
    nodes = {}
    for node_data in data:
        val = node_data[0]
        nodes[val] = GraphNode(val)

    # Add neighbors
    for node_data in data:
        val, neighbor_vals = node_data
        for neighbor_val in neighbor_vals:
            if neighbor_val in nodes:
                nodes[val].neighbors.append(nodes[neighbor_val])

    # Return the first node (or you could return all nodes)
    return nodes[data[0][0]] if data else None


def list_to_matrix(data):
    """
    Convert 2D list to Matrix.
    Format: [[row1], [row2], ...]
    Example: [[1, 2, 3], [4, 5, 6]]
    """
    return Matrix(data)


def list_to_interval(data):
    """
    Convert list to Interval.
    Format: [start, end]
    Example: [1, 5]
    """
    if not data or len(data) != 2:
        return None
    return Interval(data[0], data[1])


def list_to_point(data):
    """
    Convert list to Point.
    Format: [x, y]
    Example: [3, 4]
    """
    if not data or len(data) != 2:
        return None
    return Point(data[0], data[1])


# Step 3: Define Serializer Functions (reverse of deserializers)

def graphnode_to_list(node):
    """
    Convert GraphNode to adjacency list format.
    """
    if not node:
        return None
    # For simplicity, just return the node value and empty neighbors
    # In a real implementation, you'd traverse the entire graph
    return [[node.val, []]]


def matrix_to_list(matrix):
    """
    Convert Matrix to 2D list.
    """
    if not matrix:
        return []
    return matrix.grid


def interval_to_list(interval):
    """
    Convert Interval to list.
    """
    if not interval:
        return None
    return [interval.start, interval.end]


def point_to_list(point):
    """
    Convert Point to list.
    """
    if not point:
        return None
    return [point.x, point.y]


# Step 4: Register Your Deserializers and Serializers
register_deserializer("GraphNode", list_to_graphnode)
register_deserializer("Matrix", list_to_matrix)
register_deserializer("Interval", list_to_interval)
register_deserializer("Point", list_to_point)

register_serializer("GraphNode", graphnode_to_list)
register_serializer("Matrix", matrix_to_list)
register_serializer("Interval", interval_to_list)
register_serializer("Point", point_to_list)

# Step 5: Your Solution Class


class Solution:
    def processGraph(self, node):
        """Example function that processes a graph node"""
        if not node:
            return None
        # Simple example: return a new node with doubled value
        return GraphNode(node.val * 2)

    def processMatrix(self, matrix):
        """Example function that processes a matrix"""
        if not matrix or not matrix.grid:
            return Matrix([])
        # Simple example: transpose the matrix
        transposed = list(zip(*matrix.grid))
        return Matrix([list(row) for row in transposed])

    def processInterval(self, interval):
        """Example function that processes an interval"""
        if not interval:
            return None
        # Simple example: expand interval by 1 on each side
        return Interval(interval.start - 1, interval.end + 1)

    def processPoint(self, point):
        """Example function that processes a point"""
        if not point:
            return None
        # Simple example: move point to origin distance
        distance = (point.x ** 2 + point.y ** 2) ** 0.5
        return Point(int(distance), 0)
