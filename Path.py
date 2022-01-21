from __future__ import annotations
from Point import Point
from Route import Route
from utils import *


class Path:
    def __init__(self, routes: list[Route]):
        self.routes = routes

    def __str__(self):
        outStr = "Path: ["

        for route in self.routes:
            outStr += f"\n\t{route},"

        return f"{outStr}\n], length: {self.length()}, time: {self.time()}"

    def length(self) -> float:
        pathLength = 0

        for route in self.routes:
            pathLength += route.length()

        return pathLength

    def time(self) -> float:
        pathTime = 0

        for route in self.routes:
            pathTime += route.time()

        return pathTime

    def getRoute(self, point1: Point, point2: Point) -> Route:
        route1 = Route(point1, point2)
        r1 = findFirst(self.routes, lambda route: route == route1)

        if r1:
            return r1

        route2 = Route(point2, point1)
        r2 = findFirst(self.routes, lambda route: route == route2)
        route1.speed = r2.speed
        route1.restricted = r2.restricted

        return route1

    def getRouteRef(self, point1: Point, point2: Point) -> Route:
        route1 = Route(point1, point2)
        r1 = findFirst(self.routes, lambda route: route == route1)

        if r1:
            return r1

        return findFirst(self.routes, lambda route: route.p2 == route1.p1 and route.p1 == route1.p2)

    def pointList(self) -> list[Point]:
        output = list()
        output.append(self.routes[0].p1)

        for route in self.routes:
            output.append(route.p2)

        return list(output)

    def copy(self) -> Path:
        routes = list()
        for route in self.routes:
            routes.append(route.copy())

        return Path(routes)

    def reconstructRoutes(self, pathMap, points: list[Point]) -> None:
        length = len(points) - 1
        routes = list()

        for i in range(length):
            routes.append(pathMap.getRoute(points[i], points[i + 1]))

        self.routes = routes
