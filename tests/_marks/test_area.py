
import matplotlib as mpl
from matplotlib.colors import to_rgba, to_rgba_array

from numpy.testing import assert_array_equal

from seaborn._core.plot import Plot
from seaborn._marks.area import Area, Ribbon


class TestAreaMarks:

    def test_single_defaults(self):

        x, y = [1, 2, 3], [1, 2, 1]
        p = Plot(x=x, y=y).add(Area()).plot()
        ax = p._figure.axes[0]
        poly = ax.patches[0]
        verts = poly.get_path().vertices.T

        expected_x = [1, 2, 3, 3, 2, 1, 1]
        assert_array_equal(verts[0], expected_x)

        expected_y = [0, 0, 0, 1, 2, 1, 0]
        assert_array_equal(verts[1], expected_y)

        fc = poly.get_facecolor()
        assert_array_equal(fc, to_rgba("C0", .2))

        ec = poly.get_edgecolor()
        assert_array_equal(ec, to_rgba("C0", 1))

        lw = poly.get_linewidth()
        assert_array_equal(lw, mpl.rcParams["patch.linewidth"] * 2)

    def test_direct_parameters(self):

        x, y = [1, 2, 3], [1, 2, 1]
        mark = Area(
            color="C2",
            alpha=.3,
            edgecolor="k",
            edgealpha=.8,
            edgewidth=2,
            edgestyle=(0, (2, 1)),
        )
        p = Plot(x=x, y=y).add(mark).plot()
        ax = p._figure.axes[0]
        poly = ax.patches[0]

        fc = poly.get_facecolor()
        assert_array_equal(fc, to_rgba(mark.color, mark.alpha))

        ec = poly.get_edgecolor()
        assert_array_equal(ec, to_rgba(mark.edgecolor, mark.edgealpha))

        lw = poly.get_linewidth()
        assert_array_equal(lw, mark.edgewidth * 2)

        ls = poly.get_linestyle()
        dash_on, dash_off = mark.edgestyle[1]
        expected = (0, (mark.edgewidth * dash_on / 4, mark.edgewidth * dash_off / 4))
        assert ls == expected

    def test_mapped(self):

        x, y = [1, 2, 3, 2, 3, 4], [1, 2, 1, 1, 3, 2]
        g = ["a", "a", "a", "b", "b", "b"]
        p = Plot(x=x, y=y, color=g, edgewidth=g).add(Area()).plot()
        ax = p._figure.axes[0]

        expected_x = [1, 2, 3, 3, 2, 1, 1], [2, 3, 4, 4, 3, 2, 2]
        expected_y = [0, 0, 0, 1, 2, 1, 0], [0, 0, 0, 2, 3, 1, 0]

        for i, poly in enumerate(ax.patches):
            verts = poly.get_path().vertices.T
            assert_array_equal(verts[0], expected_x[i])
            assert_array_equal(verts[1], expected_y[i])

        fcs = [p.get_facecolor() for p in ax.patches]
        assert_array_equal(fcs, to_rgba_array(["C0", "C1"], .2))

        ecs = [p.get_edgecolor() for p in ax.patches]
        assert_array_equal(ecs, to_rgba_array(["C0", "C1"], 1))

        lws = [p.get_linewidth() for p in ax.patches]
        assert lws[0] > lws[1]

    def test_unfilled(self):

        x, y = [1, 2, 3], [1, 2, 1]
        p = Plot(x=x, y=y).add(Area(fill=False)).plot()
        ax = p._figure.axes[0]
        poly = ax.patches[0]
        assert poly.get_facecolor() == to_rgba("C0", 0)

    def test_ribbon(self):

        x, ymin, ymax = [1, 2, 4], [2, 1, 4], [3, 3, 5]
        p = Plot(x=x, ymin=ymin, ymax=ymax).add(Ribbon()).plot()
        ax = p._figure.axes[0]
        verts = ax.patches[0].get_path().vertices.T

        expected_x = [1, 2, 4, 4, 2, 1, 1]
        assert_array_equal(verts[0], expected_x)

        expected_y = [2, 1, 4, 5, 3, 3, 2]
        assert_array_equal(verts[1], expected_y)
