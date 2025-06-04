import pygame

from functions.settings import *
from functions.get_os_adapted_path import get_os_adapted_path
from classes.keyboard import handler
from classes.joystick import joystick_handler

pygame.init()
# Pour utiliser la fonction avec un hook


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = pygame.image.load(
            get_os_adapted_path("imagesOfTurgut", "row-6-column-1.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()

    def input(self):
        """initialisation du clavier et du joystick"""

        """ initialisation des variables de direction du joueur"""
        global player_direction_up
        global player_direction_down
        global player_direction_left
        global player_direction_right
        global player_direction_stay
        global player_current_direction
        global joystik_event_handler
        # Initialisation des variables de direction du joueur

        player_direction_up = False
        player_direction_down = False
        player_direction_left = False
        player_direction_right = False
        player_direction_stay = True
        player_current_direction = "stay"
        joystick_event_handler = None  # Initialisation de l'événement joystick
        # Récupère le scancode de l'événement

        """gestion du mouvement du joueur
        Touche : q, Code : 30  -- Gauche
        Touche : d, Code : 32  -- Droite
        Touche : z, Code : 17  -- Haut
        Touche : s, Code : 31  -- Bas"""
        if joystick_handler.joystick is not None:
            # Si une manette est connectée, on utilise les axes de la manette
            joystick_handler.handle_events()
            # Vérifie si l'axe gauche de la manette est utilisé

        if handler.event_scan_code == 30 or joystick_handler.joystick.get_axis(0) < -0.5 and handler.event_scan_code == None:
            print("Gauche")
            player_current_direction = "up"
            player_direction_up = True
            player_direction_down = False
            player_direction_left = False
            player_direction_right = False
            player_direction_stay = False
            self.direction.y = -1
            player_current_direction = "left"
            player_direction_left = True
            player_direction_right = False
            player_direction_up = False
            player_direction_down = False
            player_direction_stay = False
            self.direction.x = -1
            handler.event_scan_code = None  # Réinitialise l'événement après traitement
        if handler.event_scan_code == 32:
            print("Droite")
            player_current_direction = "down"
            player_direction_up = False
            player_direction_down = False
            player_direction_left = False
            player_direction_right = True
            player_direction_stay = False
            self.direction.y = 1
            player_current_direction = "right"
            player_direction_left = False
            player_direction_right = True
            player_direction_up = False
            player_direction_down = False
            player_direction_stay = False
            self.direction.x = 1
            handler.event_scan_code = None  # Réinitialise l'événement après traitement
        if handler.event_scan_code == 17:
            print("Haut")
            player_current_direction = "up"
            player_direction_up = True
            player_direction_down = False
            player_direction_left = False
            player_direction_right = False
            player_direction_stay = False
            self.direction.y = -1
            handler.event_scan_code = None
        if handler.event_scan_code == 31:
            print("Bas")
            player_current_direction = "down"
            player_direction_up = False
            player_direction_down = True
            player_direction_left = False
            player_direction_right = False
            player_direction_stay = False
            self.direction.y = 1
            handler.event_scan_code = None
        if handler.event_scan_code is None:
            player_current_direction = "stay"
            player_direction_up = False
            player_direction_down = False
            player_direction_left = False
            player_direction_right = False
            player_direction_stay = True
            self.direction.x = 0
            self.direction.y = 0

    def update(self):
        """update du joueur"""
        self.input()
