# Pyleet

Pyleet is a Python tool that allows you to **run and test your LeetCode Python solutions locally** with minimal modification. It bridges the gap between LeetCode's online environment and local development, making it easier to debug and verify your solutions offline.

---

## Features

- Run LeetCode Python solutions locally without modifying your original code
- Provide test cases in a separate file (`.txt` or `.json`)
- Simple CLI command: `pyleet solution.py --testcases cases.txt`
- **Enhanced custom class support** - Any class structure supported, no `val` attribute required
- **Flexible method selection** - Automatic selection based on input types OR explicit method specification
- **Bidirectional serialization** - Both input deserialization and output serialization
- Supports common LeetCode data structures (lists, integers, strings, TreeNode, ListNode)
- Easy installation via `pip` or `setup.py`
- Robust error handling and comparison strategies

---

## Installation

<!-- ### Using pip (after packaging/uploading)

```bash
pip install pyleet
``` -->

### From source (development mode)

```bash
git clone https://github.com/yourusername/pyleet.git
cd pyleet
pip install -e .
```

---

## Usage

Prepare your **LeetCode solution file** (e.g., `solution.py`) as you would submit it on LeetCode, without modification.

Prepare a **test case file** (e.g., `cases.txt`) containing your test inputs and expected outputs.

### Basic command

```bash
pyleet solution.py --testcases cases.txt
```

### Advanced usage with method selection

When your solution class contains multiple methods, you can specify which one to use:

```bash
# Automatic method selection (default behavior)
pyleet solution.py --testcases cases.txt

# Explicit method selection
pyleet solution.py --testcases cases.txt --method twoSum
pyleet solution.py --testcases cases.txt -m threeSum
```

### Example test case file format

Plain text format (initial version):

```
[1,2,3]
6

[4,5,6]
15
```

Each test case consists of:
- **Input arguments** (e.g., `[1,2,3]`)
- **Expected output** (e.g., `6`)
- Separated by a blank line

---

## How It Works

- Loads your solution file dynamically
- Loads and parses the test cases from the external file
- Converts inputs into Python data structures
- Calls your solution method with the inputs
- Compares the output to the expected result
- Reports pass/fail status for each test case

---

## Method Selection

Pyleet provides flexible method selection to handle solution classes with multiple methods. This is particularly useful when working on multiple LeetCode problems in a single file or when your solution class contains helper methods alongside the main solution methods.

### Automatic Method Selection (Default)

By default, Pyleet automatically selects the appropriate method using intelligent heuristics:

1. **Single method**: If only one method exists, it's used automatically
2. **Type-based matching**: Method names containing input type names are prioritized (e.g., `ListNode` input → `processListNode` method)
3. **Fallback**: Uses the first available method if no type match is found

### Explicit Method Selection

Use the `--method` (or `-m`) parameter to specify exactly which method should be executed:

```bash
pyleet solution.py --testcases cases.txt --method methodName
```

### Example: Multiple Methods in One Solution Class

Consider a solution file with multiple LeetCode problems:

```python
class Solution:
    def twoSum(self, nums, target):
        """LeetCode Problem 1: Two Sum"""
        # Implementation here
        pass

    def threeSum(self, nums):
        """LeetCode Problem 15: Three Sum"""
        # Implementation here
        pass

    def maxSubArray(self, nums):
        """LeetCode Problem 53: Maximum Subarray"""
        # Implementation here
        pass
```

**Testing different methods:**

```bash
# Test the twoSum method specifically
pyleet solution.py --testcases two_sum_cases.json --method twoSum

# Test the threeSum method specifically
pyleet solution.py --testcases three_sum_cases.json --method threeSum

# Test the maxSubArray method specifically
pyleet solution.py --testcases max_subarray_cases.json --method maxSubArray
```

### When to Use Explicit Method Selection

- **Multiple problem solutions**: When your file contains solutions to different LeetCode problems
- **Method name ambiguity**: When automatic selection might choose the wrong method
- **Testing specific implementations**: When you have multiple approaches to the same problem
- **Helper methods present**: When your class contains both solution methods and helper methods

### Error Handling

If you specify a method that doesn't exist, Pyleet will provide helpful feedback:

