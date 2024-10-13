from skyscraper_solver.skyscraperlib import INPUT_LABELS, City
from skyscraper_solver.skyscraperlib import Orientation as Grid


def permutate(blocks, stack: list, result: list):
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
    input_size = int(input("City size? "))

    city = City(input_size)

    for orientation in Grid:
        for position in range(input_size):
            input_look = []
            for label in INPUT_LABELS[orientation.value]:
                value = int(input(f"{orientation.name} {position} {label} value? "))
                input_look.append(value)
            city.setlook(orientation, position, tuple(input_look))

    progress = True
    while progress:
        initial_weight = city.weight()
        print(f"start round (weight: {initial_weight})")
        for orientation in Grid:
            for position in range(input_size):
                line = [set() for _ in range(input_size)]
                for check in permutate(city.get(orientation, position), [], []):
                    if view(check) == city.getlook(orientation, position):
                        for block, tower in zip(line, check):
                            block.add(tower)
                        print(check, view(check), orientation.name, position)
                city.put(orientation, position, line)
                line.clear()
        city.sieve()
        progress = city.weight() < initial_weight
        city.print()
        if city.weight() == (input_size * input_size):
            break
    return True


if __name__ == "__main__":
    main()
