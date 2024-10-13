from enum import Enum

MINIMUM_SIZE = 2


class Orientation(Enum):
    ROW = "row"
    COLUMN = "col"


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

    def get(self, orientation: Orientation, number):
        if number >= self.size:
            raise ValueError(f"{number} out of range 0-{self.size-1}")
        return tuple(block.tower for block in self.blocks if getattr(block, orientation.value) == number)

    def put(self, orientation: Orientation, number, content):
        if number >= self.size:
            raise ValueError(f"{number} out of range 0-{self.size-1}")
        selezione = [block for block in self.blocks if getattr(block, orientation.value) == number]
        for s, r in zip(selezione, content):
            s.update(r)
