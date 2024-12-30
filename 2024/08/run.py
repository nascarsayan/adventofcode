from __future__ import annotations

import itertools
from collections import defaultdict
from pathlib import Path

cwd = Path(__file__).parent

Cell = tuple[int, int]

def main():
    data = Path.read_text(cwd / "input.txt").splitlines()
    nr, nc = len(data), len(data[0])
    antennas: dict[str, list[Cell]] = defaultdict(list)
    for r, row in enumerate(data):
        for c, cell in enumerate(row):
            if cell != ".":
                antennas[cell].append((r, c))
    locs: set[Cell] = set()
    def isValid(r: int, c: int) -> bool:
        return 0 <= r < nr and 0 <= c < nc
    for posList in antennas.values():
        for (r1, c1), (r2, c2) in itertools.combinations(posList, 2):
            dr, dc = r2 - r1, c2 - c1
            # Part 1
            # r3, c3 = r2 + dr, c2 + dc
            # if isValid(r3, c3):
            #     locs.add((r3, c3))
            # r3, c3 = r1 - dr, c1 - dc
            # if isValid(r3, c3):
            #     locs.add((r3, c3))

            # Part 2
            r3, c3 = r2, c2
            while(isValid(r3, c3)):
                locs.add((r3, c3))
                r3, c3 = r3 + dr, c3 + dc
            r3, c3 = r1, c1
            while(isValid(r3, c3)):
                locs.add((r3, c3))
                r3, c3 = r3 - dr, c3 - dc

    print(len(locs))


if __name__ == "__main__":
    main()
