"""
Simple example of programmatic Pyleet usage.
"""

import pyleet


class Solution:
    def twoSum(self, nums, target):
        """Find two numbers that add up to target."""
        num_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], i]
            num_map[num] = i
        return []


# Define test cases directly in the code
testcases = [
    (([2, 7, 11, 15], 9), [0, 1]),
    (([3, 2, 4], 6), [1, 2]),
    (([3, 3], 6), [0, 1])
]

# Run the tests
if __name__ == "__main__":
    results = pyleet.run(testcases)
    pyleet.print_results(results)
