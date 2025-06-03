import pygame
from functions.settings import *
from functions.get_os_adapted_path import get_os_adapted_path


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = pygame.image.load(
            get_os_adapted_path("imagesOfMaps", "test01.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
