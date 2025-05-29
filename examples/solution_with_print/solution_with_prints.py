class Solution:
    def twoSum(self, nums, target):
        """
        Test solution with print statements for debugging.
        """
        print(f"Looking for target: {target}")
        print(f"Input array: {nums}")

        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            print(f"Checking index {i}, value {num}, need {complement}")

            if complement in seen:
                print(f"Found solution: indices {seen[complement]} and {i}")
                return [seen[complement], i]

            seen[num] = i
            print(f"Added {num} -> {i} to seen dict")

        print("No solution found")
        return []
