import pygame
import numpy as np
from surfaceType import SurfaceType
from soundManagement import play_sound

BLOCK_SIZE = 50  # taille imposee d'un block


class Checkpoint(SurfaceType):
    """
        Classe qui gere le dessin de Checkpoint ainsi que les comportement du kart sur ce type de block
    """

    def __init__(self, x, y, checkpoint_id, image="images/imageCheckpoint.jpg"):
        self._image = None
        self._block = None
        super()._defBlock(x, y, image)  # initialise les parametres self.block et self.image
        self.__id = checkpoint_id  # ID du checkpoint en question

    @property
    def checkpoint_id(self):
        return self.__id

    def draw(self, screen):
        screen.blit(self._image, self._block)  # Dessine le block checkpoint a la position du block en question

    def physics(self, orientation, v_orientation, ac, v, x, y, params_checkpoint):
        # Parametre de la physique
        friction = 0.02

        # Equations de la physique
        orientation += v_orientation
        a = ac - friction * v * np.cos(v_orientation)
        v = a + v * np.cos(v_orientation)
        x += v * np.cos(orientation)
        y += v * np.sin(orientation)

        return orientation, v, x, y


def save_checkpoint(x, y, orientation, checkpoint):
    """
        Fonction qui qui gere l'atteinte d'un checkpoint pour la premiere fois

        :param float x: Position horizontale du kart
        :param float y: Position veticale du kart
        :param float orientation: Orientation du kart
        :param int checkpoint: ID du dernier checkpoint enregistre
        :param play_sound: fonction qui  permet de jouer un son

        :returns: Un tuple (x, y, orientation, checkpoint + 1 )
            x : le xc qui sera sauvgardé par la suite
            y : le yc qui sera sauvgardé par la suite
            orientation : le orientation_c qui sera sauvgardé par la suite
            checkpoint : l'ID du prochain checkpoint
    """

    # Joue le son du checkpoint
    play_sound("sons/sonCheckpoint.mp3")

    checkpoint += 1  # Incremente l'ID du checkpoint

    return x, y, orientation, checkpoint


def last_checkpoint():
    """
        Fonction qui joue le son de la victoire

        :returns: Un bouleen qui correspond a has_finished

    """

    play_sound("sons/ending music.mp3")
    pygame.time.delay(5000)  # Attendre que le son de victoire se termine

    return True



