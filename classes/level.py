import pygame
from settings.settings import *
from classes.tile import Tile
from classes.player import *


class Level:
    def __init__(self):
        self .display_surface = pygame.display.get_surface()
        self.visible_sprites = YsortCameraGroup()
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
                    self.player = Player(
                        (x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        """Gère le rendu du niveau"""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
