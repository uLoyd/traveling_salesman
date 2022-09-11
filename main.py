import sys
from time import time

from ConfigReader import ConfigReader
from Display.TextFields import *
from Route import Route, routeGenerator
from GeneticAlgorithm.Population import Population
from GeneticAlgorithm.PopulationChange import DefaultPopulationChange
from GeneticAlgorithm.Crossovers import *
from utils import *
import pygame as pg
from Display.DisplayMap import DisplayMap


defaultPoints = [
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


def fitness(path: Path):
    for route in path.routes:
        if route.restricted:
            return float('inf')
    return 0.6 * path.length() + 0.4 * path.time()


def assignRouteSpeed(defined: list[Route], target: Path):
    for route in target.routes:
        routeRef = target.getRouteRef(route.p1, route.p2)
        routeAlt = Route(route.p2, route.p1)

        if route in defined:
            routeRef.speed = defined[defined.index(route)].speed
        if routeAlt in defined:
            routeRef.speed = defined[defined.index(routeAlt)].speed


def refreshTextFields(window):
    BestCurrentDisplayTitle.create(window)
    BestCurrentDisplay.create(window)
    BestCurrentTimeTitle.create(window)
    BestCurrentTime.create(window)
    BestCurrentLengthTitle.create(window)
    BestCurrentLength.create(window)
    BestLastDisplayTitle.create(window)
    BestLastDisplay.create(window)
    AverageTimeTitle.create(window)
    AverageTime.create(window)


def setup():
    configReader = ConfigReader('./UserFiles/Map/map.json', './UserFiles/PopulationData/lastPopulation.json')

    mapPoints: list[Point] = list()
    definedRoutes: list[Route] = list()

    if configReader.mapPath.exists(recursive=False):
        mapPoints, definedRoutes = configReader.getMap()
    else:
        mapPoints = defaultPoints.copy()

    pathMap = Path(routeGenerator(mapPoints))
    assignRouteSpeed(definedRoutes, pathMap)

    restrictedRoutes = list(filter(lambda route: route.restricted, definedRoutes))
    [pathMap.getRouteRef(route.p1, route.p2).restrict() for route in restrictedRoutes]

    pop = Population(fitness)

    if configReader.populationPath.exists():
        pop.population = configReader.getPopulation()
    else:
        pop.populate(mapPoints, pathMap, 500).evaluate().sort(reverse=False)

    crossovers = [
        UniformCrossoverWithCorrection(0.3),
        UniformCrossoverWithCorrection(0.5),
        UniformCrossoverWithCorrection(0.7),
        KPointCrossoverWithCorrection(3),
        KPointCrossoverWithCorrection(5),
        KPointCrossoverWithCorrection(7),
        KPointCrossoverWithCorrection(12),
    ]

    popChange = DefaultPopulationChange(crossovers, set(mapPoints), 10, 0.5)

    pop.evaluate().sort(reverse=False)
    bestOfAll = pop.population[0]
    lastBest = pop.population[1]

    pg.init()
    window = pg.display.set_mode((1080, 800))
    pg.display.set_caption("Komiwojażer genetycznie")

    refreshTextFields(window)

    displayMap = DisplayMap(mapPoints, 700, 700, 10, 10)
    displayMap.drawRestrictedRoutes(window, restrictedRoutes)
    displayMap.drawRoutes(window, bestOfAll.routes, [0, 255, 50])

    displayMap.drawPoints(window)
    pg.display.update()

    iterations = 0
    calculation_time_total = 0
    run = True

    def new_frame():
        window.fill([0, 0, 0])
        AverageTime.setText("{:.6f}".format(calculation_time_total / (iterations)))
        displayMap.drawRestrictedRoutes(window, restrictedRoutes)
        displayMap.drawRoutes(window, lastBest.routes, [50, 50, 0])
        displayMap.drawRoutes(window, bestOfAll.routes, [0, 255, 50])

        displayMap.drawPoints(window)
        refreshTextFields(window)
        pg.display.update()


    while run:
        calculation_time_start = time()

        pop.population = popChange.perform(pop.population, pathMap)
        pop.evaluate().sort(reverse=False)

        newBest = pop.population[0]

        calculation_time_total += time() - calculation_time_start

        if bestOfAll.fitness > newBest.fitness:
            lastBest = bestOfAll.copy()

            bestOfAll = newBest.copy()
            bestOfAll.fitness = fitness(bestOfAll)
            print('\nnew best: ' + str(fitness(bestOfAll)) + '\n')

            BestCurrentDisplay.setText("{:.2f}".format(bestOfAll.fitness))
            BestLastDisplay.setText(str(iterations))
            BestCurrentTime.setText("{:.2f}".format(bestOfAll.time()))
            BestCurrentLength.setText("{:.2f}".format(bestOfAll.length()))

        else:
            sys.stdout.write("\r# " + str(bestOfAll.fitness) + " it: " + str(iterations))

        iterations += 1
        new_frame()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                configReader.writePopulation(pop)
                pg.quit()


if __name__ == '__main__':
    setup()
