def build_skeleton_graph(model, output_path):
    '''
    Skeleton graph: only geometry entities without relations. Namely points and 
    frames.
    '''
    context = [
        {
            "@base": "http://exsce-floorplan.org/"
        },
        "https://comp-rob2b.github.io/metamodels/geometry/structural-entities.json"
    ]

    # Create the world origin and the world frame
    skeleton_graph = [
        {
            "@id" : "world-origin",
            "@type" : "Point"
        },
        {
            "@id" : "world-frame",
            "@type" : "Frame",
            "origin" : "world-origin"
        }
    ]

    for space in model.spaces:

        # Every space has a center point and a frame that coincides with it
        space_point = {
            "@id" : "point-center-{name}".format(name=space.name),
            "@type" : "Point"
        }
        space_frame = {
            "@id" : "frame-center-{name}".format(name=space.name),
            "@type" : "Frame",
            "origin" : "point-center-{name}".format(name=space.name)
        }
        skeleton_graph.append(space_point)
        skeleton_graph.append(space_frame)  

        # Every space has a bounding shape, so a point per vertice is created
        for i, _ in enumerate(space.get_shape().get_points()):
            space_point = {
                "@id" : "point-shape-{name}-{i}".format(name=space.name, i=i),
                "@type" : "Point"
            }
            skeleton_graph.append(space_point)

        for i, wall in enumerate(space.walls):
            
            # Every wall has a center point and a frame that coincides with it
            wall_frame_point = {
                "@id" : "point-frame-{name}-wall-{number}".format(name=space.name, number=i),
                "@type" : "Point"
            }
            wall_frame = {
                "@id" : "frame-{name}-wall-{number}".format(name=space.name, number=i),
                "@type" : "Frame",
                "origin" : "point-frame-{name}-wall-{number}".format(name=space.name, number=i)
            }
            skeleton_graph.append(wall_frame_point)
            skeleton_graph.append(wall_frame)  

            # Every wall has four points that are define wrt to the center frame
            for j in range(4):
                point = {
                    "@id" : "point-corner-{name}-wall-{number}-{j}".format(name=space.name, number=i, j=j),
                    "@type" : "Point"
                }
                skeleton_graph.append(point)
    
    # Form the skeleton json and dump it
    skeleton_json_ld = {
        "@context" : context,
        "@graph" : skeleton_graph,
    }

    return skeleton_json_ld