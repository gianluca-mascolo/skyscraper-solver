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


class Block:
    def __init__(self, size):
        self.tower = set(range(1, size + 1))
        self.row = 0
        self.col = 0

    def update(self, content):
        self.tower = content


class City:
    def __init__(self, size):
        self.size = size
        self.blocks = []
        for idx in range(size * size):
            self.blocks.append(Block(size))
            self.blocks[idx].row = idx // size
            self.blocks[idx].col = idx % size

    def get(self, kind, number):
        if number >= self.size:
            raise ValueError(f"{number} out of range 0-{self.size-1}")
        return tuple(block.tower for block in self.blocks if getattr(block, kind) == number)

    def put(self, kind, number, content):
        if number >= self.size:
            raise ValueError(f"{number} out of range 0-{self.size-1}")
        selezione = [block for block in self.blocks if getattr(block, kind) == number]
        for s, r in zip(selezione, content):
            s.update(r)


def main():
    city = City(4)
    print(city.get("col", 0))
    soluzione = [set() for _ in range(4)]
    print(soluzione)
    r = permutate(city.get("col", 0))
    for k in r:
        if view(k) == (1, 3):
            for s, r in zip(soluzione, k):
                s.add(r)
            print(k, view(k))
    print(soluzione)
    city.put("col", 0, soluzione)
    print(city.get("col", 0))
    return True


if __name__ == "__main__":
    main()
