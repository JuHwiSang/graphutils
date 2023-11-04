from matplotlib.axes import Axes
from .base import Graph2d

class Graph2dScatter(Graph2d):
    def draw(self, ax: Axes) -> None:
        if self.points.ndim == 2:
            ax.scatter(self.points[0], self.points[1])
        elif self.points.ndim == 3:
            ax.scatter(self.points[0], self.points[1], c=self.points[2])
        else:
            raise ValueError(f"Dimension of points must be 2 or 3, not {self.points.ndim}")