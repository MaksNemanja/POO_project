import time
import pygame


class Human:
    """
        Classe qui permet de recuperer les mouvement de l'uitlisateur physique
    """

    def __init__(self):
        self.kart = None

    def set_kart(self, Kart):
        """
            Cette methode existe afin d'utiliser une methode set_kart dans AI sans conflit
        """
        pass

    def move(self, string):
        """
            Cette Methode recupere l'information des touches de clavier sur lesquelles l'utilisateur a appuye
        """

        time.sleep(0.02)

        return pygame.key.get_pressed()
