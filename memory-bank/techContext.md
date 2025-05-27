# Tech Context: Pyleet

## Programming Language
- **Python 3.x**

## Packaging & Distribution
- Installable via `setup.py` or `pip`.
- Distributed as a Python package (wheel or source).
- Provides a CLI entry point `pyleet`.

## CLI Tooling
- Implemented using Python's `argparse` or `click` for argument parsing.
- Executed via `python -m pyleet` or installed `pyleet` command.

## Dynamic Code Execution
- Uses Python's `importlib` or `exec` to dynamically load user solution files.
- Reflection to invoke the `Solution` class and its method.

## Test Case Loading & Deserialization (`testcase_loader.py`)
- Loads test cases from external files (e.g., `.txt`, `.json`).
- **Deserialization during Loading:** The loader is responsible for converting raw data from the test case file into the final Python objects (both built-in types and custom classes).
- **Default Behavior (JSON):** Standard JSON values (numbers, strings, lists, plain dictionaries) are parsed directly into corresponding Python built-in types (`int`, `float`, `str`, `list`, `dict`) by the loader. No special format is needed.
- **Custom Object Deserialization (JSON):** The loader looks for custom class format in both inputs and expected outputs:
    - **Format:** `{"ClassName": <raw_data>}` - A concise format where the class name is the key
    - It uses a deserializer registry (`pyleet.datastructures`) to find a function registered for `ClassName`.
    - It recursively deserializes nested structures within the data before calling the final deserializer function.
    - The registered function converts the (potentially deserialized) data into an instance of the class.
    - Users **must define the class** (e.g., `ListNode`) within their solution file.
    - Pyleet provides default deserializers for `ListNode` and `TreeNode`.
    - Users can register deserializers for their own custom classes using `from pyleet import register_deserializer` within their solution file.
- **Text Files (`.txt`):** Parsing logic currently uses `ast.literal_eval` for lines formatted as `(input_args, expected_output)`. Does not support custom type deserialization in this mode.

## Data Structure Support
- **Built-in Types:** `int`, `float`, `str`, `list`, `dict` are handled directly from standard JSON.
- **Common LeetCode Types (`ListNode`, `TreeNode`):** Supported via the `{"ClassName": data}` format and default deserializers. Requires the user to define the class in their solution file.
- **User Custom Classes:** Supported via the `{"ClassName": data}` format, user-provided class definitions, and registration of custom deserializer functions using `pyleet.register_deserializer`.

## Dependencies
- **Standard Library Only:**
  - `argparse` (or potentially `click` later)
  - `importlib`
  - `ast`
  - `re`
  - `sys`
  - `os`
  - `json` (for test case loading)
- **Optional Future Dependencies:**
  - `pytest` or `unittest` for integration.
  - Third-party parsing libraries.

## Development Environment
- Compatible with Windows, macOS, Linux.
- Python 3.7+ recommended.
- Version control with Git.

## Constraints
- Minimal dependencies for easy installation.
- Avoid modifying user solution files.
- Keep CLI interface simple.
