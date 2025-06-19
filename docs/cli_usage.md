# CLI Usage

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
