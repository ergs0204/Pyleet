import pyleet
from pyleet import TreeNode


class Solution:
    def invertTree(self, root: TreeNode):
        """
        Invert a binary tree.
        LeetCode Problem 226: Invert Binary Tree
        """
        if not root:
            return None

        # Swap left and right children
        root.left, root.right = root.right, root.left

        # Recursively invert subtrees
        self.invertTree(root.left)
        self.invertTree(root.right)

        return root


testcases = [
    {
        "description": "Invert binary tree - simple case",
        "input": [{"TreeNode": [4, 2, 7, 1, 3, 6, 9]}],
        "expected": {"TreeNode": [4, 7, 2, 9, 6, 3, 1]}
    },
    {
        "description": "Invert binary tree - simple case",
        "input": [{"TreeNode": [4, 2]}],
        "expected": {"TreeNode": [4, None, 2]}
    },
    {
        "description": "Invert binary tree - single node",
        "input": [{"TreeNode": [1]}],
        "expected": {"TreeNode": [1]}
    },
    {
        "description": "Invert binary tree - empty tree",
        "input": [{"TreeNode": []}],
        "expected": None
    }
]

# Run the tests
if __name__ == "__main__":
    results = pyleet.run(testcases)
    pyleet.print_results(results)
