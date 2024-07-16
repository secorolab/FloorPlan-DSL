import os
import json

from textxjinja import textx_jinja_generator

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

    floorplan = build_floorplan_graph(model, output_path)
    with open("{}/floorplan.json".format(output_path), "w") as file:
        json.dump(floorplan, file, indent=4)

    coordinate = build_floorplan_coordinate_graph(model, output_path)
    with open("{}/coordinate.json".format(output_path), "w") as file:
        json.dump(coordinate, file, indent=4)


    # Prepare context dictionary
    context = dict(trim_blocks=True, lstrip_blocks=True)
    context['model'] = model

    this_folder = os.path.dirname(__file__)
    print(this_folder)
    # template_folder = os.path.join(this_folder, '../templates/skeleton.json.jinja')
    # template_folder = os.path.join(this_folder, '../templates/shape.json.jinja')
    template_folder = os.path.join(this_folder, '../templates/spatial_relations.json.jinja')
    print("Template folder: ", template_folder)

    # Run Jinja generator
    textx_jinja_generator(template_folder, output_path, context, overwrite=True)