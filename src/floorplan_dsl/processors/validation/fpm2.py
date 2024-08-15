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
