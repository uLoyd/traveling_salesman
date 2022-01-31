from Point import Point
from Route import Route
import pygame as pg


def mapAxis(ax: int, newRange: int, newMin: int, oldRange: int, oldMin: int) -> int:
    return round((((ax - oldMin) * newRange) / oldRange) + newMin)


class DisplayMap:
    def __init__(self, points: list[Point], width: int, height: int, x: int = 10, y: int = 10):
        points.sort(key=lambda point: point.x)
        self.oldXMin = points[0].x
        self.oldXMax = points[-1].x
        self.oldXRange = self.oldXMax - self.oldXMin

        points.sort(key=lambda point: point.y)
        self.oldYMin = points[0].y
        self.oldYMax = points[-1].y
        self.oldYRange = self.oldYMax - self.oldYMin

        self.points = points
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def drawRoute(self, window, route: Route, colour: list[int]) -> None:
        x1, y1 = self.mapCoords(route.p1)
        x2, y2 = self.mapCoords(route.p2)

        pg.draw.line(window, colour, (x1, y1), (x2, y2), 2)

    def drawRoutes(self, window, routes: list[Route], colour: list[int]):
        for route in routes:
            self.drawRoute(window, route, colour)

    def drawRestrictedRoutes(self, window, routeList: list[Route], colour=None):
        if not colour:
            colour = [255, 0, 0]

        self.drawRoutes(window, routeList, colour)

    def mapCoords(self, point: Point) -> tuple[int, int]:
        newX = mapAxis(point.x, self.width, self.x, self.oldXRange, self.oldXMin)
        newY = mapAxis(point.y, self.height, self.y, self.oldYRange, self.oldYMin)

        return newX, newY

    def drawPoints(self, window) -> None:
        for point in self.points:
            newX, newY = self.mapCoords(point)
            pg.draw.circle(window, [0, 0, 255], (newX, newY), 5, 10)
