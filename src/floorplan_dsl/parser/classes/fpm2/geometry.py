import numpy as np

from textx.exceptions import TextXSemanticError, TextXSyntaxError
from textx import textx_isinstance, get_metamodel

from floorplan_dsl.parser.classes.fpm2.qudt import Length, Angle


class PointCoordinate:
    def __init__(self, parent, x, y, z) -> None:
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
        else:
            raise TextXSyntaxError("Wrong type of value")


class Frame:
    def __init__(self, parent, name, origin=None) -> None:
        self.parent = parent
        self.name = "{}-frame".format(name)
        self.origin = origin


class Polytope:
    pass


class Rectangle(Polytope):
    def __init__(self, parent, width, length, height, points=None, center=True) -> None:
        self.parent = parent
        self.width = width
        if length is None and height is None:
            raise TextXSyntaxError("Missing length or height values")
        elif length is not None and height is not None:
            raise TextXSyntaxError("Only length or height must be defined")

        self.length = length
        self.height = height
        self.points = self.get_points(self.width, self.length, self.height)

    def get_points(self, width, length, height, center=True):
        x = width.value / 2

        if length is not None:
            y = length.value / 2
            points = [
                PointCoordinate(self, -x, y, 0.0),
                PointCoordinate(self, x, y, 0.0),
                PointCoordinate(self, x, -y, 0.0),
                PointCoordinate(self, -x, -y, 0.0),
            ]
        elif height is not None:
            z = height.value / 2
            points = [
                PointCoordinate(self, -x, 0.0, z),
                PointCoordinate(self, x, 0.0, z),
                PointCoordinate(self, x, 0.0, -z),
                PointCoordinate(self, -x, 0.0, -z),
            ]

        return points


class Polygon(Polytope):
    def __init__(self, parent, points) -> None:
        self.parent = parent
        self.points = points
