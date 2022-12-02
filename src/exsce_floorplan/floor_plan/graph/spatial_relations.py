from .helpers import from_ref_name, to_ref_name

def build_spatial_relations_graph(model, output_path):
    '''Returns the spatial relations graph'''

    context = [
        {
            "@base":"http://exsce-floorplan.org/", 
            "skeleton":"http://exsce-floorplan.org/"
        },
        "https://comp-rob2b.github.io/metamodels/geometry/spatial-relations.json"
    ]

    graph = []

    for space in model.spaces: 
        
        # Pose of the spaces as specificied in the model
        of = to_ref_name(space.location.to_frame, space)
        to = from_ref_name(space.location.from_frame)
        pose_space_frame_to_ref_frame = {
            "@id" : "pose-{of}-to-{to}".format(of=of, to=to),
            "@type" : "Pose",
            "of" : of,
            "with-respect-to" : to
        }

        graph.append(pose_space_frame_to_ref_frame)

        # Positions of the Polygon points to the center frame
        for i, _ in enumerate(space.get_shape().get_points(wrt=space.get_shape().get_frame())):
            position = {
                "@id" : "position-point-{i}-to-{name}-frame".format(i=i, name=space.name),
                "@type" : "Position",
                "of" : "point-shape-{name}-{i}".format(name=space.name, i=i),
                "with-respect-to" : "point-center-{name}".format(name=space.name)
            }
            graph.append(position)
        
        for i, wall in enumerate(space.walls):
            # Pose of the wall frames with regards to the space frame

            pose_space_frame_to_ref_frame = {
                "@id" : "pose-of-wall-{i}-frame-to-{name}-frame".format(name=space.name, i=i),
                "@type" : "Pose",
                "of" : "frame-{name}-wall-{number}".format(name=space.name, number=i),
                "with-respect-to" : "frame-center-{name}".format(name=space.name)
            }
            graph.append(pose_space_frame_to_ref_frame)

            for j in range(4):
                point = {
                    "@id" : "position-corner-{j}-to-{name}-wall-{i}-frame".format(i=i, name=space.name, j=j),
                    "@type" : "Position",
                    "of" : "point-corner-{name}-wall-{i}-{j}".format(name=space.name, i=i, j=j),
                    "with-respect-to" : "frame-{name}-wall-{i}".format(name=space.name, i=i)
                }
                graph.append(point)

    spatial_relations_json_ld = {
        "@context" : context,
        "@graph" : graph,
        "@id" : "{name}-spatial_relations".format(name=model.name)
    }

    return spatial_relations_json_ld