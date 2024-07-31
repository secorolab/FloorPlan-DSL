import numpy as np

from .helpers import get_value


class WallOpening(object):

    def __init__(self, parent, wall_a, wall_b, shape, pose, entryway, window, name):
        self.parent = parent
        self.wall_a = wall_a.ref.get_wall(wall_a.index)
        self.shape = shape
        self.pose = pose
        self.name = name

        if not wall_b is None:
            self.wall_b = wall_b.ref.get_wall(wall_b.index)
        else:
            self.wall_b = None

        self.determine_thickness()
        self.locate()

    def determine_thickness(self):
        thickness = get_value(self.wall_a.thickness)

        if not self.wall_b is None:
            thickness += get_value(self.wall_b.thickness)

        self.thickness = thickness

    def locate(self):
        frame = self.wall_a.get_frame()
        self.shape.change_reference_frame(frame)

        t = np.array(
            [
                get_value(self.pose.translation.x),
                get_value(self.pose.translation.y),
                get_value(self.pose.translation.z),
            ]
        )
        rotation = get_value(self.pose.rotation)

        self.shape.frame.set_translation(t)
        self.shape.frame.set_orientation(0, np.deg2rad(rotation), 0)

    def get_points(self):
        return self.shape.get_points()

    def generate_3d_structure(self):
        vertices = self.shape.get_points(self.shape.frame)[:, 0:3]
        origin, _ = self.wall_a.frame.get_transformation()

        # Modifications to the vertices made to avoid face clashing
        threshold = 0.01
        modifications = np.where(origin[2] == vertices[:, 2], -threshold, 0)
        modifications += np.where(self.wall_a.height == vertices[:, 2], threshold, 0)
        if not self.wall_b is None:
            modifications += np.where(
                self.wall_b.height == vertices[:, 2], threshold, 0
            )

        modifications = np.hstack(
            (
                np.zeros((len(modifications), 2)),
                modifications.reshape((len(modifications), 1)),
            )
        )
        vertices = vertices + modifications

        vertices[:, 1] -= threshold
        new_vertices = np.copy(vertices)
        new_vertices[:, 1] += self.thickness + threshold * 2
        vertices = np.vstack((vertices, new_vertices))
        vertices = np.hstack((vertices, np.ones((len(vertices), 1))))
        vertices = self.shape.frame.get_point_transformation_wrt(vertices)[:, 0:3]
        l = int(len(vertices) / 2)
        faces = [
            [i, (i + 1) % l, (i + 1) % l + l, i + l]
            for i, v in enumerate(vertices[0:l])
        ]
        faces.append([i for i, v in enumerate(vertices[0:l])])
        faces.append([i + l for i, v in enumerate(vertices[0:l])])

        return vertices, faces

    def generate_2d_structure(self, height, offset=0.2, wrt=None):

        shape = self.shape.get_points(self.shape.frame)

        shapeXY = np.zeros((shape.shape[0], 2))
        shapeXY[:, 0] = shape[:, 0]
        shapeXY[:, 1] = shape[:, 2]
        shapeXY[:, 1] += get_value(self.pose.translation.z)

        line = np.array([[1, height], [-1, height]])

        intersection = []
        for i, b2 in enumerate(shapeXY):
            b1 = shapeXY[i - 1]

            a1, a2 = line

            # method source: https://stackoverflow.com/a/42727584
            s = np.vstack([a1, a2, b1, b2])  # s for stacked
            h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
            l1 = np.cross(h[0], h[1])  # get first line
            l2 = np.cross(h[2], h[3])  # get second line
            x, y, z = np.cross(l1, l2)  # point of intersection
            if z == 0:  # lines are parallel
                continue
            point = (x / z, y / z)
            intersection.append(point)

        # check to see if intersections are within the shape
        intersection = np.array(intersection)
        intersection = intersection[
            np.logical_and(
                intersection[:, 0] >= np.amin(shapeXY[:, 0]),  # left
                intersection[:, 0] <= np.amax(shapeXY[:, 0]),  # right
            )
        ]
        intersection = intersection[
            np.logical_and(
                intersection[:, 1] >= np.amin(shapeXY[:, 1]),  # up
                intersection[:, 1] <= np.amax(shapeXY[:, 1]),  # down
            )
        ]

        if len(intersection) < 2:
            return None

        shape = np.array(
            [
                [intersection[0, 0], -offset, 0, 1],
                [intersection[1, 0], -offset, 0, 1],
                [intersection[1, 0], self.thickness + offset, 0, 1],
                [intersection[0, 0], self.thickness + offset, 0, 1],
            ]
        )

        return self.shape.frame.get_point_transformation_wrt(shape, wrt)
