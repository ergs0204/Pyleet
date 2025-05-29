"""
CLI entry point for Pyleet.
"""

import argparse
import sys
import importlib.util
from pyleet.testcase_loader import load_test_cases
from pyleet.runner import run_solution
from pyleet.datastructures import set_user_module


def main():
    parser = argparse.ArgumentParser(
        description="Run LeetCode Python solutions locally with test cases.")
    parser.add_argument("solution", help="Path to the solution .py file")
    parser.add_argument("--testcases", "-t", required=True,
                        help="Path to the test case file (.json or .txt)")
    parser.add_argument("--method", "-m",
                        help="Specify which method to use for testing (optional)")
    args = parser.parse_args()

    # Load the user's solution module first so deserializers can access user-defined classes
    try:
        module_name = "user_solution"
        spec = importlib.util.spec_from_file_location(
            module_name, args.solution)
        user_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = user_module
        spec.loader.exec_module(user_module)

        # Set the user module for deserializers to access user-defined classes
        set_user_module(user_module)
    except Exception as e:
        print(f"Error loading solution file: {e}")
        sys.exit(1)

    try:
        test_cases = load_test_cases(args.testcases)
    except Exception as e:
        print(f"Error loading test cases: {e}")
        sys.exit(1)

    try:
        results = run_solution(args.solution, test_cases,
                               target_method=args.method)
    except Exception as e:
        print(f"Error running solution: {e}")
        sys.exit(1)

    passed_count = 0
    for idx, result in enumerate(results, 1):
        status = "PASS" if result["passed"] else "FAIL"
        if result["passed"]:
            passed_count += 1
        print(f"Test Case {idx}: {status}")
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

    total = len(results)
    print(f"Passed {passed_count}/{total} test cases.")


if __name__ == "__main__":
    main()
