import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Pol
from mpl_toolkits.mplot3d import Axes3D

sys.path.append("..")

from exsce_floorplan.Classes.Geometry import *
from exsce_floorplan.Classes.Polytope import *
from exsce_floorplan.Classes.Floorplan import *

def draw_wall(plt, wall_points):
    p = Pol(wall_points, closed=True, edgecolor='k', fill=False)
    plt.add_patch(p)

def square_uniform_offset():
    world = Frame()
    a = Frame(world)
    a.set_translation(np.array([4, 0, 0]))
    a.set_orientation(0, 0, np.deg2rad(30))
    shape = Rectangle("a", a, 5, 10)
    space = Space("parent", "room", shape, None, None)
    space.create_walls()
    space.offset_shape()
    points = space.get_walls_wrt_world()

    plt.axis('equal') 
    ax = plt.gca()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    for point in points:
        draw_wall(ax, point[:,0:2])
    plt.show()

def square_non_uniform_offset():
    world = Frame()
    a = Frame(world)
    a.set_translation(np.array([0, 0, 0]))
    a.set_orientation(0, 0, np.deg2rad(0))
    shape = Rectangle("a", a, 5, 10)
    space = Space("parent", "room", shape, None, None)
    space.create_walls()
    space.offset_shape([0.3, 1, 0.3, 0.6])
    points = space.get_walls_wrt_world()

    plt.axis('equal') 
    ax = plt.gca()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    for point in points:
        draw_wall(ax, point[:,0:2])
    plt.show()

def custom_uniform_offset():
    world = Frame()
    a = Frame(world)

    points = [
        [  3.68688887 , 3.5       ],
        [  5.0        , 3.5       ],
        [  5.0        ,-3.25078168],
        [ 14.1346049  ,-4.86145898],
        [ 13.44001219 ,-8.80068999],
        [-14.1346049  ,-3.93854102],
        [-13.44001219 , 0.00068999],
        [ -5.0        ,-1.48751187],
        [ -5.0        , 3.5       ],
        [  0.58106033 , 3.5       ],
        [ -0.74298396 , 8.44140056],
        [  2.15479351 , 9.2178577 ]
    ]

    a.set_translation(np.array([0, 0, 0]))
    a.set_orientation(0, 0, np.deg2rad(0))

    shape = Polygon("a", a, np.array(points))
    space = Space("parent", "room", shape, None, None)
    space.create_walls()
    space.offset_shape()
    points = space.get_walls_wrt_world()

    plt.axis('equal') 
    ax = plt.gca()
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)

    for point in points:
        draw_wall(ax, point[:,0:2])

    plt.show()

def custom_non_uniform_offset():
    world = Frame()
    a = Frame(world)

    points = [
        [  3.68688887 , 3.5       ],
        [  5.0        , 3.5       ],
        [  5.0        ,-3.25078168],
        [ 14.1346049  ,-4.86145898],
        [ 13.44001219 ,-8.80068999],
        [-14.1346049  ,-3.93854102],
        [-13.44001219 , 0.00068999],
        [ -5.0        ,-1.48751187],
        [ -5.0        , 3.5       ],
        [  0.58106033 , 3.5       ],
        [ -0.74298396 , 8.44140056],
        [  2.15479351 , 9.2178577 ]
    ]

    a.set_translation(np.array([0, 0, 0]))
    a.set_orientation(0, 0, np.deg2rad(0))

    shape = Polygon("a", a, np.array(points))
    space = Space("parent", "room", shape, None, None)
    space.create_walls()
    
    plt.axis('equal') 
    ax = plt.gca()

    widths = [
        0.2, 0.3, 0.7, 0.3, 0.3, 0.3,
        0.3, 0.5, 0.3, 0.8, 0.3, 0.3
    ]
    space.offset_shape(widths)

    points = space.get_walls_wrt_world()

    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)

    for point in points:
        draw_wall(ax, point[:,0:2])

    plt.show()

