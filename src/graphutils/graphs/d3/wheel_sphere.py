from mpl_toolkits.mplot3d import Axes3D
from typing import Callable, Optional
from abc import ABCMeta
import matplotlib.patheffects as pe
import numpy as np

from graphutils.points import Points
from graphutils.types import NumberSetLiteral
from graphutils.config import DEFAULT_DETAILED, DEFAULT_SCALE, DEFAULT_ALPHA, DEFAULT_NUMBER_SET, DEFAULT_GRID_COLOR, DEFAULT_SURFACE_GRID_COLOR
from .base import Graph3d
from .plot import Graph3dPlot
from .scatter import Graph3dScatter
from .surface import Graph3dSurface



_retarder_map: dict[NumberSetLiteral, Callable[[np.ndarray], np.ndarray]] = {
    "real": lambda x:np.arctan(x),
    "positive": lambda x:np.arctan(np.log(x))
}

class Graph3dWheelSphere(Graph3d, metaclass=ABCMeta):
    number_set: NumberSetLiteral

    def __init__(self, points: Points, number_set: NumberSetLiteral = DEFAULT_NUMBER_SET) -> None:
        self.number_set = number_set
        sphere_points = self.__points_to_sphere(points)
        super().__init__(sphere_points)

    def __retard_by_set(self, x: np.ndarray) -> np.ndarray:
        return _retarder_map[self.number_set](x)
    
    def __points_to_sphere(self, points: Points) -> Points:
        x, y = points
        base = ((y**2)+(x**2))**0.5
        # tan = base / 1
        angle = -np.pi/2 + 2*self.__retard_by_set(base / 1)  # angle: '삼각형의 빗면과 원의 교점까지 이은 선분'이 이루는 동경
        print(angle)
        # angle = self.__retard_by_set(tan)
        new_z = np.sin(angle)
        # new_z = np.cos(angle)
        # print(x)
        # print(y)
        # print(tan)
        # print(angle)
        # print(new_z)
        new_w = np.cos(angle)

        ratio = new_w/base  # base : new_w = x : ?
        new_y = ratio * y
        new_x = ratio * x
        return Points.fromiter(new_x, new_y, new_z)

class Graph3dWheelSpherePlot(Graph3dWheelSphere):
    def draw(self, ax: Axes3D) -> None:
        x, y, z = self.points
        ax.plot(x, y, z)

class Graph3dWheelSphereScatter(Graph3dWheelSphere):
    def draw(self, ax: Axes3D) -> None:
        x, y, z = self.points
        ax.scatter(x, y, z)



set2labels: dict[NumberSetLiteral, list[str]] = {
    "real": ['∞', '-1', '0', '1', '-i', 'i'],
    "positive": ['0|∞', 'e^-1', '1', 'e', 'e^-i', 'e^i']
}
def _set2labels(number_set: NumberSetLiteral) -> list[str]:
    return set2labels[number_set]

class Graph3dWheelSphereGrid(Graph3d):
    number_set: NumberSetLiteral
    scale: float

    def __init__(self,
                 scale: float = DEFAULT_SCALE,
                 detailed: int = DEFAULT_DETAILED,
                 grid_color: str = DEFAULT_GRID_COLOR,
                 surface_color: str = DEFAULT_SURFACE_GRID_COLOR,
                 number_set: NumberSetLiteral = DEFAULT_NUMBER_SET,
                 alpha: float = DEFAULT_ALPHA) -> None:
        super().__init__()
        self.scale = scale
        self.number_set = number_set

        circle_x, circle_y = self.__get_circle(detailed, scale)
        zeros = np.zeros(detailed)
        self.extend_subgraph([
            Graph3dSurface(self.__get_sphere_surface(detailed, scale), surface_color, alpha),
            Graph3dPlot(Points.fromiter(circle_x, circle_y, zeros), grid_color),
            Graph3dPlot(Points.fromiter(circle_y, zeros, circle_x), grid_color),
            Graph3dPlot(Points.fromiter(zeros, circle_x, circle_y), grid_color),
            Graph3dScatter(Points.fromiter(
                [0, 0, scale, 0, 0, -scale],
                [0, scale, 0, 0, -scale, 0],
                [scale, 0, 0, -scale, 0, 0]
            ), color="black", size=30)
        ])

    @staticmethod
    def __get_circle(detailed: int = DEFAULT_DETAILED, scale: float = DEFAULT_SCALE) -> Points:
        arr = np.linspace(0, np.pi*2, detailed)
        x = np.cos(arr) * scale
        y = np.sin(arr) * scale
        return Points.fromiter(x, y)

    @staticmethod
    def __get_sphere_surface(detailed: int = DEFAULT_DETAILED, scale: float = DEFAULT_SCALE) -> Points:
        x = np.linspace(-np.pi, np.pi, detailed)
        y = np.linspace(-np.pi, np.pi, detailed)
        x, y = np.meshgrid(x, y)
        new_z = np.sin(x) * (scale)
        new_x = np.cos(x) * (scale)
        new_y = np.sin(y)*new_x
        new_x = np.cos(y)*new_x

        return Points.fromiter(new_x, new_y, new_z)

    def draw(self, ax: Axes3D) -> None:
        self.draw_subgraphs(ax)
        labels = _set2labels(self.number_set)
        ax.text(0, 0, (1+0.2)*self.scale, labels[0], color='white', fontsize=12, path_effects=[pe.withStroke(linewidth=2, foreground="black")])
        ax.text(-(1+0.2)*self.scale, 0, 0, labels[1], color='white', fontsize=12, path_effects=[pe.withStroke(linewidth=2, foreground="black")])
        ax.text(0, 0, -(1+0.2)*self.scale, labels[2], color='white', fontsize=12, path_effects=[pe.withStroke(linewidth=2, foreground="black")])
        ax.text((1+0.2)*self.scale, 0, 0, labels[3], color='white', fontsize=12, path_effects=[pe.withStroke(linewidth=2, foreground="black")])
        ax.text(0, -(1+0.2)*self.scale, 0, labels[4], color='white', fontsize=12, path_effects=[pe.withStroke(linewidth=2, foreground="black")])
        ax.text(0, (1+0.2)*self.scale, 0, labels[5], color='white', fontsize=12, path_effects=[pe.withStroke(linewidth=2, foreground="black")])