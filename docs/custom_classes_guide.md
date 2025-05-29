# Custom Classes Guide

This guide shows you how to use custom classes in Pyleet's test framework, including both built-in classes and your own custom classes.

## Overview

Pyleet supports any custom class through its extensible serialization system. You can register both deserializers (for input) and serializers (for output) for your own classes and use them in test cases with the format `{"ClassName": data}`.

**Key Features:**
- **Built-in ListNode and TreeNode** - Common LeetCode classes are provided out-of-the-box
- **Three usage patterns** - Automatic fallback, explicit import, or custom override
- **Automatic method selection** - Pyleet intelligently chooses the right method based on input types
- **Bidirectional serialization** - Both input deserialization and output serialization are supported
- **Flexible class design** - Any class structure is supported as long as you provide the serialization functions

## Built-in Classes: ListNode and TreeNode

Pyleet includes built-in `ListNode` and `TreeNode` classes. You don't need to define these common LeetCode data structures yourself.

### Usage Patterns for Built-in Classes

#### Pattern 1: Automatic Fallback (Zero Configuration)
```python
# No imports needed - Pyleet automatically provides the classes
class Solution:
    def reverseList(self, head):
        """ListNode is automatically available"""
        prev = None
        current = head
        while current:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp
        return prev
```

#### Pattern 2: Explicit Import (Recommended)
```python
from pyleet import ListNode

class Solution:
    def mergeTwoLists(self, list1, list2):
        """Explicit import for better code clarity"""
        dummy = ListNode(0)
        # ... implementation
        return dummy.next
```

#### Pattern 3: Custom Override (Advanced)
```python
# Define your own to override built-in classes
class ListNode:
    def __init__(self, val=0, next=None, custom_attr=None):
        self.val = val
        self.next = next
        self.custom_attr = custom_attr  # Your custom addition

class Solution:
    def customProcessor(self, head):
        """Uses your custom ListNode implementation"""
        # ... implementation
```

### Priority System
1. **User-defined classes** (highest priority) - Your classes override built-in ones
2. **Built-in classes** (fallback) - Used when you don't define your own
3. **Error** (last resort) - If neither is available

## Step-by-Step Process for Custom Classes

**Note**: For `ListNode` and `TreeNode`, you can skip this entire process and use the built-in classes! This section is for other custom classes like `Point`, `Matrix`, `Interval`, etc.

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

## Best Practices

### 1. Choose the Right Approach

**Use Built-in Classes When:**
- Working with standard `ListNode` or `TreeNode` problems
- You want zero configuration and minimal boilerplate
- Standard LeetCode behavior is sufficient

**Use Custom Classes When:**
- You need additional attributes or methods
- Working with unsupported data structures (`Point`, `Matrix`, `Interval`, etc.)
- You need specific behavior that differs from LeetCode standards

### 2. Always Implement `__eq__` Method

```python
def __eq__(self, other):
    if not isinstance(other, self.__class__):
        return False
    # Compare relevant attributes
    return self.attr1 == other.attr1 and self.attr2 == other.attr2
```

### 3. Implement `__repr__` for Debugging

```python
def __repr__(self):
    return f"ClassName(attr1={self.attr1}, attr2={self.attr2})"
```

### 4. Always Register Both Deserializers and Serializers

For proper bidirectional conversion, register both functions:

```python
# Register deserializer for input conversion
register_deserializer("CustomClass", list_to_custom_class)

# Register serializer for output conversion
register_serializer("CustomClass", custom_class_to_list)
```

### 5. Handle Edge Cases in Both Directions

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


## Complete Working Examples

### [Example 1](examples/builtin_classes/treenode_example.py): Using Built-in Classes (Recommended for ListNode/TreeNode)

```python
# No imports needed for basic usage!
# Or use explicit import for clarity:
from pyleet import ListNode, TreeNode

class Solution:
    def reverseList(self, head):
        """Reverse a linked list using built-in ListNode"""
        prev = None
        current = head
        while current:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp
        return prev

    def invertTree(self, root):
        """Invert a binary tree using built-in TreeNode"""
        if not root:
            return None
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
```

**Test cases for built-in classes:**
```json
[
  {
    "description": "Reverse linked list",
    "input": [{"ListNode": [1, 2, 3, 4, 5]}],
    "expected": {"ListNode": [5, 4, 3, 2, 1]}
  },
  {
    "description": "Invert binary tree",
    "input": [{"TreeNode": [4, 2, 7, 1, 3, 6, 9]}],
    "expected": {"TreeNode": [4, 7, 2, 9, 6, 3, 1]}
  }
]
```

### Example 2: Using Custom Classes (For other data structures)


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
[Alternative matrix example]((examples/custom_class/))

## Key Points

1. **Built-in classes available** - `ListNode` and `TreeNode` are provided out-of-the-box
2. **Three usage patterns** - Automatic fallback, explicit import, or custom override
3. **No special attributes required** - Your classes don't need `val` or any specific attributes
4. **Bidirectional serialization** - Register both deserializers and serializers for complete support
5. **Use concise format** - `{"ClassName": data}` in JSON test cases
6. **Handle edge cases** - Both serializers and deserializers should handle None, empty, and invalid input
7. **Implement comparison methods** - `__eq__` is essential for test validation

## When to Use What

| Scenario | Recommendation | Example |
|----------|---------------|---------|
| Standard ListNode problems | Use built-in classes | `from pyleet import ListNode` |
| Standard TreeNode problems | Use built-in classes | `from pyleet import TreeNode` |
| Custom data structures | Define custom classes | `Point`, `Matrix`, `Interval` |
| Need extra attributes | Override built-in classes | `ListNode` with timestamps |
| Zero configuration | Automatic fallback | No imports needed |



This system makes Pyleet extremely flexible for testing any type of algorithm, from simple built-in data structures to complex custom classes!
