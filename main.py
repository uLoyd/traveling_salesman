import sys

from Point import Point
from Route import Route, routeGenerator
from Path import Path
from GeneticAlgorithm.Population import Population
from GeneticAlgorithm.PopulationChange import DefaultPopulationChange
import time
from GeneticAlgorithm.Crossovers import *
from utils import *
import pygame as pg
from Display.DisplayMap import DisplayMap


def fitness(path: Path):
    if findFirst(path.routes, lambda route: route.restricted):
        return float('inf')
    return 0.6 * path.length() + 0.4 * path.time()


def userInput(routes: list[Route]):
    for route in routes:
        print(route)

        restrict = str(input("Restrict path? [Y - yes or leave blank]: "))
        print(restrict)

        if restrict == "Y" or restrict == "y":
            route.restrict()
            continue

        speed = str(input("Change route speed? [float - new speed or leave blank for default value(1)]: "))
        print(speed)

        if len(speed):
            route.speed = float(speed)


def randPoint(pointList: list[Point], maxX: int, maxY: int):
    while True:
        p = Point(randint(0, maxX), randint(0, maxY))
        if p not in pointList:
            pointList.append(p)
            break


def print_hi(name):
    pg.init()
    window = pg.display.set_mode((2080, 1000))
    pg.display.set_caption("Komiwojażer genetycznie")
    run = True

    # points = []
    # for _ in range(12):
    #     randPoint(points, 2000, 2000)

    # points = [
    #     Point(100, 50),
    #     Point(125, 25),
    #     Point(150, 0),
    #     Point(175, 25),
    #     Point(300, 50),
    #     Point(300, 100),
    #     Point(300, 125),
    #     Point(300, 150),
    #     Point(150, 300),
    #     Point(125, 150),
    #     Point(100, 150),
    #     Point(100, 100),
    # ]

    points = [
        Point(0, 0),
        Point(100, 610),
        Point(215, 340),
        Point(500, 350),
        Point(500, 450),
        Point(300, 500),
        Point(600, 600),
        Point(700, 700),
        Point(1500, 240),
        Point(512, 640),
        Point(10, 278),
        Point(500, 1500),
        Point(760, 10),
        Point(1500, 2400),
        Point(52, 640),
        Point(106, 1078),
        Point(521, 1001),
        Point(860, 10),
        Point(800, 2400),
        Point(82, 640),
        Point(806, 1078),
        Point(821, 1001),
    ]

    restrictedRoutes = [
        Route(points[0], points[2]),
        Route(points[6], points[5]),
        Route(points[7], points[8]),
        Route(points[1], points[12]),
        Route(points[7], points[16]),
        Route(points[20], points[21]),
        Route(points[3], points[10])
    ]

    displayMap = DisplayMap(points, 1000, 950, 10, 10)

    pathMap = Path(routeGenerator(points))

    for route in restrictedRoutes:
        pathMap.getRouteRef(route.p1, route.p2).restrict()

    pop = Population(fitness)
    pop.populate(points, pathMap, 500).evaluate().sort(reverse=False)

    crossovers = [
            KPointCrossoverWithCorrection(12),
            KPointCrossoverWithCorrection(7),
            KPointCrossoverWithCorrection(5),
            KPointCrossoverWithCorrection(3),
            UniformCrossoverWithCorrection(0.7),
            UniformCrossoverWithCorrection(0.5),
            UniformCrossoverWithCorrection(0.3),
        ]

    crossovers.reverse()

    popChange = DefaultPopulationChange(
        crossovers,
        set(points),
        10,
        0.5)

    bestOfAll = pop.population[0]
    lastBest = pop.population[0]

    displayMap.drawRestrictedRoutes(window, restrictedRoutes)
    displayMap.drawRoutes(window, bestOfAll.routes, [0, 255, 50])

    displayMap.drawPoints(window)
    pg.display.update()

    iterations = 0
    while run:
        pop.population = popChange.perform(pop.population, pathMap)
        pop.evaluate().sort(reverse=False)

        newBest = pop.population[0]

        if bestOfAll.fitness > newBest.fitness:
            lastBest = bestOfAll.copy()

            bestOfAll = newBest.copy()
            bestOfAll.fitness = fitness(bestOfAll)
            print('\nnew best: ' + str(fitness(bestOfAll)) + '\n')

            window.fill([0, 0, 0])

            displayMap.drawRestrictedRoutes(window, restrictedRoutes)
            displayMap.drawRoutes(window, lastBest.routes, [50, 50, 0])
            displayMap.drawRoutes(window, bestOfAll.routes, [0, 255, 50])

            displayMap.drawPoints(window)
            pg.display.update()
        else:
            sys.stdout.write("\r# " + str(bestOfAll.fitness) + " it: " + str(iterations))

        iterations += 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()


if __name__ == '__main__':
    print_hi('PyCharm')
