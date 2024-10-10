import pygame
from surfaceType import SurfaceType
from soundManagement import play_sound
BLOCK_SIZE = 50  # taille imposee d'un block


class Lava(SurfaceType):
    """
        Classe qui herite de SurfaceType et qui gere le dessin de Lava ainsi que les comportement du kart sur ce type
        de block
    """

    def __init__(self, x, y, img="images/imageLava.jpg"):

        #  Initialisation des parametres
        self._image = None
        self._block = None
        super()._defBlock(x, y, img)  # initialise les parametres self.block et self.image


    def draw(self, screen):

        screen.blit(self._image, self._block)  # Dessine le block checkpoint a la position du block en question

    def physics(self, orientation, v_orientation, ac, v, x, y, params_checkpoint):

        # Recuperation des parametres du checkpoint sauvgarde
        orientation = params_checkpoint[2]  # Correspond a orientation_c
        v = 0.0  # Vitesse mise a 0
        x = params_checkpoint[0]  # xc
        y = params_checkpoint[1]  # yc

        # Joue le son de la lave
        play_sound("sons/sonLava.mp3")

        return orientation, v, x, y
