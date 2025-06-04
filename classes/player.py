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
        self.speed = PLAYER_SPEED

    def input(self):
        """initialisation du clavier et du joystick"""

        """ initialisation des variables de direction du joueur"""
        global player_direction_up
        global player_direction_down
        global player_direction_left
        global player_direction_right
        global player_direction_stay
        global player_current_direction
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
        else:
            # Sinon, on utilise le clavier
            handler.handle_events()

        if handler.event_scan_code == 30 or joystick_handler.joystick.get_axis(0) < -0.5:
            print("Gauche")
            self.direction.x = -1
            self.direction.y = 0  # Assurer aucun mouvement vertical
            player_current_direction = "left"

        elif handler.event_scan_code == 32 or joystick_handler.joystick.get_axis(0) > 0.5:
            print("Droite")
            self.direction.x = 1
            self.direction.y = 0  # Assurer aucun mouvement vertical
            player_current_direction = "right"
        elif handler.event_scan_code == 17 or joystick_handler.joystick.get_axis(1) < -0.5:
            print("Haut")
            self.direction.x = 0  # Assurer aucun mouvement horizontal
            self.direction.y = -1
            player_current_direction = "up"
        elif handler.event_scan_code == 31 or joystick_handler.joystick.get_axis(1) > 0.5:
            print("Bas")
            self.direction.x = 0  # Assurer aucun mouvement horizontal
            self.direction.y = 1
            player_current_direction = "down"
        # si aucune touche n'est pressée, le joueur reste en place
        elif handler.event_scan_code is None or handler.event_scan_code == 0:
            print("Aucune touche pressée")
            self.direction.x = 0
            self.direction.y = 0
            player_current_direction = "stay"
        else:
            print("Rester")
            self.direction = pygame.math.Vector2(0, 0)
            player_current_direction = "stay"

    def move(self, speed):
        """déplacement du joueur"""
        self.rect.center += self.direction * speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0

    def update(self):
        """update du joueur"""
        self.input()
        self.move(self.speed)
