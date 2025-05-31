# Programmatic Usage Examples

This directory contains examples demonstrating how to use Pyleet's programmatic interface to run tests directly from Python code.

## Files

### `simple_example.py`
A minimal example showing the basic usage of `pyleet.run()`:
- Defines a simple `twoSum` solution
- Shows tuple format test cases
- Demonstrates basic test execution and result printing

**Run it:**
```bash
python simple_example.py
```

### `programmatic_example.py`
A comprehensive example demonstrating advanced features:
- Multiple solution methods (`twoSum` and `threeSum`)
- Different test case formats (tuple, dict, list)
- Method selection with the `method` parameter
- Print statement capture and display
- Error handling examples
- Verbose and concise output options

**Run it:**
```bash
python programmatic_example.py
```

## Key Features Demonstrated

1. **Multiple Test Case Formats**:
   - Tuple format: `(([2, 7, 11, 15], 9), [0, 1])`
   - Dict format: `{"input": [[2, 7, 11, 15], 9], "expected": [0, 1]}`
   - List format: `[[[2, 7, 11, 15], 9], [0, 1]]`

2. **Method Selection**:
   - Automatic selection: `pyleet.run(testcases)`
   - Explicit selection: `pyleet.run(testcases, method="twoSum")`

3. **Result Processing**:
   - Detailed output: `pyleet.print_results(results)`
   - Concise output: `pyleet.print_results(results, verbose=False)`

4. **Print Statement Capture**:
   - All `print()` statements from your solution are captured
   - Displayed in test results for debugging

## Benefits of Programmatic Interface

- **No External Files**: Test cases defined directly in code
- **Flexible Workflows**: Easy integration with notebooks and scripts
- **Better Debugging**: Print statements captured per test case
- **Programmatic Results**: Access to detailed result data for further processing

## Getting Started

1. Import pyleet: `import pyleet`
2. Define your solution class with methods
3. Create test cases in any supported format
4. Run tests: `results = pyleet.run(testcases)`
5. Display results: `pyleet.print_results(results)`

For more details, see the main [README.md](../../README.md) documentation.
