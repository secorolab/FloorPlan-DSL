class VariableReference:
    def __init__(self, parent, var_neg, variable) -> None:
        self.parent = parent
        self.var_neg = var_neg
        self.variable = variable

        if self.var_neg:
            self._sign = -1
        else:
            self._sign = 1

    @property
    def value(self):
        return self._sign * self.variable.value

    @property
    def unit(self):
        return self.variable.unit
