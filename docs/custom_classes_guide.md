# Using Custom Classes in Pyleet

This guide shows you how to use custom classes other than TreeNode and ListNode in Pyleet's test framework.

## Overview

Pyleet supports any custom class through its extensible serialization system. You can register both deserializers (for input) and serializers (for output) for your own classes and use them in test cases with the format `{"ClassName": data}`.

**Key Features:**
- **No `val` attribute required** - Unlike TreeNode/ListNode, your custom classes don't need specific attributes
- **Automatic method selection** - Pyleet intelligently chooses the right method based on input types
- **Bidirectional serialization** - Both input deserialization and output serialization are supported
- **Flexible class design** - Any class structure is supported as long as you provide the serialization functions

## Step-by-Step Process

### 1. Define Your Custom Class

```python
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):  # Important for test comparisons
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # Helpful for debugging
        return f"Point({self.x}, {self.y})"
```

### 2. Define Deserializer and Serializer Functions

```python
def list_to_point(data):
    """
    Convert list to Point (for input deserialization).
    Format: [x, y]
    Example: [3, 4] -> Point(3, 4)
    """
    if not data or len(data) != 2:
        return None
    return Point(data[0], data[1])

def point_to_list(point):
    """
    Convert Point to list (for output serialization).
    Format: Point -> [x, y]
    Example: Point(3, 4) -> [3, 4]
    """
    if not point:
        return None
    return [point.x, point.y]
```

### 3. Register Your Deserializer and Serializer

```python
from pyleet import register_deserializer, register_serializer

register_deserializer("Point", list_to_point)
register_serializer("Point", point_to_list)
```

### 4. Define Your Solution Methods

Pyleet automatically selects the appropriate method based on input types. Method names should include the class name for best results:

```python
class Solution:
    def processPoint(self, point):
        """Process a Point object"""
        if not point:
            return None
        # Example: calculate distance from origin
        distance = (point.x ** 2 + point.y ** 2) ** 0.5
        return Point(int(distance), 0)

    def processMatrix(self, matrix):
        """Process a Matrix object"""
        # Your matrix processing logic here
        pass
```

### 5. Use in Test Cases

```json
[
  {
    "description": "Point distance calculation",
    "input": [{"Point": [3, 4]}],
    "expected": {"Point": [5, 0]}
  },
  {
    "description": "Point at origin",
    "input": [{"Point": [0, 0]}],
    "expected": {"Point": [0, 0]}
  }
]
```

## Automatic Method Selection

Pyleet intelligently selects which method to call based on your input types:

- **Single method**: If your Solution class has only one method, it's used automatically
- **Type matching**: Method names containing the input type are preferred (e.g., `Point` input → `processPoint` method)
- **Fallback**: If no match is found, the first available method is used

**Examples:**
- `{"Point": [3, 4]}` → calls `processPoint()` method
- `{"Matrix": [[1, 2], [3, 4]]}` → calls `processMatrix()` method
- `{"Interval": [1, 5]}` → calls `processInterval()` method

## Common Custom Class Examples

### Example 1: Interval Class

```python
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

def list_to_interval(data):
    """Convert [start, end] to Interval"""
    if not data or len(data) != 2:
        return None
    return Interval(data[0], data[1])

def interval_to_list(interval):
    """Convert Interval to [start, end]"""
    if not interval:
        return None
    return [interval.start, interval.end]

register_deserializer("Interval", list_to_interval)
register_serializer("Interval", interval_to_list)
```

**Solution Method:**
```python
def processInterval(self, interval):
    """Expand interval by 1 on each side"""
    if not interval:
        return None
    return Interval(interval.start - 1, interval.end + 1)
```

**Test Case:**
```json
{
  "description": "Interval expansion",
  "input": [{"Interval": [2, 5]}],
  "expected": {"Interval": [1, 6]}
}
```

### Example 2: Matrix Class

```python
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

def list_to_matrix(data):
    """Convert 2D list to Matrix"""
    return Matrix(data)

def matrix_to_list(matrix):
    """Convert Matrix to 2D list"""
    if not matrix:
        return []
    return matrix.grid

register_deserializer("Matrix", list_to_matrix)
register_serializer("Matrix", matrix_to_list)
```

**Solution Method:**
```python
def processMatrix(self, matrix):
    """Transpose the matrix"""
    if not matrix or not matrix.grid:
        return Matrix([])
    transposed = list(zip(*matrix.grid))
    return Matrix([list(row) for row in transposed])
```

