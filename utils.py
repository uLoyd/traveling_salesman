def filteredList(someList: list, predicate) -> list:
    return list(filter(lambda x: predicate(x), someList))


def count(someList: list, predicate) -> int:
    return len(filteredList(someList, predicate))


def findFirst(someList: list, predicate):
    output = filteredList(someList, predicate)

    if len(output) == 0:
        return False

    else:
        return output[0]


def some(someList: list, predicate) -> bool:
    for i in range(len(someList) - 1):
        if predicate(someList[i]):
            return True

    return False


def findFirstIndex(someList: list, predicate) -> int:
    for i in range(len(someList) - 1):
        if predicate(someList[i]):
            return i

    return -1


def mapList(someList: list, someFunction) -> list:
    return list(map(someFunction, someList))

