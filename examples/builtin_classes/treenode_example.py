"""
Example showing how to use Pyleet's built-in ListNode and TreeNode classes.

This demonstrates three different usage patterns:
1. Automatic fallback (no imports needed)
2. Explicit import (recommended)
3. Custom override (advanced)
"""

# Pattern 1: Automatic fallback - no imports needed!
# Pyleet will automatically use built-in classes if you don't define your own

# Pattern 2: Explicit import (recommended for clarity)
from pyleet import TreeNode

# Pattern 3: You can still override with custom implementations if needed
# Just define your own classes and they'll take precedence


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
