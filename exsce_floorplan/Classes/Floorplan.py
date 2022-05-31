from .Polytope import *
from .Geometry import Frame

class Wall():

    def __init__(self, point_a, point_b, ref_frame):
        self.point_a = point_a
        self.point_b = point_b
        self.ref_frame = ref_frame
        self.frame = Frame(ref_frame)

        middle = (point_a + point_b)/2 
        vector = (point_b - point_a)/np.linalg.norm(point_b - point_a)

        origin, vectors = self.ref_frame.get_direction_vectors(self.ref_frame)

        angle = np.arccos(np.clip(np.dot(vector, vectors[0]), -1.0, 1.0))
        if vector[1] < 0:
            angle *= -1 
        self.frame.set_translation((middle - origin)[0:3])
        self.frame.set_orientation(0, 0, angle)

    def get_points(self):
        return self.ref_frame.get_points(np.array([self.point_a, self.point_b]))

    def get_frame(self):
        return self.frame

class Space(object):

    def __init__(self, parent, name, shape, location, floor_features):
        self.parent = parent
        self.name = name
        self.shape = shape
        self.location = location
        self.floor_features = floor_features

    def locate_space(self, from_frame, to_frame, T, wall_to_wall=False):

        self.shape.change_reference_frame(from_frame)

        if wall_to_wall:
            frame = Frame()
            frame.set_orientation(0, 0, np.deg2rad(180))
            t, R = frame.get_transformation()
            T[0:3, 0:3] = R.dot(T[0:3, 0:3])
        
        t_a, R_a = to_frame.get_transformation()

        po_p_T = np.hstack((np.vstack((R_a, np.zeros(3))), np.vstack((t_a.reshape((3,1)), [1]))))
        p_w_T = T.dot(np.linalg.inv(po_p_T))

        self.shape.set_transformation(p_w_T)

    def get_frame(self):
        return self.shape.frame

    def get_shape(self):
        return self.shape

    def create_walls(self):
        points = self.shape.get_points(self.shape.frame)
        points = np.vstack((points, points[0]))
        self.walls = [Wall(p1, p2, self.shape.frame) for p1, p2 in 
                    zip(points[:-1], points[1:])]

    def offset_room(self):
        pass
