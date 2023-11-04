from graphutils.points import Points
import numpy as np

def test_creation():
    points1 = Points.fromiter([1, 2, 3])  # default
    assert points1.ndim == 1
    assert next(iter(points1)).tolist() == [1, 2, 3]
    assert points1[0].tolist() == [1, 2, 3]
    assert points1.plen == 3

    tmp, *_ = points1
    assert tmp.tolist() == [1, 2, 3]

    points2 = Points.generate((-3, 3, 10), (-3, 3, 10), (-3, 3, 10), endpoint=True)
    assert points2.ndim == 3
    assert next(iter(points2)).tolist() == np.linspace(-3, 3, 10).repeat(100).tolist()
    assert len(points2[0]) == 1000
    assert points2.plen == 1000


def test_shuffle():
    points = Points.fromiter([1, 2, 3], [4, 5, 6])
    assert points.shuffle([1, 0]) == Points.fromiter([4, 5, 6], [1, 2, 3])

def test_calc():
    points = Points.fromiter([1, 2, 3], [4, 5, 6])
    assert points.calc(lambda p:(p[0],p[0]+p[1])) == Points.fromiter([1, 2, 3], [5, 7, 9])

def test_filter():
    points = Points.fromiter([1, 2, 3], [4, 5, 6])
    assert points.filter(lambda p:p[0]>p[1]) == Points()

def test_graph():
    points = Points.fromiter([1, 2, 3], [1, 4, 5])
    assert points.graph(lambda p:(p[0]**2,p[1]), abs_tol=0.0) == Points.fromiter([1, 2], [1, 4])

def test_lim():
    points = Points.fromiter([1, 2, 3], [4, 5, 6])
    points = points.set_lims([-10, 10], [-5, 5])
    assert points == Points.fromiter([1, 2], [4, 5])
    points = points.set_lims([-3, 3], [-4, 4], remove=False)
    assert points == Points.fromiter([1, 2], [4, 4])

# def test_calculation():
#     points1 = Points([1, 2, 3])
#     points4 = Points([1, 3, 2])

#     assert points1 + points2 == Points(points1.numpy() + points2.numpy())
#     assert points1 - points2 == Points(points1.numpy() - points2.numpy())
#     assert points1 * points2 == Points(points1.numpy() * points2.numpy())
#     assert points1 / points2 == Points(points1.numpy() / points2.numpy())
#     assert points1 ** points2 == Points(points1.numpy() ** points2.numpy())
#     assert points1 % points2 == Points(points1.numpy() % points2.numpy())
#     assert points1 ^ points2 == Points(points1.numpy() ^ points2.numpy())
#     assert points1 & points2 == Points(points1.numpy() & points2.numpy())
#     assert points1 > points2 == Points(points1.numpy() > points2.numpy())
#     assert points1 < points2 == Points(points1.numpy() < points2.numpy())
#     assert (points1 == points2) == Points(points1.numpy() == points2.numpy())
#     assert ~points1 == Points(~points1.numpy())

#     points3 = Points([[1, 2, 3]])
#     points4 = Points([[1], [2], [3]])
#     assert points3 @ points4 == Points(points3.numpy() @ points4.numpy())

