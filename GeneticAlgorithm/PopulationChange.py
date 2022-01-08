import math

from GeneticAlgorithm.Crossovers import ICrossover
from GeneticAlgorithm.Population import PathFitness
from Path import Path
from Point import Point
from random import randint, uniform


class IPopulationChange:
    def cross(self, population: list[PathFitness], pathMap: Path):
        raise Exception("Abstract")

    def mutate(self, population: list[PathFitness], pathMap: Path):
        raise Exception("Abstract")

    def perform(self, population: list[PathFitness], pathMap: Path):
        raise Exception("Abstract")


def handlePath(pathFitness, length, pathMap):
    available = list(range(length))
    ind1 = available[randint(0, len(available) - 1)]
    del available[ind1]
    ind2 = available[randint(0, len(available) - 1)]
    pointList = pathFitness.pointList()
    pointList[ind1], pointList[ind2] = pointList[ind2], pointList[ind1]
    pathFitness.reconstructRoutes(pathMap, pointList)


class DefaultPopulationChange(IPopulationChange):
    def __init__(self, crossovers: list[ICrossover], allPoints: set[Point], bestThreshold: int = 10, mutationChance: float = 0.2):
        self.crossovers = crossovers
        self.bestThreshold = bestThreshold
        self.mutationChance = mutationChance
        self.allPoints = allPoints

    def cross(self, population: list[PathFitness], pathMap: Path):
        length = len(population) - 1
        step = round((length + 2) / len(self.crossovers))

        for i in range(0, length, 2):
            self.crossovers[math.floor(i / step)].cross(pathMap, population[i], population[i + 1], self.allPoints)

    def mutate(self, population: list[PathFitness], pathMap: Path):
        length = len(population[0].pointList()) - 1
        quarterLength = round(length / 4)

        for pathFitness in population:
            if uniform(0, 1) <= self.mutationChance:
                mutationAmount = randint(1, quarterLength)

                for _ in range(mutationAmount):
                    handlePath(pathFitness, length, pathMap)

    def perform(self, population: list[PathFitness], pathMap: Path):
        goodEnoughRoutesLength = len(population) - self.bestThreshold
        newPopulation = list()

        for i in range(self.bestThreshold):
            newPopulation.append(population[i].copy())

        self.cross(population[:goodEnoughRoutesLength], pathMap)
        self.mutate(population[:goodEnoughRoutesLength], pathMap)

        newPopulation.extend(population[:goodEnoughRoutesLength])
        return newPopulation
