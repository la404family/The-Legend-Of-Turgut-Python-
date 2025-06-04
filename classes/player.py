import pygame
import keyboard
from functions.on_key_event import on_key_event
from functions.debug import debug
from functions.settings import *
from functions.get_os_adapted_path import get_os_adapted_path

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
        try:
            if jpad:
                jpad.init()
        except pygame.error:
            jpad = None

        """gestion du mouvement du joueur"""
        if keyboard.is_pressed("up") or (jpad and jpad.get_axis(1) < -0.5):
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
