from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Literal, overload
from matplotlib.axes import Axes
import matplotlib.pyplot as plt

from .types import DimensionLiteral, PositionType
from .canvas import Canvas, Canvas2d, Canvas3d



class Window:
    fig: plt.Figure
    shape: PositionType
    canvas_array: list[Canvas | None]


    def __init__(self, shape: PositionType = (1, 1)) -> None:
        self.fig = plt.figure()
        self.shape = shape
        self.canvas_array = [None] * (shape[0] * shape[1])


    @overload
    def create_canvas(self, dim: Optional[Literal['2d']] = None, position: Optional[PositionType] = None) -> Canvas2d: ...
    @overload
    def create_canvas(self, dim: Literal['3d'], position: Optional[PositionType] = None) -> Canvas3d: ...
    def create_canvas(self, dim: DimensionLiteral = '2d', position: Optional[PositionType] = None) -> Canvas:
        if position is None:
            if None not in self.canvas_array:
                raise IndexError("Canvas array is all filled")
            position = self._index_to_position(self._get_empty_index())
        if dim == '2d':
            canvas = Canvas2d(position, self._get_ax(dim, position))
        elif dim == '3d':
            canvas = Canvas3d(position, self._get_ax(dim, position))
        else:
            raise ValueError(f"Invalid DimensionLiteral: '{dim}'")

        self._set_canvas_by_position(canvas, position)
        return canvas


    # def add_canvas(self, canvas: Canvas, position: Optional[PositionType] = None) -> PositionType:
    #     if position:
    #         self._set_canvas_by_position(canvas, position)
    #         return
        
    #     if None not in self.canvas_array:
    #         raise IndexError("Canvas array is all filled")
    
    #     self.canvas_array[self.canvas_array.index(None)] = canvas

    def _get_empty_index(self) -> int:
        return self.canvas_array.index(None)
        
    def _get_ax(self, dim: DimensionLiteral, position: PositionType) -> Axes:
        kwargs = {}
        if dim == "3d":
            kwargs = {'projection': dim}
        return self.fig.add_subplot(self.shape[0], self.shape[1], self._position_to_index(position)+1, **kwargs)

    def _position_to_index(self, position: PositionType) -> int:
        if 0 <= position[0] < self.shape[0] and 0 <= position[1] < self.shape[1]:
            return self.shape[1] * position[0] + position[1]
        raise IndexError("Canvas position is out of range")
    
    def _index_to_position(self, index: int) -> PositionType:
        if index >= self.shape[0]*self.shape[1]:
            raise IndexError("Canvas index is out of range")
        return (index//self.shape[1], index%self.shape[1])


    def _set_canvas_by_position(self, canvas: Canvas, position: PositionType) -> None:
        self.canvas_array[self._position_to_index(position)] = canvas


    def draw(self):
        for canvas in self.canvas_array:
            canvas.draw()
        plt.show()

    def clear(self):
        self.fig.clf()