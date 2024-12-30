from __future__ import annotations

from pathlib import Path

cwd = Path(__file__).parent

def isPossible(arr: list[int], idx: int, agg: int, target: int) -> bool:
    if idx == len(arr):
        return agg == target
    return (
        isPossible(arr, idx+1, agg+arr[idx], target) or
        isPossible(arr, idx+1, agg*arr[idx], target) or
        isPossible(arr, idx+1, int(str(agg) + str(arr[idx])), target) # Part 2
    )

def main():
    lines = Path.read_text(cwd / "input.txt").splitlines()
    res = 0
    for line in lines:
        arr = line.split(":")
        target = int(arr[0])
        nums = list(map(int, arr[1].strip().split()))
        if len(nums) == 1:
            if target == nums[0]:
                res += target
            continue
        if isPossible(nums, 1, nums[0], target):
            # print(target)
            res += target
    print(res)


if __name__ == "__main__":
    main()
