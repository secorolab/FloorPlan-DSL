from textx.exceptions import TextXSemanticError, TextXSyntaxError
from textx import (
    textx_isinstance,
    get_metamodel,
    get_model,
    get_location,
    metamodel_for_language,
)


def validate_variable_reference_as_value(value, var_type="LengthVariable"):
    mm = get_metamodel(value)
    mm_var_type = mm[var_type]
    if textx_isinstance(value, mm["VariableReference"]) and not textx_isinstance(
        value.variable, mm_var_type
    ):
        expected_unit = mm_var_type._tx_attrs.get("unit").cls._tx_peg_rule
        raise TextXSemanticError(
            "Expected an assignment in {}. {} has {} units".format(
                expected_unit, value.variable.name, value.variable.unit
            ),
            **get_location(value),
        )


def validate_length_value(value):
    validate_variable_reference_as_value(value, "LengthVariable")


def validate_angle_value(value):
    validate_variable_reference_as_value(value, "AngleVariable")


def transformation_in_direction(direction):
    if direction and direction.value != 0.0:
        return True
    return False


def validate_opening_location(opening):
    if opening.location.rotation and (
        transformation_in_direction(opening.location.rotation.x)
        or transformation_in_direction(opening.location.rotation.z)
    ):
        raise TextXSyntaxError(
            "Openings must only specify rotations about the y-axis",
            **get_location(opening.location.rotation),
        )

    if opening.location.translation and transformation_in_direction(
        opening.location.translation.y
    ):
        raise TextXSyntaxError(
            "Openings must only define translations wrt to x and/or z",
            **get_location(opening.location.translation),
        )


def validate_element_location(element):
    element_type = element.__class__.__name__
    if element.location.rotation and (
        transformation_in_direction(element.location.rotation.x)
        or transformation_in_direction(element.location.rotation.y)
    ):
        raise TextXSyntaxError(
            "{} must only specify rotations about the z-axis".format(element_type),
            **get_location(element.location.rotation),
        )

    if element.location.translation and transformation_in_direction(
        element.location.translation.z
    ):
        raise TextXSyntaxError(
            "{} must only define translations wrt to x and/or y".format(element_type),
            **get_location(element.location.translation),
        )


def validate_size_is_non_zero_positive(metric):
    if metric.value <= 0:
        raise TextXSemanticError(
            "Width must be a positive number",
            **get_location(metric),
        )


def validate_opening_shape(opening):
    mm = get_metamodel(opening)
    if textx_isinstance(opening.shape, mm["Rectangle"]):
        if opening.shape.length:
            raise TextXSyntaxError(
                "Openings with rectangle shape must define height instead of length",
                **get_location(opening.shape.length),
            )

        validate_size_is_non_zero_positive(opening.shape.width)
        validate_size_is_non_zero_positive(opening.shape.height)


def validate_element_shape(element):
    element_type = element.__class__.__name__
    mm = get_metamodel(element)
    if textx_isinstance(element.shape, mm["Rectangle"]):
        if element.shape.height:
            raise TextXSyntaxError(
                "{} with rectangle shape must define length instead of height".format(
                    element_type
                ),
                **get_location(element.shape.height),
            )
        validate_size_is_non_zero_positive(element.shape.width)
        validate_size_is_non_zero_positive(element.shape.length)
    elif textx_isinstance(element.shape, mm["Polygon"]):
        for point in element.shape.coordinates:
            if transformation_in_direction(point.z):
                raise TextXSyntaxError(
                    "{} with polygon shape must define points with coordinates only in (x,y)".format(
                        element_type
                    ),
                    **get_location(element.shape.coordinates),
                )
