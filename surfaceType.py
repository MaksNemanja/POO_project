from abc import ABC, abstractmethod
import pygame

BLOCK_SIZE = 50  # taille imposee d'un block


class SurfaceType(ABC):
    """
        Classe abstraite definissant des methodes abstraites ( draw, physics) qui doivent etre implemente par les
        sous-classes. Cette classe fournit aussi des methodes non abstraite herite par les sous-classes
    """

    @abstractmethod
    def draw(self, screen):
        """ Methode abstraite pour dessiner les blocks """

        pass

    @abstractmethod
    def physics(self, orientation, v_orientation, ac, v, x, y, params_checkpoint):
        """ Methode abstraite pour definir la physique des blocks

        :param float orientation : Orientation du kart a l'instant (t-1)
        :param float v_orientation : Vitesse angulaire du kart a l'instant (t)
        :param float ac : Acceleration constante a l'instant (t)
        :param float v : Vitesse total du kart a l'instant (t-1)
        :param float x : Position en colonne du kart a l'instant (t-1)
        :param float y : Position en ligne du kart a l'instant (t-1)
        :param params_checkpoint : Parametres du checkpoint
            xc : Position en colonne a l'entree du checkpoint
            yc : Position en ligne a l'entree du checkpoint
            orientation_c : Orientation du kart a l'entree du checkpoint
        :type params_checkpoint : list

        :returns: Un tuple (orientation, a, v, x, y)
            orientation : Orientation du kart a l'instant (t)
            v : Vitesse du kart a l'instant (t)
            x : Position en colonne a l'instant (t)
            y : Position en ligne a l'instant (t)
        """

        pass


    def _defBlock(self, x, y, img):
        """
            Methode qui initialise les parametres

            :param float x : Position du block en horizontal
            :param float y : Position du block en vertical
            :param str img : Fichier de l'image à dessiner dans le block
        """
        self._block = (x, y)  # Cree  un tuple (coordonnee horizontale, coordonnee verticale)
        self._block_size = (BLOCK_SIZE, BLOCK_SIZE)  # surface d'un block

        # Creation de l'image qui sera afficher sur l'ecran par la suite
        self._image = pygame.image.load(img)
        self._image = pygame.transform.scale(self._image, self._block_size)
