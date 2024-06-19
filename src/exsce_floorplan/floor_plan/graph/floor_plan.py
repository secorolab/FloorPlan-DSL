def build_floorplan_graph(model, output_path):
    """Returns the floorplan graph"""
    context = [
        {
            "floorplan": "https://secorolab.github.io/metamodels/floorplan#",
            "polytope": "https://secorolab.github.io/metamodels/polytope#",
        },
        "https://secorolab.github.io/metamodels/floor-plan/floor-plan.json",
    ]

    graph = []

    for space in model.spaces:

        for i, wall in enumerate(space.walls):

            wall_json = {
                "@id": "floorplan:space-{name}-wall-{i}".format(name=space.name, i=i),
                "@type": "Wall",
                "shape": "polytope:polygon-{name}-wall-{i}".format(
                    name=space.name, i=i
                ),
            }

            graph.append(wall_json)

        for i, feature in enumerate(space.floor_features):
            feature_json = {
                "@id": "floorplan:feature-{space}-{name}".format(
                    space=space.name, name=feature.name
                ),
                "@type": "Feature",
                "shape": "polytope:polygon-{space}-feature-{name}".format(
                    space=space.name, name=feature.name
                ),
            }
            graph.append(feature_json)

        space_json = {
            "@id": "floorplan:space-{name}".format(name=space.name),
            "@type": "Space",
            "walls": [
                "floorplan:space-{name}-wall-{i}".format(name=space.name, i=i)
                for i in range(len(space.walls))
            ],
            "feature": [
                "floorplan:feature-{space}-{name}".format(
                    space=space.name, name=feature.name
                )
                for feature in space.floor_features
            ],
            "shape": "polytope:polygon-{name}".format(name=space.name),
        }

        graph.append(space_json)

    graph.append(
        {
            "@id": "floorplan:{name}".format(name=model.name),
            "@type": "FloorPlan",
            "spaces": [
                "floorplan:space-{name}".format(name=space.name)
                for space in model.spaces
            ],
        }
    )

    floorplan_json_ld = {"@context": context, "@graph": graph}

    return floorplan_json_ld
