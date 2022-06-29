import numpy as np

class Distribution(object):
    
    def __init__(self, parent):
        self.parent = parent
        self.func = None
        self.dist = None

    def sample(self):
        return np.around(self.func(**self.dist), 2)

class UniformDistribution(Distribution):
    
    def __init__(self, parent, values):
        super().__init__(parent)
        self.values = values

    def sample(self):
        index = np.random.randint(low=0, high=len(self.values))
        return self.values[index]

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

        self.func = np.random.normal
        self.dist = {
            'loc':self.mean, 
            'scale':self.std}