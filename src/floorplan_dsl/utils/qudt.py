import numpy as np


def convert_angle_units(model, unit):

    if model.unit != unit:
        if unit == "deg" and model.unit == "rad":
            model.unit = "deg"
            model.value = np.rad2deg(model.value)
        elif unit == "rad" and model.unit == "deg":
            model.unit = "rad"
            model.value = np.deg2rad(model.value)
