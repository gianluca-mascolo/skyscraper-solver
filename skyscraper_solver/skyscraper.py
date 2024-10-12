def recurse(bags, stack=[], result=[]):
    if bags:
        for ball in bags[0]:
            if ball not in stack:
                stack.append(ball)
                recurse(bags[1:], stack, result)
        if stack:
            stack.pop()
    else:
        result.append(tuple(stack))
        stack.pop()
        return []
    return result


def view(sky):
    left_count = 1
    for index, edge in enumerate(sky[1:], 1):
        if all(map(lambda cur: cur < edge, sky[:index])):
            left_count += 1
    right_count = 1
    for index, edge in enumerate(sky[:-1], 1):
        if all(map(lambda cur: cur < edge, sky[index:])):
            right_count += 1
    return (left_count, right_count)


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
    r = recurse(city.get("col", 0))
    for k in r:
        if view(k) == (3, 1):
            for s, r in zip(soluzione, k):
                s.add(r)
            print(k, view(k))
    print(soluzione)
    city.put("col", 0, soluzione)
    print(city.get("col", 0))
    return True


if __name__ == "__main__":
    main()
