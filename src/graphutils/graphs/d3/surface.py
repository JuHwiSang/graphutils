from typing import Optional

from mpl_toolkits.mplot3d import Axes3D
from graphutils.points import Points
from .base import Graph3d

class Graph3dSurface(Graph3d):
    
    color: str | None
    alpha: str | None

    def __init__(self, _points: Points | None = None, color: str | None = None, alpha: str | None = None) -> None:
        super().__init__(_points)
        self.color = color
        self.alpha = alpha

    def draw(self, ax: Axes3D) -> None:
        x, y, z = self.points
        ax.plot_surface(x, y, z, color=self.color, alpha=self.alpha)