import numpy as np

def from_ref_name(from_frame):
    '''Return the name of the reference frame'''

    if from_frame.world is True:
        return "world-frame"
    elif not from_frame.ref is None: 
        if not from_frame.index is None:
            return "frame-{name}-wall-{number}".format(name=from_frame.ref.name, number=from_frame.index)
        else:
            return "frame-center-{name}".format(name=from_frame.ref.name)

def to_ref_name(to_frame, space):
    '''Return the name of the to frame'''
    if not to_frame.index is None:
        return "frame-{name}-wall-{number}".format(name=space.name, number=to_frame.index)
    else:
        return "frame-center-{name}".format(name=space.name)

def angle_from_rotation(vectors):

    vector1 = [1, 0]
    vector2 = vectors[0, 0:2]
    
    unit_vector1 = vector1 / np.linalg.norm(vector1)
    unit_vector2 = vector2 / np.linalg.norm(vector2)

    angle = np.degrees(np.math.atan2(np.linalg.det([unit_vector1, unit_vector2]),np.dot(unit_vector1, unit_vector2)))
    return angle