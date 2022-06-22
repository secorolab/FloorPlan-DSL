from textx import TextXSemanticError, get_location
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union

def opening_fitting_processor(opening):
    wall_a = opening.wall_a

    opening_shape = opening.generate_2d_structure(opening.loc.pos.z.value, offset=0)
    opening_shape = Polygon(opening_shape[:, 0:2])
    wall_shape = Polygon(wall_a.generate_3d_structure()[0][0:4, 0:2])
    
    if not opening.wall_b is None:
        b = Polygon(opening.wall_b.generate_3d_structure()[0][0:4, 0:2])
        wall_shape = unary_union([wall_shape,b])
    
    if abs(wall_shape.intersection(opening_shape).area - opening_shape.area) > 0.05:
        raise TextXSemanticError(
            '{opening} can not fit inside of the walls'.format(
                opening=opening.name,
            ), 
            **get_location(opening))

def opening_obj_processors(opening):
    opening_fitting_processor(opening)