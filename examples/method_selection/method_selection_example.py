"""
Example demonstrating method selection functionality in Pyleet.

This solution class contains multiple methods that could potentially solve different problems.
Users can now specify which method to use with the --method flag.
"""


class Solution:
    def twoSum(self, nums, target):
        """
        LeetCode Problem 1: Two Sum
        Find two numbers that add up to target.
        """
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
        nums.sort()
        result = []

        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i-1]:
                continue

            left, right = i + 1, len(nums) - 1
            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]
                if current_sum == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif current_sum < 0:
                    left += 1
                else:
                    right -= 1

        return result
