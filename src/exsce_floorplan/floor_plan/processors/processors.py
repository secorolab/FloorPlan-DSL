from textx import TextXSemanticError, get_location
import numpy as np

# from shapely.geometry import Polygon
# from shapely.ops import unary_union


def opening_obj_processors(opening):
    # wall_a = opening.wall_a

    # opening_shape = opening.generate_2d_structure(opening.pose.translation.z.value, offset=0)
    # opening_shape = Polygon(opening_shape[:, 0:2])
    # wall_shape = Polygon(wall_a.generate_3d_structure()[0][0:4, 0:2])

    # if not opening.wall_b is None:
    #     b = Polygon(opening.wall_b.generate_3d_structure()[0][0:4, 0:2])
    #     wall_shape = unary_union([wall_shape,b])

    # if abs(wall_shape.intersection(opening_shape).area - opening_shape.area) > 0.05:
    #     raise TextXSemanticError(
    #         '{opening} can not fit inside of the walls'.format(
    #             opening=opening.name,
    #         ),
    #         **get_location(opening))
    pass


def feature_obj_processor(feature):

    # space_polygon = Polygon(feature.parent.shape.get_points()[:, 0:2])
    # feature_polygon = Polygon(feature.shape.get_points()[:, 0:2])

    # if not space_polygon.intersects(feature_polygon):
    #     raise TextXSemanticError(
    #         '{feature} is located outside {space}'.format(
    #             feature=feature.name,
    #             space=feature.parent.name),
    #         **get_location(feature))
    pass


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
                    **get_location(feature)
                )

    for opening in floorplan.wall_openings:
        if not opening.name in names:
            names.append(opening.name)
        else:
            raise TextXSemanticError(
                "Spaces and features must have unique names", **get_location(opening)
            )
