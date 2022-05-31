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
        self.parent = parent
        self.frame = Frame(frame)
        self.points = np.array([])

    def set_points(self, points=[]):
        self.points = np.array(points)

    def get_points(self, wrt=None):
        points = np.hstack(
            (copy.copy(self.points), np.ones((len(self.points), 1)))
            )
        return self.frame.get_point_transformation_wrt(points, wrt)

    def translation(self, x, y, z=0):
        self.frame.set_translation(np.array([x, y, z]))

    def rotation(self, angle, rad=False):
        if not rad:
            angle = np.deg2rad(angle)
        self.frame.set_orientation(0, 0, angle)

    def set_transformation(self, T):
        self.frame.set_translation(T[0:3, 3])
        self.frame.set_rotation_matrix(T[0:3, 0:3])

    def change_reference_frame(self, new_frame):
        self.frame.change_reference_frame(new_frame)

    def get_frame(self):
        return self.frame

class Rectangle(Polytope):

    def __init__(self, parent, frame, w, l):
        super().__init__(parent, frame)
        self.w = w
        self.l = l
        self.generate()

    def generate(self):
        w = self.w /2
        l = self.l/2

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
        self.r = radius
        self.generate()

    def generate(self):
        arc_definition = 40
        arc_interval = 360.0/arc_definition
        points = [[self.r * np.cos(np.deg2rad(a)), self.r * np.sin(np.deg2rad(a)), 0] for a in np.arange(0, 360, arc_interval)]
        self.set_points(np.array(points))

# Experimental - Not part of the final tooling
class RegularPolygon(Polytope):

    def __init__(self, parent, frame, radius, vertices):
        super().__init__(parent, frame)
        self.r = radius
        self.vertices = vertices
        self.generate()

    def generate(self):
        arc_interval = 360.0/self.vertices
        points = [[self.r * np.cos(np.deg2rad(a)), self.r * np.sin(np.deg2rad(a)), 0] for a in np.arange(0, 360, arc_interval)]
        self.set_points(np.array(points))