from floorplan_dsl.classes.fpm2.geometry import (
    Frame,
)

from floorplan_dsl.processors.semantics.fpm2 import (
    SpaceSemantics,
    FeatureSemantics,
    OpeningSemantics,
    WallSemantics,
)


class Space(SpaceSemantics):
    def __init__(
        self, parent, name, shape, location, features, defaults, walls=None, frame=None
    ):
        self.parent = parent
        self.name = name
        self.shape = shape
        self.location = location
        self.defaults = defaults
        self.features = features

        # Semantics
        if self.defaults is None:
            self.defaults = self.parent.defaults
        elif self.defaults.wall is None:
            self.defaults.wall = self.parent.defaults.wall
        else:
            if self.defaults.wall.thickness is None:
                self.defaults.wall.thickness = self.parent.defaults.wall.thickness
            elif self.defaults.wall.height is None:
                self.defaults.wall.height = self.parent.defaults.wall.height

        self.frame = Frame(self, "{}".format(self.name))

        edges = self.get_wall_edges(self.shape.coordinates)
        self.walls = [
            Wall(
                self,
                [p1, p2],
                i,
                self.defaults.wall.thickness,
                self.defaults.wall.height,
            )
            for i, (p1, p2) in enumerate(edges)
        ]

        # TODO: Move to semantics processor?
        self.compute_outer_wall_edges()
        self.process_shape_semantics()
        self.compute_3d_shape()


class Wall(WallSemantics):
    def __init__(
        self,
        parent,
        points,
        idx,
        thickness,
        height,
        shape=None,
        frame=None,
        shape_3d=None,
    ) -> None:
        self.parent = parent
        self.idx = idx
        self.points = points
        self.thickness = thickness
        self.height = height
        self.shape = shape
        self.shape_3d = shape_3d

        # Semantics
        self.name = "{}-wall-{}".format(self.parent.name, self.idx)
        self.frame = Frame(self, self.name)


class Feature(FeatureSemantics):
    pass


class Column(Feature):
    def __init__(
        self, parent, name, shape, height, location, frame=None, shape_3d=None
    ) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.height = height
        self.location = location
        self.shape_3d = shape_3d

        if frame is None:
            self.frame = Frame(self, "column-{}".format(self.name))

        self.process_shape_semantics()
        self.compute_3d_shape()


class Divider(Feature):
    def __init__(
        self, parent, name, shape, height, location, frame=None, shape_3d=None
    ) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.height = height
        self.location = location
        self.shape_3d = shape_3d

        if frame is None:
            self.frame = Frame(self, "divider-{}".format(self.name))

        self.process_shape_semantics()
        self.compute_3d_shape()


class Opening(OpeningSemantics):
    pass


class Entryway(Opening):
    def __init__(
        self, parent, name, shape, location, frame=None, shape_3d=None
    ) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.location = location
        self.shape_3d = shape_3d

        if frame is None:
            self.frame = Frame(self, "entryway-{}".format(self.name))

        self.process_shape_semantics()


class Window(Opening):
    def __init__(
        self, parent, name, shape, location, frame=None, shape_3d=None
    ) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.location = location
        self.shape_3d = shape_3d

        if frame is None:
            self.frame = Frame(self, "window-{}".format(self.name))

        self.process_shape_semantics()
