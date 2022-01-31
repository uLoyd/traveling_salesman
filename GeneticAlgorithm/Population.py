from __future__ import annotations
from Point import Point
from Path import Path
from random import randint


def populationGenerator(points: list[Point], pathMap: Path, populationSize: int = 100) -> list[Path]:
    pointsSize = len(points)
    population = list()

    for _ in range(populationSize):
        available = list(range(pointsSize))
        newPathPoints = list()

        while len(available) != 0:
            pointId = randint(0, len(available) - 1)
            newPathPoints.append(points[available[pointId]])
            del available[pointId]

        routes = list()

        for index in range(len(newPathPoints) - 1):
            routes.append(pathMap.getRoute(newPathPoints[index], newPathPoints[index + 1]))

        population.append(Path(routes))

    return population


class Population:
    def __init__(self, fitness, generator=populationGenerator):
        self.generator = generator
        self.fitness = fitness
        self.population: list[Path] = list()

    def evaluate(self) -> Population:
        for sample in self.population:
            sample.fitness = self.fitness(sample)

        return self

    def populate(self, *args) -> Population:
        self.population = self.generator(*args)
        return self

    def sort(self, **kwargs) -> Population:
        self.population.sort(**kwargs)
        return self
