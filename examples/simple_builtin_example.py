"""
Simple example demonstrating Pyleet's built-in ListNode and TreeNode classes.
No imports needed - Pyleet automatically provides these classes!
"""

class Solution:
    def reverseList(self, head):
        """
        Reverse a linked list.
        LeetCode Problem 206: Reverse Linked List
        """
        prev = None
        current = head
        while current:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp
        return prev
    
    def invertTree(self, root):
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
