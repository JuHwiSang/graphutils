from typing import Any, Literal
import numpy as np

DimensionLiteral = Literal['2d', '3d']
PositionType = tuple[int, int]
NumberSetLiteral = Literal["real", "positive"]

class PointHandleFuncType:
    def __call__(self, points: np.ndarray) -> np.ndarray | tuple:
        ...