**Test Case:**
```json
{
  "description": "Matrix transpose",
  "input": [{"Matrix": [[1, 2, 3], [4, 5, 6]]}],
  "expected": {"Matrix": [[1, 4], [2, 5], [3, 6]]}
}
```

### Example 3: Graph Node

```python
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

    # Return the first node
    return nodes[data[0][0]] if data else None

register_deserializer("GraphNode", list_to_graphnode)
```

**Test Case:**
```json
{
  "input": [{"GraphNode": [[1, [2, 3]], [2, [1]], [3, [1]]]}],
  "expected": {"GraphNode": [[2, []]]}
}
```

## Best Practices

### 1. Always Implement `__eq__` Method

```python
def __eq__(self, other):
    if not isinstance(other, self.__class__):
        return False
    # Compare relevant attributes
    return self.attr1 == other.attr1 and self.attr2 == other.attr2
```

### 2. Implement `__repr__` for Debugging

```python
def __repr__(self):
    return f"ClassName(attr1={self.attr1}, attr2={self.attr2})"
```

### 3. Always Register Both Deserializers and Serializers

For proper bidirectional conversion, register both functions:

```python
# Register deserializer for input conversion
register_deserializer("CustomClass", list_to_custom_class)

# Register serializer for output conversion
register_serializer("CustomClass", custom_class_to_list)
```

### 4. Handle Edge Cases in Both Directions

```python
def list_to_custom_class(data):
    # Handle None/empty input
    if not data:
        return None

    # Validate input format
    if not isinstance(data, list) or len(data) != expected_length:
        raise ValueError(f"Expected list of length {expected_length}, got {data}")

    # Create and return instance
    return CustomClass(data[0], data[1])

def custom_class_to_list(obj):
    # Handle None input
    if not obj:
        return None

    # Convert back to list format
    return [obj.attr1, obj.attr2]
```

### 5. Use Descriptive Method Names

Method names should include the class type for automatic selection:

```python
class Solution:
    def processPoint(self, point):      # Will be called for Point inputs
        pass

    def processMatrix(self, matrix):    # Will be called for Matrix inputs
        pass

    def processInterval(self, interval): # Will be called for Interval inputs
        pass
```

### 6. Use Descriptive Function Names

```python
# Good
register_deserializer("Point", list_to_point)
register_serializer("Point", point_to_list)

# Avoid
register_deserializer("P", some_function)
register_serializer("Data", generic_function)
```

## Complete Working Example

Here's a complete example you can run:

```python
from pyleet import register_deserializer, register_serializer

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

def list_to_point(data):
    if not data or len(data) != 2:
        return None
    return Point(data[0], data[1])

def point_to_list(point):
    if not point:
        return None
    return [point.x, point.y]

register_deserializer("Point", list_to_point)
register_serializer("Point", point_to_list)

class Solution:
    def processPoint(self, point):
        """Calculate distance from origin and return as new point"""
        if not point:
            return None
        distance = (point.x ** 2 + point.y ** 2) ** 0.5
        return Point(int(distance), 0)
```

**Test Cases (point_testcases.json):**
```json
[
  {
    "description": "Point distance calculation",
    "input": [{"Point": [3, 4]}],
    "expected": {"Point": [5, 0]}
  },
  {
    "description": "Point at origin",
    "input": [{"Point": [0, 0]}],
    "expected": {"Point": [0, 0]}
  }
]
```

**Run with:**
```bash
pyleet your_solution.py --testcases point_testcases.json
```

## Key Points

1. **No special attributes required** - Your classes don't need `val` or any specific attributes
2. **Bidirectional serialization** - Register both deserializers and serializers for complete support
3. **Automatic method selection** - Pyleet chooses the right method based on input types
4. **Use concise format** - `{"ClassName": data}` in JSON test cases
5. **Handle edge cases** - Both serializers and deserializers should handle None, empty, and invalid input
6. **Implement comparison methods** - `__eq__` is essential for test validation
7. **Descriptive naming** - Use clear names for methods and functions to enable automatic selection

## Recent Improvements

- ✅ **Fixed serialization errors** - Custom classes no longer need `val` attributes
- ✅ **Enhanced method selection** - Automatic selection based on input types
- ✅ **Bidirectional support** - Both input and output serialization
- ✅ **Robust comparison** - Multiple fallback strategies for output comparison

This system makes Pyleet extremely flexible for testing any type of algorithm that uses custom data structures!
