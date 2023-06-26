def get_value(variable):
    """Helper function to retrive a numeric value from the model"""

    if variable is None:
        return 0
    elif not variable.ref is None:
        return variable.ref.value.value if variable.neg is False else (variable.ref.value.value * (-1))
    else:
        return variable.value.value