"""
Simple example showing how to use a custom Point class in Pyleet.
"""

from pyleet import register_deserializer


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


def list_to_point(data):
    """
    Convert list to Point.
    Format: [x, y]
    Example: [3, 4] -> Point(3, 4)
    """
    if not data or len(data) != 2:
        return None
    return Point(data[0], data[1])


# Register the deserializer
register_deserializer("Point", list_to_point)


class Solution:

    def movePoint(self, point):
        """Move point by (1, 1)"""
        if not point:
            return None
        return Point(point.x + 1, point.y + 1)
