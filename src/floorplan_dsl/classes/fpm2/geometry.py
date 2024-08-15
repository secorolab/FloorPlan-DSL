import numpy as np

from textx.exceptions import TextXSemanticError, TextXSyntaxError
from textx import textx_isinstance, get_metamodel

from floorplan_dsl.classes.fpm2.qudt import Length, Angle


class PointCoordinate:
    def __init__(self, parent, x=None, y=None, z=None) -> None:
        self.parent = parent
        self.x = self._get_value(x)
        self.y = self._get_value(y)
        self.z = self._get_value(z)

    def _get_value(self, value):
        if value is None:
            return Length(self)
        elif isinstance(value, int) or isinstance(value, float):
            return Length(self, value)

        mm = get_metamodel(value)
        if textx_isinstance(value, mm["VariableReference"]):
            return value
        elif textx_isinstance(value, mm["Length"]):
            return value


class EulerAngles:
    def __init__(self, parent, x=None, y=None, z=None) -> None:
        self.parent = parent
        self.x = self._get_value(x)
        self.y = self._get_value(y)
        self.z = self._get_value(z)

    def _get_value(self, value):
        if value is None:
            return Angle(self)
        elif isinstance(value, int) or isinstance(value, float):
            return Angle(self, value)

        mm = get_metamodel(value)
        if textx_isinstance(value, mm["VariableReference"]):
            return value
        elif textx_isinstance(value, mm["Angle"]):
            return value


class Point:
    def __init__(self, parent, name) -> None:
        self.parent = parent
        self.name = name


class Frame:
    def __init__(self, parent, name, origin=None) -> None:
        self.parent = parent
        self.name = "{}-frame".format(name)
        if origin is None:
            self.origin = Point(self, "{}-origin".format(name))
        else:
            self.origin = origin


# TODO Utils to determine frame poses wrt one another. Move to apropriate module
def _get_unit_vector(vector):
    # Inputs need to be transformed to unit vectors so we can use np.arccos
    return vector / np.linalg.norm(vector)


def get_angle_between_vectors(v1, v2):
    # Adapted from https://stackoverflow.com/a/13849249
    u1 = _get_unit_vector(v1)
    u2 = _get_unit_vector(v2)

    sign = 1
    if u1[1] < 0:
        sign = -1
    return sign * np.rad2deg(np.arccos(np.dot(u1, u2)))


class PositionCoordinate:
    def __init__(self, parent, translation, of, wrt) -> None:
        self.parent = parent
        self.translation = translation
        self.of = of
        self.wrt = wrt
        self.name = "position-{}-wrt-{}".format(of.name, wrt.name)


class PoseCoordinate:
    def __init__(self, parent, of, wrt, translation=None, orientation=None) -> None:
        self.parent = parent
        self.of = of
        self.wrt = wrt
        self.translation = translation
        self.orientation = orientation
        self.name = "pose-{}-wrt-{}".format(of.name, wrt.name)

    # TODO Move to right place
    @classmethod
    def wall_wrt_parent_space(cls, wall):
        x, y, theta = wall.get_wall_origin_pose_coord()
        rotation = EulerAngles(wall, z=theta)
        translation = PointCoordinate(wall, x, y)
        return cls(wall, wall.frame, wall.parent.frame, translation, rotation)

    @classmethod
    def opening_wrt_wall(cls, opening):
        translation = opening.location.translation
        rotation = opening.location.rotation
        if opening.location.rotation is None:
            rotation = EulerAngles(opening, y=0.0)

        if opening.location.translation is None:
            translation = PointCoordinate(opening, x=0.0, z=0.0)

        return cls(
            opening, opening.frame, opening.location.walls[0], translation, rotation
        )

    @classmethod
    def feature_wrt_space(cls, feature):
        translation = feature.location.translation
        rotation = feature.location.rotation
        if feature.location.rotation is None:
            rotation = EulerAngles(feature, z=0.0)

        if feature.location.translation is None:
            translation = PointCoordinate(feature, x=0.0, y=0.0)

        return cls(feature, feature.frame, feature.location.wrt, translation, rotation)


class Polytope:
    pass


class Rectangle(Polytope):
    def __init__(
        self, parent, width, length, height, coordinates=None, points=None, center=True
    ) -> None:
        self.parent = parent
        self.width = width
        if length is None and height is None:
            raise TextXSyntaxError("Missing length or height values")
        elif length is not None and height is not None:
            raise TextXSyntaxError("Only length or height must be defined")

        self.length = length
        self.height = height
        self.coordinates = self.get_point_coordinates(
            self.width, self.length, self.height
        )
        self.points = points

    def get_point_coordinates(self, width, length, height, center=True):
        x = width.value / 2

        if length is not None:
            y = length.value / 2
            coords = [
                PointCoordinate(self, -x, y, 0.0),
                PointCoordinate(self, x, y, 0.0),
                PointCoordinate(self, x, -y, 0.0),
                PointCoordinate(self, -x, -y, 0.0),
            ]
        elif height is not None:
            z = height.value / 2
            coords = [
                PointCoordinate(self, -x, 0.0, z),
                PointCoordinate(self, x, 0.0, z),
                PointCoordinate(self, x, 0.0, -z),
                PointCoordinate(self, -x, 0.0, -z),
            ]

        return coords


class Circle(Polytope):
    def __init__(self, parent, radius) -> None:
        self.parent = parent
        self.radius = radius
        self.coordinates = list()


class Polygon(Polytope):
    def __init__(self, parent, coordinates, points=None) -> None:
        self.parent = parent
        self.coordinates = coordinates
        self.points = points

    # TODO Move this to interpreter
    @classmethod
    def from_wall(cls, wall, corners=4):
        points = [
            Point(wall, "{}-corner-{}".format(wall.name, i)) for i in range(corners)
        ]

        poly = cls(wall, list(), points)

        x = wall.width / 2
        coords = [
            PointCoordinate(poly, -x, 0.0, 0.0),
            PointCoordinate(poly, -x, wall.thickness, 0.0),
            PointCoordinate(poly, x, wall.thickness, 0.0),
            PointCoordinate(poly, x, 0.0, 0.0),
        ]

        poly.coordinates = coords

        return poly
