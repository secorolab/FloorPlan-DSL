import numpy as np

from .geometry import Frame
from .helpers import get_value, angle_from_rotation


class Wall:
    """
    A class to represent a wall.

    ...

    Attributes
    ----------
    point_a : numpy Array
        Starting point of the wall, expressed wrt the reference frame
    point_b : numpy Array
        End point of the wall, expressed wrt the reference frame
    ref_frame : Frame
        Reference frame for the frame of the wall
    frame : Frame
        Frame of the wall concept
    polygon : numpy Array
        Polygon that describes the boundary of the wall in the 3D world
    thickness : Float
        thickness of the wall
    height : Float
        Height of the wall

    Methods
    -------
    get_points()
        returns the starting and end points of the wall wrt to the world frame
    get_frame()
        returns the frame of the wall concept
    set_wall_polygon(points)
        sets the boundary polygon of the wall concept
    generate_3d_structure()
        returns the vertices and faces of the wall polytope to generate a 3D
        mesh of the wall
    """

    def __init__(self, point_a, point_b, ref_frame, thickness, height, parent, index):
        """
        Constructs the wall object

        Parameters
        ----------
        point_a : numpy Array
                Starting point of the wall, expressed wrt the reference frame
        point_b : numpy Array
            End point of the wall, expressed wrt the reference frame
        ref_frame : Frame
            Reference frame for the frame of the wall
        frame : Frame
            Frame of the wall concept
        polygon : numpy Array
            Polygon that describes the boundary of the wall in the 3D world
        thickness : Float
            thickness of the wall
        height : Float
            Height of the wall

        Returns
        -------
        None
        """
        self.point_a = point_a
        self.point_b = point_b
        self.ref_frame = ref_frame
        self.frame = Frame(ref_frame)
        self.polygon = []
        self.thickness = thickness
        self.height = height
        self.parent = parent
        self.index = index

        self.name = "{space}.wall{index}".format(
            space=self.parent.name, index=self.index
        )

        # determine middle point of wall and calculate x vector
        middle = (point_a + point_b) / 2
        vector = (point_b - point_a) / np.linalg.norm(point_b - point_a)
        origin, vectors = self.ref_frame.get_direction_vectors(self.ref_frame)

        # determine the angle of the frame
        angle = np.arccos(np.clip(np.dot(vector, vectors[0]), -1.0, 1.0))
        if vector[1] < 0:
            angle *= -1

        # set the translation and angle wrt to the reference frame
        self.frame.set_translation((middle - origin)[0:3])
        self.frame.set_orientation(0, 0, angle)

    def get_points(self):
        """
        Returns the starting and end points of the wall wrt to the world frame

        Parameters
        ----------
        None

        Returns
        -------
        points : numpy Array
            Starting and end points expressed wrt the world frame
        """

        return self.ref_frame.get_points(np.array([self.point_a, self.point_b]))

    def get_frame(self):
        """
        Returns the frame of the wall object

        Parameters
        ----------
        None

        Returns
        -------
        frame : Frame
            Frame of the wall object
        """

        return self.frame

    def set_wall_polygon(self, points):
        """
        Sets the boundary polygon of the wall concept

        Parameters
        ----------
        points : numpy Array
            points describing the boundary polygon of the wall in 2D, points
            expressed wrt of the reference frame of the wall/frame of the space

        Returns
        -------
        None
        """

        self.polygon = np.array(points)

    def generate_3d_structure(self):
        """
        returns the vertices and faces of the wall polytope to generate a 3D
        mesh of the wall

        Parameters
        ----------
        None

        Returns
        -------
        vertices : numpy Array
            Array of vertices describing the polytope of the wall in the 3D
            world
        faces : Matrix
            Matrix that describe the vertices that form a face of the mesh.
            Each row containt the index of the vertices that form the face.
            This matrix is constant.
        """

        elevated_polygon = np.copy(self.polygon)
        elevated_polygon[:, 2] = get_value(self.height)

        vertices = np.concatenate((self.polygon, elevated_polygon), axis=0)
        vertices = np.hstack((vertices, np.ones((len(vertices), 1))))

        # The points of the polygon are expressed from the perspective of the
        # frame of reference and not the internal frame of the wall
        vertices = self.ref_frame.get_point_transformation_wrt(vertices)[:, 0:3]

        # The faces (group of vertices) for this concept are constant
        faces = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [1, 2, 6, 5],
            [2, 3, 7, 6],
            [3, 0, 4, 7],
        ]

        return vertices, faces

    def get_wall_origin_coord(self):
        origin, vectors = self.get_frame().get_direction_vectors(
            self.get_frame().ref
        )
        theta = angle_from_rotation(vectors)
        return origin, theta

