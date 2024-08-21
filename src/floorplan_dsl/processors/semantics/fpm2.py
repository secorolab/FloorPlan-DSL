import itertools
import math

import numpy as np
from textx.exceptions import TextXSemanticError
from textx import textx_isinstance, get_metamodel, get_model
from textx.scoping.tools import get_unique_named_object

from floorplan_dsl.classes.fpm2.geometry import (
    PointCoordinate,
    EulerAngles,
    PositionCoordinate,
    PoseCoordinate,
    Point,
    Frame,
    SimplePolygon,
)

from floorplan_dsl.utils.geometry import get_intersection, get_angle_between_vectors
from floorplan_dsl.utils.transformations import Transformation


def process_location(element):
    element.process_location()


def space_obj_processor(space):
    process_location(space)
    space.wall_pose_coords = space.get_wall_poses()
    space.pose = space.get_pose_coord_wrt_location()


def feature_obj_processor(feature):
    process_location(feature)
    feature.pose = feature.get_pose_coord_wrt_location()


def opening_obj_processor(opening):
    process_location(opening)
    opening.pose = opening.get_pose_coord_wrt_location()


def process_angle_units(v):
    mm = get_metamodel(v)
    if (
        textx_isinstance(v, mm["AngleVariable"]) or textx_isinstance(v, mm["Angle"])
    ) and v.unit == "deg":
        v.value = np.deg2rad(v.value)
        v.unit = "rad"


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

    def process_shape_semantics(self):
        self.shape.points = self.set_shape_points()
        self.shape_position_coords = self.get_shape_point_positions()
        self.set_polytope_name()


class SpaceSemantics(FloorPlanElement):
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

    def get_pose_coord_wrt_location(self):
        # TODO This might be an alternative to replacing model data in the obj_processor
        if self.location.rotation:
            rot_z = self.location.rotation.z.value
        else:
            rot_z = 0
        if self.location.translation and self.location.translation.x:
            x = self.location.translation.x.value
        else:
            x = 0
        if self.location.translation and self.location.translation.y:
            y = self.location.translation.y.value
        else:
            y = 0

        mm = get_metamodel(self)

        # Check if two walls are being used as frames of reference
        if textx_isinstance(self.location.of.parent, mm["Wall"]) and textx_isinstance(
            self.location.wrt.parent, mm["Wall"]
        ):

            # If the walls are spaced, the translation in y should include the thickness of both walls
            # See https://github.com/secorolab/FloorPlan-DSL/blob/c2d5db45302a1506d17afe62140398d79abcf21d/src/exsce_floorplan/floor_plan/classes/space.py#L169
            if self.location.spaced:
                y = (
                    y
                    + self.defaults.wall.thickness.value
                    + self.location.wrt.parent.thickness.value
                )

            # The aligned flag adds a rotation of 180 deg to align the walls or spaces
            # See https://github.com/secorolab/FloorPlan-DSL/blob/c2d5db45302a1506d17afe62140398d79abcf21d/src/exsce_floorplan/floor_plan/classes/space.py#L188
            if not self.location.aligned:
                rot_z = rot_z + np.deg2rad(180)

        rotation = EulerAngles(self, z=rot_z)
        translation = PointCoordinate(self, x, y)
        return PoseCoordinate(
            self, self.location.of, self.location.wrt, translation, rotation
        )

    def get_wall_poses(self):
        pose_coords = list()
        for w in self.walls:
            pose_coords.append(w.get_pose_coord_wrt_parent())
        return pose_coords

    def _get_outer_wall_points(self):
        outer_wall_points = list()
        for i, wall in enumerate(self.walls):
            prev_wall = self.walls[i - 1]
            a1, a2 = wall.get_points_in_outer_wall_line_wrt_space_frame()
            b1, b2 = prev_wall.get_points_in_outer_wall_line_wrt_space_frame()

            # Find intersection between the two lines
            x, y = get_intersection(a1, a2, b1, b2)
            outer_wall_points.append((x, y))

        return outer_wall_points

    @staticmethod
    def get_wall_edges(coordinates):
        vertices = list()
        vertices.extend(coordinates)
        vertices.append(coordinates[0])

        edges = list()
        for v1, v2 in itertools.pairwise(vertices):
            edges.append((v1, v2))

        return edges

    def compute_outer_wall_edges(self):
        outer_wall_points = self._get_outer_wall_points()
        outer_edges = self.get_wall_edges(outer_wall_points)
        for edge, wall in zip(outer_edges, self.walls):

            outer_edge_wrt_wall_frame = wall.get_outer_edge_points(edge)
            wall.compute_2d_shape(outer_edge_wrt_wall_frame)
            wall.process_shape_semantics()