```bash
$ pyleet solution.py --testcases cases.txt --method nonExistentMethod
Error: Method 'nonExistentMethod' not found. Available methods: ['twoSum', 'threeSum', 'maxSubArray']
```


---

## Recent Improvements

- ✅ **Enhanced custom class support** - Any class structure now supported
- ✅ **Fixed serialization errors** - No more `val` attribute requirements
- ✅ **Flexible method selection** - Both automatic selection and explicit method specification via `--method` parameter
- ✅ **Bidirectional serialization** - Both input and output serialization support
- ✅ **Robust comparison** - Multiple fallback strategies for output comparison
- ✅ **Improved error handling** - Clear feedback when specified methods are not found

## Roadmap

- Optional feature to **fetch test cases automatically from LeetCode**
- Integration with testing frameworks (pytest, unittest)
- Performance optimizations for large test suites

---

## Using Custom Classes (e.g., ListNode, TreeNode, or your own)

Pyleet supports any custom data structure through its enhanced serialization system. **No special attributes like `val` are required** - your classes can have any structure you need.

### 1. Include your class definitions inside your solution file

Define your custom classes with any attributes you need:

```python
# Traditional LeetCode classes
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Your own custom classes - any structure works!
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Matrix:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
```

### 2. Write deserializer and serializer functions

Define both directions of conversion:

```python
# Deserializer: converts JSON data to your class instance
def list_to_point(data):
    if not data or len(data) != 2:
        return None
    return Point(data[0], data[1])

# Serializer: converts your class instance back to JSON data
def point_to_list(point):
    if not point:
        return None
    return [point.x, point.y]
```

### 3. Register both deserializer and serializer

In your solution file, register both functions:

```python
from pyleet import register_deserializer, register_serializer

register_deserializer("Point", list_to_point)
register_serializer("Point", point_to_list)
```

### 4. Define your solution methods with descriptive names

Pyleet can automatically select the right method based on input types, or you can specify the method explicitly:

```python
class Solution:
    def processPoint(self, point):
        """Process a Point - method name includes 'Point' for automatic selection"""
        if not point:
            return None
        # Example: calculate distance from origin
        distance = (point.x ** 2 + point.y ** 2) ** 0.5
        return Point(int(distance), 0)

    def processMatrix(self, matrix):
        """Process a Matrix - method name includes 'Matrix' for automatic selection"""
        # Your matrix processing logic here
        pass

    def alternativePointProcessor(self, point):
        """Alternative Point processing method - use --method to select this one"""
        # Different implementation
        pass
```

**Running with different methods:**
```bash
# Automatic selection (chooses processPoint for Point input)
pyleet solution.py --testcases point_cases.json

# Explicit selection
pyleet solution.py --testcases point_cases.json --method alternativePointProcessor
```

### 5. Prepare your test cases using the concise format

Write your test cases using the concise format for custom classes:

```json
[
  {
    "input": [{"Point": [3, 4]}],
    "expected": {"Point": [5, 0]}
  },
  {
    "input": [{"Matrix": [[1, 2, 3], [4, 5, 6]]}],
    "expected": {"Matrix": [[1, 4], [2, 5], [3, 6]]}
  }
]
```

The format is simple: `{"ClassName": data}` where:
- `ClassName` is the name of your custom class (e.g., "Point", "Matrix", "ListNode")
- `data` is the raw data that will be passed to your deserializer function

### 6. How it works

- **Input**: Pyleet detects the custom class format `{"ClassName": data}` and uses your registered deserializer to convert the data into an instance of your class
- **Method Selection**: Pyleet automatically chooses the method whose name contains the class name (e.g., `Point` input → `processPoint` method)
- **Output**: Pyleet uses your registered serializer to convert the output back to JSON format for comparison
- **Comparison**: Multiple comparison strategies ensure robust test validation

### Key Advantages

- **No attribute restrictions** - Your classes can have any structure
- **Flexible method selection** - Automatic selection OR explicit specification with `--method`
- **Bidirectional serialization** - Both input and output are properly handled
- **Multiple methods support** - Handle solution classes with multiple problem solutions
- **Flexible design** - Works with any custom class you can imagine

---

## License

MIT License