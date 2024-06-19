import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Pol
from mpl_toolkits.mplot3d import Axes3D

sys.path.append("..")

from exsce_floorplan.Classes.Geometry import *
from exsce_floorplan.Classes.Polytope import *
from exsce_floorplan.Classes.Floorplan import *


def draw_coordinate_frame_2D(plt, frame, text=""):
    origin, vectors = frame.get_direction_vectors()

    plt.quiver(
        origin[0], origin[1], vectors[0, 0], vectors[0, 1], color="red", width=0.004
    )
    plt.quiver(
        origin[0], origin[1], vectors[1, 0], vectors[1, 1], color="green", width=0.004
    )
    plt.text(origin[0], origin[1] - 1, "%s" % (str(text)), size=10, zorder=1, color="k")


def draw_shape(plt, points):
    plt.add_patch(Pol(points, closed=True, edgecolor="k", fill=False))


def square_space_creation_test():

    world = Frame()
    a = Frame(world)
    a.set_translation(np.array([4, 3, 0]))
    a.set_orientation(0, 0, np.deg2rad(35))
    shape = Rectangle("a", a, 5, 10)
    space = Space("parent", "room", shape, None, None)
    space.create_walls()

    points = space.get_shape().get_points()

    plt.axis("equal")
    ax = plt.gca()
    draw_shape(ax, points[:, 0:2])

    for i, wall in enumerate(space.walls):
        frame = wall.get_frame()
        draw_coordinate_frame_2D(ax, frame, i)

    draw_coordinate_frame_2D(ax, shape.get_frame())
    draw_coordinate_frame_2D(ax, world)

    plt.show()


def polygon_space_creation_test():

    world = Frame()
    a = Frame(world)

    points = [
        [3.68688887, 3.5],
        [5.0, 3.5],
        [5.0, -3.25078168],
        [14.1346049, -4.86145898],
        [13.44001219, -8.80068999],
        [-14.1346049, -3.93854102],
        [-13.44001219, 0.00068999],
        [-5.0, -1.48751187],
        [-5.0, 3.5],
        [0.58106033, 3.5],
        [-0.74298396, 8.44140056],
        [2.15479351, 9.2178577],
    ]

    a.set_translation(np.array([5, 3, 0]))
    a.set_orientation(0, 0, np.deg2rad(65))

    shape = Polygon("a", a, np.array(points))
    space = Space("parent", "room", shape, None, None)
    space.create_walls()

    points = space.get_shape().get_points()

    plt.axis("equal")
    ax = plt.gca()
    draw_shape(ax, points[:, 0:2])

    for i, wall in enumerate(space.walls):
        frame = wall.get_frame()
        draw_coordinate_frame_2D(ax, frame, i)

    draw_coordinate_frame_2D(ax, shape.get_frame(), "shape")
    draw_coordinate_frame_2D(ax, world, "world")

    plt.show()


def locate_space_wrt_another_space_one():

    world = Frame()
    a = Frame(world)

    a.set_translation(np.array([4, 3, 0]))
    a.set_orientation(0, 0, np.deg2rad(35))

    shape_a = Rectangle("a", Frame(world), 5, 10)
    space_a = Space("parent", "room", shape_a, None, None)

    space_a.create_walls()

    shape_b = Rectangle("a", Frame(world), 5, 8)
    space_b = Space("parent", "room", shape_b, None, None)
    space_b.create_walls()

    t_a, R_a = a.get_transformation()
    T_a = np.hstack(
        (np.vstack((R_a, np.zeros(3))), np.vstack((t_a.reshape((3, 1)), [1])))
    )

    T_b = np.identity(4)

    space_a.locate_space(world, space_a.shape.frame, T_a)
    space_b.locate_space(space_a.walls[1].frame, space_b.walls[3].frame, T_b, True)
    points = space_a.get_shape().get_points()

    plt.axis("equal")
    ax = plt.gca()
    draw_shape(ax, points[:, 0:2])

    for i, wall in enumerate(space_a.walls):
        frame = wall.frame
        draw_coordinate_frame_2D(ax, frame, str(id(wall.frame))[-3:])

    draw_coordinate_frame_2D(ax, shape_a.frame, str(id(shape_a.frame))[-3:])
    draw_coordinate_frame_2D(ax, world, str(id(world))[-3:])

    points = space_b.get_shape().get_points()
    draw_shape(ax, points[:, 0:2])

    for i, wall in enumerate(space_b.walls):
        frame = wall.frame
        draw_coordinate_frame_2D(ax, frame, str(id(wall.frame))[-3:])

    draw_coordinate_frame_2D(ax, shape_b.frame, str(id(shape_b.frame))[-3:])

    plt.show()


