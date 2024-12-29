from __future__ import annotations

import itertools
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

import attrs
import cattrs

cwd = Path(__file__).parent

Node = int

@attrs.define(frozen=True)
class Rule:
    first: Node
    second: Node

class Graph:
    def __init__(self) -> None:
        self.nodes: set[Node] = set()
        self.edges: dict[Node, list[Node]] = defaultdict(list)

    def addEdge(self, edge: Rule):
        if edge.second in self.edges[edge.first]:
            return
        self.edges[edge.first].append(edge.second)
        self.nodes.add(edge.first)
        self.nodes.add(edge.second)

    def topoSort(self, rules: list[Node]):
        _rules = set(rules)
        inDegree: dict[Node, int] = defaultdict(int)
        for u in self.nodes:
            if u not in _rules:
                continue
            inDegree[u] += 0
            for v in self.edges[u]:
                if v not in _rules:
                    continue
                inDegree[v] += 1

        q: deque[Node] = deque([u for u in _rules if inDegree[u] == 0])
        topo: list[Node] = []
        while q:
            u = q.pop()
            topo.append(u)
            for v in self.edges[u]:
                if v not in _rules:
                    continue
                inDegree[v] -= 1
                if inDegree[v] == 0:
                    q.append(v)

        return topo

    def getFixedOrder(self, rules: list[Node]):
        topo = self.topoSort(rules)
        print(topo)
        return topo


converter = cattrs.Converter()
@converter.register_structure_hook
def parseRule(data: str, _: Any) -> Rule:
    items = data.rstrip("\n").split("|")
    if len(items) != 2:  # noqa: PLR2004
        raise ValueError(f"{data} does not match pattern <num1>|<num2>")
    return Rule(int(items[0]), int(items[1]))

def isValidUpdate(graph: Graph, update: list[int]):
    combos = itertools.combinations(update, 2)
    return all(n1 not in graph.edges[n2] for n1, n2 in combos)

def main():
    sum1, sum2 = 0, 0
    with Path.open(cwd / "input.txt") as fp:
        graph = Graph()
        while True:
            data = fp.readline().strip()
            if not data:
                break
            rule = converter.structure(data, Rule)
            graph.addEdge(rule)

        while True:
            data = fp.readline().strip()
            if not data:
                break
            update = list(map(int, data.strip().split(",")))
            if isValidUpdate(graph, update):
                sum1 += update[len(update) // 2]
            else:
                updateNew = graph.getFixedOrder(update)
                sum2 += updateNew[len(updateNew) // 2]

        print(sum1)
        print(sum2)


if __name__ == "__main__":
    main()
