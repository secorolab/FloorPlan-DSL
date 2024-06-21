import os
import json


from .graph.skeleton import build_skeleton_graph
from .graph.shape import build_shape_graph
from .graph.spatial_relations import build_spatial_relations_graph
from .graph.floor_plan import build_floorplan_graph
from .graph.coordinate import build_floorplan_coordinate_graph


def jsonld_floorplan_generator(
    metamodel, model, output_path, overwrite=True, debug=False, **custom_args
):

    if "{{model_name}}" in output_path:
        output_path = output_path.replace("{{model_name}}", model.name)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    skeleton = build_skeleton_graph(model, output_path)
    with open("{}/skeleton.json".format(output_path), "w") as file:
        json.dump(skeleton, file, indent=4)

    shape = build_shape_graph(model, output_path)
    with open("{}/shape.json".format(output_path), "w") as file:
        json.dump(shape, file, indent=4)

    spatial_relations = build_spatial_relations_graph(model, output_path)
    with open("{}/spatial_relations.json".format(output_path), "w") as file:
        json.dump(spatial_relations, file, indent=4)

    floorplan = build_floorplan_graph(model, output_path)
    with open("{}/floorplan.json".format(output_path), "w") as file:
        json.dump(floorplan, file, indent=4)

    coordinate = build_floorplan_coordinate_graph(model, output_path)
    with open("{}/coordinate.json".format(output_path), "w") as file:
        json.dump(coordinate, file, indent=4)


if __name__ == "__main__":
    import sys
    import configparser
    from textx import metamodel_for_language
    import traceback

    try:
        my_metamodel = metamodel_for_language("exsce-floorplan-dsl")
        argv = sys.argv[sys.argv.index("--") + 1 :]
        my_model = my_metamodel.model_from_file(argv[0])

        config = configparser.ConfigParser()
        config.read("setup.cfg")

        output_path = config["composable_models"]["output_folder"]

        if "{{model_name}}" in output_path:
            output_path = output_path.replace("{{model_name}}", my_model.name)
            if not os.path.exists(output_path):
                os.makedirs(output_path)

        jsonld_floorplan_generator(my_metamodel, my_model, output_path)

    except Exception:
        print(traceback.format_exc())
        sys.exit(1)
