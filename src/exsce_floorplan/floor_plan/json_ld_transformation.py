import json, os
import traceback, sys
import configparser
from textx import metamodel_for_language
from pathlib import Path

from .graph.skeleton import build_skeleton_graph
from .graph.shape import build_shape_graph
from .graph.spatial_relations import build_spatial_relations_graph
from .graph.floor_plan import build_floorplan_graph
from .graph.coordinate import build_floorplan_coordinate_graph

# import rdflib
# from rdflib.tools.rdf2dot import rdf2dot


def jsonld_floorplan_generator(
    metamodel, model, output_path, overwrite=True, debug=False, **custom_args
):

    config = configparser.ConfigParser()
    path_to_file = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.parent

    config.read(os.path.join(path_to_file, "setup.cfg"))

    print("config", config)

    output_path = config["composable_models"]["output_folder"]

    if "{{model_name}}" in output_path:
        output_path = output_path.replace("{{model_name}}", model.name)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    skeleton = build_skeleton_graph(model, output_path)
    shape = build_shape_graph(model, output_path)
    spatial_relations = build_spatial_relations_graph(model, output_path)
    floorplan = build_floorplan_graph(model, output_path)
    coordinate = build_floorplan_coordinate_graph(model, output_path)

    directory = os.path.join(output_path, "{name}_json_ld".format(name=model.name))
    print(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open("{}/skeleton.json".format(directory), "w") as file:
        json.dump(skeleton, file, indent=4)

    with open("{}/shape.json".format(directory), "w") as file:
        json.dump(shape, file, indent=4)

    with open("{}/spatial_relations.json".format(directory), "w") as file:
        json.dump(spatial_relations, file, indent=4)

    with open("{}/floorplan.json".format(directory), "w") as file:
        json.dump(floorplan, file, indent=4)

    with open("{}/coordinate.json".format(directory), "w") as file:
        json.dump(coordinate, file, indent=4)


if __name__ == "__main__":
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
