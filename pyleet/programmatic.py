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

    # Load the user's solution module
    try:
        module_name = "user_solution"

        # Remove existing module if it exists to ensure fresh load
        if module_name in sys.modules:
            del sys.modules[module_name]

        spec = importlib.util.spec_from_file_location(
            module_name, solution_path)
        user_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = user_module
        spec.loader.exec_module(user_module)

        # Set the user module for deserializers to access user-defined classes
        set_user_module(user_module)
    except Exception as e:
        raise ValueError(f"Error loading solution file '{solution_path}': {e}")

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


def print_results(results, verbose=True):
    """
    Print test results in a formatted way.

    Args:
        results (list): List of result dictionaries from run().
        verbose (bool): Whether to show detailed output including inputs, outputs, expected and print.
    """
    if not results:
        print("No test results to display.")
        return

    passed_count = sum(1 for result in results if result["passed"])
    total_count = len(results)

    for idx, result in enumerate(results, 1):
        status = "PASS" if result["passed"] else "FAIL"
        print(f"Test Case {idx}: {status}")

        if verbose:
            print(f"  Input: {result['input']}")
            print(f"  Expected: {result['expected']}")
            print(f"  Actual: {result['actual']}")

            # Display captured print output if any
            if result.get("print_output") and result["print_output"].strip():
                print(f"  Print Output:")
                # Indent each line of print output for clear association
                for line in result["print_output"].rstrip('\n').split('\n'):
                    print(f"    {line}")

        print()

    # Summary
    print(f"Passed {passed_count}/{total_count} test cases.")
