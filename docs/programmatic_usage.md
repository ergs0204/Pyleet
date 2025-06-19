# Programmatic Usage

Programmatic interface that allows you to run tests directly from your Python code. This approach offers better IDE integration, more convenient debugging workflows, and eliminates the need for external test case files.

### Basic Programmatic Usage

```python
import pyleet

class Solution:
    def twoSum(self, nums, target):
        """Find two numbers that add up to target."""
        num_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], i]
            num_map[num] = i
        return []

# Define test cases directly in your code
testcases = [
    (([2, 7, 11, 15], 9), [0, 1]),
    (([3, 2, 4], 6), [1, 2]),
    (([3, 3], 6), [0, 1])
]

# Run the tests
results = pyleet.run(testcases)
pyleet.print_results(results)
```

### Test Case Formats

The programmatic interface supports multiple test case formats for flexibility:

#### 1. Tuple Format (Recommended for simple cases)
```python
testcases = [
    (([2, 7, 11, 15], 9), [0, 1]),  # ((input_args), expected_output)
    (([3, 2, 4], 6), [1, 2])
]
```

#### 2. Dictionary Format (Recommended for complex cases)
```python
testcases = [
    {
        "input": [[2, 7, 11, 15], 9],
        "expected": [0, 1]
    },
    {
        "input": [[3, 2, 4], 6],
        "expected": [1, 2]
    }
]
```

### Method Selection

Just like the CLI, you can specify which method to test:

```python
# Automatic method selection (default)
results = pyleet.run(testcases)

# Explicit method selection
results = pyleet.run(testcases, method="twoSum")
```


### Using `pyleet.print_results()`

The `print_results()` function provides formatted output with customizable verbosity:

```python
# Detailed output (default, including inputs, outputs, expected, and print statements)
pyleet.print_results(results)

# Concise output (only pass/fail status)
pyleet.print_results(results, verbose=False)
```

### Working with Custom Classes

The programmatic interface fully supports custom classes and complex data structures:

```python
import pyleet

# Register custom deserializers if needed
# (See [Custom Classes Guide](custom_classes_guide.md) for details)

testcases = [
    {
        "input": [{"TreeNode": [4, 2, 7, 1, 3, 6, 9]}],
        "expected": {"TreeNode": [4, 7, 2, 9, 6, 3, 1]}
    }
]

results = pyleet.run(testcases, method="invertTree")
pyleet.print_results(results)
```

### Auto-Retrieve Test Cases from LeetCode

Pyleet can automatically fetch test cases directly from LeetCode:

```python
import pyleet

class Solution:
    def twoSum(self, nums, target):
        num_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], i]
            num_map[num] = i
        return []

# Automatically get test cases from LeetCode
testcases = pyleet.get_testcase(problem_id=1)  # Two Sum
results = pyleet.run(testcases)
pyleet.print_results(results)

# Or use title slug
testcases = pyleet.get_testcase(title_slug="two-sum")
results = pyleet.run(testcases)
```

### Complete Example

See the full example in [`examples/programmatic_usage/`](https://github.com/ergs0204/pyleet/tree/main/examples/programmatic_usage/) and [`examples/testcase_retrieval/`](https://github.com/ergs0204/pyleet/tree/main/examples/testcase_retrieval/)
