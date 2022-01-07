from __future__ import annotations


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __str__(self):
        return f"Point(x: {self.x}, y: {self.y})"

    def copy(self) -> Point:
        return Point(self.x, self.y)
