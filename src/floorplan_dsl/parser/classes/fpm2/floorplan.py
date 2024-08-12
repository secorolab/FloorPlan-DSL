import math
import itertools

from textx.exceptions import TextXSemanticError
from textx import textx_isinstance, get_metamodel, get_model
from textx.scoping.tools import get_unique_named_object

from floorplan_dsl.parser.classes.fpm2.geometry import PointCoordinate, Polygon, Frame


class Space:
    def __init__(
        self, parent, name, shape, location, features, defaults, walls=None, frame=None
    ):
        self.parent = parent
        self.name = name
        self.shape = shape
        self.location = location
        self.defaults = defaults

        if self.defaults is None:
            self.defaults = self.parent.defaults
        elif self.defaults.wall is None:
            self.defaults.wall = self.parent.defaults.wall
        else:
            if self.defaults.wall.thickness is None:
                self.defaults.wall.thickness = self.parent.defaults.wall.thickness
            elif self.defaults.wall.height is None:
                self.defaults.wall.height = self.parent.defaults.wall.height

        self.features = features

        self.frame = Frame(self, "{}".format(self.name))

        vertices = list()
        vertices.extend(self.shape.points)
        vertices.append(self.shape.points[0])
        self.walls = [
            Wall(
                self,
                [p1, p2],
                i,
                self.defaults.wall.thickness,
                self.defaults.wall.height,
            )
            for i, (p1, p2) in enumerate(itertools.pairwise(vertices))
        ]

    def process_location(self):
        mm = get_metamodel(self)
        m = get_model(self)

        if textx_isinstance(self.location.of, mm["WallFrame"]):
            self.location.of = self.location.of.space.walls[
                self.location.of.wall_idx
            ].frame
        elif textx_isinstance(self.location.of, mm["SpaceFrame"]):
            self.location.of = self.location.of.space.frame
        else:
            raise TextXSemanticError(
                "Can't find 'of' frame for space {}".format(self.name)
            )

        if textx_isinstance(self.location.wrt, mm["WorldFrame"]):
            if m.frame is None:
                m.frame = Frame(m, "world")
                self.location.wrt = m.frame
            else:
                wf = get_unique_named_object(m, "world-frame")
                self.location.wrt = wf
        elif textx_isinstance(self.location.wrt, mm["WallFrame"]):
            self.location.wrt = self.location.wrt.space.walls[
                self.location.wrt.wall_idx
            ].frame
        elif textx_isinstance(self.location.wrt, mm["SpaceFrame"]):
            self.location.wrt = self.location.wrt.space.frame


class Wall:
    def __init__(
        self, parent, points, idx, thickness, height, shape=None, frame=None
    ) -> None:
        self.parent = parent
        self.points = points
        self.idx = idx
        self.thickness = thickness
        self.height = height
        self.frame = Frame(self, "{}-wall-{}".format(self.parent.name, self.idx))
        self.shape = self.get_2D_shape()

    @property
    def width(self):
        x1 = self.points[0].x.value
        y1 = self.points[0].y.value
        x2 = self.points[1].x.value
        y2 = self.points[1].y.value

        return math.dist((x1, y1), (x2, y2))

    def get_2D_shape(self):
        x = self.width / 2

        points = [
            PointCoordinate(self, -x, 0.0, 0.0),
            PointCoordinate(self, -x, self.thickness, 0.0),
            PointCoordinate(self, x, self.thickness, 0.0),
            PointCoordinate(self, x, 0.0, 0.0),
        ]
        return Polygon(self, points)


class Feature:
    def process_location(self):
        mm = get_metamodel(self)

        if textx_isinstance(self.location.wrt, mm["WallFrame"]):
            self.location.wrt = self.location.wrt.space.walls[
                self.location.wrt.wall_idx
            ].frame
        elif textx_isinstance(self.location.wrt, mm["SpaceFrame"]):
            self.location.wrt = self.location.wrt.space.frame


class Column(Feature):
    def __init__(self, parent, name, shape, height, location, frame=None) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.height = height
        self.location = location

        if frame is None:
            self.frame = Frame(self, "column-{}".format(self.name))


class Divider(Feature):
    def __init__(self, parent, name, shape, height, location, frame=None) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.height = height
        self.location = location

        if frame is None:
            self.frame = Frame(self, "divider-{}".format(self.name))


class Opening:
    def process_location(self):
        mm = get_metamodel(self)
        if len(self.location.walls) > 2:
            raise TextXSemanticError("Wrong number of walls")

        frames = list()

        for w in self.location.walls:
            if textx_isinstance(w, mm["WallFrame"]):
                frames.append(w.space.walls[w.wall_idx].frame)
            else:
                raise TextXSemanticError("Opening location is not a wall frame")

        self.location.walls = frames


class Entryway(Opening):
    def __init__(self, parent, name, shape, location, frame=None) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.location = location

        if frame is None:
            self.frame = Frame(self, "entryway-{}".format(self.name))


class Window(Opening):
    def __init__(self, parent, name, shape, location, frame=None) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.location = location

        if frame is None:
            self.frame = Frame(self, "window-{}".format(self.name))
