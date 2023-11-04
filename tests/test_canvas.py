from graphutils.window import Window
from graphutils.canvas import Canvas2d, Canvas3d, Canvas
from graphutils.graphs.d2 import Graph2dScatter
from graphutils.points import Points
import pytest
import numpy

@pytest.fixture(scope="function")
def canvas2d():
    window = Window()
    canvas2d = window.create_canvas('2d')
    return canvas2d

@pytest.fixture(scope="function")
def points():
    points = Points.generate([-3, 3, 10], [-3, 3, 10], [-3, 3, 10])
    return points

def test_creation():
    window = Window(shape=(1, 4))
    canvas1 = window.create_canvas()
    canvas2 = window.create_canvas()
    canvas3 = window.create_canvas('3d')
    # canvas1 = Canvas('2d', window=window)
    # canvas1 = window.canvases[0]
    # canvas2 = window.canvases[1]
    # canvas3 = window.canvases[2]
    # canvas2 = Canvas2d(window=window)
    # canvas3 = Canvas3d(window=window)

    assert window.shape == (1, 4)
    assert window.canvas_array == [canvas1, canvas2, canvas3, None]
    assert canvas1.position == (0, 0)
    assert canvas2.position == (0, 1)
    assert canvas3.position == (0, 2)
    assert canvas1.graphs == []
    assert canvas2.graphs == []
    assert canvas3.graphs == []
    
    # canvas4 = window.create_canvas('3d')
    # position = window.add_canvas(canvas4)
    # assert position == (1, 4)
    # assert canvas4 in window.canvas_array

    canvas3.clear() # ax cla
    window.clear() # fig clf


def test_lim(canvas2d: Canvas2d):
    canvas2d.set_lims((-3, 3), (-3, 3)) # None: 기존꺼유지?
    assert canvas2d.lims == ((-3, 3), (-3, 3))

def test_add_graph(canvas2d: Canvas2d):
    points = Points.generate([-3, 3, 10], [-3, 3, 10], [-3, 3, 10])
    graph_scatter = Graph2dScatter(points) # default order
    canvas2d.add_graph(graph_scatter)
    assert canvas2d.graphs == [graph_scatter]

def test_fix_center(canvas2d: Canvas2d, points: Points):
    canvas2d.add_graph(Graph2dScatter(points))
    canvas2d.fix_center()
    assert canvas2d.lims == ((-3, 3), (-3, 3))