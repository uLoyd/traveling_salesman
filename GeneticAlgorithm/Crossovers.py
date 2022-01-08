import math
from Path import Path
from Point import Point
from random import randint, uniform, choice
from utils import *


def swapPoints(points: list[Point], val1: Point, val2: Point):
    ind1 = points.index(val1)
    ind2 = points.index(val2)
    points[ind1], points[ind2] = points[ind2], points[ind1]


def pointListCorrections(points: list[Point], allPoints: set[Point]) -> list[Point]:
    newPoints = list()
    checkPoints = set()
    notUsedPoints = allPoints.difference(set(points.copy()))

    if not notUsedPoints:
        return points

    for point in points:
        l1 = len(checkPoints)
        checkPoints.add(point)
        l2 = len(checkPoints)

        if l1 == l2:
            randomNotUsedPoint = choice(tuple(notUsedPoints)).copy()
            newPoints.append(randomNotUsedPoint)
            notUsedPoints.remove(randomNotUsedPoint)
        else:
            newPoints.append(point.copy())

    return newPoints


class ICrossover:
    def cross(self, pathMap: Path, path1: Path, path2: Path, allPoints: set[Point]):
        raise Exception("Abstract")


class UniformCrossoverWithCorrection(ICrossover):
    def __init__(self, probability: float):
        self.probability = probability

    def cross(self, pathMap: Path, path1: Path, path2: Path, allPoints: set[Point]):
        pl1 = path1.pointList()
        pl2 = path2.pointList()
        length = len(pl1)

        for i in range(length - 1):
            if uniform(0, 1) <= self.probability:
                o1 = pl1[i].copy()
                o2 = pl2[i].copy()
                pl1[i] = o2
                pl2[i] = o1

        path1.reconstructRoutes(pathMap, pointListCorrections(pl1, allPoints))
        path2.reconstructRoutes(pathMap, pointListCorrections(pl2, allPoints))


class KPointCrossoverWithCorrection(ICrossover):
    def __init__(self, k: int = 1):
        self.k = k

    def cross(self, pathMap: Path, path1: Path, path2: Path, allPoints: set[Point]):
        pl1 = path1.pointList()
        pl2 = path2.pointList()
        length = len(pl1)

        # if length <= self.k - 1:
        #    raise Exception(f"{self.k}-point crossover can't be performed on {length}-element point list")

        change = True
        step = math.floor(length / self.k)
        stepCount = 0
        iterRange = range(length - 1)
        for i in iterRange:
            if stepCount % step == 0:
                change = not change

            o1 = pl1[i].copy()
            o2 = pl2[i].copy()

            if change:
                pl1[i] = o2
            if not change:
                pl2[i] = o1

        path1.reconstructRoutes(pathMap, pointListCorrections(pl1, allPoints))
        path2.reconstructRoutes(pathMap, pointListCorrections(pl2, allPoints))

# class UniformCrossover(ICrossover):
#     def __init__(self, probability: float):
#         self.probability = probability
#
#     def cross(self, pathMap: Path, path1: Path, path2: Path):
#         pl1 = path1.pointList()
#         pl2 = path2.pointList()
#         length = len(pl1)
#
#         for i in range(length - 1):
#             if uniform(0, 1) <= self.probability:
#                 o1 = pl1[i].copy()
#                 o2 = pl2[i].copy()
#                 swapPoints(pl1, o1, o2)
#                 swapPoints(pl2, o1, o2)
#
#         path1.reconstructRoutes(pathMap, pl1)
#         path2.reconstructRoutes(pathMap, pl2)
#
#
# class KPointCrossover(ICrossover):
#     def __init__(self, k: int = 1):
#         self.k = k
#
#     def cross(self, pathMap: Path, path1: Path, path2: Path):
#         pl1 = path1.pointList()
#         pl2 = path2.pointList()
#         length = len(pl1)
#
#         if length <= self.k - 2:
#             raise Exception(f"{self.k}-point crossover can't be performed on {length}-element point list")
#
#         initial = 0
#         for i in range(self.k):
#             furthestPoint = length - self.k + i
#             crossStartPoint = randint(initial, furthestPoint - 1)
#             crossEndPoint = (randint(crossStartPoint, furthestPoint), length - 1)[i == length - 1]
#
#             for j in range(crossStartPoint, crossEndPoint):
#                 swapPoints(pl1, pl1[j], pl2[j])
#                 swapPoints(pl2, pl1[j], pl2[j])
#
#             initial = crossEndPoint
#
#         path1.reconstructRoutes(pathMap, pl1)
#         path2.reconstructRoutes(pathMap, pl2)
