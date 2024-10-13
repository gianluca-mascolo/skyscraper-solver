from enum import Enum

MINIMUM_SIZE = 2


class Orientation(Enum):
    ROW = "row"
    COLUMN = "col"


INPUT_LABELS = {Orientation.COLUMN.value: ["top", "bottom"], Orientation.ROW.value: ["left", "right"]}


class Block:
    def __init__(self, max_height: int):
        if max_height < MINIMUM_SIZE:
            raise ValueError(f"invalid max height {max_height}")
        self.tower = set(range(1, max_height + 1))
        self.row = 0
        self.col = 0
        self.max_height = max_height

    def update(self, towers):
        if not all(t > 0 and t <= self.max_height for t in towers):
            raise ValueError(f"towers out of range 1-{self.max_height}")
        self.tower = towers


class City:
    def __init__(self, size):
        if size < MINIMUM_SIZE:
            raise ValueError(f"city of size {size} is too small! Minimum size is {MINIMUM_SIZE}.")
        self.size = size
        self.blocks = []
        for idx in range(size * size):
            self.blocks.append(Block(size))
            self.blocks[idx].row = idx // size
            self.blocks[idx].col = idx % size
        self.look = {Orientation.COLUMN.value: [tuple() for _ in range(size)], Orientation.ROW.value: [tuple() for _ in range(size)]}

    def get(self, orientation: Orientation, position):
        if position >= self.size:
            raise ValueError(f"{orientation.name} {position} out of range 0-{self.size-1}")
        return tuple(block.tower for block in self.blocks if getattr(block, orientation.value) == position)

    def put(self, orientation: Orientation, position, line):
        if position >= self.size:
            raise ValueError(f"{orientation.name} {position} out of range 0-{self.size-1}")
        if len(line) != self.size:
            raise ValueError(f"invalid line {line}")
        destination_blocks = [block for block in self.blocks if getattr(block, orientation.value) == position]
        for block, towers in zip(destination_blocks, line):
            block.update(towers)

    def setlook(self, orientation: Orientation, position, limit: tuple):
        self.look[orientation.value][position] = limit

    def getlook(self, orientation: Orientation, position):
        return self.look[orientation.value][position]

    def print(self):
        for i in range(self.size):
            print("|".join(str(list(x)[0]) if len(x) == 1 else "?" for x in self.get(Orientation.ROW, i)))

    def weight(self):
        return sum([len(block.tower) for block in self.blocks])

    def sieve(self):
        for orientation in Orientation:
            for position in range(self.size):
                line = list(self.get(orientation, position))
                unique_values = set()
                for u in filter(lambda block: len(block) == 1, line):
                    unique_values.add(list(u)[0])
                for block in line:
                    if len(block) > 1:
                        for element in unique_values:
                            block.discard(element)
                self.put(orientation, position, line)
