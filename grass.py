import pygame
import numpy as np
from surfaceType import SurfaceType

BLOCK_SIZE = 50


class Grass(SurfaceType):

    def __init__(self, x, y, img="images/imageGrass.jpeg"):
        self._image = None
        self._block = None
        super()._defBlock(x, y, img)  # initialise les parametres self.block et self.image

    def draw(self, screen):
        screen.blit(self._image, self._block)

    def physics(self, orientation, v_orientation, ac, v, x, y, params_checkpoint):

        # Parametre de la physique
        friction = 0.2

        # Equations de la physique
        orientation += v_orientation
        a = ac - friction * v * np.cos(v_orientation)
        v = a + v * np.cos(v_orientation)
        x += v * np.cos(orientation)
        y += v * np.sin(orientation)

        return orientation, v, x, y
