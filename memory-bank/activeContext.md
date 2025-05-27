# Active Context: Pyleet

## Current Focus
- Refine the core functionality of Pyleet.
- Ensure robust handling of test cases and solution execution.
- Improve documentation and user guidance.

## Recent Changes & Decisions
- **Refactored Deserialization Logic:**
    - Moved the responsibility of deserializing test case inputs (including handling custom class formats) from the runner (`runner.py`) to the loader (`testcase_loader.py`).
    - The loader now performs recursive deserialization on both inputs and expected outputs found in JSON test case files.
    - The runner now receives fully formed Python objects from the loader.
- **Enhanced Custom Class Support (as part of refactor):**
    - The loader utilizes the deserializer registry (`pyleet.datastructures`) and the exposed `pyleet.register_deserializer` function.
    - Users use the concise format `{"ClassName": data}` for custom types in JSON.
    - Users still need to define classes (`ListNode`, etc.) in their solution file.
- **Clarified Documentation:** Updated Memory Bank (`techContext.md`, `systemPatterns.md`) to reflect the loader's responsibility for deserialization and the default handling of built-in types.
- Maintained reliance on external test case files (`.txt`, `.json`).
- Kept standard library dependency constraint.

## Next Steps
1.  Update `memory-bank/progress.md` to reflect the completed refactoring.
2.  Update `README.md` with usage instructions, ensuring it clearly explains the concise JSON format (`{"ClassName": data}`) and the need for user-defined classes and registration.
3.  Consider improving the output comparison logic (`_compare_outputs` in `runner.py`) now that it receives potentially complex, deserialized objects for both `actual` and `expected`.
4.  Continue implementing core features if not already done (CLI, reporting).
5.  Add example usage for custom class registration.

## Considerations
- **Output Comparison:** The current `==` comparison might be insufficient for custom objects without `__eq__`. This needs further review or enhancement.
- **Error Handling:** Improve error messages if a custom class format is specified but no deserializer is registered or if the user forgets to define the class.
- Keep CLI usage simple despite added features.
