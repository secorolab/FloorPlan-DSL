import floorplan_dsl.processors.semantics.fpm2 as s2
import floorplan_dsl.processors.validation.fpm2 as v2


def space_processor(space):
    v2.validate_element_location(space)
    v2.validate_element_shape(space)
    s2.space_obj_processor(space)


def feature_processor(feature):
    v2.validate_element_location(feature)
    v2.validate_element_shape(feature)
    s2.feature_obj_processor(feature)


def opening_processor(opening):
    v2.validate_opening_location(opening)
    v2.validate_opening_shape(opening)
    s2.opening_obj_processor(opening)


def wall_processor(wall):
    v2.validate_element_shape(wall)
