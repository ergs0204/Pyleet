# Product Context: Pyleet

## Why This Project Exists
LeetCode provides an online environment optimized for coding interviews, but its code structure is not designed for local testing. Users often struggle to run their LeetCode solutions locally because:
- The function signature is embedded in a class without a main entry point.
- Test cases are not included in the code.
- Data structures like linked lists or trees require boilerplate code to instantiate.

Pyleet addresses these pain points by enabling users to:
- Save test cases in a separate file (e.g., `.txt` or `.json`).
- Run these solutions locally without modifying their original code.
- Avoid rewriting or restructuring their code just to test locally.

## Problems It Solves
- Eliminates the need to manually wrap LeetCode code with boilerplate for local testing.
- Simplifies the process of adding and running test cases via an external file.
- Reduces friction in debugging and verifying solutions offline.
- Saves time during interview preparation or practice.

## How It Should Work
- Users write their LeetCode solution as usual.
- They save test cases in a separate file in a simple, structured format (e.g., plain text or JSON).
- Running `pyleet solution.py --testcases cases.txt`:
  - Extracts the solution class and method.
  - Loads and parses the external test cases.
  - Converts input strings into appropriate data structures.
  - Calls the solution method with parsed inputs.
  - Compares outputs to expected results and reports success/failure.

## User Experience Goals
- **Minimal Setup:** Users should not need to modify their LeetCode code.
- **Simple CLI:** A single command to run tests with an external test case file.
- **Clear Feedback:** Easy-to-understand output showing passed/failed cases.
- **Extensible:** Ability to support more data structures, languages, or automated test case fetching in the future.
