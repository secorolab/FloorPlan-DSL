from textx import TextXSemanticError, get_location
import numpy as np


def unique_names_processor(floorplan):

    names = []

    for space in floorplan.spaces:

        if not space.name in names:
            names.append(space.name)
        else:
            raise TextXSemanticError(
                "Spaces and features must have unique names", **get_location(space)
            )

        for feature in space.floor_features:
            fqn = "{space}.{feature}".format(space=space.name, feature=feature.name)
            if not fqn in names:
                names.append(fqn)
            else:
                raise TextXSemanticError(
                    "Spaces and features must have unique names",
                    **get_location(feature),
                )

    for opening in floorplan.wall_openings:
        if not opening.name in names:
            names.append(opening.name)
        else:
            raise TextXSemanticError(
                "Spaces and features must have unique names", **get_location(opening)
            )