def locate_space_wrt_another_space_two():

    world = Frame()
    a = Frame(world)

    a.set_translation(np.array([4, -3, 0]))
    a.set_orientation(0, 0, np.deg2rad(60))

    shape_a = Rectangle("a", Frame(world), 5, 8)
    space_a = Space("parent", "room", shape_a, None, None)

    space_a.create_walls()

    shape_b = Rectangle("a", Frame(world), 5, 8)
    space_b = Space("parent", "room", shape_b, None, None)
    space_b.create_walls()

    t_a, R_a = a.get_transformation()
    T_a = np.hstack(
        (np.vstack((R_a, np.zeros(3))), np.vstack((t_a.reshape((3, 1)), [1])))
    )

    b = Frame()
    b.set_translation(np.array([1, 1, 0]))
    b.set_orientation(0, 0, np.deg2rad(-10))
    t_b, R_b = b.get_transformation()
    T_b = np.hstack(
        (np.vstack((R_b, np.zeros(3))), np.vstack((t_b.reshape((3, 1)), [1])))
    )

    space_a.locate_space(world, space_a.get_frame(), T_a)
    space_b.locate_space(space_a.get_frame(), space_b.walls[2].get_frame(), T_b)

    points = space_a.get_shape().get_points()

    plt.axis("equal")
    ax = plt.gca()
    draw_shape(ax, points[:, 0:2])

    for i, wall in enumerate(space_a.walls):
        frame = wall.get_frame()
        draw_coordinate_frame_2D(ax, frame, i)

    draw_coordinate_frame_2D(ax, shape_a.get_frame(), "shape")
    draw_coordinate_frame_2D(ax, world, "world")

    points = space_b.get_shape().get_points()
    draw_shape(ax, points[:, 0:2])

    for i, wall in enumerate(space_b.walls):
        frame = wall.get_frame()
        draw_coordinate_frame_2D(ax, frame, i)

    draw_coordinate_frame_2D(ax, shape_b.get_frame(), "shape")

    plt.show()


def locate_space_wrt_another_space_three():

    points = [
        [3.68688887, 3.5],
        [5.0, 3.5],
        [5.0, -3.25078168],
        [14.1346049, -4.86145898],
        [13.44001219, -8.80068999],
        [-14.1346049, -3.93854102],
        [-13.44001219, 0.00068999],
        [-5.0, -1.48751187],
        [-5.0, 3.5],
        [0.58106033, 3.5],
        [-0.74298396, 8.44140056],
        [2.15479351, 9.2178577],
    ]

    world = Frame()
    a = Frame(world)

    a.set_translation(np.array([4, -3, 0]))
    a.set_orientation(0, 0, np.deg2rad(180))

    shape_a = Polygon("a", Frame(world), np.array(points))
    space_a = Space("parent", "room", shape_a, None, None)

    space_a.create_walls()

    shape_b = Rectangle("a", Frame(world), 5, 8)
    space_b = Space("parent", "room", shape_b, None, None)
    space_b.create_walls()

    t_a, R_a = a.get_transformation()
    T_a = np.hstack(
        (np.vstack((R_a, np.zeros(3))), np.vstack((t_a.reshape((3, 1)), [1])))
    )

    b = Frame()
    b.set_translation(np.array([9, 0.4, 0]))
    b.set_orientation(0, 0, np.deg2rad(0))
    t_b, R_b = b.get_transformation()
    T_b = np.hstack(
        (np.vstack((R_b, np.zeros(3))), np.vstack((t_b.reshape((3, 1)), [1])))
    )

    space_a.locate_space(world, space_a.get_frame(), T_a)
    space_b.locate_space(
        space_a.walls[4].get_frame(), space_b.walls[1].get_frame(), T_b, True
    )

    points = space_a.get_shape().get_points()

    plt.axis("equal")
    ax = plt.gca()
    draw_shape(ax, points[:, 0:2])

    for i, wall in enumerate(space_a.walls):
        frame = wall.get_frame()
        draw_coordinate_frame_2D(ax, frame, i)

    draw_coordinate_frame_2D(ax, shape_a.get_frame(), "shape")
    draw_coordinate_frame_2D(ax, world, "world")

    points = space_b.get_shape().get_points()
    draw_shape(ax, points[:, 0:2])

    for i, wall in enumerate(space_b.walls):
        frame = wall.get_frame()
        draw_coordinate_frame_2D(ax, frame, i)

    draw_coordinate_frame_2D(ax, shape_b.get_frame(), "shape")

    plt.show()


