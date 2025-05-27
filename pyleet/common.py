"""
Built-in common LeetCode data structures.

This module provides standard implementations of ListNode and TreeNode
that are commonly used in LeetCode problems. Users can import these
directly or let Pyleet use them automatically as fallbacks.
"""


class ListNode:
    """
    Standard LeetCode ListNode implementation.
    
    Attributes:
        val: The value stored in the node
        next: Reference to the next node in the list
    """
    
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __eq__(self, other):
        """Compare two linked lists for equality."""
        if not isinstance(other, ListNode):
            return False
        
        current_self = self
        current_other = other
        
        while current_self and current_other:
            if current_self.val != current_other.val:
                return False
            current_self = current_self.next
            current_other = current_other.next
        
        # Both should be None at the end
        return current_self is None and current_other is None
    
    def __repr__(self):
        """String representation for debugging."""
        values = []
        current = self
        visited = set()
        
        while current and id(current) not in visited:
            visited.add(id(current))
            values.append(str(current.val))
            current = current.next
            
            # Prevent infinite loops in case of cycles
            if len(values) > 100:
                values.append("...")
                break
        
        return f"ListNode([{' -> '.join(values)}])"
    
    def to_list(self):
        """Convert linked list to Python list for easier testing."""
        result = []
        current = self
        visited = set()
        
        while current and id(current) not in visited:
            visited.add(id(current))
            result.append(current.val)
            current = current.next
            
            # Prevent infinite loops
            if len(result) > 1000:
                break
        
        return result


class TreeNode:
    """
    Standard LeetCode TreeNode implementation.
    
    Attributes:
        val: The value stored in the node
        left: Reference to the left child node
        right: Reference to the right child node
    """
    
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __eq__(self, other):
        """Compare two binary trees for equality."""
        if not isinstance(other, TreeNode):
            return False
        
        # Both None
        if self is None and other is None:
            return True
        
        # One None, one not None
        if self is None or other is None:
            return False
        
        # Compare values and recursively compare children
        return (self.val == other.val and 
                self._compare_subtree(self.left, other.left) and
                self._compare_subtree(self.right, other.right))
    
    def _compare_subtree(self, node1, node2):
        """Helper method to compare subtrees."""
        if node1 is None and node2 is None:
            return True
        if node1 is None or node2 is None:
            return False
        return (node1.val == node2.val and
                self._compare_subtree(node1.left, node2.left) and
                self._compare_subtree(node1.right, node2.right))
    
    def __repr__(self):
        """String representation for debugging."""
        if not self:
            return "TreeNode(None)"
        
        # Level-order traversal representation
        result = []
        queue = [self]
        
        while queue and any(node is not None for node in queue):
            level_size = len(queue)
            level_values = []
            
            for _ in range(level_size):
                node = queue.pop(0)
                if node is None:
                    level_values.append("null")
                    queue.extend([None, None])
                else:
                    level_values.append(str(node.val))
                    queue.extend([node.left, node.right])
            
            result.extend(level_values)
            
            # Prevent infinite representation
            if len(result) > 50:
                result.append("...")
                break
        
        # Remove trailing nulls
        while result and result[-1] in ["null", "..."]:
            if result[-1] == "...":
                result.append("...")
                break
            result.pop()
        
        return f"TreeNode([{', '.join(result)}])"
    
    def to_list(self):
        """Convert binary tree to level-order list representation."""
        if not self:
            return []
        
        result = []
        queue = [self]
        
        while queue:
            node = queue.pop(0)
            if node is None:
                result.append(None)
            else:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
        
        # Remove trailing None values
        while result and result[-1] is None:
            result.pop()
        
        return result
