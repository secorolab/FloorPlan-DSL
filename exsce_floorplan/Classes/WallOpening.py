import numpy as np 

class WallOpening(object):

    def __init__(self, parent, wall_a, wall_b, shape, loc, entryway, window, name):
        self.parent = parent
        self.wall_a = wall_a
        self.wall_b = wall_b
        self.shape = shape
        self.loc = loc
        self.name = name

        self.determine_thickness()
        self.locate()
        
    def determine_thickness(self):
        thickness = self.wall_a.ref.get_wall_thickness(self.wall_a.index)

        if not self.wall_b is None:
            thickness += self.wall_b.ref.get_wall_thickness(self.wall_b.index)

        self.thickness = thickness

    def locate(self):
        frame = self.wall_a.ref.get_wall_frame(self.wall_a.index)
        self.shape.change_reference_frame(frame)
        
        t = np.array([self.loc.pos.x.value, self.loc.pos.y.value, self.loc.pos.z.value])
        rot = self.loc.rot.value 

        self.shape.frame.set_translation(t)
        self.shape.frame.set_orientation(0, np.deg2rad(rot), 0)

    def get_points(self):
        return self.shape.get_points()

    def generate_3d_structure(self):
        print(self.shape.get_points())

        return 0,0 