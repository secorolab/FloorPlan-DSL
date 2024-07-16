import numpy as np


def get_value(variable):
    """Helper function to retrive a numeric value from the model"""

    if variable is None:
        return 0
    elif not variable.ref is None:
        return (
            variable.ref.value.value
            if variable.neg is False
            else (variable.ref.value.value * (-1))
        )
    else:
        return variable.value.value


def angle_from_rotation(vectors):

    vector1 = [1, 0]
    vector2 = vectors[0, 0:2]

    unit_vector1 = vector1 / np.linalg.norm(vector1)
    unit_vector2 = vector2 / np.linalg.norm(vector2)

    angle = np.degrees(
        np.math.atan2(
            np.linalg.det([unit_vector1, unit_vector2]),
            np.dot(unit_vector1, unit_vector2),
        )
    )
    return angle