# Pyleet Custom Class Serialization: Dictionary Handling Guide

This guide provides comprehensive documentation on how Pyleet's custom class serialization system handles different types of dictionaries in test case JSON files.

## Table of Contents

1. [Overview](#overview)
2. [Dictionary Processing Rules](#dictionary-processing-rules)
3. [Concrete Examples](#concrete-examples)
4. [Edge Cases and Limitations](#edge-cases-and-limitations)
5. [Key Insights](#key-insights)
6. [Best Practices](#best-practices)

## Overview

Pyleet's custom class serialization system automatically detects and deserializes custom class instances from JSON test case files. The system uses a specific set of rules to differentiate between regular Python dictionaries and custom class dictionaries that should be converted into class instances.

The core logic is implemented in the `_deserialize_recursive()` function in `pyleet/testcase_loader.py`.

## Dictionary Processing Rules

### Rule 1: Single-Key Dictionary + Registered Deserializer → Custom Class Instance

**Condition:** Dictionary has exactly one key AND the key matches a registered deserializer

```python
# Input JSON
{"ListNode": [1, 2, 3]}

# Output
ListNode([1, 2, 3])  # Custom class instance
```

### Rule 2: Single-Key Dictionary + Unregistered Key → Regular Dictionary

**Condition:** Dictionary has exactly one key BUT the key does NOT match any registered deserializer

```python
# Input JSON
{"CustomClass": [1, 2, 3]}

# Output
{"CustomClass": [1, 2, 3]}  # Regular Python dict
```

### Rule 3: Multi-Key Dictionary → Regular Dictionary (Always)

**Condition:** Dictionary has multiple keys (regardless of whether any keys match deserializers)

```python
# Input JSON
{"key": "value", "count": 5, "active": True}

# Output
{"key": "value", "count": 5, "active": True}  # Regular Python dict
```

### Rule 4: Empty Dictionary → Regular Dictionary

**Condition:** Dictionary is empty

```python
# Input JSON
{}

# Output
{}  # Regular Python dict
```

### Rule 5: Recursive Processing

**Condition:** All nested structures are processed recursively using the same rules

```python
# Input JSON
{
    "nodes": [{"ListNode": [1, 2]}, {"ListNode": [3, 4]}],
    "metadata": {"count": 2, "type": "linked_list"}
}

# Output
{
    "nodes": [ListNode([1, 2]), ListNode([3, 4])],  # Custom classes
    "metadata": {"count": 2, "type": "linked_list"}  # Regular dict
}
```

## Concrete Examples

### Example 1: Custom Class Deserialization

```json
{
  "input": [{"ListNode": [1, 2, 3]}],
  "expected": {"ListNode": [3, 2, 1]}
}
```

**Processing:**
- `{"ListNode": [1, 2, 3]}` → `ListNode([1, 2, 3])` (custom class instance)
- `{"ListNode": [3, 2, 1]}` → `ListNode([3, 2, 1])` (custom class instance)

### Example 2: Regular Dictionary (Unregistered Key)

```json
{
  "input": [{"CustomClass": [1, 2, 3]}],
  "expected": {"result": "processed"}
}
```

**Processing:**
- `{"CustomClass": [1, 2, 3]}` → `{"CustomClass": [1, 2, 3]}` (regular dict)
- `{"result": "processed"}` → `{"result": "processed"}` (regular dict)

### Example 3: Multi-Key Regular Dictionary

```json
{
  "input": [{"key": "value", "count": 5}],
  "expected": {"processed": true}
}
```

**Processing:**
- `{"key": "value", "count": 5}` → `{"key": "value", "count": 5}` (regular dict)
- `{"processed": true}` → `{"processed": true}` (regular dict)

### Example 4: Mixed Nested Structure

```json
{
  "input": [
    {
      "nodes": [{"ListNode": [1, 2]}, {"ListNode": [3, 4]}],
      "metadata": {"count": 2, "type": "linked_list"}
    }
  ],
  "expected": {"ListNode": [1, 2, 3, 4]}
}
```

**Processing:**
- Outer dict has multiple keys → treated as regular dict
- `{"ListNode": [1, 2]}` → `ListNode([1, 2])` (custom class)
- `{"ListNode": [3, 4]}` → `ListNode([3, 4])` (custom class)
- `{"count": 2, "type": "linked_list"}` → regular dict (multiple keys)
- `{"ListNode": [1, 2, 3, 4]}` → `ListNode([1, 2, 3, 4])` (custom class)

### Example 5: List with Mixed Dictionary Types

```json
{
  "input": [
    [
      {"ListNode": [1, 2, 3]},
      {"key": "value"},
      {"TreeNode": [5]}
    ]
  ],
  "expected": {"processed": "mixed_types"}
}
```

**Processing:**
- `{"ListNode": [1, 2, 3]}` → `ListNode([1, 2, 3])` (custom class)
- `{"key": "value"}` → `{"key": "value"}` (regular dict, unregistered key)
- `{"TreeNode": [5]}` → `TreeNode(5)` (custom class)

## Edge Cases and Limitations

### Edge Case 1: Non-String Keys

**Rule:** Only string keys can trigger custom class deserialization

```python
# Input JSON
{1: [1, 2, 3]}           # Numeric key
{true: [1, 2, 3]}        # Boolean key

# Output
{1: [1, 2, 3]}           # Regular dict (numeric key ignored)
{True: [1, 2, 3]}        # Regular dict (boolean key ignored)
```

### Edge Case 2: Invalid Data Types for Deserializers

**Rule:** Deserializers receive whatever data is provided (no type validation)

```python
# Input JSON
{"ListNode": "string_instead_of_list"}

# Output
ListNode(['s', 't', 'r', 'i', 'n', 'g', '_', 'i', 'n', 's', 't', 'e', 'a', 'd', '_', 'o', 'f', '_', 'l', 'i', 's', 't'])
# The deserializer iterates over the string characters!
```

**⚠️ Warning:** This can lead to unexpected behavior. Deserializers should handle invalid input gracefully.

### Edge Case 3: None and Empty Values

```python
# Input JSON
{"ListNode": null}       # null in JSON becomes None in Python
{"ListNode": []}         # Empty list

# Output
None                     # Both cases return None (handled by deserializer)
None
```

### Edge Case 4: Complex Nested Data

**Rule:** Deserializers receive recursively processed data

```python
# Input JSON
{"ListNode": [{"nested": "dict"}, [1, 2], "mixed"]}

# Output
ListNode([{"nested": "dict"}, [1, 2], "mixed"])
# The nested dict and list are preserved as-is
```

### Edge Case 5: Deep Nesting

**Rule:** Custom class detection happens at every nesting level

```python
# Input JSON
{
  "level1": {
    "level2": {
      "level3": {"ListNode": [1, 2, 3]}
    }
  }
}

# Output
{
  "level1": {
    "level2": {
      "level3": ListNode([1, 2, 3])  # Only this gets deserialized
    }
  }
}
```

### Edge Case 6: Multi-Key Dictionary with Registered Key

**Rule:** Multi-key dictionaries are NEVER treated as custom classes, even if one key matches a deserializer

```python
# Input JSON
{"ListNode": [1, 2, 3], "metadata": "info"}

# Output
{"ListNode": [1, 2, 3], "metadata": "info"}  # Regular dict (multiple keys)
# The ListNode key is ignored because there are multiple keys
```

## Key Insights

### Critical Requirements for Custom Class Deserialization

1. **Exactly One Key:** The dictionary must have exactly one key-value pair
2. **String Key:** The key must be a string (not numeric, boolean, or other types)
3. **Registered Deserializer:** The key must exactly match a registered deserializer name (case-sensitive)
4. **Valid Deserializer Function:** The registered deserializer must be callable

### Important Limitations

1. **No Type Validation:** Deserializers receive raw data without validation
2. **Multi-Key Exclusion:** Dictionaries with multiple keys are never custom classes
3. **Non-String Key Exclusion:** Only string keys can trigger deserialization
4. **Case Sensitivity:** Deserializer names are case-sensitive (`"listnode"` ≠ `"ListNode"`)
5. **No Error Recovery:** Invalid data passed to deserializers may cause unexpected behavior

### Processing Behavior

1. **Recursive Processing:** All nested structures are processed using the same rules
2. **Depth-First:** Processing occurs from innermost to outermost structures
3. **Immutable Rules:** The same rules apply at every nesting level
4. **Mixed Types Allowed:** Regular dictionaries can contain custom classes as values

## Best Practices

### For Test Case Authors

1. **Use Single-Key Format:** Always use `{"ClassName": data}` for custom classes
2. **Avoid Multi-Key Custom Classes:** Don't mix custom class keys with other keys
3. **Validate Data Types:** Ensure data passed to deserializers is in expected format
4. **Test Edge Cases:** Verify behavior with None, empty, and invalid data

### For Deserializer Authors

1. **Handle Invalid Input:** Always validate input data in deserializer functions
2. **Return Appropriate Defaults:** Handle None and empty inputs gracefully
3. **Document Expected Format:** Clearly document what data format your deserializer expects
4. **Use Descriptive Names:** Choose clear, unambiguous names for custom classes

### Example of Robust Deserializer

```python
def list_to_listnode(data):
    """
    Convert list data to ListNode linked list.

    Args:
        data: Expected to be a list of values, but handles edge cases

    Returns:
        ListNode: Head of linked list, or None if data is empty/invalid
    """
    # Handle None and empty cases
    if not data:
        return None

    # Handle non-list input
    if not isinstance(data, list):
        raise ValueError(f"Expected list, got {type(data).__name__}: {data}")

    # Create linked list
    dummy = ListNode(0)
    current = dummy
    for val in data:
        current.next = ListNode(val)
        current = current.next
    return dummy.next
```

---

This guide provides the complete picture of how Pyleet handles dictionary serialization. Understanding these rules will help you write effective test cases and avoid common pitfalls when working with custom classes in Pyleet.
