import pygame
import random
from settings.settings import *
from classes.tile import *
from classes.player import *
from classes.camera import YsortCameraGroup


class Level:
    def __init__(self):
        self .display_surface = pygame.display.get_surface()
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        """Crée la carte du niveau"""
        # for row_index, row in enumerate(WORLD_MAP_TEST):
        #     for col_index, col in enumerate(row):
        #         x = col_index * TILE_SIZE
        #         y = row_index * TILE_SIZE
        #         if col == "x":
        #             Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
        #         if col == "p":

        # faire un random sur le tableau PLAYER_START_POSITION

        random_position = random.choice(PLAYER_START_POSITION)
        self.player = Player(
            (random_position), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        """Gère le rendu du niveau"""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
