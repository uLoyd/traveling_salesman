from Point import Point
from Route import Route
from Path import Path
from random import randint
from utils import *


# simply adds fitness member
class PathFitness:
    def __init__(self, path: Path):
        self.path = path
        self.fitness = float('inf')

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __str__(self):
        return f"{self.path}, fitness: {self.fitness}"

    def copy(self):
        return PathFitness(self.path.copy())


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
    def __init__(self, fitness, generator = populationGenerator):
        self.generator = generator
        self.fitness = fitness
        self.population: list[PathFitness] = list()

    def evaluate(self):
        for sample in self.population:
            sample.fitness = self.fitness(sample.path)

        return self

    def populate(self, *args):
        self.population = mapList(self.generator(*args), lambda path: PathFitness(path))
        return self

    def sort(self, **kwargs):
        self.population.sort(**kwargs)
        return self
