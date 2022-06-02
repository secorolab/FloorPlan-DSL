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
    set_transformation()
        sets the transformation of polytope the frame
    change_reference_frame()
        changes the reference frame for the polytope frame
    get_frame()
        returns the polytope frame
    '''

    def __init__(self, parent, frame):
        '''
        constructor of the polytope class

        Parameters
        ----------
        parent : Textx object
            Textx requirement, parent class for this object
        frame : Frame
            Frame of reference for the polytope points that define its boundary

        Returns
        -------
        None
        '''

        self.parent = parent
        self.frame = frame
        self.points = np.array([])

    def set_points(self, points=np.array([])):
        '''
        sets the points for the that define its boundary wrt to the polytope
        frame

        Parameters
        ----------
        points : numpy array
            list of 3D points that define the boundary of the polytope

        Returns
        -------
        None
        '''

        self.points = points

    def get_points(self, wrt=None):
        '''
        returns the boundary points wrt to a specified frame

        Parameters
        ----------
        wrt : Frame
            Frame of reference for the points


        Returns
        -------
        points : numpy array
            array of 3D points with an extra row for calculation 
        '''

        points = np.hstack(
            (copy.copy(self.points), np.ones((len(self.points), 1)))
            )
        return self.frame.get_point_transformation_wrt(points, wrt)

    def translation(self, x, y, z=0):
        '''
        translate the polytope in the x, y, and z dimensions

        Parameters
        ----------
        x : float
            translation in x
        y : float
            translation in y
        z : float
            translation in z (optional)

        Returns
        -------
        None
        '''

        self.frame.set_translation(np.array([x, y, z]))

    def rotation(self, angle, rad=False):
        '''
        rotates the polytope in the z direction

        Parameters
        ----------
        angle : float
            Angle in degrees
        rad : bool
            (optional) when False the angle is specified in degrees, when True
            the angle is specified in radians. Default is False. 

        Returns
        -------
        None
        '''

        if not rad:
            angle = np.deg2rad(angle)
        self.frame.set_orientation(0, 0, angle)

    def set_transformation(self, T):
        '''
        Sets the transformation (position and orientation) of the polytope 
        using the homogeneous transformation matrix

        Parameters
        ----------
        T : numpy array
            4x4 homogeneous transformation matrix

        Returns
        -------
        None
        '''

        self.frame.set_translation(T[0:3, 3])
        self.frame.set_rotation_matrix(T[0:3, 0:3])

    def change_reference_frame(self, new_frame):
        '''
        Change the reference frame of the polytope

        Parameters
        ----------
        new_frame : Frame
            new frame of reference

        Returns
        -------
        None
        '''

        self.frame.change_reference_frame(new_frame)

    def get_frame(self):
        '''
        returns the polytope frame 

        Parameters
        ----------
        None

        Returns
        -------
        frame : Frame
            frame of polytope
        '''

        return self.frame

class Rectangle(Polytope):
    '''
    Class to represent a rectangle.

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
    w : float
        width of rectangle 
    l : float
        lenght of rectangle
    '''

    def __init__(self, parent, frame, w, l):
        '''
        constructor of the rectangle class

        Parameters
        ----------
        parent : Textx object
            Textx requirement, parent class for this object
        frame : Frame
            Frame of reference for the polytope points that define its boundary
        w : float
            width of rectangle 
        l : float
            lenght of rectangle

        Returns
        -------
        None
        '''

        super().__init__(parent, frame)
        self.w = w
        self.l = l
        
        w = self.w /2
        l = self.l/2

        self.set_points(np.array([
            [-w, l, 0], 
            [w, l, 0], 
            [w, -l, 0], 
            [-w, -l, 0]
        ]))    

class Polygon(Polytope):
    '''
    Class to represent a custom polygon.

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
    '''
    
    def __init__(self, parent, frame, points):
        '''
        constructor of the Polygon class

        Parameters
        ----------
        parent : Textx object
            Textx requirement, parent class for this object
        frame : Frame
            Frame of reference for the polytope points that define its boundary
        points : numpy array
            Points that define the boundary of the space wrt to the polytope
            frame

        Returns
        -------
        None
        '''

        super().__init__(parent, frame)
        self.set_points(np.hstack((points, np.zeros((len(points), 1)))))

class Circle(Polytope):
    '''
    Class to represent a  circle.

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
    r : float
        Radius of the circle
    '''
    
    def __init__(self, parent, frame, radius):
        '''
        constructor of the Circle class

        Parameters
        ----------
        parent : Textx object
            Textx requirement, parent class for this object
        frame : Frame
            Frame of reference for the polytope points that define its boundary
        radius : float
            radius of the circle

        Returns
        -------
        None
        '''

        super().__init__(parent, frame)
        self.r = radius
        arc_definition = 40
        arc_interval = 360.0/arc_definition
        points = [
            [self.r * np.sin(np.deg2rad(a)), 
            self.r * np.cos(np.deg2rad(a)), 
            0] for a in np.arange(0, 360, arc_interval)]
        self.set_points(np.array(points))

# Experimental - Not part of the final tooling
class RegularPolygon(Polytope):

    def __init__(self, parent, frame, radius, vertices):
        '''
        description

        Parameters
        ----------

        Returns
        -------
        '''

        super().__init__(parent, frame)
        self.r = radius
        self.vertices = vertices
        arc_interval = 360.0/self.vertices
        points = [
            [self.r * np.sin(np.deg2rad(a)), 
            self.r * np.cos(np.deg2rad(a)), 
            0] for a in np.arange(0, 360, arc_interval)]
        self.set_points(np.array(points))