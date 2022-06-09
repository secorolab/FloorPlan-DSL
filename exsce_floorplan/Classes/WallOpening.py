import numpy as np 

class WallOpening(object):

    def __init__(self, parent, wall_a, wall_b, shape, loc, entryway, window, name):
        self.parent = parent
        self.wall_a = wall_a.ref.get_wall(wall_a.index)
        self.shape = shape
        self.loc = loc
        self.name = name

        if not wall_b is None:
            self.wall_b = wall_b.ref.get_wall(wall_b.index)
        else:
            self.wall_b = None

        self.determine_thickness()
        self.locate()
        
    def determine_thickness(self):
        thickness = self.wall_a.thickness

        if not self.wall_b is None:
            thickness += self.wall_b.thickness

        self.thickness = thickness

    def locate(self):
        frame = self.wall_a.get_frame()
        self.shape.change_reference_frame(frame)
        
        t = np.array([self.loc.pos.x.value, self.loc.pos.y.value, self.loc.pos.z.value])
        rot = self.loc.rot.value 

        self.shape.frame.set_translation(t)
        self.shape.frame.set_orientation(0, np.deg2rad(rot), 0)

    def get_points(self):
        return self.shape.get_points()

    def generate_3d_structure(self):
        vertices = self.shape.get_points(self.shape.frame)[:, 0:3]
        origin, _ = self.wall_a.frame.get_transformation()
        
        # Modifications to the vertices made to avoid face clashing
        threshold = 0.01
        modifications = np.where(origin[2] == vertices[:,2], -threshold, 0)
        modifications += np.where(self.wall_a.height == vertices[:,2], threshold, 0)
        if not self.wall_b is None:
            modifications += np.where(self.wall_b.height == vertices[:,2], threshold, 0)

        modifications = np.hstack((
            np.zeros((len(modifications), 2)),
            modifications.reshape((len(modifications), 1))
        ))
        vertices = vertices + modifications

        vertices[:,1] -= threshold
        new_vertices = np.copy(vertices)
        new_vertices[:, 1] += self.thickness + threshold * 2
        vertices = np.vstack((vertices, new_vertices))
        vertices = np.hstack((vertices, np.ones((len(vertices), 1))))
        vertices = self.shape.frame.get_point_transformation_wrt(vertices)[:,0:3]
        l = int(len(vertices)/2)
        faces = [[i, (i+1)%l, (i+1)%l+l, i+l] for i,v in enumerate(vertices[0:l])]
        faces.append([i for i,v in enumerate(vertices[0:l])])
        faces.append([i+l for i,v in enumerate(vertices[0:l])])

        return vertices, faces