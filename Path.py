from __future__ import annotations
from Point import Point
from Route import Route
from utils import *


class Path:
    def __init__(self, routes: list[Route], fitness: float=float('inf')):
        self.routes = routes
        self.fitness = fitness

    def __hash__(self) -> hash:
        out = hash(self.routes[0])

        for i in range(1, len(self.routes) - 1):
            out = out ^ hash(self.routes[i])

        return out

    def __str__(self) -> str:
        outStr = "Path: ["

        for route in self.routes:
            outStr += f"\n\t{route},"

        return f"{outStr}\n], length: {self.length()}, time: {self.time()}"

    def __lt__(self, other):
        return self.fitness < other.fitness

    def length(self) -> float:
        return sum([route.length() for route in self.routes])

    def time(self) -> float:
        return sum([route.time() for route in self.routes])

    def getRoute(self, point1: Point, point2: Point) -> Route:
        route1 = Route(point1, point2)
        r1 = next(iter(route for route in self.routes if route == route1), None)

        if r1:
            return r1

        route2 = Route(point2, point1)
        r2 = next(iter(route for route in self.routes if route == route2), None)
        route1.speed = r2.speed
        route1.restricted = r2.restricted

        return route1

    def getRouteRef(self, point1: Point, point2: Point) -> Route:
        route_from_points = Route(point1, point2)
        found_route = next(iter(route for route in self.routes if route == route_from_points), None)

        return found_route if found_route else self.getRouteRef(point2, point1)

    def pointList(self) -> list[Point]:
        output = [self.routes[0].p1]
        [output.append(route.p2) for route in self.routes]
        return list(output)

    def copy(self) -> Path:
        return Path([route.copy() for route in self.routes])

    def reconstructRoutes(self, pathMap, points: list[Point]) -> None:
        length = len(points) - 1
        self.routes = [pathMap.getRoute(points[i], points[i + 1]) for i in range(length)]
