import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
 
class KartSelection:
    """
       Classe qui va permettre à l'utilisateur de choisir un kart avant le début du jeu. Les karts vont être affichés dans une fenêtre avec leur indice et l'utilisateur devra cliquer sur le kart avec lequel il veut jouer
    """

    def __init__(self):

        self.name_karts = ["kart Mario", "kart Toad", "kart jaune"] # liste des noms des différents karts
        self.image_karts = ["images/image kart1.png", "images/image kart2.png", "images/image kart3.png"] # Liste des chemins d'accès des images des différents karts dans le dossier
        self.screen = pygame.display.set_mode((300, 400)) # Fenêtre qui va afficher les images des karts
        self.selected_kart=None # Indique l'indice du kart qui a été sélectionné 
        self.display_kart_list() # Affichage de la liste des karts dans le terminal

    def display_kart_list(self):
        """
           Méthode qui va afficher dans le terminal un message demandant à l'utilisateur de sélectionner un kart et aussi le nom des karts avec leur indice associé
        """
        print("Choisissez un kart :")
        for i, kart in enumerate(self.name_karts, start=1):
            print(f"{i}. {kart}")

    def user_selection(self):
        """
           Méthode qui va permettre d'afficher les images des karts et leur indice associé dans une fenêtre.
           :return: integer selected_kart
        """

        while True:
            self.screen.fill((128,128,128))  # création d'une fenêtre avec un fond gris

            
            for i, kart_image in enumerate(self.image_karts, start=1):
                # Affichage des images des karts
                kart_surface = pygame.image.load(kart_image) # Chargement de l'image du kart
                dim_kart = pygame.transform.scale(kart_surface, (80, 60)) # Redimensionnement de l'image
                kart_rect = dim_kart.get_rect(center=(150, 100 * i)) # Création d'un rectangle représentant la position de l'image dans la fenêtre
                self.screen.blit(dim_kart, kart_rect) # Affichage de l'image dans la fenêtre

                # Affichage des indices des karts
                text = pygame.font.Font(None, 36).render(str(i), True, (255,0,0)) # Texte à afficher en rouge
                text_rect = text.get_rect(center=(100, 100*i)) # Création d'un rectangle représentant la position du texte dans la fenêtre
                self.screen.blit(text, text_rect) # Affichage du texte dans la fenêtre

            pygame.display.flip() # Mise à jour de la fenêtre                                         
            pygame.time.Clock().tick(30) # Permet de gérer la vitesse de la boucle

            for event in pygame.event.get():
                #Fermeture de la fenêtre
                if event.type == QUIT:
                    pygame.quit()

                #Detection du clic de la souris
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos # Coordonnées du clic de la souris
                    for i, kart_rect in enumerate(self.get_kart_rects()):

                        # Si le clic de la souris se fait dans un des rectangles délimités par les karts, on retourne son indice
                        if kart_rect.collidepoint(x,y):
                            self.selected_kart = i+1
                            return self.selected_kart

        

    def get_kart_rects(self):
        """
           Méthode qui retourne une liste de rectangles qui représentent la position des images des karts
          :return rects
        """
        rects=[] #initialisation de la liste de rectangles
        for i, kart_image in enumerate(self.image_karts, start=1):
            kart_surface= pygame.image.load(kart_image)
            dim_kart= pygame.transform.scale(kart_surface, (80,60))
            kart_rect= dim_kart.get_rect(center=(150, 100*i))
            rects.append(kart_rect)
        return rects
                                   