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
    input_size = 4
    city = City(input_size)

    city.setlook(Grid.COLUMN, 0, (2,2))
    city.setlook(Grid.COLUMN, 1, (2,2))
    city.setlook(Grid.COLUMN, 2, (4,1))
    city.setlook(Grid.COLUMN, 3, (1,4))

    city.setlook(Grid.ROW, 0, (2,1))
    city.setlook(Grid.ROW, 1, (1,2))
    city.setlook(Grid.ROW, 2, (2,3))
    city.setlook(Grid.ROW, 3, (3,2))

    progress = True
    while progress:
        initial_weight = city.weight()
        print(f"start round (weight: {initial_weight})")
        for orientation in Grid:
            for position in range(input_size):
                line = [set() for _ in range(input_size)]
                for check in permutate(city.get(orientation, position)):
                    if view(check) == city.getlook(orientation, position):
                        for block, tower in zip(line, check):
                            block.add(tower)
                        print(check, view(check), orientation.name, position)
                city.put(orientation, position, line)
                line.clear()
        city.sieve()
        progress = city.weight() < initial_weight
        city.print()
    print("XXXXXXXXXXX")
    print(city.get(Grid.ROW, 0))
    for i,p in enumerate(permutate(city.get(Grid.ROW, 0))):
        print(i,p)
    return True


if __name__ == "__main__":
    main()
