import sys
import traceback
import os
import io
import yaml
from PIL import Image, ImageDraw, ImageOps
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
from Classes.FloorFeature import FloorFeature

from Blender.blender import (
    boolean_operation_difference,
    clear_scene,
    create_mesh,
    create_collection,
    export
)

'''
TODO
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

        with open("config.yaml", 'r') as stream:
            self.config = yaml.safe_load(stream)

    def debug_mpl_show_floorplan(self):

        plt.axis('equal') 
        ax = plt.gca()
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)

        def draw_vector(name, origin, vectors, d):
            ax.quiver(origin[0], origin[1], vectors[0,0], vectors[0,1], color="red", zorder=10)
            ax.quiver(origin[0], origin[1], vectors[1,0], vectors[1,1], color="green", zorder=10)
            props = dict(boxstyle='round', facecolor='white', alpha=0.5)
            ax.text(origin[0], origin[1] - (1*d), name, size=6, color='k', zorder=11, bbox=props)

        for j, space in enumerate(self.spaces):
            points = space.get_walls_wrt_world()
            for point in points:
                p = Pol(point[:, 0:2], closed=True, color=np.random.random(3))
                ax.add_patch(p)

            d = (-1)**(j+1)
            # for i, wall in enumerate(space.walls):
            #     origin, directions = wall.get_frame().get_direction_vectors()
            #     draw_vector("{name}.walls[{i}]".format(name=space.name, i=str(i)), origin, directions, d)

            origin, directions = space.get_frame().ref.get_direction_vectors()
            draw_vector("world", origin, directions, d)

            origin, directions = space.get_frame().get_direction_vectors()
            draw_vector(space.name, origin, directions, d)
            
        # for wall_opening in self.wall_openings:
        #     points = wall_opening.get_points()
            
        #     ax.plot(points[:,0], points[:,1], c='k',linewidth=2.0)
            

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

            for feature in space.floor_features:
                feature.locate()
                vertices, faces = feature.generate_3d_structure()
                create_mesh(building, feature.name, vertices, faces)

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

        export(self.model.name)

    def model_to_occupancy_grid_transformation(self):
        
        pgm = self.config["pgm"]

        unknown = pgm["unknown"]
        occupied = pgm["occupied"]
        free = pgm["free"]
        res = pgm["resolution"]
        border = 100
        laser_height = pgm["laser_height"]

        points = []
        directions = []

        for space in self.spaces:
            
            shape = space.get_shape()
            shape_points = shape.get_points()
            points.append(shape_points)

            directions.append([
                np.amax(shape_points[:, 1]),            # north
                np.amin(shape_points[:, 1]),            # south 
                np.amax(shape_points[:, 0]),            # east
                np.amin(shape_points[:, 0])             # west
                ])

        directions = np.array(directions)
        north = np.amax(directions[:,0])
        south = np.amin(directions[:,1])
        east = np.amax(directions[:,2])
        west = np.amin(directions[:,3])

        # Create canvas
        floor = (
            int(abs(east-west)/res)+border, 
            int(abs(north-south)/res)+border)
        
        im = Image.new('L', floor, unknown)
        draw = ImageDraw.Draw(im)

        for shape in points:
            shape[:, 0] = (shape[:, 0] + abs(west))/res
            shape[:, 1] = (shape[:, 1] + abs(south))/res
            shape += border/2
            shape = shape.astype(int)

            draw.polygon(shape[:, 0:2].flatten().tolist(), fill=free)
            
        for space in self.spaces:
            for wall in space.walls:
                points, _ = wall.generate_3d_structure()

                shape = points[0:int(len(points)/2), 0:2]
                shape[:, 0] = (shape[:, 0] + abs(west))/res
                shape[:, 1] = (shape[:, 1] + abs(south))/res
                shape += border/2
                shape = shape.astype(int)

                draw.polygon(shape[:, 0:2].flatten().tolist(), fill=occupied)

            for feature in space.floor_features:
                points, _ = feature.generate_3d_structure()

                if points[int(len(points)/2):,2][0] < laser_height:
                    continue

                shape = points[0:int(len(points)/2), 0:2]
                shape[:, 0] = (shape[:, 0] + abs(west))/res
                shape[:, 1] = (shape[:, 1] + abs(south))/res
                shape += border/2
                shape = shape.astype(int)

                draw.polygon(shape[:, 0:2].flatten().tolist(), fill=occupied)

        # with io.open(pgm["map_configuration"], 'w', encoding='utf8') as outfile:
        #     yaml.dump(pgm, outfile, default_flow_style=False, allow_unicode=True)
        
        for wall_opening in self.wall_openings:

            shape = wall_opening.generate_2d_structure(laser_height)
            
            if shape is None:
                continue

            shape[:, 0] = (shape[:, 0] + abs(west))/res
            shape[:, 1] = (shape[:, 1] + abs(south))/res
            shape += border/2
            shape = shape.astype(int)

            draw.polygon(shape[:, 0:2].flatten().tolist(), fill=free)

        im = ImageOps.flip(im)
        im.show()
        im.save('output/{name}'.format(name=pgm["image"]), quality=95)
            
                
            
    def interpret(self):
    # perform all boolean operations and merge spaces accordingly

    # consider the order integer of each room

    # determine the points for each area: i.e room, walls, doorways, windows

    # generate JSON-LD file with all this information 

    # draw walls
        #self.debug_mpl_show_floorplan()
        self.model_to_3d_transformation()
        self.model_to_occupancy_grid_transformation()

if __name__ == '__main__':

    try:
        my_metamodel = metamodel_from_file('exsce_floorplan/exsce_floorplan.tx', 
            classes=[Space, 
                    Rectangle, 
                    Polygon, 
                    Circle,
                    VerticalRectangle,
                    WallOpening,
                    FloorFeature])    
        argv = sys.argv[sys.argv.index("--") + 1:]
        my_model = my_metamodel.model_from_file(argv[0])
        floor_plan = FloorPlan(my_model)
        floor_plan.interpret()
    except Exception:
        print(traceback.format_exc())
        sys.exit(1)