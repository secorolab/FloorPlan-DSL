def build_shape_graph(model, output_path):
    '''
    Shape graph: shape relationships
    '''
    context = [ 
        {
            "@base": "http://exsce-floorplan.org/",
            "fp" : "http://exsce-floorplan.org/",
            "Polygon" : "fp:Polygon",
            "points": {
                "@id": "fp:points",
                "@container": "@list",
                "@type": "@id"
            }
        }
    ]

    graph = []

    for space in model.spaces:

        space_polygon = {
            "@id" : "polygon-{name}".format(name=space.name),
            "@type" : "Polygon",
            "points" : ["point-shape-{name}-{i}".format(name=space.name, i=i) for i, _ in enumerate(space.get_shape().get_points())]
        }

        graph.append(space_polygon)

        for i, wall in enumerate(space.walls):
            wall_polygon = {
                "@id" : "polygon-{name}-wall-{i}".format(name=space.name, i=i),
                "@type" : "Polygon",
                "points" : ["point-corner-{name}-wall-{i}-{j}".format(name=space.name, i=i, j=j) for j in range(4)]
            }

            graph.append(wall_polygon)

    #     for feature in space.floor_features:
    #         feature_polygon = {
    #             "@id" : "polygon-{space}-{name}".format(space=space.name, name=feature.name),
    #             "@type" : "Polygon",
    #             "points" : ["point-feature-shape-{name}-{i}".format(name=feature.name, i=i) for i, _ in enumerate(feature.get_points())]
    #         }
    #         graph.append(feature_polygon)

    # for opening in model.wall_openings:
    #     opening_polygon =  {
    #         "@id" : "polygon-opening-{name}".format(name=opening.name),
    #         "@type" : "Polygon",
    #         "points" : ["point-opening-shape-{name}-{i}".format(name=opening.name, i=i) for i, _ in enumerate(opening.get_points())]
    #     }
    #     graph.append(opening_polygon)

    shape_json_ld = {
        "@context" : context,
        "@graph" : graph,
    }

    return shape_json_ld