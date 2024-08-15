import sys
import os

from operator import attrgetter
import numpy.random as random

from textx import TextXSemanticError, get_children_of_type, metamodel_for_language
from textx.scoping.tools import get_unique_named_object

from textxjinja import textx_jinja_generator

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)


def get_variable_from_fqn(obj, fqn):
    """Recursive function to get to the object of interest when using a FQN"""
    f = attrgetter(fqn)
    return f(obj)


def new_sample(fp_model, var_model):
    """Perform a sample of each distribution of the variation model"""

    # For each variation set
    for var in var_model.variations:
        print("---")
        print(var.ref.name)

        # If it's a variable, sample a new value for it
        if var.__class__.__name__ == "VariableRef":
            var_obj = get_unique_named_object(fp_model, var.ref.name)
            var_obj.value = var.distribution.sample()
            continue

        # Otherwise select the of attributes
        attributes = get_children_of_type("Attribute", var)

        for att in attributes:
            print("\t", att.fqn)
            fp_obj = get_unique_named_object(fp_model, var.ref.name)
            var_obj = get_variable_from_fqn(fp_obj, att.fqn)
            if var_obj.__class__.__name__ in ["LengthValue", "AngleValue"]:
                var_obj.value.value = att.distribution.sample()
            elif var_obj.__class__.__name__ in ["Length", "Angle"]:
                var_obj.value = att.distribution.sample()


def variation_floorplan_generator(
    metamodel, var_model, output_path, overwrite, debug, **custom_args
):

    model_folder_path = os.path.dirname(var_model._tx_parser.file_name)
    fp_model_path = var_model.import_uri.importURI

    fp_mm = metamodel_for_language("floorplan-v2")

    # Remove the object processors to have references to location.wrt and location.of
    fp_mm._obj_processors = fp_mm._default_obj_processors

    fp_model = fp_mm.model_from_file(os.path.join(model_folder_path, fp_model_path))

    this_folder = os.path.dirname(__file__)
    template_folder = os.path.join(
        this_folder, "../templates/fpm2/__name_____seed__.fpm2.jinja"
    )

    variations = custom_args["variations"]

    for i in range(int(variations)):
        seed = random.randint(1000, 9999)
        random.seed(seed)
        fp_model.seed = seed
        new_sample(fp_model, var_model)
        context = dict(trim_blocks=True, lstrip_blocks=True)
        context["model"] = fp_model
        context["seed"] = seed
        context["name"] = fp_model.name
        textx_jinja_generator(
            template_folder, output_path, context, overwrite=overwrite
        )
