from __future__ import annotations
from math import sqrt
from Point import Point


class Route:
    # speed: (0, inf] - 0 excluded
    def __init__(self, point1: Point, point2: Point, maxSpeed: float = 1, restricted: bool = False):
        self.p1 = point1
        self.p2 = point2
        self.speed = maxSpeed
        self.restricted = restricted

    def __eq__(self, other) -> bool:
        return (self.p1 == other.p1) and (self.p2 == other.p2)

    def __hash__(self) -> hash:
        return hash(self.p1) ^ hash(self.p2)

    def __str__(self) -> str:
        return f"Route: [{self.p1}, {self.p2}, restricted: {self.restricted}, " \
               f"speed: {self.speed}, length: {self.length()}, time: {self.time()}]"

    def length(self) -> float:
        return sqrt(abs(self.p1.x - self.p2.x) ** 2 + abs(self.p1.y - self.p2.y) ** 2)

    def time(self) -> float:
        return self.length() / self.speed

    def restrict(self) -> None:
        self.restricted = True

    def copy(self) -> Route:
        return Route(self.p1.copy(), self.p2.copy(), self.speed, self.restricted)


def routeGenerator(points: list[Point]) -> list[Route]:
    routes = []
    pointsLength = len(points) - 1

    for p1Index, point1 in enumerate(points):
        [routes.append(Route(point1, points[p1Index + p2Index + 1])) for p2Index in range(pointsLength - p1Index)]

    return routes
