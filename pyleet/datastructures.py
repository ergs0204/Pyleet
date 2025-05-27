"""
Utility functions to convert basic data structures into custom classes
like ListNode or TreeNode, and a registry for custom deserializers and serializers.
"""

_deserializer_registry = {}
_serializer_registry = {}


def register_deserializer(type_name, func):
    """
    Register a deserializer function for a custom class.

    Args:
        type_name (str): Name of the target class.
        func (callable): Function that takes raw data and returns an instance.
    """
    _deserializer_registry[type_name] = func


def get_deserializer(type_name):
    """
    Get the deserializer function for a custom class.

    Args:
        type_name (str): Name of the target class.

    Returns:
        callable or None: The deserializer function, or None if not registered.
    """
    return _deserializer_registry.get(type_name)


def register_serializer(type_name, func):
    """
    Register a serializer function for a custom class.

    Args:
        type_name (str): Name of the source class.
        func (callable): Function that takes an instance and returns raw data.
    """
    _serializer_registry[type_name] = func


def get_serializer(type_name):
    """
    Get the serializer function for a custom class.

    Args:
        type_name (str): Name of the source class.

    Returns:
        callable or None: The serializer function, or None if not registered.
    """
    return _serializer_registry.get(type_name)


def list_to_listnode(lst):
    """
    Convert a list to a ListNode linked list.
    Uses user-defined ListNode class if available, otherwise falls back to built-in.
    """
    if lst is None or (isinstance(lst, list) and len(lst) == 0):
        return None

    # Get ListNode class (user-defined or built-in)
    ListNode = _get_user_class("ListNode")
    if ListNode is None:
        raise ValueError(
            "ListNode class not found. Please define ListNode in your solution file or import from pyleet.common.")

    dummy = ListNode(0)
    current = dummy
    for val in lst:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def listnode_to_list(node):
    """
    Convert a ListNode linked list to a list.
    Works with any ListNode implementation that has 'val' and 'next' attributes.
    """
    if node is None:
        return []

    result = []
    current = node
    visited = set()

    while current and id(current) not in visited:
        visited.add(id(current))
        result.append(current.val)
        current = current.next

        # Prevent infinite loops
        if len(result) > 1000:
            break

    return result


def list_to_tree(lst):
    """
    Convert a list to a TreeNode binary tree using level-order representation.
    Uses user-defined TreeNode class if available, otherwise falls back to built-in.
    """
    if not lst:
        return None

    # Get TreeNode class (user-defined or built-in)
    TreeNode = _get_user_class("TreeNode")
    if TreeNode is None:
        raise ValueError(
            "TreeNode class not found. Please define TreeNode in your solution file or import from pyleet.common.")

    # Create root node
    root = TreeNode(lst[0])
    queue = [root]
    i = 1

    while queue and i < len(lst):
        node = queue.pop(0)

        # Add left child
        if i < len(lst) and lst[i] is not None:
            node.left = TreeNode(lst[i])
            queue.append(node.left)
        i += 1

        # Add right child
        if i < len(lst) and lst[i] is not None:
            node.right = TreeNode(lst[i])
            queue.append(node.right)
        i += 1

    return root


def tree_to_list(root):
    """
    Convert a TreeNode binary tree to level-order list representation.
    Works with any TreeNode implementation that has 'val', 'left', and 'right' attributes.
    """
    if not root:
        return []

    # Safety check: ensure this is actually a tree node
    if not (hasattr(root, 'val') and hasattr(root, 'left') and hasattr(root, 'right')):
        raise ValueError(
            f"tree_to_list called on non-TreeNode object: {type(root).__name__}")

    result = []
    queue = [root]

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


# Global variable to store reference to user module
_user_module = None


def set_user_module(module):
    """
    Set the user module so deserializers can access user-defined classes.
    """
    global _user_module
    _user_module = module


def _get_user_class(class_name):
    """
    Get a class from the user module by name, with fallback to built-in classes.
    Priority: User-defined > Built-in > None
    """
    global _user_module

    # First, try to get from user module
    if _user_module is not None:
        user_class = getattr(_user_module, class_name, None)
        if user_class is not None:
            return user_class

    # Fallback to built-in classes for common LeetCode types
    if class_name in ["ListNode", "TreeNode"]:
        try:
            from pyleet.common import ListNode, TreeNode
            return {"ListNode": ListNode, "TreeNode": TreeNode}[class_name]
        except ImportError:
            pass

    return None


def serialize_object(obj):
    """
    Serialize an object to its JSON-compatible representation.
    For custom classes, this will use registered serializers.
    """
    if obj is None:
        return None

    # Handle basic types
    if isinstance(obj, (int, float, str, bool)):
        return obj
    elif isinstance(obj, list):
        return [serialize_object(item) for item in obj]
    elif isinstance(obj, tuple):
        return [serialize_object(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: serialize_object(v) for k, v in obj.items()}

    # Handle custom objects
    class_name = type(obj).__name__
    serializer = get_serializer(class_name)
    if serializer:
        # Use registered serializer
        serialized_data = serializer(obj)
        return {class_name: serialize_object(serialized_data)}

    # Special handling for common LeetCode classes without registered serializers
    if class_name == "ListNode" and hasattr(obj, 'val') and hasattr(obj, 'next') and not hasattr(obj, 'left'):
        return {class_name: listnode_to_list(obj)}
    elif class_name == "TreeNode" and hasattr(obj, 'val') and hasattr(obj, 'left') and hasattr(obj, 'right'):
        return {class_name: tree_to_list(obj)}

    # Fallback: try to use __dict__ or __repr__
    if hasattr(obj, '__dict__'):
        # For objects with attributes, try to serialize their dict representation
        return {class_name: serialize_object(obj.__dict__)}
    else:
        # Last resort: convert to string representation
        return str(obj)


# Register default deserializers and serializers
register_deserializer("ListNode", list_to_listnode)
register_deserializer("TreeNode", list_to_tree)
register_serializer("ListNode", listnode_to_list)
register_serializer("TreeNode", tree_to_list)

# Placeholder for ListNode and TreeNode class definitions
# The actual classes should be provided by the user inside their solution file
# Example:
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
#
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
