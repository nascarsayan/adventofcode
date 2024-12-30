from __future__ import annotations

import itertools
from enum import Enum, auto
from pathlib import Path

cwd = Path(__file__).parent

class Cell(Enum):
    blank = auto()
    obstruct = auto()

Position = tuple[tuple[int, int], tuple[int, int]]

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
chDirs = ">v<^"

def nextDir(pos: tuple[int, int]) -> tuple[int, int]:
    return directions[(directions.index(pos) + 1) % len(directions)]


def mapper(ch: str) -> Cell:
    if ch == "#":
        return Cell.obstruct
    return Cell.blank


class Solution:

    def __init__(self, data: str):
        self.matrix: list[list[Cell]] = []
        initPos = None
        for r, dataRow in enumerate(data.splitlines()):
            row: list[Cell] = []
            for c, ch in enumerate(dataRow.strip()):
                cell = mapper(ch)
                row.append(cell)
                if ch in chDirs:
                    initPos = ((r, c), directions[chDirs.index(ch)])
            self.matrix.append(row)
        if initPos is None:
            raise ValueError("Starting position not given")
        self.initPos = initPos
        self.nr, self.nc = len(self.matrix), len(self.matrix[0])

    def printMat(self, pos: Position, res: set[tuple[int, int]]) -> None:
        (r, c), (dr, dc) = pos
        ch = chDirs[directions.index((dr, dc))]
        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if (r, c) == pos:
                    print(ch, end=" ")
                if (i, j) in res:
                    print("X", end=" ")
                    continue
                if cell == Cell.obstruct:
                    print("#", end=" ")
                else:
                    print(".", end=" ")
            print()
        print("\n")

    def patrol(self, initPos: Position):
        visPosAndDir: set[Position] = set()
        visPos: set[tuple[int, int]] = set()
        pos = initPos
        while True:
            if pos in visPosAndDir:
                raise ValueError
            (r, c), (dr, dc) = pos
            if not all([0 <= r < self.nr, 0 <= c < self.nc]):
                break
            visPosAndDir.add(pos)
            visPos.add((r, c))
            # self.printMat(pos)
            r2, c2 = (r+dr, c+dc)
            if (
                all([0 <= r2 < self.nr, 0 <= c2 < self.nc]) and
                self.matrix[r2][c2] == Cell.obstruct
            ):
                pos = (r, c), nextDir((dr, dc))
            else:
                pos = ((r2, c2), (dr, dc))
        return visPosAndDir, visPos

    def newObstruct(self):
        res = 0
        for r, c in itertools.product(range(self.nr), range(self.nc)):
            if self.matrix[r][c] == Cell.obstruct:
                continue
            if (r, c) == self.initPos:
                continue
            self.matrix[r][c] = Cell.obstruct
            try:
                self.patrol(self.initPos)
            except ValueError:
                print(r, c)
                res += 1
            finally:
                self.matrix[r][c] = Cell.blank
        return res


def main():
    data = Path.read_text(cwd / "input.txt")
    sol = Solution(data)
    _, visPos = sol.patrol(sol.initPos)
    print(len(visPos))
    # NOTE: answer is wrong: should be 1586 but getting 1587.
    res = sol.newObstruct()
    print(res)

if __name__ == "__main__":
    main()
