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
