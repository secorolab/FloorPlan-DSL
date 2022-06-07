import sys
from os.path import dirname, join
from textx import metamodel_from_file

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Pol
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from Classes.Floorplan import Space
from Classes.Polytope import Rectangle, Polygon, Circle

'''
TODO
interprate model
code doorways and windows
code columns and dividers
code constraints
'''

class FloorPlan(object):
    """
    Floor plan model interpreter
    """

    def __init__(self, model):
        # instanciate all walls (boundary lines for each space)
        self.model = model
        self.spaces = model.spaces

    def debug_mpl_show_floorplan(self):

        plt.axis('equal') 
        ax = plt.gca()
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)

        for space in self.spaces:
            points = space.get_walls_wrt_world()
            for point in points:
                p = Pol(point[:, 0:2], closed=True, color=np.random.random(3))
                ax.add_patch(p)

        plt.show()

    def interpret(self):
        
        #for space in self.spaces:
            # print(space)
            # print(space.shape)
            # print(space.location._from.ref, space.location._from.world, space.location._from.index)
            # print(space.location.to.ref,space.location.to.this, space.location.to.index)

        # locate all rooms according to the description w/o wall thickness

        # perform all boolean operations and merge spaces accordingly

        # consider the order integer of each room

        # offset the walls to their desired width

        # determine the points for each area: i.e room, walls, doorways, windows

        # generate JSON-LD file with all this information 
    
        # draw walls
        self.debug_mpl_show_floorplan()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python {} <model>".format(sys.argv[0]))
    else:
        my_metamodel = metamodel_from_file('exsce_floorplan.tx', 
            classes=[Space, Rectangle, Polygon, Circle])    
        my_model = my_metamodel.model_from_file(sys.argv[1])
        floor_plan = FloorPlan(my_model)
        floor_plan.interpret()