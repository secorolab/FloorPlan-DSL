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

from Classes.Space import Space
from Classes.Polytope import (
                        Circle, 
                        Polygon, 
                        Rectangle, 
                        VerticalPolygon,
                        VerticalRectangle
                        ) 
from Classes.WallOpening import WallOpening

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

        building = bpy.data.collections.new(self.model.name)
        bpy.context.scene.collection.children.link(building)

        # clear the blender scene
        for obj in bpy.context.scene.objects:
            obj.select_set(True)
            bpy.ops.object.delete()

        # create wall spaces
        for space in self.spaces:
            for i, wall in enumerate(space.walls):
                vertices, faces = wall.generate_3d_structure()

                space_name = "{space}.wall{index}".format(space=space.name, 
                                                            index=i
                                                        )

                me = bpy.data.meshes.new(space_name)
                me.from_pydata(vertices, [], faces)
                me.update()

                bm = bmesh.new()
                bm.from_mesh(me, face_normals=True) 

                bm.to_mesh(me)
                bm.free()
                me.update()

                obj = bpy.data.objects.new(space_name, me)
                building.objects.link(obj)

        # create wall openings
        for wall_opening in self.wall_openings:
            vertices, faces = wall_opening.generate_3d_structure()




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