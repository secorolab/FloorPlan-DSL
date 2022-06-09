import sys
import os
from textx import metamodel_from_file

# Blender
import bpy
import bmesh

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

# Debug graphic
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Pol
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

np.set_printoptions(suppress=True)

from Classes.Space import Space
from Classes.Polytope import (
                        Circle, 
                        Polygon, 
                        Rectangle, 
                        VerticalPolygon,
                        VerticalRectangle
                        ) 
from Classes.WallOpening import WallOpening

from Blender.blender import (
    clear_scene,
    create_mesh,
    create_collection,
    boolean_operation_difference
)

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
        self.wall_openings = model.wall_openings

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

        for wall_opening in self.wall_openings:
            points = wall_opening.get_points()
            
            ax.plot(points[:,0], points[:,1], c='k',linewidth=2.0)
            

        plt.show()

    def model_to_jsonld_transformation(self, model):
        pass

    def model_to_3d_transformation(self):

        building = create_collection(self.model.name)
        # clear the blender scene
        clear_scene()

        # create wall spaces
        for space in self.spaces:
            for i, wall in enumerate(space.walls):
                vertices, faces = wall.generate_3d_structure()
                create_mesh(building, wall.name, vertices, faces)

        # create wall openings
        for wall_opening in self.wall_openings:

            vertices, faces = wall_opening.generate_3d_structure()
            create_mesh(building, wall_opening.name, vertices, faces)
            
            # boolean operation for walls and opening
            boolean_operation_difference(wall_opening.wall_a.name, 
                                        wall_opening.name)
            if not wall_opening.wall_b is None:
                boolean_operation_difference(wall_opening.wall_b.name, 
                                        wall_opening.name)
            
            bpy.data.objects[wall_opening.name].select_set(True)
            bpy.ops.object.delete()
        
    def interpret(self):
        # perform all boolean operations and merge spaces accordingly

        # consider the order integer of each room

        # determine the points for each area: i.e room, walls, doorways, windows

        # generate JSON-LD file with all this information 

        # draw walls
        #self.debug_mpl_show_floorplan()
        self.model_to_3d_transformation()

if __name__ == '__main__':

    my_metamodel = metamodel_from_file('exsce_floorplan.tx', 
        classes=[Space, 
                Rectangle, 
                Polygon, 
                Circle,
                VerticalRectangle,
                WallOpening])    
    argv = sys.argv[sys.argv.index("--") + 1:]
    print(argv)
    my_model = my_metamodel.model_from_file(argv[0])
    floor_plan = FloorPlan(my_model)
    floor_plan.interpret()