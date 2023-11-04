from mpl_toolkits.mplot3d import Axes3D
from typing import Optional

from graphutils.points import Points
from .base import Graph3d

class Graph3dPlot(Graph3d):

    color: str | None
    alpha: float | None

    def __init__(self, points: Points, color: Optional[str] = None, alpha: Optional[float] = None) -> None:
        super().__init__(points)
        self.color = color
        self.alpha = alpha

    def draw(self, ax: Axes3D) -> None:
        ax.plot(self.points[0], self.points[1], self.points[2], color=self.color)