def locate_space_wrt_another_space_four():

    world = Frame()
    a = Frame(world)

    a.set_translation(np.array([4, -3, 0]))
    a.set_orientation(0, 0, np.deg2rad(60))

    shape_a = Rectangle("a", Frame(world), 5, 8)
    space_a = Space("parent", "room", shape_a, None, None)

    space_a.create_walls()

    shape_b = Rectangle("a", Frame(world), 5, 8)
    space_b = Space("parent", "room", shape_b, None, None)
    space_b.create_walls()

    t_a, R_a = a.get_transformation()
    T_a = np.hstack(
        (np.vstack((R_a, np.zeros(3))), np.vstack((t_a.reshape((3, 1)), [1])))
    )

    b = Frame()
    b.set_translation(np.array([1, 1, 0]))
    b.set_orientation(0, 0, np.deg2rad(-10))
    t_b, R_b = b.get_transformation()
    T_b = np.hstack(
        (np.vstack((R_b, np.zeros(3))), np.vstack((t_b.reshape((3, 1)), [1])))
    )

    space_a.locate_space(world, space_a.get_frame(), T_a)
    space_b.locate_space(space_a.get_frame(), space_b.get_frame(), T_b)

    points = space_a.get_shape().get_points()

    plt.axis("equal")
    ax = plt.gca()
    draw_shape(ax, points[:, 0:2])

    for i, wall in enumerate(space_a.walls):
        frame = wall.get_frame()
        draw_coordinate_frame_2D(ax, frame, i)

    draw_coordinate_frame_2D(ax, shape_a.get_frame(), "A")
    draw_coordinate_frame_2D(ax, world, "world")

    points = space_b.get_shape().get_points()
    draw_shape(ax, points[:, 0:2])

    for i, wall in enumerate(space_b.walls):
        frame = wall.get_frame()
        draw_coordinate_frame_2D(ax, frame, i)

    draw_coordinate_frame_2D(ax, shape_b.get_frame(), "B")

    plt.show()


def circle_space_creation():

    world = Frame()
    a = Frame(world)
    a.set_translation(np.array([4, 3, 0]))
    a.set_orientation(0, 0, np.deg2rad(0))
    shape = Circle("a", a, 10)
    space = Space("parent", "room", shape, None, None)
    space.create_walls()

    points = space.get_shape().get_points()

    plt.axis("equal")
    ax = plt.gca()
    draw_shape(ax, points[:, 0:2])

    for i, wall in enumerate(space.walls):
        frame = wall.get_frame()
        draw_coordinate_frame_2D(ax, frame, i)

    draw_coordinate_frame_2D(ax, shape.get_frame())
    draw_coordinate_frame_2D(ax, world)

    plt.show()


if __name__ == "__main__":
    square_space_creation_test()
    polygon_space_creation_test()
    locate_space_wrt_another_space_one()
    locate_space_wrt_another_space_two()
    locate_space_wrt_another_space_three()
    locate_space_wrt_another_space_four()
    circle_space_creation()
