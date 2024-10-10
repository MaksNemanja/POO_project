import pygame
import numpy as np
from surfaceType import SurfaceType
from soundManagement import play_sound
BLOCK_SIZE = 50  # taille imposee d'un block


class Boost(SurfaceType):
    """
        Classe qui herite de SurfaceType et qui gere le dessin de Boost ainsi que les comportement du kart sur ce type de block
    """

    def __init__(self, x, y, img="images/imageBoost.jpg"):
        self._image = None
        self._block = None
        super()._defBlock(x, y, img)  # initialise les parametres self.block et self.image

        self.__vBoost = 25.0

    @property
    def vBoost(self):
        return self.__vBoost

    def draw(self, screen):
        screen.blit(self._image, self._block)

    def physics(self, orientation, v_orientation, ac, v, x, y, params_checkpoint):

        # Equations de la physique
        orientation += v_orientation
        v = self.vBoost
        x += v * np.cos(orientation)
        y += + v * np.sin(orientation)

        # Joue le son du boost
        play_sound("sons/sonBoost.mp3")

        return orientation, v, x, y
