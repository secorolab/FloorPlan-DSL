from .Polytope import *
from .Geometry import Frame
from .Wall import Wall
'''
TODO
* Do not return a wall polygon if the width is 0
* Add methods for boolean operations with 
'''

class Space(object):
    '''
    A class to represent a space.

    ... 

    Attributes
    ----------
    parent : Textx object
        Parent element of the space object
    name : String
        Name of the space
    shape : Polytope
        Polytope that describe the inner boundary of the space
    location : Textx object 
        Textx object that contains information on reference frames, translation
        and rotation
    walls : list[Walls]
        walls of the space
    floor_features : list[FloorFeatures] optional
        list of FloorFeature objects
    order : int optional
        Order index for resolving space overlaps
    wall_thickness : Float optional
        Thickness of the walls of the space, if not specified default value is 
        taken
    wall_height : Float optional 
        Height of the walls of the space, if not specified default value is 
        taken

    Methods
    -------
    locate_space(parent, name, shape, location, floor_features, wall_thickness, 
                wall_height, order)
        Calculates the transformation needed to locate the space according to 
        the model
    get_frame()
        returns the frame of the bounding polytope
    get_shape()
        returns the bounding polytope
    create_walls()
        creates the wall objects for the space, each wall contains a frame 
        to describe pose relations
    get_wall_frame(index)
        returns the frame for the wall at the specified index
    get_wall_thickness(index)
        returns the thickness of the wall at the specified index
    offset_shape()
        creates the polygons that bound each wall in accordance to their 
        thickness and the thickness of the neighbour walls
    get_walls_wrt_world()
        returns the inner boundary polygon for the space expressed wrt to the 
        world
    '''

    def __init__(self, parent, name, shape, location, floor_features, 
                wall_thickness, wall_height, order):
        '''
        Constructs the wall object

        Parameters
        ----------
        parent : Textx object
            Parent element of the space object
        name : String
            Name of the space
        shape : Polytope
            Polytope that describe the inner boundary of the space
        location : Textx object 
            Textx object that contains information on reference frames, 
            translation and rotation
        floor_features : list[FloorFeatures] optional
            list of FloorFeature objects
        order : int optional
            Order index for resolving space overlaps
        wall_thickness : Float optional
            Thickness of the walls of the space, if not specified default value 
            is             taken
        wall_height : Float optional 
            Height of the walls of the space, if not specified default value is 
            taken
        
        Returns
        -------
        None
        '''

        self.parent = parent
        self.name = name
        self.shape = shape
        self.location = location
        self.floor_features = floor_features
        self.order = order  

        # Get values for height and thickness of wall, default if not specified
        self.wall_thickness =(wall_thickness.value if not wall_thickness is None 
                                else self.parent.default.wall_thickness.value)

        self.wall_height = (wall_height.value if not wall_height is None 
                                    else self.parent.default.wall_height.value)

        # Create the walls, offset the inner boundary, and locate the space
        self.create_walls()
        self.offset_shape(self.wall_thickness)
        self.locate_space()

    def locate_space(self):
        '''
        Calculates the transformation needed to locate the space according to 
        the model

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''
        # Select the correct frames of reference for the transformation
        from_frame = Frame()
        to_frame = self.get_frame()

        if not self.location._from.index is None:
            from_frame = self.location._from.ref.get_wall_frame(
                                        self.location._from.index)
        if not self.location.to.index is None:
            to_frame = self.get_wall_frame(self.location.to.index)

        # Extract from the model the translation and rotation
        pose = self.location.pose.pos
        x = pose.x.value
        y = pose.y.value
        z = pose.z.value if not pose.z is None else 0

        rot = self.location.pose.rot.value

        # Determine if two walls are selected as frames
        wall_to_wall = ((not (self.location.to.index is None)) 
                        and (not (self.location._from.index is None)))

        # if spaced flag is on and two walls are used, then add to the y value
        # the wall thickness of the two walls
        if (wall_to_wall and self.location.spaced):
            wall_thickness = (self.location._from.ref.get_wall_thickness(
                            self.location._from.index) + 
                            self.get_wall_thickness(
                            self.location.to.index)
                            )
            y += wall_thickness

        # Build the transformation matrix with an auxiliary frame
        aux_frame = Frame()
        aux_frame.set_translation(np.array([x, y, z]))
        aux_frame.set_orientation(0, 0, np.deg2rad(rot))
        T = aux_frame.get_transformation_matrix()

        # For the shape to transform, change the frame of reference
        self.shape.change_reference_frame(from_frame)

        # If two walls were selected, rotate 180 to align the walls of the 
        # spaces
        if wall_to_wall:
            frame = Frame()
            frame.set_orientation(0, 0, np.deg2rad(180))
            t, R = frame.get_transformation()
            T[0:3, 0:3] = R.dot(T[0:3, 0:3])
        
        # Calculate the transfomation needed to obtain desired result
        t_a, R_a = to_frame.get_transformation()

        po_p_T = np.hstack((np.vstack((R_a, np.zeros(3))), 
                            np.vstack((t_a.reshape((3,1)), [1]))))
        p_w_T = T.dot(np.linalg.inv(po_p_T))

        self.shape.set_transformation(p_w_T)

    def get_frame(self):
        '''
        Returns the frame of the bounding polytope

        Parameters
        ----------
        None
        
        Returns
        -------
        frame : Frame
            The frame of the polytope
        '''
        return self.shape.frame

    def get_shape(self):
        '''
        Returns the bounding polytope

        Parameters
        ----------
        None
        
        Returns
        -------
        shape : Polyotpe
            Polytope object
        '''
        return self.shape

    def create_walls(self):
        '''
        Creates the wall objects for the space, each wall contains a frame 
        to describe pose relations

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''
        points = self.shape.get_points(self.shape.frame)
        points = np.vstack((points, points[0]))
        self.walls = [Wall(p1, p2, self.shape.frame, self.wall_thickness, 
                self.wall_height) for p1, p2 in zip(points[:-1], points[1:])]

    def get_wall_frame(self, index):
        '''
        Returns the frame for the wall at the specified index

        Parameters
        ----------
        index : int
            Index of the wall to be returned
        
        Returns
        -------
        wall : Wall
            Wall object
        '''
        if index is None:
            return self.get_frame()
        return self.walls[index].get_frame()

    def get_wall_thickness(self, index):
        '''
        Returns the thickness of the wall at the specified index

        Parameters
        ----------
        index : int
            Index of the wall to be returned
        
        Returns
        -------
        wall : Wall
            Wall object
        '''

        return self.wall_thickness

    def offset_shape(self, widths=0.3):
        '''
        Creates the polygons that bound each wall in accordance to their 
        thickness and the thickness of the neighbour walls

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''
        
        num_vertices = len(self.shape.points)
        new_vertices = []

        for i, wall in enumerate(self.walls):
            
            prev_wall = self.walls[i-1]
            
            points_line1 = np.array([
                [-1, wall.thickness, 0, 1], [1, wall.thickness, 0, 1]]
                )
            points_line2 = np.array([
                [-1, prev_wall.thickness, 0, 1], [1, prev_wall.thickness, 0, 1]]
                )

            points_line1 = wall.frame.get_point_transformation_wrt(
                                                points_line1, 
                                                self.shape.frame)[:,0:2]
            points_line2 = prev_wall.frame.get_point_transformation_wrt(
                                                points_line2, 
                                                self.shape.frame)[:,0:2]

            a1, a2 = points_line1
            b1, b2 = points_line2

            point = []

            # method source: https://stackoverflow.com/a/42727584
            s = np.vstack([a1,a2,b1,b2])        # s for stacked
            h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
            l1 = np.cross(h[0], h[1])           # get first line
            l2 = np.cross(h[2], h[3])           # get second line
            x, y, z = np.cross(l1, l2)          # point of intersection
            if z == 0:                          # lines are parallel
                point = (float('inf'), float('inf'))
            point = (x/z, y/z)
            new_vertices.append([point[0], point[1], 0])
        
        for i, wall in enumerate(self.walls):
            next_point = (i + 1) % num_vertices
            wall.set_wall_polygon([new_vertices[i], new_vertices[next_point], 
                self.shape.points[next_point], self.shape.points[i]])

    def get_walls_wrt_world(self):
        '''
        Returns the inner boundary polygon for the space expressed wrt to the 
        world

        Parameters
        ----------
        None
        
        Returns
        -------
        wall_points : Numpy array
            The boundary points of the walls wrt to the world
        '''
        wall_points = []

        for wall in self.walls:
            points = np.hstack(
                (np.array(wall.polygon), np.ones((len(wall.polygon), 1)))
            )
            wall_points.append(
                self.shape.frame.get_point_transformation_wrt(points)
            )

        return wall_points