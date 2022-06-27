import numpy as np

class Distribution(object):
    
    def __init__(self, parent):
        self.parent = parent
        self.func = None
        self.dist = None

    def sample(self):
        return self.func(**self.dist)

class UniformDistribution(Distribution):
    
    def __init__(self, parent, values):
        super().__init__(parent)
        self.values = values

class DiscreteDistribution(Distribution):
    
    def __init__(self, parent, values):
        super().__init__(parent)
        self.values = values

    def sample(self):
        pass

class NormalDistribution(Distribution):
    
    def __init__(self, parent, mean, std):
        super().__init__(parent)
        self.mean = mean
        self.std = std
