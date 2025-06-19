"""
Basic usage examples for pyleet.get_testcase() function.

This example demonstrates different ways to retrieve test cases from LeetCode
using the get_testcase() function.
"""

import pyleet


def example_by_problem_id():
    """Example: Get test cases using problem ID."""
    print("=== Getting test cases by Problem ID ===")

    try:
        # Get test cases for Two Sum (Problem ID: 1)
        testcases = pyleet.get_testcase(problem_id=1)

        print(f"Retrieved {len(testcases)} test cases for Two Sum:")
        for i, (inputs, expected) in enumerate(testcases, 1):
            print(f"  Test Case {i}:")
            print(f"    Input: {inputs}")
            print(f"    Expected: {expected}")

        return testcases

    except Exception as e:
        print(f"Error retrieving test cases: {e}")
        return []


def example_by_title_slug():
    """Example: Get test cases using title slug."""
    print("\n=== Getting test cases by Title Slug ===")

    try:
        # Get test cases for Two Sum using title slug
        testcases = pyleet.get_testcase(title_slug="two-sum")

        print(f"Retrieved {len(testcases)} test cases for 'two-sum':")
        for i, (inputs, expected) in enumerate(testcases, 1):
            print(f"  Test Case {i}:")
            print(f"    Input: {inputs}")
            print(f"    Expected: {expected}")

        return testcases

    except Exception as e:
        print(f"Error retrieving test cases: {e}")
        return []


if __name__ == "__main__":
    print("Pyleet Test Case Retrieval - Basic Usage Examples")
    print("=" * 55)

    # Run examples
    example_by_problem_id()
    example_by_title_slug()

    print("\n" + "=" * 55)
    print("Examples completed!")
