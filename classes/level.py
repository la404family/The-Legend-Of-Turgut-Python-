import pygame
from functions.settings import *
from classes.tile import Tile
from classes.player import Player
from classes.tile import Tile


class Level:
    def __init__(self):
        self .display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP_TEST):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == "x":
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == "p":
                    from classes.player import Player
                    self.player = Player((x, y), [self.visible_sprites])

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
