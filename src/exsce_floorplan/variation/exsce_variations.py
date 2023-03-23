import sys, os

from textx import TextXSemanticError, get_location

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

import jinja2
from textx import metamodel_for_language

import numpy.random as random

def get_variable_from_fqn(obj, fqn):
    '''Recursive function to get to the object of interest when using a FQN'''
    return (getattr(obj,fqn[0]) if len(fqn) == 1 
            else get_variable_from_fqn(getattr(obj,fqn[0]), fqn[1:]))

def new_sample(fp_model, var_model):
    '''Perform a sample of each distribution of the variation model'''

    # For each variation set
    for var in var_model.variations:

        # If a variable is the target of a distribution, then create a new list of 
        # attributes with only the variable. Otherwise select the list of attributes
        attributes = var.attributes if hasattr(var, "attributes") else [var]

        # For each attribute, select the value to set and sample the distribution
        for att in attributes:
            name = var.ref.name
            class_name = var.ref.__class__.__name__
            obj = fp_model["{class_name}.{name}".format(class_name=class_name, name=name)]

            if hasattr(att, "fqn"):
                fqn = att.fqn.split('.')
                obj = get_variable_from_fqn(obj, fqn)

            if not hasattr(obj.value, "value"):
                raise TextXSemanticError('Semantic Error: This attribute is originally set by a variable.', 
                                **get_location(att))
            elif obj is fp_model["Default.WallThickness"] or obj is fp_model["Default.WallHeight"]:
                raise TextXSemanticError('Semantic Error: This attribute must set in the original model.', 
                                **get_location(att))

            obj.value.value = att.distribution.sample()

def variation_floorplan_generator(metamodel, var_model, output_path, overwrite, debug, **custom_args):

    model_folder_path = os.path.dirname(var_model._tx_parser.file_name)
    fp_model_path = var_model.import_uri.importURI

    fp_mm = metamodel_for_language('exsce-floorplan-dsl')
    fp_model = fp_mm.model_from_file(os.path.join(model_folder_path, fp_model_path))
    
    full_path = os.path.realpath(__file__)
    _path, filename = os.path.split(full_path)
    
    path = os.path.join(_path, 'templates')
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path),
        trim_blocks=True,
        lstrip_blocks=True)
    template = jinja_env.get_template('__floorplan_name_____seed__.floorplan.jinja')

    variations = custom_args["variations"]
    output = custom_args["output"]

    fp_model_hashtable = {}
    for space in fp_model.spaces:
        fp_model_hashtable["Space.{}".format(space.name)] = space
        for feature in space.floor_features:
            fp_model_hashtable["FloorFeature.{}".format(feature.name)] = feature
    for variable in fp_model.variables:
        fp_model_hashtable["{type}.{name}".format(type=variable.__class__.__name__, name=variable.name)] = variable
    for wall_opening in fp_model.wall_openings:
        fp_model_hashtable["WallOpening.{}".format(wall_opening.name)] = wall_opening
    fp_model_hashtable["Default.WallThickness"] = fp_model.default.wall_thickness
    fp_model_hashtable["Default.WallHeight"] = fp_model.default.wall_height

    for i in range(int(variations)):
        seed = random.randint(1000, 9999)
        random.seed(seed)
        fp_model.seed = seed
        new_sample(fp_model_hashtable, var_model)
        with open(os.path.join(output, 
                "{name}_{seed}.floorplan".format(name=fp_model.name, seed=seed)), 'w') as f:
            f.write(template.render(fp=fp_model))