class WallSemantics(FloorPlanElement):

    def process_semantics(self):
        self.process_shape_semantics()

    def _get_points_in_outer_wall_line(self):
        x = self.width / 2
        return -x, self.thickness.value, x, self.thickness.value

    def get_transformation_matrix_wrt_parent(self):
        # Get transformation matrix of wall frame wrt space
        return Transformation.get_transformation_matrix_from_model(
            self.get_pose_coord_wrt_parent()
        )

    def get_points_in_outer_wall_line_wrt_space_frame(self):
        x1, y1, x2, y2 = self._get_points_in_outer_wall_line()
        points = np.array(
            [
                [x1, y1, 0, 1],
                [x2, y2, 0, 1],
            ]
        )

        tm_wall = self.get_transformation_matrix_wrt_parent()

        # Transform points wrt to space frame
        points_wrt_space = np.einsum("ij,kj->ki", tm_wall, points)
        x1_space, y1_space = points_wrt_space[0, :2]
        x2_space, y2_space = points_wrt_space[1, :2]
        return [x1_space, y1_space], [x2_space, y2_space]

    def get_outer_edge_points(self, edge):
        # The edge has the outer points wrt to space frame
        tm_wall = self.get_transformation_matrix_wrt_parent()

        p1, p2 = edge
        x1, y1 = p1
        x2, y2 = p2
        points = np.array(
            [
                [x1, y1, 0],
                [x2, y2, 0],
            ]
        )

        # points are defined wrt to the space frame First, translate the points to the wall origin by subtracting the
        # origin (also defined wrt space frame) Next, rotate values back to the wall frame.
        # The transpose of the rotation matrix gives us the rotation wrt wall frame
        points_wrt_wall = np.einsum(
            "ij, kj->ki", tm_wall[:3, :3].T, points - tm_wall[:3, -1]
        )

        x1_wall, y1_wall = points_wrt_wall[0, :2]
        x2_wall, y2_wall = points_wrt_wall[1, :2]
        return x1_wall, y1_wall, x2_wall, y2_wall

    def compute_2d_shape(self, outer_edge):
        poly = SimplePolygon(self, list(), None)

        x = self.width / 2
        x1, y1, x2, y2 = outer_edge

        coords = [
            PointCoordinate(poly, x1, y1, 0.0),
            PointCoordinate(poly, x2, y2, 0.0),
            PointCoordinate(poly, x, 0.0, 0.0),
            PointCoordinate(poly, -x, 0.0, 0.0),
        ]

        poly.coordinates = coords

        self.shape = poly

    def _get_point_values(self):
        x1 = self.points[0].x.value
        y1 = self.points[0].y.value

        x2 = self.points[1].x.value
        y2 = self.points[1].y.value

        return x1, y1, x2, y2

    @property
    def width(self):
        x1, y1, x2, y2 = self._get_point_values()

        return math.dist((x1, y1), (x2, y2))

    def get_origin_translation_coord_values(self):
        x1, y1, x2, y2 = self._get_point_values()
        return (x1 + x2) / 2, (y1 + y2) / 2

    def get_frame_rotation_wrt_parent_value(self):
        x1, y1, x2, y2 = self._get_point_values()
        orig = [1, 0]  # x-axis of space
        x_axis = [x2 - x1, y2 - y1]  # x vector of wall
        rotation = get_angle_between_vectors(x_axis, orig)

        return rotation

    def get_wall_origin_pose_coord_values(self):
        """Return the values of the pose coordinates of the wall frame wrt to its parent (space)"""
        x, y = self.get_origin_translation_coord_values()
        rotation = self.get_frame_rotation_wrt_parent_value()
        return x, y, rotation

    def get_pose_coord_wrt_parent(self):
        x, y, rotation = self.get_wall_origin_pose_coord_values()
        rotation = EulerAngles(self, z=rotation)
        translation = PointCoordinate(self, x, y)
        return PoseCoordinate(
            self, self.frame, self.parent.frame, translation, rotation
        )


class FeatureSemantics(FloorPlanElement):
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
        translation = self.location.translation
        rotation = self.location.rotation
        if self.location.rotation is None:
            rotation = EulerAngles(self, z=0.0)

        if self.location.translation is None:
            translation = PointCoordinate(self, x=0.0, y=0.0)

        return PoseCoordinate(
            self, self.frame, self.location.wrt, translation, rotation
        )


class OpeningSemantics(FloorPlanElement):
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
        translation = self.location.translation
        rotation = self.location.rotation
        if self.location.rotation is None:
            rotation = EulerAngles(self, y=0.0)

        if self.location.translation is None:
            translation = PointCoordinate(self, x=0.0, z=0.0)

        return PoseCoordinate(
            self, self.frame, self.location.walls[0], translation, rotation
        )
