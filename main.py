import pygame
from track import Track
from ai import AI
from human import Human
from kart import Kart
from kartselect import KartSelection

# La chaine de caractere decrivant le terrain
string = "GGGGGGGGGGGGGGGGGGGGGGGGGG\nGRRRRRRCRRRRRRRRRBRRRRRRRG\nGRRRRRRCRRRRRRRRRBRRRRRRRG\n" \
         "GRRRRRRCRRRRRRRRRRRRRRRRRG\nGRRRRRRCRRRRRRRRRRRRRRRRRG\nGGGGGGGGGGGGGGGGGGGGGRRRRG\n" \
         "GGGGGGGGGGGGGGGGGGGGGRRRRG\nGRRRRGGGGGGGGGGGGGGGGRRRRG\nGFFRRGGGGGGGGGGGGGGGGRRRRG\n" \
         "GLRRRGGGGGGGGGGGGGGGGRRRRG\nGRRRRGGGGGGGGGGGGGGGGDDDDG\nGRRRRRERRRRRRRBRRRRRRRRLLG\n" \
         "GRRRRRERRRRRRRBRRRRRRRRRRG\nGLRRRRERRRRRGGBRRRRRRRRRRG\nGLLRRRERRRRRGGBRRRRRRRRRRG\n" \
         "GGGGGGGGGGGGGGGGGGGGGGGGGG"

# La position et l'orientation initiale du kart
initial_position = [150, 150]
initial_angle = 0

controller = AI()  # ou AI()

# Selection du kart
pygame.init()
kart_selection = KartSelection()
choice = kart_selection.user_selection()

# Affichage du nom du kart choisi
selected_kart = kart_selection.name_karts[choice - 1]
print(f"Vous avez choisi le kart : {selected_kart}")

"""
==================== ATTENTION =====================
Vous ne devez pas modifier ces quatre lignes de code 
====================================================
"""
kart = Kart(controller)
kart.kart_id(choice)  # Import du kart choisi par l'utilisateur
track = Track(string, initial_position, initial_angle)
track.add_kart(kart)
track.play()