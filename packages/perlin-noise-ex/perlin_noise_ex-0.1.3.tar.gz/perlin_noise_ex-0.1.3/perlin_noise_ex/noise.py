import numpy as np
import matplotlib.pyplot as plot
from perlin_noise import PerlinNoise

class CreateNewPerlinNoise:
    def __init__(self, seed = 5, octaves = 2, amp = 7, period = 24, width=300, height=300):
        self.seed = seed
        self.octaves = octaves
        self.amp = amp
        self.period = period
        self.width = width
        self.height = height

        self.noise = PerlinNoise(seed=seed, octaves=octaves)

    def createPerlin(self):
        landscale = [[0 for i in range(self.width)] for i in range(self.height)]

        for position in range(self.width ** 2):
            x = np.floor(position / self.width)
            z = np.floor(position % self.width)
            y = np.floor(self.noise([x / self.period, z / self.period]) * self.amp)
            landscale[int(x)][int(z)] = y
        
        return landscale

    def showGraph(self, matrix):
        plot.imshow(matrix)
        plot.colorbar()
        plot.show()