def two_spaces_with_location_and_offset():
    world = Frame()

    a = Frame(world)
    a.set_translation(np.array([4, 3, 0]))
    a.set_orientation(0, 0, np.deg2rad(35))

    shape_a = Rectangle("a", Frame(world), 5, 15)
    space_a = Space("parent", "room", shape_a, None, None)

    space_a.create_walls()
    space_a.offset_shape(0.3)

    shape_b = Rectangle("a", Frame(world), 5, 8)
    space_b = Space("parent", "room", shape_b, None, None)
    space_b.create_walls()
    space_b.offset_shape(0.4)

   
    t_a, R_a = a.get_transformation()
    T_a = np.hstack((np.vstack((R_a, np.zeros(3))), np.vstack((t_a.reshape((3,1)), [1]))))

    b = Frame(world)
    b.set_translation(np.array([3, 0.7, 0]))
    t_b, R_b = b.get_transformation()
    T_b = np.hstack((np.vstack((R_b, np.zeros(3))), np.vstack((t_b.reshape((3,1)), [1]))))

    space_a.locate_space(world, space_a.shape.frame, T_a)
    space_b.locate_space(space_a.walls[1].frame, space_b.walls[2].frame, T_b, True)

    plt.axis('equal') 
    ax = plt.gca()
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)

    points = space_a.get_walls_wrt_world()

    for point in points:
        draw_wall(ax, point[:,0:2])

    points = space_b.get_walls_wrt_world()

    for point in points:
        draw_wall(ax, point[:,0:2])

    plt.show()

def more_complex_shapes():
    world = Frame()

    c = Frame(world)
    c.set_orientation(0, 0, np.deg2rad(-20))

    a = Frame(world)

    points = [
        [0, 6],
        [3, 3],
        [2, -2],
        [-2, -2],
        [-3, 3]
    ]

    a.set_translation(np.array([0, 0.6, 0]))
    a.set_orientation(0, 0, np.deg2rad(0))

    shape = Polygon("a", a, np.array(points))
    space = Space("parent", "room", shape, None, None)
    space.create_walls()
    space.offset_shape([0.5, 0.3, 0.3, 0.3, 0.3])

    shape_a = Rectangle("a", Frame(world), 3, 15)
    space_a = Space("parent", "room", shape_a, None, None)

    space_a.create_walls()
    space_a.offset_shape(0.3)

    shape_b = Rectangle("a", Frame(world), 3, 8)
    space_b = Space("parent", "room", shape_b, None, None)
    space_b.create_walls()
    space_b.offset_shape(0.4)

    t_a, R_a = a.get_transformation()
    T_a = np.hstack((np.vstack((R_a, np.zeros(3))), np.vstack((t_a.reshape((3,1)), [1]))))

    b = Frame(world)
    b.set_translation(np.array([0, 0.9, 0]))
    t_b, R_b = b.get_transformation()
    T_b = np.hstack((np.vstack((R_b, np.zeros(3))), np.vstack((t_b.reshape((3,1)), [1]))))

    t_c, R_c = c.get_transformation()
    T_c = np.hstack((np.vstack((R_c, np.zeros(3))), np.vstack((t_c.reshape((3,1)), [1]))))

    space.locate_space(world, space.shape.frame, T_c)
    space_a.locate_space(space.walls[3].frame, space_a.walls[2].frame, T_a, True)
    space_b.locate_space(space.walls[0].frame, space_b.walls[2].frame, T_b, True)

    spaces = [space, space_a, space_b]

    plt.axis('equal') 
    ax = plt.gca()
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)

    for s in spaces:
        points = s.get_walls_wrt_world()

        for point in points:
            draw_wall(ax, point[:,0:2])

    plt.show()

def no_show_wall():
    world = Frame()
    a = Frame(world)
    a.set_translation(np.array([0, 0, 0]))
    a.set_orientation(0, 0, np.deg2rad(0))
    shape = Rectangle("a", a, 5, 10)
    space = Space("parent", "room", shape, None, None)
    space.create_walls()
    space.offset_shape([0.3, 0.3, 0, 0.3])
    points = space.get_walls_wrt_world()

    plt.axis('equal') 
    ax = plt.gca()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    for point in points:
        draw_wall(ax, point[:,0:2])
    plt.show()


if __name__=='__main__':
    square_uniform_offset()
    square_non_uniform_offset()
    custom_uniform_offset()
    custom_non_uniform_offset()
    two_spaces_with_location_and_offset()
    more_complex_shapes()
    no_show_wall()