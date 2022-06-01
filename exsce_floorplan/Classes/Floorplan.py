from .Polytope import *
from .Geometry import Frame

class Wall():

    def __init__(self, point_a, point_b, ref_frame):
        self.point_a = point_a
        self.point_b = point_b
        self.ref_frame = ref_frame
        self.frame = Frame(ref_frame)
        self.polygon = []

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

    def set_wall_polygon(self, points):
        self.polygon = points

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

    def offset_shape(self, widths=0.3):

        if type(widths) is int or type(widths) is float: 
            widths = [widths for i in range(len(self.walls))]
        
        num_vertices = len(self.shape.points)
        new_vertices = []

        for i, (wall, width) in enumerate(zip(self.walls, widths)):
            
            # find equation for line at width distance from the internal wall 
            # border
            prev_wall = self.walls[i-1]

            points_line1 = np.array([[-1, width, 0, 1], [1, width, 0, 1]])
            points_line2 = np.array([[-1, widths[i-1], 0, 1], [1, widths[i-1], 0, 1]])

            points_line1 = wall.frame.get_point_transformation_wrt(points_line1, self.shape.frame)[:,0:2]
            points_line2 = prev_wall.frame.get_point_transformation_wrt(points_line2, self.shape.frame)[:,0:2]

            a1, a2 = points_line1
            b1, b2 = points_line2

            point = []

            # method source: https://stackoverflow.com/questions/3252194/numpy-and-line-intersections
            s = np.vstack([a1,a2,b1,b2])        # s for stacked
            h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
            l1 = np.cross(h[0], h[1])           # get first line
            l2 = np.cross(h[2], h[3])           # get second line
            x, y, z = np.cross(l1, l2)          # point of intersection
            if z == 0:                          # lines are parallel
                point = (float('inf'), float('inf'))
            point = (x/z, y/z)
            new_vertices.append([point[0], point[1], 0])
        
        for i, wall in enumerate(self.walls):
            next_point = (i + 1) % num_vertices
            wall.set_wall_polygon([new_vertices[i], new_vertices[next_point], 
                self.shape.points[next_point], self.shape.points[i]])

    def get_walls_wrt_world(self):
        wall_points = []

        for wall in self.walls:
            points = np.hstack(
                (np.array(wall.polygon), np.ones((len(wall.polygon), 1)))
            )
            wall_points.append(self.shape.frame.get_point_transformation_wrt(points))

        return wall_points