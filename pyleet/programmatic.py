"""
Programmatic interface for Pyleet.
Allows users to run test cases directly from Python code without using the CLI.
"""

import sys
import inspect
import importlib.util
from .testcase_loader import process_test_cases
from .runner import run_solution
from .datastructures import set_user_module
from .colors import green, red

# Global set to track files currently being loaded to prevent infinite recursion
_loading_files = set()


def run(testcases, method=None, solution_path=None):
    """
    Run test cases programmatically using the specified method.

    Args:
        testcases (list): List of test cases in various supported formats:
            - Tuples: [(input_args, expected), ...]
            - Dicts: [{"input": input_args, "expected": expected}, ...]
            - Lists: [[input_args, expected], ...]
        method (str, optional): Specific method name to use for testing.
            If not provided, uses automatic method selection.
        solution_path (str, optional): Path to solution file. If not provided,
            attempts to determine the calling file automatically.

    Returns:
        list of dict: Each dict contains input, expected, actual, passed status,
            and print_output for each test case.

    Example:
        # Basic usage with tuples
        testcases = [
            (([2, 7, 11, 15], 9), [0, 1]),
            (([3, 2, 4], 6), [1, 2])
        ]
        results = pyleet.run(testcases)

        # With method selection
        results = pyleet.run(testcases, method="twoSum")

        # With dict format
        testcases = [
            {"input": [[2, 7, 11, 15], 9], "expected": [0, 1]},
            {"input": [[3, 2, 4], 6], "expected": [1, 2]}
        ]
        results = pyleet.run(testcases)
    """
    # Determine the solution path if not provided
    if solution_path is None:
        solution_path = _get_caller_file_path()
        if solution_path is None:
            raise ValueError(
                "Could not determine solution file path. Please provide solution_path parameter.")

    # Check for recursive loading to prevent infinite loops
    if solution_path in _loading_files:
        # Instead of raising an error, try to use the already loaded module
        module_name = "user_solution"
        if module_name in sys.modules:
            user_module = sys.modules[module_name]
            set_user_module(user_module)
        else:
            raise ValueError(
                f"Recursive loading detected for '{solution_path}' but no module found. "
                f"This usually happens when pyleet.run() is called at module level without "
                f"'if __name__ == \"__main__\":' guard. Either add the guard or provide "
                f"solution_path parameter explicitly to avoid auto-detection.")
    else:
        # Load the user's solution module
        try:
            # Mark this file as currently being loaded
            _loading_files.add(solution_path)

            module_name = "user_solution"

            # Remove existing module if it exists to ensure fresh load
            if module_name in sys.modules:
                del sys.modules[module_name]

            # Use a safer module loading approach that doesn't execute all module-level code
            user_module = _load_module_safely(solution_path, module_name)

            # Set the user module for deserializers to access user-defined classes
            set_user_module(user_module)
        except Exception as e:
            raise ValueError(
                f"Error loading solution file '{solution_path}': {e}")
        finally:
            # Always remove from loading set, even if an error occurred
            _loading_files.discard(solution_path)

    # Process the test cases
    try:
        processed_testcases = process_test_cases(testcases)
    except Exception as e:
        raise ValueError(f"Error processing test cases: {e}")

    # Run the solution
    try:
        results = run_solution(
            solution_path, processed_testcases, target_method=method)
    except Exception as e:
        raise ValueError(f"Error running solution: {e}")

    return results


def _load_module_safely(solution_path, module_name):
    """
    Load a module in a way that minimizes the risk of infinite recursion
    when the module contains pyleet.run() calls at module level.

    This function uses AST parsing to extract only the class and function definitions
    without executing module-level code that could cause recursion.
    """
    import ast
    import types

    # Read the source code
    with open(solution_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    # Parse the AST
    try:
        tree = ast.parse(source_code, filename=solution_path)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in solution file: {e}")

    # Create a new module
    user_module = types.ModuleType(module_name)
    user_module.__file__ = solution_path
    sys.modules[module_name] = user_module

    # Execute only class and function definitions, skip module-level calls
    safe_nodes = []
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.Import, ast.ImportFrom, ast.Assign)):
            # Include class definitions, function definitions, imports, and assignments
            safe_nodes.append(node)
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            # Skip expression statements that are function calls (like pyleet.run())
            continue
        else:
            # Include other safe statements like variable assignments
            safe_nodes.append(node)

    # Create a new AST with only safe nodes
    safe_tree = ast.Module(body=safe_nodes, type_ignores=[])

    # Compile and execute the safe AST
    try:
        code = compile(safe_tree, solution_path, 'exec')
        exec(code, user_module.__dict__)
    except Exception as e:
        raise ValueError(f"Error executing solution file: {e}")

    return user_module


def _get_caller_file_path():
    """
    Attempt to determine the file path of the caller.

    Returns:
        str or None: Path to the calling file, or None if unable to determine.
    """
    try:
        # Get the current frame and walk up the stack
        frame = inspect.currentframe()

        # Walk up the call stack to find the first frame outside this module
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            # Get the filename from the frame
            filename = frame.f_code.co_filename

            # Skip frames from this module and built-in modules
            if (filename != __file__ and
                not filename.startswith('<') and
                    filename.endswith('.py')):
                return filename

        return None
    except Exception:
        return None


def print_results(results, verbose=True, colored=True):
    """
    Print test results in a formatted way.

    Args:
        results (list): List of result dictionaries from run().
        verbose (bool): Whether to show detailed output including inputs, outputs, expected and print.
        colored (bool): Whether to use colored output for pass/fail status.
    """
    if not results:
        print("No test results to display.")
        return

    passed_count = sum(1 for result in results if result["passed"])
    total_count = len(results)

    for idx, result in enumerate(results, 1):
        if result["passed"]:
            status = green("PASS", bold=True) if colored else "PASS"
        else:
            status = red("FAIL", bold=True) if colored else "FAIL"

        print(f"Test Case {idx}: {status}")

        if verbose:
            print(f"  Input: {result['input']}")
            print(f"  Expected: {result['expected']}")

            # Color the actual output based on pass/fail status
            if result["passed"]:
                actual_text = f"  Actual: {result['actual']}"
            else:
                actual_text = f"  Actual: {red(str(result['actual']))}" if colored else f"  Actual: {result['actual']}"
            print(actual_text)

            # Display captured print output if any
            if result.get("print_output") and result["print_output"].strip():
                print(f"  Print Output:")
                # Indent each line of print output for clear association
                for line in result["print_output"].rstrip('\n').split('\n'):
                    print(f"    {line}")

        print()

    # Summary with color
    if colored:
        if passed_count == total_count:
            summary_text = green(
                f"Passed {str(passed_count)}/{total_count} test cases.")
        else:
            summary_text = red(
                f"Passed {str(passed_count)}/{total_count} test cases.")
    else:
        summary_text = f"Passed {passed_count}/{total_count} test cases."
    print(summary_text)
