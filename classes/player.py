import pygame
import keyboard
from functions.settings import *
from functions.get_os_adapted_path import get_os_adapted_path
from functions.on_key_event import on_key_event

pygame.init()


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
        jpad = pygame.joystick.Joystick(
            0) if pygame.joystick.get_count() > 0 else None
        """ initialisation des variables de direction du joueur"""
        global player_direction_up
        global player_direction_down
        global player_direction_left
        global player_direction_right
        global player_direction_stay
        global player_current_direction
        player_direction_up = False
        player_direction_down = False
        player_direction_left = False
        player_direction_right = False
        player_direction_stay = True
        player_current_direction = "stay"

        """gestion du mouvement du joueur
        Touche : q, Code : 30  -- Haut
        Touche : d, Code : 32  -- Droite
        Touche : z, Code : 17  -- Bas
        Touche : s, Code : 31  -- Gauche"""
        print(f"Ligne ${keyboard.on_press(on_key_event)}")
        if keyboard.on_press(on_key_event) == 32:
            print("Haut (Joystick)")
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
        else:
            player_direction_left = False
            player_direction_right = False
            player_direction_up = False
            player_direction_down = False
            player_direction_stay = True
            self.direction.x = 0

    def update(self):
        """update du joueur"""
        self.input()
