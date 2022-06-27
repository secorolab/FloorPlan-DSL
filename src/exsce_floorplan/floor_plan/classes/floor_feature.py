import numpy as np

class FloorFeature(object):

    def __init__(self, parent, name, shape, loc, divider, column, height):
        self.parent = parent
        self.name = name
        self.shape = shape
        self.loc = loc
        self.divider = divider
        self.column = column
        self.height = height

    def locate(self):
        frame = self.parent.get_frame()
        if not self.loc._from.index is None:
            frame = self.parent.get_wall(self.loc._from.index).get_frame()
        self.shape.change_reference_frame(frame)
        
        pose = self.loc.pos.pos
        x = pose.x.value
        y = pose.y.value
        z = pose.z.value if not pose.z is None else 0

        t = np.array([x, y, z])
        rot = self.loc.pos.rot.value 

        self.shape.frame.set_translation(t)
        self.shape.frame.set_orientation(0, 0, np.deg2rad(rot))

    def get_points(self):
        return self.shape.get_points()

    def generate_3d_structure(self):
        vertices = self.shape.get_points(self.shape.frame)[:, 0:3]

        new_vertices = np.copy(vertices)
        new_vertices[:, 2] += self.height.value
    
        vertices = np.vstack((vertices, new_vertices))
        vertices = np.hstack((vertices, np.ones((len(vertices), 1))))
        vertices = self.shape.frame.get_point_transformation_wrt(vertices)[:,0:3]
        
        l = int(len(vertices)/2)
        faces = [[i, (i+1)%l, (i+1)%l+l, i+l] for i,v in enumerate(vertices[0:l])]
        faces.append([i for i,v in enumerate(vertices[0:l])])
        faces.append([i+l for i,v in enumerate(vertices[0:l])])

        return vertices, faces