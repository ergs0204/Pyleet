# Pyleet

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/github/license/ergs0204/Pyleet)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ergs0204/Pyleet)

Pyleet is a Python tool that allows you to **run and test your LeetCode Python solutions locally** with minimal modification. It bridges the gap between LeetCode's online environment and local development, making it easier to debug and verify your solutions offline.

---
## Features

- **Local Testing**: Run LeetCode Python solutions locally without modifying code.
- **Test Case Flexibility**: Support for `.txt` and `.json` test case files.
- **Intuitive CLI**: Run tests easily with commands like `pyleet solution.py --testcases cases.txt`.
- - **Smart Method Detection**: Automatically selects methods based on input types or allows explicit selection with `--method`.
- **Built-in Data Structures**: Includes `ListNode` and `TreeNode` with automatic serialization, eliminating boilerplate code.
- **Customizable Execution**: Choose automatic fallback, explicit imports, or custom class overrides for flexible usage.
- **Broad Data Support**: Seamlessly handles lists, integers, strings, and custom classes with bidirectional serialization.
- **Clear Error Reporting**: Provides detailed feedback and comparison for accurate test results.
- **Debugging Support**: Displays `print()` output from solutions in test results for easier debugging.

---
## Installation

### Using pip (coming soon)
We'll update this section once Pyleet is available on PyPI.

### From source (development mode)

```bash
git clone https://github.com/ergs0204/pyleet.git
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
# or using the shorthand
pyleet solution.py -t cases.txt
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

#### Text format:

```
(([2, 7, 11, 15], 9), [0, 1])
(([3, 2, 4], 6), [1, 2])
(([3, 3], 6), [0, 1])
```

Each test case in text format follows the same structure:
- Input arguments in parentheses
- Expected output after a comma

#### JSON format (recommended):

```json
[
  {
    "input": [[2, 7, 11, 15], 9],
    "expected": [0, 1]
  },
  {
    "input": [[3, 2, 4], 6],
    "expected": [1, 2]
  },
  {
    "input": [[3, 3], 6],
    "expected": [0, 1]
  }
]
```

#### Advanced JSON example with TreeNode:

```json
[
  {
    "description": "Invert binary tree - simple case",
    "input": [{"TreeNode": [4, 2, 7, 1, 3, 6, 9]}],
    "expected": {"TreeNode": [4, 7, 2, 9, 6, 3, 1]}
  },
  {
    "description": "Single node tree",
    "input": [{"TreeNode": [1]}],
    "expected": {"TreeNode": [1]}
  }
]
```

**JSON format features:**
- **Structured data**: Each test case is a JSON object with `input` and `expected` fields
- **Multiple arguments**: Input can be a list of arguments: `"input": [arg1, arg2, arg3]`
- **Single argument**: For single arguments, wrap in a list: `"input": [arg1]`
- **Complex data types**: Supports nested structures, objects, and custom classes
- **Optional descriptions**: Add `"description"` field for test case documentation

---

## How It Works

- Loads your solution file dynamically
- Loads and parses the test cases from the external file
- Converts inputs into Python data structures
- Calls your solution method with the inputs
- Compares the output to the expected result
- Reports pass/fail status for each test case
- Any `print()` output from your solution will be shown in  test result, helping with step-by-step debugging


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

## Built-in and Custom Class Support

Pyleet supports both **built-in** and **custom** data structures commonly used in LeetCode problems, such as `ListNode`, `TreeNode`, or your own custom classes like `Point` or `Matrix`.

### Built-in Support for `ListNode` and `TreeNode`

Pyleet includes built-in `ListNode` and `TreeNode` classes that match LeetCode specifications.

#### Key Benefits

* ✅ **Zero boilerplate** – No need to copy-paste class definitions into your solution
* ✅ **Flexible** – Use built-in classes or override with your own if needed
* ✅ **Standard compliant** – Compatible with LeetCode's input/output formats
* ✅ **Automatic serialization** – Input/output conversion is handled seamlessly

---

### Custom Class Support

Pyleet allows full support for custom data types and complex class structures. You can:

* Define and register your own classes
* Create custom serializers and deserializers
* Use automatic or explicit method selection with type-based heuristics
* Build reusable and maintainable test cases using JSON-based formats

**For full details**, including setup examples and best practices, see the [Custom Classes Guide](docs/custom_classes_guide.md).


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
- Run solution file as script (eg: adding `pyleet.run()` in the end).
- Support for more data structures.
- Run tests in parallel.
- Record running time.
- Performance optimizations for large test suites

---
## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests.

1. Fork the repo
2. Create a feature branch
3. Commit your changes with clear messages
4. Push and open a PR.
---

## License

[MIT License](LICENSE)
