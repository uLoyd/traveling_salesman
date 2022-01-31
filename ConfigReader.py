import glob
import json
from GeneticAlgorithm.Population import Population
from Path import Path
from Point import Point
from Route import Route


def parsePoint(point):
    return Point(int(point['x']), int(point['y']))

class PathHandler:
    def __init__(self, path: str):
        self.path = path

    def get(self, **kwargs) -> list[str]:
        return glob.glob(self.path, **kwargs)

    def exists(self, **kwargs) -> bool:
        return len(self.get(**kwargs)) != 0


class ConfigReader:
    def __init__(self, mapPath: str, populationPath: str):
        self.mapPath = PathHandler(mapPath)
        self.populationPath = PathHandler(populationPath)

    def getMap(self) -> tuple[list[Point], list[Route]]:
        firstMap = json.load(open(self.mapPath.get()[0]))

        points = [Point(1, 1)] * len(firstMap['map'])
        routes = list()

        for point in firstMap['map']:
            id = int(point['id'])
            points[id] = parsePoint(point)

        for route in firstMap['definedRoutes']:
            p1 = points[int(route['point1'])]
            p2 = points[int(route['point2'])]
            speed = float(route['speed'])
            restricted = route['restricted'] == 'y'
            routes.append(Route(p1.copy(), p2.copy(), speed, restricted))

        return points, routes

    def getPopulation(self) -> list[Path]:
        savedPopulation = json.load(open(self.populationPath.get()[0], 'r'))
        paths = list()

        for obj in savedPopulation:
            pathRoutes: list[Route] = list()

            for route in obj['routes']:
                p1 = parsePoint(route['p1']).copy()
                p2 = parsePoint(route['p2']).copy()
                speed = float(route['speed'])
                restricted = route['restricted'] == "True"
                pathRoutes.append(Route(p1, p2, speed, restricted))

            parsedPath = Path(pathRoutes, float(str(obj['fitness'])))
            paths.append(parsedPath)

        return paths

    def writePopulation(self, population: Population):
        with open(self.populationPath.path, 'w') as populationDump:
            json.dump(population.population, populationDump, default=lambda x: x.__dict__, indent=4)

