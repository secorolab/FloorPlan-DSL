import math
import itertools

from textx.exceptions import TextXSemanticError
from textx import textx_isinstance, get_metamodel, get_model
from textx.scoping.tools import get_unique_named_object

from floorplan_dsl.parser.classes.fpm2.geometry import (
    PointCoordinate,
    Polygon,
    Point,
    Frame,
    PositionCoordinate,
    PoseCoordinate,
    get_angle_between_vectors,
)


class FloorPlanElement:
    def set_shape_points(self):

        points = list()
        for i, c in enumerate(self.shape.coordinates):
            p = Point(self, "{}-corner-{}".format(self.name, i))
            points.append((p))

        return points

    def set_polytope_name(self):
        self.shape.name = "{}-polygon".format(self.name)

    def get_shape_point_positions(self):
        position_coords = list()
        for c, p in zip(self.shape.coordinates, self.shape.points):
            coord = PositionCoordinate(self, c, p, self.frame)
            position_coords.append(coord)
        return position_coords


class Space(FloorPlanElement):
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
        vertices.extend(self.shape.coordinates)
        vertices.append(self.shape.coordinates[0])
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

        # self.pose = self.get_pose_coord_wrt_location()
        self.shape.points = self.set_shape_points()
        self.set_polytope_name()
        self.shape_position_coords = self.get_shape_point_positions()
        # self.wall_pose_coords = self.get_wall_poses()

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

    # TODO: Move this to interpreter?
    def get_pose_coord_wrt_location(self):
        # TODO This might be an alternative to replacing model data in the obj_processor
        return PoseCoordinate(
            self,
            self.location.of,
            self.location.wrt,
            self.location.translation,
            self.location.rotation,
        )

    def get_wall_poses(self):
        pose_coords = list()
        for w in self.walls:
            pose_coords.append(PoseCoordinate.wall_wrt_parent_space(w))
        return pose_coords


class Wall(FloorPlanElement):
    def __init__(
        self, parent, points, idx, thickness, height, shape=None, frame=None
    ) -> None:
        self.parent = parent
        self.idx = idx
        self.points = points
        self.thickness = thickness
        self.height = height

        self.name = "{}-wall-{}".format(self.parent.name, self.idx)

        # Semantics
        self.frame = Frame(self, self.name)
        self.shape = self.get_2D_shape()
        self.point_positions = self.get_wall_point_positions()
        self.set_polytope_name()

    @property
    def width(self):
        x1 = self.points[0].x.value
        y1 = self.points[0].y.value
        x2 = self.points[1].x.value
        y2 = self.points[1].y.value

        return math.dist((x1, y1), (x2, y2))

    # TODO: Move this to interpreter
    def get_2D_shape(self):
        return Polygon.from_wall(self)

    def get_wall_origin_pose_coord(self):
        """Pose of the wall frame wrt to its parent (space)"""
        x1 = self.points[0].x.value
        y1 = self.points[0].y.value
        x2 = self.points[1].x.value
        y2 = self.points[1].y.value

        orig = [1, 0]  # x-axis of space
        x_axis = [x2 - x1, y2 - y1]  # x vector from wall
        rotation = get_angle_between_vectors(x_axis, orig)

        return (x1 + x2) / 2, (y1 + y2) / 2, rotation

    def get_wall_point_positions(self):
        """Positions of the wall polygon wrt to the wall frame"""
        position_coords = list()
        for i in range(4):
            p = self.shape.points[i]
            c = self.shape.coordinates[i]
            coord = PositionCoordinate(self, c, p, self.frame)
            position_coords.append(coord)
        return position_coords


class Feature(FloorPlanElement):
    def process_location(self):
        mm = get_metamodel(self)

        if textx_isinstance(self.location.wrt, mm["WallFrame"]):
            self.location.wrt = self.location.wrt.space.walls[
                self.location.wrt.wall_idx
            ].frame
        elif textx_isinstance(self.location.wrt, mm["SpaceFrame"]):
            self.location.wrt = self.location.wrt.space.frame

    def get_pose_coord_wrt_location(self):
        # TODO This might be an alternative to replacing model data in the obj_processor
        return PoseCoordinate.feature_wrt_space(self)


class Column(Feature):
    def __init__(self, parent, name, shape, height, location, frame=None) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.height = height
        self.location = location

        if frame is None:
            self.frame = Frame(self, "column-{}".format(self.name))

        self.shape.points = self.set_shape_points()
        self.shape_position_coords = self.get_shape_point_positions()
        self.set_polytope_name()


class Divider(Feature):
    def __init__(self, parent, name, shape, height, location, frame=None) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.height = height
        self.location = location

        if frame is None:
            self.frame = Frame(self, "divider-{}".format(self.name))

        self.shape.points = self.set_shape_points()
        self.shape_position_coords = self.get_shape_point_positions()
        self.set_polytope_name()


class Opening(FloorPlanElement):
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

    def get_pose_coord_wrt_location(self):
        # TODO This might be an alternative to replacing model data in the obj_processor
        return PoseCoordinate.opening_wrt_wall(self)


class Entryway(Opening):
    def __init__(self, parent, name, shape, location, frame=None) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.location = location

        if frame is None:
            self.frame = Frame(self, "entryway-{}".format(self.name))

        self.shape.points = self.set_shape_points()
        self.shape_position_coords = self.get_shape_point_positions()
        self.set_polytope_name()


class Window(Opening):
    def __init__(self, parent, name, shape, location, frame=None) -> None:
        self.parent = parent
        self.name = name
        self.shape = shape
        self.location = location

        if frame is None:
            self.frame = Frame(self, "window-{}".format(self.name))

        self.shape.points = self.set_shape_points()
        self.shape_position_coords = self.get_shape_point_positions()
        self.set_polytope_name()
