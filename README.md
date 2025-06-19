# Pyleet

![Python](https://img.shields.io/pypi/pyversions/pyleet)
![License](https://img.shields.io/github/license/ergs0204/Pyleet)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ergs0204/Pyleet)

Pyleet is a Python tool that allows you to **run and test your LeetCode Python solutions locally** with minimal modification. It bridges the gap between LeetCode's online environment and local development, making it easier to debug and verify your solutions offline.

---
## Features

- **Local Testing**: Run LeetCode Python solutions locally without modifying code.
- **Test Case Flexibility**: Support for `.txt` and `.json` test case files.
- **Intuitive CLI**: Run tests easily with commands like `pyleet solution.py --testcases cases.txt`.
- **Smart Method Detection**: Automatically selects methods based on input types or allows explicit selection with `--method`.
- **Built-in Data Structures**: Includes `ListNode` and `TreeNode` with automatic serialization, eliminating boilerplate code.
- **Customizable Execution**: Choose automatic fallback, explicit imports, or custom class overrides for flexible usage.
- **Broad Data Support**: Seamlessly handles lists, integers, strings, and custom classes with bidirectional serialization.
- **Clear Error Reporting**: Provides detailed feedback and comparison for accurate test results.
- **Debugging Support**: Displays `print()` output from solutions in test results for easier debugging.
- **Programmatic Interface**: Run tests directly from Python code with `pyleet.run()` for better integration.
- **Auto Test Case Retrieval**: Automatically fetch test cases from LeetCode. ([Learn more](https://github.com/ergs0204/pyleet/blob/main/docs/test_case_retrieval.md))

---
## Installation

### Using pip

```
pip install pyleet
```

### From source

```bash
git clone https://github.com/ergs0204/pyleet.git
cd pyleet
pip install -e .
```

---
## Quick Start

Run your LeetCode solution against a test case file using the CLI:

```bash
pyleet your_solution_file.py --testcases test_cases.txt
```

For example, if your solution is in `solution.py` and test cases in `cases.txt`:
```bash
pyleet solution.py -t cases.txt
```

Pyleet also supports programmatic usage. See the Detailed Documentation for more.

---
## Detailed Documentation

For more in-depth information on specific features and usage, please refer to the following documents:

- **[Programmatic Usage](https://github.com/ergs0204/pyleet/blob/main/docs/programmatic_usage.md)**: Learn how to integrate Pyleet into your Python scripts and debugging workflows.
- **[CLI Usage](https://github.com/ergs0204/pyleet/blob/main/docs/cli_usage.md)**: Explore advanced command-line options and test case formats.
- **[Auto Test Case Retrieval](https://github.com/ergs0204/pyleet/blob/main/docs/test_case_retrieval.md)**: Discover how to fetch test cases directly from LeetCode.
- **[Method Selection](https://github.com/ergs0204/pyleet/blob/main/docs/method_selection.md)**: Understand how Pyleet handles solutions with multiple methods.
- **[Custom Class Support](https://github.com/ergs0204/pyleet/blob/main/docs/custom_classes_guide.md)**: Guide for working with custom data structures.
- **[Dictionary Handling Guide](https://github.com/ergs0204/pyleet/blob/main/docs/dictionary_handling_guide.md)**: Learn how Pyleet handles dictionaries as inputs and outputs.

---

## CLI vs Programmatic Comparison

| Feature           | CLI Approach                     | Programmatic Approach           |
| ----------------- | -------------------------------- | ------------------------------- |
| Test Case Storage | External files (`.txt`, `.json`) | Python code                     |
| IDE Integration   | Limited                          | Full autocomplete/debugging     |
| Debugging         | Terminal only                    | IDE debugger integration        |
| Method Selection  | `--method` flag                  | `method` parameter              |
| Output            | Printed in terminal              | Captured in variables           |
| Automation        | CI / Shell scripts               | Python / Notebooks              |
| Best For          | Quick tests, CI/CD               | Development, notebooks, IDE use |

### When to Use Each Approach

**Use Programmatic Interface when:**
- Developing and debugging in an IDE
- Working in Jupyter notebooks
- Need tight integration with Python workflows
- Want to process test results programmatically
- Prefer keeping tests close to solution code

**Use CLI when:**
- Quick testing of solutions
- CI/CD pipelines
- Sharing test cases with others
- Working with large test suites in files

---

## How It Works

- Loads your solution file dynamically
- Loads and parses the test cases from the external file
- Converts inputs into Python data structures
- Calls your solution method with the inputs
- Compares the output to the expected result
- Reports pass/fail status for each test case
- Any `print()` output from your solution will be shown in test result, helping with step-by-step debugging

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

This section provides a brief overview. For full details, see the [Custom Classes Guide](https://github.com/ergs0204/pyleet/blob/main/docs/custom_classes_guide.md).

Pyleet allows full support for custom data types and complex class structures. You can:

* Define and register your own classes
* Create custom serializers and deserializers
* Use automatic or explicit method selection with type-based heuristics
* Build reusable and maintainable test cases using JSON-based formats

---

## Recent Improvements

- ✅ **Testcases fetching** - Fetch testcases with `pyleet.get_testcase()`.
- ✅ **Programmatic Interface** - Run tests directly from Python code with `pyleet.run()` for better IDE integration
- ✅ **Built-in ListNode and TreeNode classes** - Zero configuration needed for common LeetCode problems
- ✅ **Three usage patterns** - Automatic fallback, explicit import, or custom override
- ✅ **Enhanced custom class support** - Any class structure now supported
- ✅ **Fixed serialization errors** - No more `val` attribute requirements
- ✅ **Flexible method selection** - Both automatic selection and explicit method specification via `--method` parameter
- ✅ **Bidirectional serialization** - Both input and output serialization support
- ✅ **Robust comparison** - Multiple fallback strategies for output comparison
- ✅ **Improved error handling** - Clear feedback when specified methods are not found

## Roadmap

- Integration with testing frameworks (pytest, unittest)
- Support for more data structures.
- Run tests in parallel.
- Record running time.
- Performance optimizations for large test suites
- Better documentation and examples.

---
## 🤝 Contributing

For detailed information on contributing, see [Contributing](https://github.com/ergs0204/pyleet/blob/main/docs/contributing.md).

---

## License

[MIT License](LICENSE)
