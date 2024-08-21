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

    @property
    def rotation(self):
        return self.orientation


class Polytope:
    pass


class Rectangle(Polytope):
    def __init__(
        self, parent, width, length, height, coordinates=None, points=None, center=True
    ) -> None:
        self.parent = parent
        self.width = width

        self.length = length
        self.height = height
        self.coordinates = self.get_point_coordinates(
            self.width, self.length, self.height
        )
        self.points = points

    def get_point_coordinates(self, width, length, height):
        x = width.value / 2

        coords = list()
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
