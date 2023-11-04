from __future__ import annotations
from typing import TypeVar, Generic, Iterable, Iterator, cast, Any, Optional, Callable
from functools import reduce
import numpy.typing as npt
import numpy as np

from .types import PointHandleFuncType


class Points():
    _points: np.ndarray

    def __init__(self, _points: Optional[np.ndarray] = None) -> None:
        if _points is None:
            _points = np.array([[]])
        self._points = _points
        self.check_validation()

    @classmethod
    def fromiter(cls, *axes: Iterable | np.ndarray, dtype: npt.DTypeLike = np.float64) -> Points:
        axes_list = []
        for axis in axes:
            if not isinstance(axis, np.ndarray):
                axis = cast(np.ndarray, np.fromiter(axis, dtype=dtype))
            axes_list.append(axis)

        _points = np.array(axes_list)
        return Points(_points)

    def check_validation(self) -> None:
        if self.numpy().ndim < 2:
            raise ValueError(f"Dimension of _points must be bigger than 2, not '{self.numpy().ndim}'")
        
    @classmethod
    def generate(cls, *linspace_ranges: tuple[float, float, int], endpoint: bool = True) -> Points:
        ndim = len(linspace_ranges)
        plen = reduce(lambda acc,cur:acc*cur[2], linspace_ranges, 1)
        linspaces = (np.linspace(*linspace_range, endpoint=endpoint) for linspace_range in linspace_ranges)
        meshgrid = np.array(np.meshgrid(*linspaces, indexing='ij'))
        _points = meshgrid.reshape((ndim, plen))
        return cls(_points)
    
    @classmethod
    def concat(cls, *points: Points) -> Points:
        return Points(np.concatenate([point.numpy() for point in points], axis=1))
    
    def numpy(self, copy: bool = False) -> np.ndarray:
        if copy:
            return self._points.copy()
        return self._points

    def shuffle(self, new_order: list[int]) -> Points:
        return Points(np.array([self.numpy()[i] for i in new_order]))
    
    def calc(self, func: PointHandleFuncType) -> Points:
        new_points_np = np.array(func(self.numpy()))
        new_points_np = new_points_np[:, (~np.isnan(new_points_np)).all(axis=0)]
        return Points(new_points_np)
    
    def filter(self, func: PointHandleFuncType) -> Points:
        return Points(self.numpy()[:, np.array(func(self.numpy()))])
    
    @staticmethod
    def __gap_of_res(res: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
        return np.abs(res[0] - res[1])

    def graph(self, func: PointHandleFuncType, abs_tol: float = 0.2) -> Points:
        return self.filter(lambda p:self.__gap_of_res(func(p))<=abs_tol)
    
    def set_lims(self, *lims: tuple[float, float], remove: bool = True) -> Points:
        if remove:
            return Points(self.numpy()[:, np.array(
                    [
                        (lim[0]<=axis_points) & (axis_points<=lim[1])
                        for lim, axis_points in zip(lims, self.numpy())
                    ]
                ).all(axis=0)]
            )

        else:
            return Points(np.array([np.clip(axis_points, lim[0], lim[1]) for lim, axis_points in zip(lims, self.numpy())]))

    @property
    def ndim(self) -> int:
        return self.numpy().shape[0]
    
    @property
    def plen(self) -> int:
        return self.numpy().shape[1]
    
    def __len__(self):
        return len(self.numpy())
    
    def __iter__(self) -> Iterator[np.ndarray]:
        return iter(self.numpy())

    def __getitem__(self, key: Any):
        return self.numpy().__getitem__(key)
    
    def __setitem__(self, key: Any, value: Any) -> None:
        self.numpy().__setitem__(key, value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(array({self.numpy().tolist()}))"

    def __eq__(self, obj: Any):
        if isinstance(obj, Points):
            return not cast(np.ndarray, self.numpy() != obj._points).any()
        else:
            return False