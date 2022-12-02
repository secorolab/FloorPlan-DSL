from .helpers import from_ref_name, to_ref_name, angle_from_rotation

def build_floorplan_coordinate_graph(model, output_path):
    '''Returns the coordinate graph'''

    context = [
        "https://comp-rob2b.github.io/metamodels/geometry/coordinates.json",
        "https://comp-rob2b.github.io/metamodels/qudt.json",
        {
            "rob": "https://comp-rob2b.github.io/modelling-tutorial/robot#",
            "theta" : "rob:theta",
            "degress" : "rob:degrees"
        }
    ]

    graph = []

    for space in model.spaces: 
        
        # Pose of the spaces as specificied in the model
        of = to_ref_name(space.location.to_frame, space)
        to = from_ref_name(space.location.from_frame)
        
        pose_space_frame_to_ref_frame = {
            "@id" : "coord-pose-{of}-to-{to}".format(of=of, to=to),
            "@type" : ["PoseReference", "PoseCoordinate","VectorXY"],
            "of-pose" : "pose-{of}-to-{to}".format(of=of, to=to),
            "as-seen-by" : to,
            "unit": ["M","degrees"],
            "theta" : space.location.pose.rotation.value,
            "x": space.location.pose.translation.x.value,
            "y": space.location.pose.translation.y.value
        }

        graph.append(pose_space_frame_to_ref_frame)

        # Coordinates of vertices of space shape
        for i, point in enumerate(space.get_shape().get_points(wrt=space.get_shape().get_frame())):
            position_shape_point_to_space_frame = {
                "@id" : "coord-position-point-{i}-to-{name}-frame".format(name=space.name, i=i),
                "@type" : ["PositionReference", "PositionCoordinate","VectorXY"],
                "of-position" : "position-point-{i}-to-{name}-frame".format(name=space.name, i=i),
                "with-respect-to": "point-center-{name}".format(name=space.name),
                "as-seen-by" : "frame-center-{name}".format(name=space.name),
                "unit": "M",
                "x": point[0],
                "y": point[1]
            }
            graph.append(position_shape_point_to_space_frame)
        
        for i, wall in enumerate(space.walls):
            # Pose of the wall frames with regards to the space frame
            origin, vectors = wall.get_frame().get_direction_vectors(wall.get_frame().ref)
            theta = angle_from_rotation(vectors)

            pose_wall_frame_to_space_frame = {
                "@id" : "coord-pose-of-wall-{i}-frame-to-{name}-frame".format(name=space.name, i=i),
                "@type" : ["PoseReference", "PoseCoordinate","VectorXY"],
                "of-pose" : "pose-of-wall-{i}-frame-to-{name}-frame".format(name=space.name, i=i),
                "as-seen-by" : "frame-center-{name}".format(name=space.name),
                "unit": ["M","degrees"],
                "theta" : theta,
                "x": origin[0],
                "y": origin[1]
            }
            graph.append(pose_wall_frame_to_space_frame)
            
            for j, point in enumerate(wall.polygon):

                position_shape_point_to_wall_frame = {
                    "@id" : "coord-position-corner-{j}-to-{name}-wall-{i}-frame".format(i=i, name=space.name, j=j),
                    "@type" : ["PositionReference", "PositionCoordinate","VectorXY"],
                    "of-position" : "position-corner-{j}-to-{name}-wall-{i}-frame".format(i=i, name=space.name, j=j),
                    "with-respect-to": "point-frame-{name}-wall-{number}".format(name=space.name, number=i),
                    "as-seen-by" : "frame-{name}-wall-{i}".format(name=space.name, i=i),
                    "unit": "M",
                    "x": point[0],
                    "y": point[1]
                }
                graph.append(position_shape_point_to_wall_frame)


    coordinate_json_ld = {
        "@context" : context,
        "@id" : "{name}-coordinates".format(name=model.name),
        "@graph" : graph
    }

    return coordinate_json_ld