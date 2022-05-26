from .Polytope import *

class Space(object):

    def __init__(self, parent, name, shape, location, floor_features):
        self.__parent = parent
        self.__name = name
        self.__shape = shape
        self.__location = location
        self.__floor_features = floor_features

    def create_walls(self, shape, location):
        """

        """
        pass

    def offset_room(self):
        pass
