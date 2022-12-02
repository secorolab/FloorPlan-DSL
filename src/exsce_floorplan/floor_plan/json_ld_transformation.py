import json, os
import traceback, sys
from textx import metamodel_for_language
from pathlib import Path

from graph.skeleton import build_skeleton_graph
from graph.shape import build_shape_graph
from graph.spatial_relations import build_spatial_relations_graph
from graph.floor_plan import build_floorplan_graph
from graph.coordinate import build_floorplan_coordinate_graph

import rdflib
from rdflib.tools.rdf2dot import rdf2dot

def jsonld_floorplan_generator(metamodel, model, output_path, overwrite=True, debug=False, **custom_args):
    
    skeleton = build_skeleton_graph(model, output_path)
    shape = build_shape_graph(model, output_path)
    spatial_relations = build_spatial_relations_graph(model, output_path)
    floorplan = build_floorplan_graph(model, output_path)
    coordinate = build_floorplan_coordinate_graph(model, output_path)
    
    directory = "{output}/{name}_json_ld".format(output=output_path, name=model.name)
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

        
    # g = rdflib.ConjunctiveGraph()

    # TUTORIAL = directory
    # g.parse(TUTORIAL + "/skeleton.json", format="json-ld")
    # g.parse(TUTORIAL + "/spatial_relations.json", format="json-ld")
    # g.parse(TUTORIAL + "/coordinate.json", format="json-ld")
    # g.parse(TUTORIAL + "/floorplan.json", format="json-ld")
    # g.parse(TUTORIAL + "/shape.json", format="json-ld")

    # j = json.loads(g.serialize(format="json-ld"))

    # with open("{}/all.json".format(directory), "w") as file:
    #     json.dump(j, file)


if __name__ == '__main__':
    try:
        my_metamodel = metamodel_for_language('exsce-floorplan-dsl')
        argv = sys.argv[sys.argv.index("--") + 1:]
        my_model = my_metamodel.model_from_file(argv[0])
        output_path = argv[1]

        jsonld_floorplan_generator(my_metamodel, my_model, output_path)

    except Exception:
        print(traceback.format_exc())
        sys.exit(1)