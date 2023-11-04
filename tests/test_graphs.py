# from graphutils.graphs import Graph3dWheelCylinder, Graph3dWheelSphear
# from graphutils.canvas import Canvas3d
# from graphutils.window import Window
# from graphutils.points import Points
from graphutils import (
    Window,
    Points,
    Canvas3d
)
from graphutils.graphs.d3 import Graph3dWheelCylinderPlot
import pytest

@pytest.fixture(scope='function')
def canvas3d():
    window = Window()
    canvas3d = window.create_canvas('3d')
    return canvas3d

def test_graph3d_wheel_cylinder(canvas3d: Canvas3d):
    points = Points.fromiter([1, 2, 3], [1, 3, 5])
    graph3d = Graph3dWheelCylinderPlot(points, number_set="real")
    canvas3d.add_graph(graph3d)
    assert canvas3d.graphs == [graph3d]

def test_graph3d_wheel_sphear(canvas3d: Canvas3d):
    points = Points.fromiter([1, 2, 3], [1, 3, 5])
    graph3d = Graph3dWheelCylinderPlot(points)
    canvas3d.add_graph(graph3d)
    assert canvas3d.graphs == [graph3d]