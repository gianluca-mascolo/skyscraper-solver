from skyscraper_solver.skyscraperlib import City
from skyscraper_solver.skyscraperlib import Orientation as Grid


def permutate(blocks, stack=[], result=[]):
    if blocks:
        for tower in blocks[0]:
            if tower not in stack:
                stack.append(tower)
                permutate(blocks[1:], stack, result)
        if stack:
            stack.pop()
    else:
        result.append(tuple(stack))
        if stack:
            stack.pop()
        return []
    return result


def view(sky):
    left_towers = 1
    for index, observer_position in enumerate(sky[1:], 1):
        if all(map(lambda left_horizon: observer_position > left_horizon, sky[:index])):
            left_towers += 1
    right_towers = 1
    for index, observer_position in enumerate(sky[:-1], 1):
        if all(map(lambda right_horizon: observer_position > right_horizon, sky[index:])):
            right_towers += 1
    return (left_towers, right_towers)


def main():
    city = City(4)
    print(city.get(Grid.COLUMN, 0))
    soluzione = [set() for _ in range(4)]
    print(soluzione)
    r = permutate(city.get(Grid.COLUMN, 0))
    for k in r:
        if view(k) == (1, 3):
            for s, r in zip(soluzione, k):
                s.add(r)
            print(k, view(k))
    print(soluzione)
    city.put(Grid.COLUMN, 0, soluzione)
    print(city.get(Grid.COLUMN, 0))
    return True


if __name__ == "__main__":
    main()
