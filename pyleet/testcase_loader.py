"""
Module to load and parse test cases from an external file.
Supports plain text or JSON formats.
Handles default data structures: int, str, list, dict, set.
"""

import json
import ast
import os
from .datastructures import get_deserializer


def load_test_cases(file_path):
    """
    Load test cases from the given file path.

    Args:
        file_path (str): Path to the test case file.

    Returns:
        list of tuples: Each tuple contains (input_args, expected_output).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test case file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # Try JSON first
    try:
        data = json.loads(content)
        return _parse_json_cases(data)
    except json.JSONDecodeError:
        pass  # Not JSON, try plain text

    # Fallback: parse as plain text, line by line
    lines = content.splitlines()
    cases = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # skip empty lines and comments
        try:
            parsed = ast.literal_eval(line)
            # Expect tuple: (input_args, expected_output)
            if not isinstance(parsed, tuple) or len(parsed) != 2:
                raise ValueError(f"Invalid test case format: {line}")
            input_args, expected = parsed
            cases.append((input_args, expected))
        except Exception as e:
            raise ValueError(
                f"Failed to parse test case line: {line}\nError: {e}")
    return cases


def _deserialize_recursive(item):
    """
    Recursively traverse data and apply deserializers where needed.
    Supports the format: {"ClassName": <raw_data>}
    """
    if isinstance(item, dict):
        # Check for custom class format: {"ClassName": <raw_data>}
        # Look for a single key that matches a registered deserializer
        if len(item) == 1:
            key, data = next(iter(item.items()))
            deserializer = get_deserializer(key)
            if deserializer:
                # Recursively deserialize the data part *before* passing to the final deserializer
                # This handles cases like List[ListNode] or nested custom types
                deserialized_data = _deserialize_recursive(data)
                try:
                    return deserializer(deserialized_data)
                except Exception as e:
                    # Add context to the error
                    raise ValueError(
                        f"Error deserializing type '{key}' with data '{data}': {e}") from e
            else:
                # Not a custom type, handle as regular dictionary
                return {k: _deserialize_recursive(v) for k, v in item.items()}
        else:
            # Handle regular dictionaries recursively too
            return {k: _deserialize_recursive(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [_deserialize_recursive(elem) for elem in item]
    elif isinstance(item, tuple):
        return tuple(_deserialize_recursive(elem) for elem in item)
    else:
        # Base case: return primitive types as is
        return item


def process_test_cases(testcases):
    """
    Process test cases from in-memory data, applying deserialization.

    Args:
        testcases (list): List of test case tuples, dicts, or lists.

    Returns:
        list of tuples: Each tuple contains (input_args, expected_output).
    """
    if not isinstance(testcases, list):
        raise ValueError("Test cases must be provided as a list")

    cases = []
    for entry in testcases:
        if isinstance(entry, tuple) and len(entry) == 2:
            # Direct tuple format: (input_args, expected)
            input_args, expected = entry
        elif isinstance(entry, dict):
            if 'input' not in entry or 'expected' not in entry:
                raise ValueError(
                    f"Test case dict missing 'input' or 'expected': {entry}")
            input_args = entry['input']
            expected = entry['expected']
        elif isinstance(entry, list) and len(entry) == 2:
            input_args, expected = entry
        else:
            raise ValueError(f"Invalid test case entry: {entry}")

        # Deserialize inputs and expected output
        deserialized_input_args = _deserialize_recursive(input_args)
        deserialized_expected = _deserialize_recursive(expected)

        # Ensure input_args is a tuple for the runner
        if not isinstance(deserialized_input_args, tuple):
            # For multiple inputs packed as list, convert to tuple
            if isinstance(deserialized_input_args, list):
                deserialized_input_args = tuple(deserialized_input_args)
            else:  # Single input case
                deserialized_input_args = (deserialized_input_args,)

        cases.append((deserialized_input_args, deserialized_expected))
    return cases


def _parse_json_cases(data):
    """
    Parse test cases from JSON data, applying deserialization.

    Args:
        data (list): List of test case dicts or lists.

    Returns:
        list of tuples: Each tuple contains (input_args, expected_output).
    """
    cases = []
    if not isinstance(data, list):
        raise ValueError(
            "JSON test case file must contain a list of test cases")

    for entry in data:
        if isinstance(entry, dict):
            if 'input' not in entry or 'expected' not in entry:
                raise ValueError(
                    f"Test case dict missing 'input' or 'expected': {entry}")
            input_args = entry['input']
            expected = entry['expected']
        elif isinstance(entry, list) and len(entry) == 2:
            input_args, expected = entry
        else:
            raise ValueError(f"Invalid test case entry: {entry}")

        # Deserialize inputs and expected output
        deserialized_input_args = _deserialize_recursive(input_args)
        deserialized_expected = _deserialize_recursive(expected)

        # Ensure input_args is a tuple for the runner
        if not isinstance(deserialized_input_args, tuple):
            # For multiple inputs packed as list, convert to tuple
            if isinstance(deserialized_input_args, list):
                deserialized_input_args = tuple(deserialized_input_args)
            else:  # Single input case
                deserialized_input_args = (deserialized_input_args,)

        cases.append((deserialized_input_args, deserialized_expected))
    return cases
