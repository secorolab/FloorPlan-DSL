import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

sys.path.append("..")
from exsce_floorplan.Classes.Geometry import *
from exsce_floorplan.Classes.Polytope import *

def frame_location_test():
    world = Frame()
    a = Frame(world)
    b = Frame(a) 
    c = Frame(world)

    a.set_translation(np.array([2, 3, 0]))
    b.set_translation(np.array([4, 4, 0]))
    c.set_translation(np.array([-3, -5, 0]))

    a.set_orientation(0, 0, np.deg2rad(45))
    c.set_orientation(0, 0, np.deg2rad(-30))

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim3d(-8, 8)
    ax.set_ylim3d(-8, 8)
    ax.set_zlim3d(-8, 8)
    
    frames = [world, a, b, c]
    frame_name = ['world', 'a', 'b', 'c']

    for frame, color in zip(frames, frame_name):
        origin, vectors = frame.get_direction_vectors()
        ax.quiver(origin[0], origin[1], origin[2], vectors[0,0], vectors[0,1], vectors[0,2], color="red")
        ax.quiver(origin[0], origin[1], origin[2], vectors[1,0], vectors[1,1], vectors[1,2], color="green")
        ax.quiver(origin[0], origin[1], origin[2], vectors[2,0], vectors[2,1], vectors[2,2], color="blue")
        ax.text(origin[0], origin[1], origin[2] - 1,  '%s' % (str(color)), size=10, zorder=1,color='k')
        
    plt.show()

def frame_location_test_two():
    world = Frame()
    a = Frame(world)
    b = Frame(a) 
    c = Frame(world)

    a.set_translation(np.array([2, 3, 2]))
    b.set_translation(np.array([4, 4, -4]))
    c.set_translation(np.array([-3, -5, -2]))

    a.set_orientation(0, np.deg2rad(10), np.deg2rad(45))
    b.set_orientation(0, 0, np.deg2rad(-45))
    c.set_orientation(np.deg2rad(-10), 0, np.deg2rad(-30))

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim3d(-8, 8)
    ax.set_ylim3d(-8, 8)
    ax.set_zlim3d(-8, 8)
    
    frames = [world, a, b, c]
    frame_name = ['world', 'a', 'b', 'c']

    for frame, color in zip(frames, frame_name):
        origin, vectors = frame.get_direction_vectors()
        ax.quiver(origin[0], origin[1], origin[2], vectors[0,0], vectors[0,1], vectors[0,2], color="red")
        ax.quiver(origin[0], origin[1], origin[2], vectors[1,0], vectors[1,1], vectors[1,2], color="green")
        ax.quiver(origin[0], origin[1], origin[2], vectors[2,0], vectors[2,1], vectors[2,2], color="blue")
        ax.text(origin[0], origin[1], origin[2] - 1,  '%s' % (str(color)), size=10, zorder=1,color='k')
        
    plt.show()

def square_room_location_test():
    world = Frame()
    rect_a = Rectangle("a", Frame(world),10, 10)
    rect_b = Rectangle("a", Frame(world), 2, 7)
    rect_c = Rectangle("a", Frame(world), 4, 10)

    rect_a.translation(4, 4)
    rect_b.translation(-2, -6)
    rect_c.translation(10, 10)

    rect_a.rotation(-23)
    rect_b.rotation(45)
    rect_c.rotation(0)

    rect_a_points = rect_a.get_points()
    rect_b_points = rect_b.get_points()
    rect_c_points = rect_c.get_points()

    plt.scatter(rect_a_points[:, 0], rect_a_points[:, 1], color='r')
    plt.scatter(rect_b_points[:, 0], rect_b_points[:, 1], color='b')
    plt.scatter(rect_c_points[:, 0], rect_c_points[:, 1], color='g')
    plt.axis('equal')

    frames = [world, rect_a.get_frame(), rect_b.get_frame(), rect_c.get_frame()]
    frame_name = ["world", "rect_a_frame", "rect_b_frame", "rect_c_frame"]

    for frame, color in zip(frames, frame_name):
        origin, vectors = frame.get_direction_vectors()
        plt.quiver(origin[0], origin[1], vectors[0,0], vectors[0,1], color="red")
        plt.quiver(origin[0], origin[1], vectors[1,0], vectors[1,1], color="green")
        plt.text(origin[0], origin[1] -1,  '%s' % (str(color)), size=10, zorder=1,color='k')
        
    plt.show()

    plt.show()

