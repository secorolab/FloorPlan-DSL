from .helpers import from_ref_name, to_ref_name


def build_spatial_relations_graph(model, output_path):
    """Returns the spatial relations graph"""

    context = [
        {
            "geor": "https://comp-rob2b.github.io/metamodels/geometry/spatial-relations#",
            "geom": "https://comp-rob2b.github.io/metamodels/geometry/structural-entities#",
        },
        "https://comp-rob2b.github.io/metamodels/geometry/spatial-relations.json",
    ]

    graph = []

    for space in model.spaces:

        # Pose of the spaces as specificied in the model
        of = to_ref_name(space.location.to_frame, space)
        to = from_ref_name(space.location.from_frame)
        pose_space_frame_to_ref_frame = {
            "@id": "geor:pose-{of}-to-{to}".format(of=of, to=to),
            "@type": "Pose",
            "of": "geom:{}".format(of),
            "with-respect-to": "geom:{}".format(to),
        }

        graph.append(pose_space_frame_to_ref_frame)

        # Positions of the Polygon points to the center frame
        for i, _ in enumerate(
            space.get_shape().get_points(wrt=space.get_shape().get_frame())
        ):
            position = {
                "@id": "geor:position-point-{i}-to-{name}-frame".format(
                    i=i, name=space.name
                ),
                "@type": "Position",
                "of": "geom:point-shape-{name}-{i}".format(name=space.name, i=i),
                "with-respect-to": "geom:point-center-{name}".format(name=space.name),
            }
            graph.append(position)

        for i, wall in enumerate(space.walls):
            # Pose of the wall frames with regards to the space frame

            pose_space_frame_to_ref_frame = {
                "@id": "geor:pose-of-wall-{i}-frame-to-{name}-frame".format(
                    name=space.name, i=i
                ),
                "@type": "Pose",
                "of": "geom:frame-{name}-wall-{number}".format(
                    name=space.name, number=i
                ),
                "with-respect-to": "geom:frame-center-{name}".format(name=space.name),
            }
            graph.append(pose_space_frame_to_ref_frame)

            for j in range(4):
                point = {
                    "@id": "geor:position-corner-{j}-to-{name}-wall-{i}-frame".format(
                        i=i, name=space.name, j=j
                    ),
                    "@type": "Position",
                    "of": "geom:point-corner-{name}-wall-{i}-{j}".format(
                        name=space.name, i=i, j=j
                    ),
                    "with-respect-to": "geom:frame-{name}-wall-{i}".format(
                        name=space.name, i=i
                    ),
                }
                graph.append(point)

        # for i, feature in enumerate(space.floor_features):

        #     for i, p in enumerate(feature.get_points()):
        #         point = {
        #             "@id" : "position-point-feature-shape-{name}-{i}".format(name=feature.name, i=i),
        #             "@type" : "Position",
        #             "of" : "point-feature-shape-{name}-{i}".format(name=feature.name, i=i),
        #             "with-respect-to" : "frame-center-{name}".format(name=feature.name),
        #         }
        #         graph.append(point)

        #     to = to_ref_name(feature.location.from_frame, space)

        #     pose_feature_frame_to_ref_frame = {
        #         "@id" : "pose-frame-center-{name}-to-{to}".format(name=feature.name, to=to),
        #         "@type" : "Pose",
        #         "of" : "frame-center-{name}".format(name=feature.name),
        #         "with-respect-to" : to
        #     }
        #     graph.append(pose_feature_frame_to_ref_frame)

    spatial_relations_json_ld = {
        "@context": context,
        "@graph": graph,
    }

    return spatial_relations_json_ld
