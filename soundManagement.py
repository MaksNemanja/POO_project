import pygame


def play_music():
    """
        Cette fonction permet de jouer la musique du jeu
    """

    pygame.mixer.music.load("sons/main music.mp3")
    pygame.mixer.music.play(-1)  # Permet de jouer la musique en boucle
    pass

def play_sound(sound):
    """
        Methode qui joue un son

        :param str sound : fichier du son a jouer
    """
    pygame.mixer.Sound(sound).play()
    pass

