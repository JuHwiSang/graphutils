from mpl_toolkits.mplot3d import Axes3D
from typing import Callable
from abc import ABCMeta
import matplotlib.patheffects as pe

from graphutils.points import Points
from graphutils.types import NumberSetLiteral
from graphutils.config import DEFAULT_GRID_COLOR, DEFAULT_SURFACE_GRID_COLOR, DEFAULT_DETAILED, DEFAULT_NUMBER_SET, DEFAULT_SCALE, DEFAULT_ALPHA
from .base import Graph3d
from .surface import Graph3dSurface
from .plot import Graph3dPlot
import numpy as np


_retarder_map: dict[NumberSetLiteral, Callable[[np.ndarray], np.ndarray]] = {
    "real": lambda y:np.arctan(y)*2,
    "positive": lambda y:np.arctan(np.log(y)) * 2
}

class Graph3dWheelCylinder(Graph3d, metaclass=ABCMeta):
    number_set: NumberSetLiteral

    def __init__(self, points: Points, number_set: NumberSetLiteral = "real") -> None:
        self.number_set = number_set
        super().__init__(points)

    def _retard_by_set(self, y: np.ndarray) -> np.ndarray:
        return _retarder_map[self.number_set](y)


class Graph3dWheelCylinderPlot(Graph3dWheelCylinder):
    def draw(self, ax: Axes3D) -> None:
        x, y = self.points
        retarded = self._retard_by_set(y)
        new_y = -np.cos(retarded)  # to reverse y
        new_z = np.sin(retarded)
        ax.plot(x, new_y, new_z)

class Graph3dWheelCylinderScatter(Graph3dWheelCylinder):
    def draw(self, ax: Axes3D) -> None:
        x, y = self.points
        retarded = self._retard_by_set(y)
        new_y = -np.cos(retarded)  # to reverse y
        new_z = np.sin(retarded)
        ax.scatter(x, new_y, new_z)



set2labels: dict[NumberSetLiteral, list[str]] = {
    "real": ['∞', '-1', '0', '1'],
    "positive": ['0 | ∞', 'e^-1', '1', 'e']
}
def _set2labels(number_set: NumberSetLiteral) -> list[str]:
    return set2labels[number_set]

class Graph3dWheelCylinderGrid(Graph3d):
    scale: float
    xlim: tuple[float, float]
    number_set: NumberSetLiteral

    def __init__(self,
                 xlim: tuple[float, float],
                 scale: float = DEFAULT_SCALE,
                 detailed: int = DEFAULT_DETAILED,
                 grid_color: str = DEFAULT_GRID_COLOR,
                 surface_color: str = DEFAULT_SURFACE_GRID_COLOR,
                 alpha: float = DEFAULT_ALPHA,
                 number_set: NumberSetLiteral = DEFAULT_NUMBER_SET) -> None:
        super().__init__()
        self.xlim = xlim
        self.scale = scale
        self.number_set = number_set

        arr = np.linspace(0, np.pi*2, detailed)
        circle_y = np.cos(arr) * scale
        circle_z = np.sin(arr) * scale
        self.extend_subgraph([
            Graph3dSurface(self.__get_cylinder_surface(xlim, scale, detailed), surface_color, alpha),
            Graph3dPlot(Points.fromiter([xlim[0], xlim[1]], [1, 1], [0, 0]), grid_color, alpha),
            Graph3dPlot(Points.fromiter([xlim[0], xlim[1]], [-1, -1], [0, 0]), grid_color, alpha),
            Graph3dPlot(Points.fromiter([xlim[0], xlim[1]], [0, 0], [1, 1]), grid_color, alpha),
            Graph3dPlot(Points.fromiter([xlim[0], xlim[1]], [0, 0], [-1, -1]), grid_color, alpha),
            Graph3dPlot(Points.fromiter(np.full(detailed, xlim[0]), circle_y, circle_z), grid_color, alpha),
            Graph3dPlot(Points.fromiter(np.full(detailed, xlim[1]), circle_y, circle_z), grid_color, alpha),
        ])


    @staticmethod
    def __get_cylinder_surface(xlim: tuple[float, float], scale: float = DEFAULT_SCALE, detailed: float = DEFAULT_DETAILED) -> Points:
        x = np.linspace(xlim[0], xlim[1], detailed)
        y = np.linspace(-np.pi, np.pi, detailed)
        x, y = np.meshgrid(x, y)
        z = np.sin(y) * scale
        y = np.cos(y) * scale
        return Points.fromiter(x, y, z)

    def draw(self, ax: Axes3D) -> None:
        self.draw_subgraphs(ax)
        labels = _set2labels(self.number_set)
        # to reverse y, labels 2 and 0 is changed.
        ax.text(self.xlim[0], (-1-0.2)*self.scale, 0, labels[2], color='white', fontsize=12, path_effects=[pe.withStroke(linewidth=2, foreground="black")])
        ax.text(self.xlim[0], 0, (-1-0.2)*self.scale, labels[1], color='white', fontsize=12, path_effects=[pe.withStroke(linewidth=2, foreground="black")])
        ax.text(self.xlim[0], (1+0.2)*self.scale, 0, labels[0], color='white', fontsize=12, path_effects=[pe.withStroke(linewidth=2, foreground="black")])
        ax.text(self.xlim[0], 0, (1+0.2)*self.scale, labels[3], color='white', fontsize=12, path_effects=[pe.withStroke(linewidth=2, foreground="black")])