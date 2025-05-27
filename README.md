# Pyleet

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/github/license/ergs0204/Pyleet)

Pyleet is a Python tool that allows you to **run and test your LeetCode Python solutions locally** with minimal modification. It bridges the gap between LeetCode's online environment and local development, making it easier to debug and verify your solutions offline.

---

## Features

- Run LeetCode Python solutions locally without modifying your original code
- Provide test cases in a separate file (`.txt` or `.json`)
- Simple CLI command: `pyleet solution.py --testcases cases.txt`
- **🎯 Built-in ListNode and TreeNode classes** - No need to define common LeetCode classes yourself!
- **🔄 Three usage patterns** - Automatic fallback, explicit import, or custom override
- **🧠 Flexible method selection** - Automatic selection based on input types OR explicit method specification
- **↔️ Bidirectional serialization** - Both input deserialization and output serialization
- **🔧 Enhanced custom class support** - Any class structure supported, no `val` attribute required
- Supports all common LeetCode data structures (lists, integers, strings, TreeNode, ListNode, and more)
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

## Built-in ListNode and TreeNode Classes

🎉 **New Feature**: Pyleet now includes built-in `ListNode` and `TreeNode` classes, so you don't need to define these common LeetCode data structures yourself!

### Three Usage Patterns

#### 1. **Automatic Fallback** (Zero Configuration)
Just write your solution - Pyleet automatically provides the classes:

```python
# No imports needed!
class Solution:
    def reverseList(self, head):
        """Reverse a linked list - ListNode is automatically available"""
        prev = None
        current = head
        while current:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp
        return prev

    def invertTree(self, root):
        """Invert a binary tree - TreeNode is automatically available"""
        if not root:
            return None
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
```

#### 2. **Explicit Import** (Recommended)
Import the classes for better code clarity:

```python
from pyleet import ListNode, TreeNode

class Solution:
    def mergeTwoLists(self, list1, list2):
        """Merge two sorted linked lists"""
        dummy = ListNode(0)
        current = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next

        current.next = list1 or list2
        return dummy.next
```

#### 3. **Custom Override** (Advanced)
Define your own classes to override the built-in ones:

```python
# Your custom implementation takes precedence
class ListNode:
    def __init__(self, val=0, next=None, custom_attr=None):
        self.val = val
        self.next = next
        self.custom_attr = custom_attr  # Your custom attribute

class Solution:
    def customListProcessor(self, head):
        """Uses your custom ListNode implementation"""
        # Your implementation here
        pass
```

### Test Cases Work Seamlessly

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

### Key Benefits

- ✅ **Zero boilerplate** - No need to copy-paste class definitions
- ✅ **Flexible** - Use built-in classes or define your own
- ✅ **Standard compliant** - Built-in classes match LeetCode specifications
- ✅ **Automatic serialization** - Input/output conversion handled automatically

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

## Custom Classes Support

For detailed information about using custom classes with Pyleet, including:
- How to define and register custom classes
- Serialization and deserialization
- Method selection with custom classes
- Best practices and examples

Please see the [Custom Classes Guide](docs/custom_classes_guide.md).

---

## Recent Improvements

- 🎯 **NEW: Built-in ListNode and TreeNode classes** - Zero configuration needed for common LeetCode problems
- 🔄 **NEW: Three usage patterns** - Automatic fallback, explicit import, or custom override
- ✅ **Enhanced custom class support** - Any class structure now supported
- ✅ **Fixed serialization errors** - No more `val` attribute requirements
- ✅ **Flexible method selection** - Both automatic selection and explicit method specification via `--method` parameter
- ✅ **Bidirectional serialization** - Both input and output serialization support
- ✅ **Robust comparison** - Multiple fallback strategies for output comparison
- ✅ **Improved error handling** - Clear feedback when specified methods are not found

## Roadmap

- Optional feature to **fetch test cases automatically from LeetCode**
- Integration with testing frameworks (pytest, unittest)
- Handle print correctly. Currently print everything before showing test result.
- Run solution file as script (eg: adding `pyleet.run()` in the end).
- Support for more data structures.
- Run tests in parallel.
- Record running time.
- Performance optimizations for large test suites

---

## License

MIT License