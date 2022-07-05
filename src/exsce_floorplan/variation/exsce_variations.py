#!/usr/bin/env python3
import sys
import traceback
import os
import io
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

from textxjinja import textx_jinja_generator
from textx import metamodel_for_language

import numpy as np 
import numpy.random as random

from helpers.helpers import (
    pose_json, 
    shape_json, 
    floor_feature_json, 
    space_json, 
    wall_opening_json, 
    default_json, 
    get_floorplan_as_json
)

def sample(context, variations):

    for var in variations.variations:

        for att in var.attributes:
            fqn = att.fqn.split('.')
            
            aux = {}
            if var.ref.__class__.__name__ == 'Space':
                for i, space in enumerate(context["spaces"]):
                    if space["name"] == var.ref.name:
                        aux = context['spaces'][i]
                        break
            elif var.ref.__class__.__name__ == 'WallOpening':
                for i, wall_opening in enumerate(context["wall_openings"]):
                    if wall_opening["name"] == var.ref.name:
                        aux = context['wall_openings'][i]
                        break
            elif var.ref.__class__.__name__ == 'FloorFeature':
                for i, space in enumerate(context["spaces"]):
                    for j, feature in enumerate(space["floor_features"]):
                        if feature["name"] == var.ref.name:
                            aux = context['spaces'][i]['floor_features'][j]
                            break

            if len(fqn) == 1:
                aux[fqn[0]] = att.distribution.sample()
            else:
                while True:
                    name = fqn.pop(0)
                    aux = aux[name]
                    if len(fqn) == 1:
                        name = fqn.pop(0)
                        aux[name] = att.distribution.sample()
                        break

    return context

def variation_floorplan_generator(metamodel, var_model, output_path, overwrite, debug, **custom_args):
    # get parent node
    flp_model = var_model.variations[0].ref
    while True:
        flp_model = flp_model.parent
        if flp_model.__class__.__name__ == "FloorPlan":
            break

    full_path = os.path.realpath(__file__)
    _path, filename = os.path.split(full_path)
    path = os.path.join(_path, 'templates')
    context = get_floorplan_as_json(flp_model)
    variations = custom_args["variations"]
    output = custom_args["output"]

    for i in range(int(variations)):
        seed = random.randint(1000, 9999)
        random.seed(seed)
        context["seed"] = seed
        sample(context, var_model)
        textx_jinja_generator(path, output, context, True)