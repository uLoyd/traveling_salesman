def filteredList(someList: list, predicate) -> list:
    return list(filter(lambda x: predicate(x), someList))


def count(someList: list, predicate) -> int:
    return len(filteredList(someList, predicate))


def some(someList: list, predicate) -> bool:
    for i in range(len(someList) - 1):
        if predicate(someList[i]):
            return True

    return False


def mapList(someList: list, someFunction) -> list:
    return list(map(someFunction, someList))

