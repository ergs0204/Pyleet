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
    
    def fourSum(self, nums, target):
        """
        LeetCode Problem 18: Four Sum
        Find all unique quadruplets that sum to target.
        """
        nums.sort()
        result = []
        n = len(nums)
        
        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i-1]:
                continue
                
            for j in range(i + 1, n - 2):
                if j > i + 1 and nums[j] == nums[j-1]:
                    continue
                    
                left, right = j + 1, n - 1
                while left < right:
                    current_sum = nums[i] + nums[j] + nums[left] + nums[right]
                    if current_sum == target:
                        result.append([nums[i], nums[j], nums[left], nums[right]])
                        while left < right and nums[left] == nums[left + 1]:
                            left += 1
                        while left < right and nums[right] == nums[right - 1]:
                            right -= 1
                        left += 1
                        right -= 1
                    elif current_sum < target:
                        left += 1
                    else:
                        right -= 1
        
        return result
    
    def maxSubArray(self, nums):
        """
        LeetCode Problem 53: Maximum Subarray
        Find the contiguous subarray with the largest sum.
        """
        max_sum = nums[0]
        current_sum = nums[0]
        
        for i in range(1, len(nums)):
            current_sum = max(nums[i], current_sum + nums[i])
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def productExceptSelf(self, nums):
        """
        LeetCode Problem 238: Product of Array Except Self
        Return array where each element is product of all elements except itself.
        """
        n = len(nums)
        result = [1] * n
        
        # Left pass
        for i in range(1, n):
            result[i] = result[i-1] * nums[i-1]
        
        # Right pass
        right_product = 1
        for i in range(n-1, -1, -1):
            result[i] *= right_product
            right_product *= nums[i]
        
        return result
