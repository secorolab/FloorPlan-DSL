import numpy as np


class Angle:
    def __init__(self, parent, value=0.0, unit="rad") -> None:
        self.parent = parent
        self.value = value
        self.unit = unit

    # TODO move this elsewhere
    def to_deg(self):
        if self.unit == "deg":
            return self.value
        elif self.unit == "rad":
            return np.rad2deg(self.value)


class Length:
    def __init__(self, parent, value=0.0, unit="m") -> None:
        self.parent = parent
        self.value = value
        self.unit = unit
