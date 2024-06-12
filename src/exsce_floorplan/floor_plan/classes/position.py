class Position(object):

    def __init__(self, parent, x, y, z):
        self.parent = parent
        self.x = x
        self.y = y
        self.z = z


class PoseDescription(object):

    def __init__(self, parent, translation, rotation):
        self.parent = parent
        self.translation = translation
        self.rotation = rotation