def custom_shape_room():
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
    world = Frame()
    pol1 = Polygon("a", Frame(world), np.array(points))
    pol2 = Polygon("a", Frame(world), np.array(points))

    pol1.translation(2, 5)
    pol2.translation(0, -15)
    pol2.rotation(180)

    pol1_points = pol1.get_points()
    pol2_points = pol2.get_points()

    plt.scatter(pol1_points[:, 0], pol1_points[:, 1], color='b')
    plt.scatter(pol2_points[:, 0], pol2_points[:, 1], color='g')
    plt.axis('equal') 

    frames = [world, pol1.get_frame(), pol2.get_frame()]
    frame_name = ["world", "pol1_frame", "pol2_frame"]

    for frame, color in zip(frames, frame_name):
        origin, vectors = frame.get_direction_vectors()
        plt.quiver(origin[0], origin[1], vectors[0,0], vectors[0,1], color="red")
        plt.quiver(origin[0], origin[1], vectors[1,0], vectors[1,1], color="green")
        plt.text(origin[0], origin[1] -1,  '%s' % (str(color)), size=10, zorder=1,color='k')
        
    plt.show()

def circle_shape_room():
    world = Frame()
    c1 = Circle("a", Frame(world), 5)
    c2 = Circle("a", Frame(world), 10)

    c1.translation(3, 0)
    c2.translation(-4, -10)
    c2.rotation(40)

    c1_points = c1.get_points()
    c2_points = c2.get_points()

    plt.scatter(c1_points[:, 0], c1_points[:, 1], color='b')
    plt.scatter(c2_points[:, 0], c2_points[:, 1], color='g')
    plt.axis('equal')

    frames = [world, c1.get_frame(), c2.get_frame()]
    frame_name = ["world", "c1_frame", "c2_frame"]

    for frame, color in zip(frames, frame_name):
        origin, vectors = frame.get_direction_vectors()
        plt.quiver(origin[0], origin[1], vectors[0,0], vectors[0,1], color="red")
        plt.quiver(origin[0], origin[1], vectors[1,0], vectors[1,1], color="green")
        plt.text(origin[0], origin[1] -1,  '%s' % (str(color)), size=10, zorder=1,color='k')
        
    plt.show()

def regular_polygon_room():
    world = Frame()
    c1 = RegularPolygon("a", Frame(world), 5, 5)
    c2 = RegularPolygon("a", Frame(world), 10, 6)

    c1.translation(3, 0)
    c2.translation(-4, -10)
    c2.rotation(40)

    c1_points = c1.get_points()
    c2_points = c2.get_points()

    plt.scatter(c1_points[:, 0], c1_points[:, 1], color='b')
    plt.scatter(c2_points[:, 0], c2_points[:, 1], color='g')
    plt.axis('equal')

    frames = [world, c1.get_frame(), c2.get_frame()]
    frame_name = ["world", "c1_frame", "c2_frame"]

    for frame, color in zip(frames, frame_name):
        origin, vectors = frame.get_direction_vectors()
        plt.quiver(origin[0], origin[1], vectors[0,0], vectors[0,1], color="red")
        plt.quiver(origin[0], origin[1], vectors[1,0], vectors[1,1], color="green")
        plt.text(origin[0], origin[1] -1,  '%s' % (str(color)), size=10, zorder=1,color='k')
        
    plt.show()

if __name__ == '__main__':
    frame_location_test()
    frame_location_test_two()
    square_room_location_test()
    custom_shape_room()
    circle_shape_room()
    regular_polygon_room()