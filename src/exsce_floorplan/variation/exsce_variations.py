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

def pose_json(pose):

    return {
        'translation' : {
            'x' : pose.translation.x.value,
            'y' : pose.translation.y.value,
            'z' : pose.translation.z.value if not pose.translation.z is None else 0 
        },
        'rotation' : pose.rotation.value
    }

def space_json(space):
    return {
        'name' : space.name,
        'location' : {
            'pose' : pose_json(space.location.pose),
            'from' : {
                'world' : space.location.from_frame.world,
                'ref' : space.location.from_frame.ref,
                'index' : space.location.from_frame.index
            },
            'to' : {
                'index' : space.location.to_frame.index
            },
            'spaced' : space.location.spaced,
            'not_aligned' : space.location.aligned
        },
        'shape' : space.shape,
        'wall_thickness' : space.wall_thickness,
        'wall_height' : space.wall_height
    }

def wall_opening_json(wall_opening):
    print(vars(wall_opening.wall_a))
    return {
        'entryway' : wall_opening.entryway,
        'window'  : wall_opening.window,
        'name' : wall_opening.name,
        'in' : {
            'wall_a' : wall_opening.wall_a,
            'wall_b' : wall_opening.wall_b
        },
        'shape' : wall_opening.shape,
        'pose' : pose_json(wall_opening.pose)
    }

def get_floorplan_as_json(flp_model):
    
    # convert the original model into a context dictionary
    context = {
        'floorplan_name' : flp_model.name,
        'name' : flp_model.name,
        'spaces' : [space_json(space) for space in flp_model.spaces],
        'wall_openings' : [wall_opening_json(wall_opening) for wall_opening in flp_model.wall_openings]
    }
    print(context)
    return context

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
                pass

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

    


# if __name__ == '__main__':

#     mm_variation = metamodel_for_language('exsce-variation-dsl')

#     model = mm_variation.model_from_file('models/hospital.variation')

#     # Sample
#     for var in model.variations:
#         print(getattr(var.ref, 'name'))
#         print(getattr(var.ref, 'shape'))

#     # Generate
    


# formulate the evaluation wrt to the requirmements/interview
# system usibilty test sus
# 
# questionare?
# fomulate a research question around the effectiveness
