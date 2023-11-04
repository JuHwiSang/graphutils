from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from .types import DimensionLiteral, PositionType
from .graphs import Graph
from .resize_3d_canvas import resize
from .config import DEFAULT_RESIZE_Z


class Canvas:
    dim: DimensionLiteral
    ndim: int
    position: PositionType
    ax: Axes
    graphs: list[Graph]
    lims: tuple[tuple[float, float], ...]

    # fix_center: bool

    def __init__(self, dim: DimensionLiteral, position: PositionType, ax: Axes) -> None:
        self.dim = dim
        self.ndim = int(dim[:-1])
        self.position = position
        self.ax = ax
        self.graphs = []
        self.lims = ()
        # self.fix_center = False

    def add_graph(self, graph: Graph) -> None:
        self.graphs.append(graph)

    def set_lims(self, *lims: tuple[float, float]) -> None:
        if len(lims) != self.ndim:
            raise ValueError(f"Dimension of lims not equal with dimension of canvas('{self.dim}')")
        self.lims = lims

    def fix_center(self) -> None:
        max_num = max(graph.points.numpy().max() for graph in self.graphs)
        self.set_lims(*((-max_num, max_num),)*self.ndim)

    def draw(self) -> None:
        for graph in self.graphs:
            graph.draw(self.ax)
        if self.lims:
            self._apply_lims()

    def _apply_lims(self):
        self.ax.set_xlim(self.lims[0])
        self.ax.set_ylim(self.lims[1])
        # if self.dim == "3d":
        if isinstance(self.ax, Axes3D):
            self.ax.set_zlim(self.lims[2])

    def clear(self) -> None:
        self.ax.cla()
        


class Canvas2d(Canvas):
    def __init__(self, position: PositionType, ax: Axes) -> None:
        super().__init__('2d', position, ax)

    def set_lims(self, xlim: tuple[float, float], ylim: tuple[float, float]) -> None:
        return super().set_lims(xlim, ylim)
    
    
class Canvas3d(Canvas):
    def __init__(self, position: PositionType, ax: Axes) -> None:
        super().__init__('3d', position, ax)
        self.resize()

    def set_lims(self, xlim: tuple[float, float], ylim: tuple[float, float], zlim: tuple[float, float]) -> None:
        return super().set_lims(xlim, ylim, zlim)
    
    def resize(self, scale_x: float = 1, scale_y: float = 1, scale_z: float = DEFAULT_RESIZE_Z) -> None:
        resize(self.ax, scale_x, scale_y, scale_z)