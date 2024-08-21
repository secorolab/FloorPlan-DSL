class Angle:
    def __init__(self, parent, value=0.0, unit="rad") -> None:
        self.parent = parent
        self.value = value
        self.unit = unit


class Length:
    def __init__(self, parent, value=0.0, unit="m") -> None:
        self.parent = parent
        self.value = value
        self.unit = unit
