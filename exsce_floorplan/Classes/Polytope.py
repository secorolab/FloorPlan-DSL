from .Geometry import Frame
import copy
import numpy as np

class Polytope(object):
    '''
    An abstract class to represent a polytope.

    ... 

    Attributes
    ----------
    parent : object
        TextX requirement
    frame : Frame
        Refernce frame for the polytope
    points : Numpy array
        Group of points that bound the polytope, specified wrt the polytope 
        frame

    Methods
    -------
    set_points(points)
        sets the points that bound the polytope wrt the polytope frame.
    get_points(wrt=None)
        returns the points from the perspective of the specified frame (default
        is world frame)
    translation(x, y, z=0)
        sets the position of the polytope frame wrt to the reference frame
    rotation(angle, rad=False)
        sets the orientation of the polytope in the z axis. 
    get_frame()
        returns the polytope frame
    '''
    def __init__(self, parent, frame):
        self.__parent = parent
        self.__frame = Frame(frame)
        self.__points = np.array([])

    def set_points(self, points=[]):
        self.__points = np.array(points)

    def get_points(self, wrt=None):
        points = np.hstack(
            (copy.copy(self.__points), np.ones((len(self.__points), 1)))
            )
        return self.__frame.get_point_transformation_wrt(points, wrt)

    def translation(self, x, y, z=0):
        self.__frame.set_translation(np.array([x, y, z]))

    def rotation(self, angle, rad=False):
        if not rad:
            angle = np.deg2rad(angle)
        self.__frame.set_orientation(0, 0, angle)

    def get_frame(self):
        return self.__frame

class Rectangle(Polytope):

    def __init__(self, parent, frame, w, l):
        super().__init__(parent, frame)
        self.__w = w
        self.__l = l
        self.generate()

    def generate(self):
        w = self.__w /2
        l = self.__l/2

        self.set_points(np.array([
            [-w, l, 0], 
            [w, l, 0], 
            [w, -l, 0], 
            [-w, -l, 0]
        ]))

class Polygon(Polytope):
    
    def __init__(self, parent, frame, points):
        super().__init__(parent, frame)
        self.set_points(np.hstack((points, np.zeros((len(points), 1)))))

class Circle(Polytope):
    
    def __init__(self, parent, frame, radius):
        super().__init__(parent, frame)
        self.__r = radius
        self.generate()

    def generate(self):
        arc_definition = 40
        arc_interval = 360.0/arc_definition
        points = [[self.__r * np.cos(np.deg2rad(a)), self.__r * np.sin(np.deg2rad(a)), 0] for a in np.arange(0, 360, arc_interval)]
        self.set_points(np.array(points))

# Experimental - Not part of the final tooling
class RegularPolygon(Polytope):

    def __init__(self, parent, frame, radius, vertices):
        super().__init__(parent, frame)
        self.__r = radius
        self.__vertices = vertices
        self.generate()

    def generate(self):
        arc_interval = 360.0/self.__vertices
        points = [[self.__r * np.cos(np.deg2rad(a)), self.__r * np.sin(np.deg2rad(a)), 0] for a in np.arange(0, 360, arc_interval)]
        self.set_points(np.array(points))