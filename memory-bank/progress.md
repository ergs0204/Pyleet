# Progress: Pyleet

## What Works
- Project goals, architecture, and technical context defined.
- Memory bank initialized and updated.
- Standard Python `.gitignore` file added.
- **Test Case Loading & Deserialization (`testcase_loader.py`):**
    - Loader now handles parsing and deserialization of test cases from files.
    - Correctly parses standard JSON types into Python built-ins by default.
    - Uses custom class format (`{"ClassName": data}`) to trigger custom class deserialization for inputs and expected outputs via a registry (`pyleet.datastructures`).
    - Recursively handles nested structures during deserialization.
    - Exposes `pyleet.register_deserializer` for users to add support for their own custom classes.
    - Requires users to define classes (like `ListNode`) in their solution file.
- **Runner (`runner.py`):**
    - Simplified to receive fully deserialized objects from the loader.
- **Documentation:** Memory Bank (`techContext.md`, `systemPatterns.md`, `activeContext.md`) updated to reflect the refactored architecture.

## What's Left to Build / Refine
- Implement core CLI functionality (`pyleet` entry point, argument parsing in `cli.py`).
- Implement result reporting (likely in `cli.py` or a dedicated reporter module).
- Complete `setup.py` for packaging.
- **Improve Output Comparison:** Enhance `_compare_outputs` in `runner.py` to handle custom objects better now that it receives deserialized expected outputs.
- **Documentation:** Update `README.md` with clear usage instructions for the concise JSON format (`{"ClassName": data}`), class definition, and registration.
- Add examples demonstrating custom class usage.
- Improve error handling in `testcase_loader.py` (e.g., for missing deserializers or class definitions during loading).
- Test thoroughly with various LeetCode problems and edge cases.

## Current Status
- Deserialization logic successfully refactored into `testcase_loader.py`.
- Runner (`runner.py`) simplified.
- Internal documentation (Memory Bank) updated.
- Ready to proceed with CLI implementation, README updates, and output comparison refinement.

## Known Issues / Challenges
- **Output Comparison:** The current `==` comparison in `runner.py` is insufficient for many custom objects, especially now that `expected` is also deserialized.
- Ensuring the concise format `{"ClassName": data}` is user-friendly and well-documented in the `README.md`.
- Providing clear error messages during the loading/deserialization phase in `testcase_loader.py`.

## Evolution of Decisions
- Shifted from potential "helper classes" provided by Pyleet to a user-driven approach requiring users to define classes and register deserializers.
- **Refactored:** Moved deserialization responsibility from the runner to the loader for better separation of concerns.
- Maintained standard library dependency.
