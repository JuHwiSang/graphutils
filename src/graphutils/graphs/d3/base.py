from abc import ABCMeta, abstractmethod
from mpl_toolkits.mplot3d import Axes3D

from ..base import Graph


class Graph3d(Graph, metaclass=ABCMeta):
    
    @abstractmethod
    def draw(self, ax: Axes3D) -> None:
        return super().draw(ax)