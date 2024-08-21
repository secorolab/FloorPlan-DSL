import numpy as np

from floorplan_dsl.utils.transformations import Transformation

cos = np.cos
sin = np.sin
rad = np.deg2rad
array = np.array


class Frame:
    """
    A class to represent a coordinate frame.

    ...

    Attributes
    ----------
    ref : Frame, optional
        The reference frame for the translation and rotation of this frame (no
        reference frame means that this is the world frame).
    t : Numpy array
        3-dimensional vector with the translation from the perspective of the
        reference frame.
    R : Numpy array
        Rotation matrix for the orientation of the frame from the perspective
        of the reference frame.

    Methods
    -------
    set_translation(t)
        sets the translation of the frame wrt to the reference frame.
    set_orientation(gamma, beta, alpha)
        sets the orientation of the frame wrt to the reference frame.
    get_transformation()
        returns the translation and rotation matrix for the frame.
    get_transformation_matrix()
        returns the 4x4 transformation matrix
    set_rotation_matrix(R)
        sets the rotation matrix directly
    get_reference_frame()
        returns the reference frame
    change_reference_frame(new_frame)
        set the new reference frame
    get_point_transformation_wrt(points, wrt=None)
        transforms a group of points defined wrt the frame to a specified frame,
        the default is the world frame.
    get_direction_vectors(wrt=None)
        returns the origin and unit vectors of the frame wrt to a specified
        frame, the default is the world frame.
    """

    def __init__(self, ref_frame=None):
        """
        Constructs the frame, set the initial values for the translation and
        rotation.

        Parameters
        ----------
        ref_frame : Frame, optional
            The reference frame for the translation and rotation of this frame
            (no reference frame means that this is the world frame).

        Returns
        -------
        None
        """

        self.t = array([0.0, 0.0, 0.0])  # translation
        self.R = np.identity(3)  # rotation
        self.ref = ref_frame  # reference frame

    def set_translation(self, t):
        """
        Sets the translation

        Parameters
        ----------
        t : Numpy array
            3-dimensional vector

        Returns
        -------
        None
        """

        self.t = t

    def set_orientation(self, gamma, beta, alpha):
        self.R = Transformation.get_rotation_matrix(gamma, beta, alpha)

    def get_transformation(self):
        """
        returns the position and the orientation of the frame wrt to the
        reference frame

        Parameters
        ----------
        None

        Returns
        -------
        t : numpy array
            A 3-dimensional vector
        R : numpy array
            The rotation matrix (3x3)
        """

        return self.t, self.R

    def get_transformation_matrix(self):
        return Transformation.get_transformation_matrix(self.t, self.R)

    def set_rotation_matrix(self, R):
        """
        sets the rotation matrix directly

        Parameters
        ----------
        R : numpy array
            The 3x3 rotation matrix

        Returns
        -------
        None
        """
        self.R = R

    def get_reference_frame(self):
        """
        returns the reference frame

        Parameters
        ----------
        None

        Returns
        -------
        ref : Frame
            the reference frame
        """

        return self.ref

    def change_reference_frame(self, new_frame):
        """
        Changes the reference frame for the frame

        Parameters
        ----------
        new_frame : Frame
            the new reference frame

        Returns
        -------
        None
        """
        self.ref = new_frame

    def get_point_transformation_wrt(self, points, wrt=None):
        """
        calculates the transformation of a group of points that are specified
        with respect to the frame to another specified frame.

        Parameters
        ----------
        points : numpy array
            The array of points to be transformed, each point must be described
            in a 4D vector with the last value set to 1: [x, y, z, 1]
        wrt : Frame, optional
            new reference frame for the points, default is world frame
        Returns
        -------
        points : numpy array
            The matrix with the points transformed
        """
        # calculate the transformation for this frame wrt a specified frame
        frame = self
        while True:

            # break loop if we arrived at frame of reference, default is world
            if (frame.get_reference_frame() is None) or (frame is wrt):
                break

            T = frame.get_transformation_matrix()

            # calculate transformation up to current frame
            points = np.einsum("ij,kj->ki", T, points)

            # get the next frame
            frame = frame.get_reference_frame()

        return points

    def get_direction_vectors(self, wrt=None):
        """
        returns the origin and direction of the orthonormal vectors describing
        the frame axis using the (x, y, z) convention wrt another frame.

        Parameters
        ----------
        wrt : Frame, optional
            reference frame for vectors, default is world frame
        Returns
        -------
        origin : numpy array
            the origin of the frame wrt the specified frame.
        vectors : numpy array
            Array of direction vectors for the orthonormal axis.
        """

        points = array(
            [
                array([0.0, 0.0, 0.0, 1.0]),  # origin
                array([1.0, 0.0, 0.0, 1.0]),  # x
                array([0.0, 1.0, 0.0, 1.0]),  # y
                array([0.0, 0.0, 1.0, 1.0]),  # z
            ]
        )

        frame = self

        points = self.get_point_transformation_wrt(points, wrt)

        x = (points[1] - points[0]) / np.linalg.norm(points[1] - points[0])
        y = (points[2] - points[0]) / np.linalg.norm(points[2] - points[0])
        z = (points[3] - points[0]) / np.linalg.norm(points[3] - points[0])

        return points[0], array([x, y, z])
