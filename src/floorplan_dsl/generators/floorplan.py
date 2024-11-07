import os
import sys
import traceback

# Debug graphic
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon as Pol


from textx import metamodel_for_language

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

np.set_printoptions(suppress=True)


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

        plt.axis("equal")
        ax = plt.gca()
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)

        def draw_vector(name, origin, vectors, d):
            ax.quiver(
                origin[0],
                origin[1],
                vectors[0, 0],
                vectors[0, 1],
                color="red",
                zorder=10,
            )
            ax.quiver(
                origin[0],
                origin[1],
                vectors[1, 0],
                vectors[1, 1],
                color="green",
                zorder=10,
            )
            props = dict(boxstyle="round", facecolor="white", alpha=0.5)
            ax.text(
                origin[0],
                origin[1] - (1 * d),
                name,
                size=6,
                color="k",
                zorder=11,
                bbox=props,
            )

        for j, space in enumerate(self.spaces):
            points = space.get_walls_wrt_world()
            for point in points:
                p = Pol(point[:, 0:2], closed=True, color=np.random.random(3))
                ax.add_patch(p)

            d = (-1) ** (j + 1)
            # for i, wall in enumerate(space.walls):
            #     origin, directions = wall.get_frame().get_direction_vectors()
            #     draw_vector("{name}.walls[{i}]".format(name=space.name,
            #                            i=str(i)), origin, directions, d)

            origin, directions = space.get_frame().ref.get_direction_vectors()
            draw_vector("world", origin, directions, d)

            origin, directions = space.get_frame().get_direction_vectors()
            draw_vector(space.name, origin, directions, d)

        # for wall_opening in self.wall_openings:
        #     points = wall_opening.get_points()

        #     ax.plot(points[:,0], points[:,1], c='k',linewidth=2.0)

        plt.show()

    def interpret(self):
        self.model_to_3d_transformation()
        self.model_to_occupancy_grid_transformation()


if __name__ == "__main__":

    try:

        my_metamodel = metamodel_for_language("floorplan-v1")
        argv = sys.argv[sys.argv.index("--") + 1 :]
        my_model = my_metamodel.model_from_file(argv[0])
        floor_plan = FloorPlan(my_model)
        floor_plan.interpret()

    except Exception:
        print(traceback.format_exc())
        sys.exit(1)
