import os

import numpy as np

from textx import get_children_of_type
from textxjinja import textx_jinja_generator

from floorplan_dsl.utils.qudt import convert_angle_units


def jsonld_floorplan_generator(
    metamodel, model, output_path, overwrite=True, debug=False, **custom_args
):

    if "{{model_name}}" in output_path:
        output_path = output_path.replace("{{model_name}}", model.name)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    angle_unit = custom_args.get("angle-unit", "rad")
    for a in get_children_of_type("Angle", model):
        convert_angle_units(a, angle_unit)
    for a in get_children_of_type("AngleVariable", model):
        convert_angle_units(a, angle_unit)

    # Change the frame of reference of wall's shape points to compare against v1 models
    # TODO Remove this once v1 is deprecated
    wall_point_reference = custom_args.get("change-wall-point-reference", False)
    if wall_point_reference:
        for s in get_children_of_type("Space", model):
            for w in s.walls:
                tm = w.get_transformation_matrix_wrt_parent()
                for p in w.shape.coordinates:
                    point = np.array([p.x.value, p.y.value, p.z.value, 1])
                    point_wrt_space = np.einsum("ij,j->i", tm, point)
                    p.x.value = round(point_wrt_space[0], 2)
                    p.y.value = round(point_wrt_space[1], 2)

    # Prepare context dictionary
    context = dict(trim_blocks=True, lstrip_blocks=True)
    context["model"] = model

    this_folder = os.path.dirname(__file__)
    # If given a directory instead of a single template, textX-Jinja copies the entire file/folder tree to the output folder
    # For now we invoke the generator for each template we are interested in
    # TODO Find more optimal way to handle templates
    template_folder = os.path.join(
        this_folder, "../templates/json-ld/skeleton.json.jinja"
    )

    # Run Jinja generator
    textx_jinja_generator(template_folder, output_path, context, overwrite=True)

    template_folder = os.path.join(this_folder, "../templates/json-ld/shape.json.jinja")
    textx_jinja_generator(template_folder, output_path, context, overwrite=True)
    template_folder = os.path.join(
        this_folder, "../templates/json-ld/spatial_relations.json.jinja"
    )
    textx_jinja_generator(template_folder, output_path, context, overwrite=True)
    template_folder = os.path.join(
        this_folder, "../templates/json-ld/floorplan.json.jinja"
    )
    textx_jinja_generator(template_folder, output_path, context, overwrite=True)
    template_folder = os.path.join(
        this_folder, "../templates/json-ld/coordinate.json.jinja"
    )
    textx_jinja_generator(template_folder, output_path, context, overwrite=True)


def v1_to_v2_converter(metamodel, model, output_path, overwrite, debug, **kwargs):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Prepare context dictionary
    context = dict(trim_blocks=True, lstrip_blocks=True)
    context["model"] = model
    context["name"] = model.name

    this_folder = os.path.dirname(__file__)
    template_folder = os.path.join(this_folder, "../templates/fpm2/__name__.fpm2.jinja")

    # Run Jinja generator
    textx_jinja_generator(template_folder, output_path, context, overwrite=overwrite)
