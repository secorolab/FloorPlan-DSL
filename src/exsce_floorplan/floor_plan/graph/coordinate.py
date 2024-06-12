from .helpers import from_ref_name, to_ref_name, angle_from_rotation, get_value


def build_floorplan_coordinate_graph(model, output_path):
    """Returns the coordinate graph"""

    context = [
        {
            "coord": "https://comp-rob2b.github.io/metamodels/geometry/coordinates#",
            "coordinate": "https://hbrs-sesame.github.io/metamodels/coordinates#",
            "geor": "https://comp-rob2b.github.io/metamodels/geometry/spatial-relations#",
            "geom": "https://comp-rob2b.github.io/metamodels/geometry/structural-entities#",
        },
        "https://comp-rob2b.github.io/metamodels/qudt.json",
        "https://comp-rob2b.github.io/metamodels/geometry/coordinates.json",
        "https://hbrs-sesame.github.io/metamodels/geometry/coordinate-extension.json",
    ]

    graph = []

    for space in model.spaces:

        # Pose of the spaces as specificied in the model
        of = to_ref_name(space.location.to_frame, space)
        to = from_ref_name(space.location.from_frame)

        theta_space = get_value(space.location.pose.rotation)

        wall_to_wall = (not (space.location.to_frame.index is None)) and (
            not (space.location.from_frame.index is None)
        )

        if not space.location.aligned and wall_to_wall:
            theta_space += 180

        y = get_value(space.location.pose.translation.y)
        if wall_to_wall and space.location.spaced:
            from_wall = space.location.from_frame.ref.get_wall(
                space.location.from_frame.index
            )
            to_wall = space.get_wall(space.location.to_frame.index)
            wall_thickness = get_value(from_wall.thickness) + get_value(
                to_wall.thickness
            )
            y += wall_thickness

        pose_space_frame_to_ref_frame = {
            "@id": "coord:coord-pose-{of}-to-{to}".format(of=of, to=to),
            "@type": ["PoseReference", "PoseCoordinate", "VectorXY"],
            "of-pose": "geor:pose-{of}-to-{to}".format(of=of, to=to),
            "as-seen-by": to,
            "unit": ["M", "degrees"],
            "theta": theta_space,
            "x": get_value(space.location.pose.translation.x),
            "y": y,
        }

        graph.append(pose_space_frame_to_ref_frame)

        # Coordinates of vertices of space shape
        for i, point in enumerate(
            space.get_shape().get_points(wrt=space.get_shape().get_frame())
        ):
            position_shape_point_to_space_frame = {
                "@id": "coord:coord-position-point-{i}-to-{name}-frame".format(
                    name=space.name, i=i
                ),
                "@type": ["PositionReference", "PositionCoordinate", "VectorXY"],
                "of-position": "geor:position-point-{i}-to-{name}-frame".format(
                    name=space.name, i=i
                ),
                "with-respect-to": "geom:point-center-{name}".format(name=space.name),
                "as-seen-by": "geom:frame-center-{name}".format(name=space.name),
                "unit": "M",
                "x": point[0],
                "y": point[1],
            }
            graph.append(position_shape_point_to_space_frame)

        for i, wall in enumerate(space.walls):
            # Pose of the wall frames with regards to the space frame
            origin, vectors = wall.get_frame().get_direction_vectors(
                wall.get_frame().ref
            )
            theta = angle_from_rotation(vectors)

            pose_wall_frame_to_space_frame = {
                "@id": "coord:coord-pose-of-wall-{i}-frame-to-{name}-frame".format(
                    name=space.name, i=i
                ),
                "@type": ["PoseReference", "PoseCoordinate", "VectorXY"],
                "of-pose": "geor:pose-of-wall-{i}-frame-to-{name}-frame".format(
                    name=space.name, i=i
                ),
                "as-seen-by": "geom:frame-center-{name}".format(name=space.name),
                "unit": ["M", "degrees"],
                "theta": theta,
                "x": origin[0],
                "y": origin[1],
            }
            graph.append(pose_wall_frame_to_space_frame)

            for j, point in enumerate(wall.polygon):

                position_shape_point_to_wall_frame = {
                    "@id": "coord:coord-position-corner-{j}-to-{name}-wall-{i}-frame".format(
                        i=i, name=space.name, j=j
                    ),
                    "@type": ["PositionReference", "PositionCoordinate", "VectorXY"],
                    "of-position": "geor:position-corner-{j}-to-{name}-wall-{i}-frame".format(
                        i=i, name=space.name, j=j
                    ),
                    "with-respect-to": "geom:point-frame-{name}-wall-{number}".format(
                        name=space.name, number=i
                    ),
                    "as-seen-by": "geom:frame-{name}-wall-{i}".format(
                        name=space.name, i=i
                    ),
                    "unit": "M",
                    "x": point[0],
                    "y": point[1],
                }
                graph.append(position_shape_point_to_wall_frame)

        # for feature in space.floor_features:
        #     to = to_ref_name(feature.location.from_frame, space)
        #     pose_feature_frame_to_ref_frame = {
        #         "@id" : "coord-pose-frame-center-{name}-to-{to}".format(name=feature.name, to=to),
        #         "@type" : ["PoseReference", "PoseCoordinate","VectorXY"],
        #         "of-pose" : "pose-frame-center-{name}-to-{to}".format(name=feature.name, to=to),
        #         "as-seen-by" : to,
        #         "unit": ["M","degrees"],
        #         "theta" : get_value(feature.location.pose.rotation),
        #         "x": get_value(feature.location.pose.translation.x),
        #         "y": get_value(feature.location.pose.translation.y),
        #         "z": get_value(feature.location.pose.translation.z)
        #     }
        #     graph.append(pose_feature_frame_to_ref_frame)

        #     for i, point in enumerate(feature.get_points()):
        #         position_shape_point_to_feature_frame = {
        #             "@id" : "coord-position-point-feature-shape-{name}-{i}".format(name=feature.name, i=i),
        #             "@type" : ["PositionReference", "PositionCoordinate","VectorXY"],
        #             "of-position" : "position-point-feature-shape-{name}-{i}".format(name=feature.name, i=i),
        #             "with-respect-to":  "point-center-{name}".format(name=feature.name),
        #             "as-seen-by" : "frame-center-{name}".format(name=feature.name),
        #             "unit": "M",
        #             "x": point[0],
        #             "y": point[1]
        #         }
        #         graph.append(position_shape_point_to_feature_frame)

    coordinate_json_ld = {"@context": context, "@graph": graph}

    return coordinate_json_ld
