from __future__ import annotations

from enum import Enum, auto
from pathlib import Path

cwd = Path(__file__).parent

class Cell(Enum):
    blank = auto()
    obstruct = auto()

Position = tuple[tuple[int, int], tuple[int, int]]

def main():
    data = Path.read_text(cwd / "input.txt")
    visited: set[Position] = set()
    matrix: list[list[Cell]] = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    def nextDir(pos: tuple[int, int]) -> tuple[int, int]:
        return directions[(directions.index(pos) + 1) % len(directions)]
    chDirs = ">v<^"
    def mapper(ch: str) -> Cell:
        if ch == "#":
            return Cell.obstruct
        return Cell.blank
    pos = None
    for r, dataRow in enumerate(data.splitlines()):
        row: list[Cell] = []
        for c, ch in enumerate(dataRow.strip()):
            cell = mapper(ch)
            row.append(cell)
            if ch in chDirs:
                pos = ((r, c), directions[chDirs.index(ch)])
        matrix.append(row)
    if pos is None:
        raise ValueError("Starting position not given")
    nr, nc = len(matrix), len(matrix[0])
    res: set[tuple[int, int]] = set()
    def printMat(pos: Position) -> None:
        (r, c), (dr, dc) = pos
        ch = chDirs[directions.index((dr, dc))]
        for i, row in enumerate(matrix):
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

    while pos not in visited:
        (r, c), (dr, dc) = pos
        if not all([0 <= r < nr, 0 <= c < nc]):
            break
        visited.add(pos)
        res.add((r, c))
        # printMat(pos)
        r2, c2 = (r+dr, c+dc)
        try:
            if matrix[r2][c2] == Cell.obstruct:
                pos = (r, c), nextDir((dr, dc))
            else:
                pos = ((r2, c2), (dr, dc))
        except:
            pass
    print(len(res))

if __name__ == "__main__":
    main()
