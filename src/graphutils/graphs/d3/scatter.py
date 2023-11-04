from typing import Optional
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from graphutils.points import Points
from .base import Graph3d

class Graph3dScatter(Graph3d):
    color: str | int | np.ndarray | None
    size: float | int | np.ndarray | None
    color_index = int | None
    size_index = int | None

    def __init__(self, _points: Points | None = None,
                 color: Optional[str | np.ndarray] = None,
                 size: Optional[float | np.ndarray] = None,
                 color_index: Optional[int] = None,
                 size_index: Optional[int] = None) -> None:
        super().__init__(_points)
        self.color = color
        self.size = size
        self.color_index = color_index
        self.size_index = size_index

    def draw(self, ax: Axes3D) -> None:
        kwargs = {}
        if self.color_index is not None:
            kwargs['color'] = self.points[self.color_index]
        elif self.color is not None:
            kwargs['color'] = self.color

        if self.size_index is not None:
            kwargs['s'] = self.points[self.size_index]
        elif self.size is not None:
            kwargs['s'] = self.size
            
        ax.scatter(*self.points[:3], **kwargs)

        # if self.points.ndim == 3:
        #     x, y, z = self.points
        #     ax.scatter(x, y, z)
        # elif self.points.ndim == 4:
        #     x, y, z, w = self.points
        #     ax.scatter(x, y, z, c=w)
