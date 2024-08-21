import numpy as np


class Transformation:
    @staticmethod
    def get_rotation_matrix(gamma=0.0, beta=0.0, alpha=0.0):
        """
        Sets the orientation by calculating the rotation matrix

        Parameters
        ----------
        gamma: float
            Angle in radians for the rotation with respect to the X axis
        beta: float
            Angle in radians for the rotation with respect to the Y axis
        alpha: float
            Angle in radians for the rotation with respect to the Z axis

        """

        rx = np.array(
            [
                [1, 0, 0],
                [0, np.cos(gamma), -np.sin(gamma)],
                [0, np.sin(gamma), np.cos(gamma)],
            ]
        )

        ry = np.array(
            [
                [np.cos(beta), 0, np.sin(beta)],
                [0, 1, 0],
                [-np.sin(beta), 0, np.cos(beta)],
            ]
        )

        rz = np.array(
            [
                [np.cos(alpha), -np.sin(alpha), 0],
                [np.sin(alpha), np.cos(alpha), 0],
                [0, 0, 1],
            ]
        )

        return rz.dot(ry.dot(rx))

    @classmethod
    def get_rotation_matrix_from_model(cls, model):
        x, y, z = (0, 0, 0)
        if model.x:
            x = model.x.value
        if model.y:
            y = model.y.value
        if model.z:
            z = model.z.value
        return cls.get_rotation_matrix(x, y, z)

    @staticmethod
    def get_translation_vector(x=0.0, y=0.0, z=0.0):
        return np.array([x, y, z])

    @classmethod
    def get_translation_vector_from_model(cls, model):
        return cls.get_translation_vector(model.x.value, model.y.value, model.z.value)

    @classmethod
    def get_transformation_matrix(cls, t=None, r=None):
        """
        Returns the 4x4 transformation matrix

        Parameters
        ----------
        t: numpy array for the translation matrix
        r: numpy array for the rotation matrix

        Returns
        -------
        T : numpy array
            The 4x4 transformation matrix
        """
        if r is None:
            r = cls.get_rotation_matrix()
        rotation = np.vstack((r, np.zeros(3)))

        if t is None:
            t = cls.get_translation_vector()
        translation = np.vstack((t.reshape(3, 1), np.array([1])))

        return np.hstack((rotation, translation))

    @classmethod
    def get_transformation_matrix_from_model(cls, model):
        if model.translation is None:
            t = cls.get_translation_vector()
        else:
            t = cls.get_translation_vector_from_model(model.translation)

        if model.rotation is None:
            r = cls.get_rotation_matrix()
        else:
            r = cls.get_rotation_matrix_from_model(model.rotation)
        return cls.get_transformation_matrix(t, r)

    @staticmethod
    def transform(of, wrt):
        """Return the transformation matrix resulting from the dot product of two 4x4 transformation matrices"""
        return of.dot(np.linalg.inv(wrt))

    # @staticmethod
    # def _get_spaced_matrix(y):
    #     t = Transformation.get_translation_vector(y=y)
    #     r = Transformation.get_rotation_matrix()
    #     return Transformation.get_transformation_matrix(t, r)
    #
    # @staticmethod
    # def _get_aligned_matrix():
    #     import numpy as np
    #
    #     t = Transformation.get_translation_vector()
    #     r = Transformation.get_rotation_matrix(alpha=np.deg2rad(180))
    #     return Transformation.get_transformation_matrix(t, r)
    #
    # @staticmethod
    # def _transformation_matrix_to_models(T):
    #     translation = None
    #     rotation = None
    #     return translation, rotation
