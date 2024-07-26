import os

from textxjinja import textx_jinja_generator


def jsonld_floorplan_generator(
    metamodel, model, output_path, overwrite=True, debug=False, **custom_args
):

    if "{{model_name}}" in output_path:
        output_path = output_path.replace("{{model_name}}", model.name)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Prepare context dictionary
    context = dict(trim_blocks=True, lstrip_blocks=True)
    context["model"] = model

    this_folder = os.path.dirname(__file__)
    # If given a directory instead of a single template, textX-Jinja copies the entire file/folder tree to the output folder
    # For now we invoke the generator for each template we are interested in
    # TODO Find more optimal way to handle templates
    template_folder = os.path.join(this_folder, "../templates/skeleton.json.jinja")

    # Run Jinja generator
    textx_jinja_generator(template_folder, output_path, context, overwrite=True)

    template_folder = os.path.join(this_folder, "../templates/shape.json.jinja")
    textx_jinja_generator(template_folder, output_path, context, overwrite=True)
    template_folder = os.path.join(
        this_folder, "../templates/spatial_relations.json.jinja"
    )
    textx_jinja_generator(template_folder, output_path, context, overwrite=True)
    template_folder = os.path.join(this_folder, "../templates/floorplan.json.jinja")
    textx_jinja_generator(template_folder, output_path, context, overwrite=True)
    template_folder = os.path.join(this_folder, "../templates/coordinate.json.jinja")
    textx_jinja_generator(template_folder, output_path, context, overwrite=True)
