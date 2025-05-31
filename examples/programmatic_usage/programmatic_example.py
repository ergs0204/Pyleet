"""
Example demonstrating programmatic usage of Pyleet.

This example shows how to run test cases directly from Python code
without using the command line interface.
"""

import pyleet


class Solution:
    def twoSum(self, nums, target):
        """
        LeetCode Problem 1: Two Sum
        Find two numbers that add up to target.
        """
        print(f"Processing nums={nums}, target={target}")
        num_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], i]
            num_map[num] = i
        return []

    def threeSum(self, nums):
        """
        LeetCode Problem 15: Three Sum
        Find all unique triplets that sum to zero.
        """
        print(f"Processing nums={nums}")
        nums.sort()
        result = []

        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i-1]:
                continue

            left, right = i + 1, len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1

        return result


if __name__ == "__main__":
    # Example 1: Basic usage with tuple format
    print("=== Example 1: Two Sum with tuple format ===")
    testcases_two_sum = [
        (([2, 7, 11, 15], 9), [0, 1]),
        (([3, 2, 4], 6), [1, 2]),
        (([3, 3], 6), [0, 1])
    ]

    results = pyleet.run(testcases_two_sum, method="twoSum")
    pyleet.print_results(results, verbose=False)  # Less verbose output

    # Example 2: Dict format test cases
    print("\n=== Example 2: Three Sum with dict format ===")
    testcases_three_sum = [
        {
            "input": [[-1, 0, 1, 2, -1, -4]],
            "expected": [[-1, -1, 2], [-1, 0, 1]]
        },
        {
            "input": [[0, 1, 1]],
            "expected": []
        },
        {
            "input": [[0, 0, 0]],
            "expected": [[0, 0, 0]]
        }
    ]

    results = pyleet.run(testcases_three_sum, method="threeSum")
    pyleet.print_results(results)

    # Example 3: List format test cases
    print("\n=== Example 3: Two Sum with list format ===")
    print("Note: The first test case has incorrect input format.")
    testcases_list_format = [
        # Note: this will fail as input format is wrong
        [[2, 7, 11, 15, 9], [0, 1]],
        [[[3, 2, 4], 6], [1, 2]]      # Correct format with nested list for input
    ]

    results = pyleet.run(testcases_list_format, method="twoSum")
    pyleet.print_results(results)
