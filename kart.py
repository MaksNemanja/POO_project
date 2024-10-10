import pygame
import numpy as np
from grass import Grass
from lava import Lava
from boost import Boost
from checkpoint import Checkpoint, save_checkpoint, last_checkpoint
from road import Road
from soundManagement import play_music

MAX_ANGLE_VELOCITY = 0.05
MAX_ACCELERATION = 0.25
BLOCK_SIZE = 50

pygame.mixer.init()


class Kart:
    """
    Classe implementant l'affichage et la physique du kart dans le jeu
    """

    # Ce dictionnaire permet de donner la classe et les parametres d'instanciation
    # correspondant a chaque lettre dans la chaine de caractere decrivant le circuit
    char_to_track_element = {
        'G': {
            'class': Grass,
            'params': []
        },
        'B': {
            'class': Boost,
            'params': []
        },
        'C': {
            'class': Checkpoint,  # le C indique le checkpoint d'id 0
            'params': [0]
        },
        'D': {
            'class': Checkpoint,  # Le D indique le checkpoint d'id 1
            'params': [1]
        },
        'E': {
            'class': Checkpoint,  # etc.
            'params': [2]
        },
        'F': {
            'class': Checkpoint,
            'params': [3]
        },
        'L': {
            'class': Lava,
            'params': []
        },
        'R': {
            'class': Road,
            'params': []
        }
    }

    def __init__(self, controller):
        # Sert a faire un traitement qui se fera qu'a la premiere iteration de update position
        self.__condition = True

        self.__matriceMap = None  # Devindra par la suite une matrice d'object des type de block

        # Initialisation de la position en x et y, de l'orientation, ainsi que la vitesse du kart
        self.__x = 0.0
        self.__y = 0.0
        self.__orientation = 0.0
        self.__vitesse = 0.0

        # Initialisation de l'acceleration constante et de la vitesse angulaire
        self.__ac = 0.0
        self.__v_orientation = 0.0

        # Position et orientation du checkpoint
        self.__xc = self.__x
        self.__yc = self.__y
        self.__orientation_c = self.__orientation
        self.__checkpoint = 0  # checkpoint actuel

        self.__last_checkpoints_ID = None  # ID du checkpoint qui designe la ligne d'arriver

        self.__music = play_music()   # Lance la musique du jeu

        # Les differentes images des kart possible. Sera utilisee pour dessiner le kart
        self.image_karts = ["images/image kart1.png", "images/image kart2.png", "images/image kart3.png"]
        self.idKartImg = None  # ID de l'image du kart choisi

        self.has_finished = False  # Indique si le kart a atteint la fin

        # Vont servir pour la partie AI
        self.controller = controller
        controller.set_kart(self)  # Afin de recuperer la position du kart dans AI

    @property
    def condition(self):
        return self.__condition

    @property
    def last_checkpoints_ID(self):
        return self.__last_checkpoints_ID

    @property
    def checkpoint(self):
        return self.__checkpoint

    @property
    def xPosCheckpoint(self):
        return self.__xc

    @property
    def yPosCheckpoint(self):
        return self.__yc

    @property
    def orientationCheckpoint(self):
        return self.__orientation_c

    @property
    def v_orientation(self):
        return self.__v_orientation

    @property
    def accelerationConstante(self):
        return self.__ac

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def orientation(self):
        return self.__orientation

    @property
    def vitesse(self):
        return self.__vitesse

    @property
    def matriceMap(self):
        return self.__matriceMap

    def reset(self, initial_position, initial_orientation):

        # Initialisation des parametres du kart et du checkpoint enregistre
        self.__x, self.__y, self.__orientation = initial_position[0],initial_position[1],initial_orientation
        self.__xc, self.__yc, self.__orientation_c = self.__x, self.__y,self.__orientation

        # Initialisation de la vitesse, vitesse d'orientation et de l'acceleration continue
        self.__vitesse, self.__v_orientation, self.__ac = [0.0] * 3

        # Initialisation du dernier checkpoint enregistre l'ID du dernier checkpoint de la partie
        self.__checkpoint = 0
        self.__last_checkpoints_ID = None

        self.has_finished = False  # Renvoie False pour permttre a la partie de proceder

        self.__condition = True  # Renvoie True pour permettre la traitement de la premiere boucle

    def parse_string(self, string):
        """
        Cette methode instancie les composants et calcule les dimensions du circuit

        :param string: La chaine de caractere decrivant le circuit
        :returns: Un tuple (track_objects, width, height)
            track_objects: tableau d'objets composant le circuit
            width: largeur du circuit
            height: hauteur du circuit
        """
        track_objects = []
        track_objects_line = []

        # On utilise x et y pour decrire les coordonnees dans la chaine de caractere
        # x indique le numero de colonne
        # y indique le numero de ligne
        x = 0
        y = 0
        cpt = 1
        for c in string:
            # Pour chaque caractere on ajoute un object a track_objects
            if c in Kart.char_to_track_element.keys():
                track_element = Kart.char_to_track_element[c]
                track_class = track_element['class']
                track_params = [x, y] + track_element['params']
                track_objects_line.append(track_class(*track_params))

                x += BLOCK_SIZE
                if cpt == len(string) - 1:
                    track_objects.append(track_objects_line)
            elif c == '\n':
                x = 0
                y += BLOCK_SIZE
                track_objects.append(track_objects_line)
                track_objects_line = []
            cpt += 1
        return track_objects

    def forward(self):
        self.__ac = min(self.__ac + MAX_ACCELERATION, MAX_ACCELERATION)
        return self.__ac

    def backward(self):
        self.__ac = max(self.__ac - MAX_ACCELERATION, -MAX_ACCELERATION)
        return self.__ac

    def turn_left(self):
        self.__v_orientation = max(self.__v_orientation - MAX_ANGLE_VELOCITY, -MAX_ANGLE_VELOCITY)
        return self.__v_orientation

    def turn_right(self):
        self.__v_orientation = min(self.__v_orientation + MAX_ANGLE_VELOCITY, MAX_ANGLE_VELOCITY)
        return self.__v_orientation

    def remise_a_zero(self):
        self.__ac = 0
        self.__v_orientation = 0

    def limite_map(self):
        outside = Lava(self.__x, self.__y)
        self.__orientation, self.__vitesse, self.__x, self.__y = outside.physics(self.__orientation,
                                                                                 self.__v_orientation, self.__ac,
                                                                                 self.__vitesse, self.__x, self.__y,
                                                                                 [self.__xc, self.__yc,
                                                                                  self.__orientation_c])

    def update_position(self, string, screen):

        # pour ce reperer sur quelle type de bloc je suis
        while self.__condition:
            self.__matriceMap = self.parse_string(string)

            checkpoints_ID = []
            for mapStrLine in self.__matriceMap:
                for element in mapStrLine:
                    if isinstance(element, Checkpoint):
                        checkpoints_ID.append(element.checkpoint_id)

            self.__last_checkpoints_ID = max(checkpoints_ID)
            self.__condition = False
            
        # Pour connaitre sur quel block le kart se trouve
        [blockX, blockY] = [int(self.__x / BLOCK_SIZE), int(self.__y / BLOCK_SIZE)]
        blockActuel = self.__matriceMap[blockY][blockX]

        self.__orientation, self.__vitesse, self.__x, self.__y = blockActuel.physics(self.__orientation,
                                                                                     self.__v_orientation,
                                                                                     self.__ac,
                                                                                     self.__vitesse, self.__x,
                                                                                     self.__y,
                                                                                     [self.__xc, self.__yc,
                                                                                      self.__orientation_c])
        if self.__x > screen.get_width() or self.__y > screen.get_height() or self.__x < 0 or self.__y < 0:
            self.limite_map()
            
        if isinstance(blockActuel, Checkpoint):
            if blockActuel.checkpoint_id == self.__checkpoint:
                self.__xc, self.__yc, self.__orientation_c, self.__checkpoint = save_checkpoint(self.__x, self.__y,
                                                                                                self.__orientation,
                                                                                                self.__checkpoint)
            if self.__checkpoint == self.__last_checkpoints_ID + 1:
                pygame.mixer.music.stop()
                self.has_finished = last_checkpoint()

        self.remise_a_zero()

    def kart_id(self, id_img):
        self.idKartImg = id_img

    def draw(self, screen):

        if self.idKartImg is None:  # condition si on effectue un test, on selectionne par defaut le premier kart
            image = "images/image kart1.png"
        else:
            image = self.image_karts[self.idKartImg - 1]

        kart_image = pygame.image.load(image)
        dim_kart = pygame.transform.scale(kart_image, (60, 40))
        rot_kart_im = pygame.transform.rotate(dim_kart, float(np.degrees(self.__orientation * (-1))))
        rot_kart_rect = rot_kart_im.get_rect()
        rot_kart_rect.center = (int(self.__x), int(self.__y))
        # affichage de l'image du kart sur l'écran
        screen.blit(rot_kart_im, rot_kart_rect)




