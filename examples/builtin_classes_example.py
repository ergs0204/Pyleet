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
from pyleet import ListNode, TreeNode

# Pattern 3: You can still override with custom implementations if needed
# Just define your own classes and they'll take precedence

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
    
    def mergeTwoLists(self, list1, list2):
        """
        Merge two sorted linked lists.
        LeetCode Problem 21: Merge Two Sorted Lists
        """
        dummy = ListNode(0)
        current = dummy
        
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        
        # Append remaining nodes
        current.next = list1 or list2
        
        return dummy.next
    
    def maxDepth(self, root):
        """
        Find maximum depth of binary tree.
        LeetCode Problem 104: Maximum Depth of Binary Tree
        """
        if not root:
            return 0
        
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        
        return max(left_depth, right_depth) + 1
