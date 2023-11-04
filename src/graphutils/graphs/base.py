from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Optional
from matplotlib.axes import Axes

from graphutils.points import Points


class Graph(metaclass=ABCMeta):

    _points: Points
    subgraphs: list[Graph]

    def __init__(self, _points: Optional[Points] = None) -> None:
        self._points = Points() if _points is None else _points
        self.subgraphs = []

    @abstractmethod
    def draw(self, ax: Axes) -> None: ...

    def draw_subgraphs(self, ax: Axes) -> None:
        for subgraph in self.subgraphs:
            subgraph.draw(ax)

    def add_subgraph(self, subgraph: Graph) -> None:
        if not self.subgraphs: self.subgraphs = []
        self.subgraphs.append(subgraph)

    def extend_subgraph(self, subgraphs: list[Graph]) -> None:
        if not self.subgraphs: self.subgraphs = []
        self.subgraphs.extend(subgraphs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(array({self.points.numpy().tolist()}))"
    
    @property
    def points(self) -> Points:
        return Points.concat(self._points, *(subgraph.points for subgraph in self.subgraphs))