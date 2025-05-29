"""
Module to dynamically load and run the user's LeetCode solution
with provided test cases.
"""

import importlib.util
import sys
import io
import contextlib
from pyleet.datastructures import set_user_module, serialize_object


def run_solution(solution_path, test_cases, target_method=None):
    """
    Run the solution with the given test cases.

    Args:
        solution_path (str): Path to the user's solution .py file.
        test_cases (list): List of (input_args, expected_output) tuples.
        target_method (str, optional): Specific method name to use for testing.

    Returns:
        list of dict: Each dict contains input, expected, actual, and pass/fail status.
    """
    # Get the user's solution module (already loaded by CLI)
    module_name = "user_solution"
    if module_name in sys.modules:
        user_module = sys.modules[module_name]
    else:
        # Fallback: load the module if not already loaded
        spec = importlib.util.spec_from_file_location(
            module_name, solution_path)
        user_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = user_module
        spec.loader.exec_module(user_module)

        # Set the user module for deserializers to access user-defined classes
        set_user_module(user_module)

    # Find the solution function or class
    solution_instance = None
    solution_methods = {}

    if hasattr(user_module, "Solution"):
        solution_instance = user_module.Solution()
        # Collect all non-dunder methods
        for attr in dir(solution_instance):
            if not attr.startswith("__") and callable(getattr(solution_instance, attr)):
                solution_methods[attr] = getattr(solution_instance, attr)
    else:
        # Use the first non-dunder function in the module
        for attr in dir(user_module):
            obj = getattr(user_module, attr)
            if callable(obj) and not attr.startswith("__"):
                solution_methods[attr] = obj

    if not solution_methods:
        raise ValueError(
            "No solution function or class found in the provided file.")

    results = []
    # The test_cases list now contains already deserialized input_args and expected values
    for deserialized_input_args, deserialized_expected in test_cases:
        # Capture print output for this specific test case
        print_capture = io.StringIO()

        try:
            # Determine which method to call based on target method or input types
            solution_func = _select_solution_method(
                solution_methods, deserialized_input_args, target_method)

            # Capture print statements during solution execution
            with contextlib.redirect_stdout(print_capture):
                # The runner now receives fully formed objects
                actual = solution_func(*deserialized_input_args)

            passed = _compare_outputs(actual, deserialized_expected)
        except Exception as e:
            actual = f"Error: {e}"
            passed = False

        # Get captured print output
        print_output = print_capture.getvalue()

        results.append({
            "input": deserialized_input_args,  # Store the deserialized input for reporting
            # Store the deserialized expected for reporting
            "expected": deserialized_expected,
            "actual": actual,
            "passed": passed,
            "print_output": print_output  # Store captured print statements
        })

    return results


def _select_solution_method(solution_methods, input_args, target_method=None):
    """
    Select the appropriate solution method based on target method or input types.

    Args:
        solution_methods (dict): Dictionary of method_name -> method_function
        input_args (tuple): Input arguments for the method
        target_method (str, optional): Specific method name to use

    Returns:
        callable: The selected method function

    Raises:
        ValueError: If target_method is specified but not found
    """
    if not solution_methods:
        raise ValueError("No solution methods found")

    # If target method is specified, try to find it
    if target_method:
        if target_method in solution_methods:
            return solution_methods[target_method]
        else:
            available_methods = list(solution_methods.keys())
            raise ValueError(
                f"Method '{target_method}' not found. Available methods: {available_methods}")

    # Original automatic selection logic
    if len(solution_methods) == 1:
        # Only one method available, use it
        return next(iter(solution_methods.values()))

    # Try to match method name with input type
    if len(input_args) == 1:
        arg = input_args[0]
        arg_type = type(arg).__name__

        # Look for method names that match the input type
        for method_name, method_func in solution_methods.items():
            if arg_type.lower() in method_name.lower():
                return method_func

    # Fallback: use the first method
    return next(iter(solution_methods.values()))


def _compare_outputs(actual, expected):
    """
    Compare actual output with expected output.
    Uses serialization to handle custom objects properly.
    """
    try:
        # First try direct comparison (for simple cases)
        if actual == expected:
            return True
    except:
        pass

    # If direct comparison fails, try serializing both and comparing
    try:
        serialized_actual = serialize_object(actual)
        serialized_expected = serialize_object(expected)
        return serialized_actual == serialized_expected
    except Exception:
        # Fallback to string comparison
        return str(actual) == str(expected)
