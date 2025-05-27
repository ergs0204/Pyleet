"""
Example solution for testing the new serialization format with linked lists.
"""


# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

#     def __eq__(self, other):
#         if not isinstance(other, ListNode):
#             return False
#         current_self = self
#         current_other = other
#         while current_self and current_other:
#             if current_self.val != current_other.val:
#                 return False
#             current_self = current_self.next
#             current_other = current_other.next
#         return current_self is None and current_other is None


class Solution:
    def reverseList(self, head):
        """
        Reverse a linked list.
        """
        prev = None
        current = head
        while current:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp
        return prev
