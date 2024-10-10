import pygame
import numpy as np
from surfaceType import SurfaceType

BLOCK_SIZE = 50  # taille imposee d'un block


class Road(SurfaceType):
    """
        Classe qui gere le dessin de Road ainsi que les comportement du kart sur ce type de block
    """
    def __init__(self, x, y, img="images/imageRoad.jpg"):
        self._image = None
        self._block = None
        super()._defBlock(x, y, img)  # initialise les parametres self.block et self.image

    def draw(self, screen):
        screen.blit(self._image, self._block)
    
    def physics(self, orientation, v_orientation, ac, v, x, y, params_checkpoint):

        # parametre de la physique
        friction = 0.02

        # Equations de la physique
        orientation += v_orientation
        a = ac - friction * v * np.cos(v_orientation)
        v = a + v * np.cos(v_orientation)
        x += v * np.cos(orientation)
        y += + v * np.sin(orientation)

        return orientation, v, x, y