# Auto Test Case Retrieval

Pyleet can automatically retrieve test cases from LeetCode, eliminating the need to manually copy test cases:

### `pyleet.get_testcase()`

```python
# Get test cases by problem ID
testcases = pyleet.get_testcase(problem_id=1)

# Get test cases by title slug
testcases = pyleet.get_testcase(title_slug="two-sum")

# Use with pyleet.run()
results = pyleet.run(testcases)
```

**Parameters:**
- `problem_id` (int, optional): LeetCode problem ID (e.g., 1 for Two Sum)
- `title_slug` (str, optional): LeetCode problem title slug (e.g., "two-sum")
- `include_hidden` (bool): Whether to attempt to get hidden test cases (default: False)

**Returns:** List of test cases in Pyleet format `[(input_args, expected_output), ...]`

**Features:**
- ✅ Automatic test case retrieval from LeetCode
- ✅ Support for both problem ID and title slug
- ✅ Seamless integration with `pyleet.run()`
- ✅ Proper error handling for invalid problems
- ✅ Works with all LeetCode problem types

**Limitations:**
- Requires internet connection
- Only retrieves public example test cases
- Premium problems require LeetCode Premium subscription

### Examples

See [`examples/testcase_retrieval/`](https://github.com/ergs0204/pyleet/tree/main/examples/testcase_retrieval/) for comprehensive examples including error handling and integration patterns.
