import pygame
from settings.settings import *
from classes.level import *
from classes.player import *
from classes.tile import Tile


class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.zoom_scale = 3  # Facteur de zoom (x3)

        # Créer une surface pour le zoom
        self.internal_surface_size = (self.display_surface.get_size()[0] // self.zoom_scale,
                                      self.display_surface.get_size()[1] // self.zoom_scale)
        self.internal_surface = pygame.Surface(
            self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(
            center=(self.half_width, self.half_height))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - \
            self.internal_surface_size[0] // 2
        self.offset.y = player.rect.centery - \
            self.internal_surface_size[1] // 2

        # Effacer la surface interne
        self.internal_surface.fill((0, 0, 0, 0))

        # Dessiner tous les sprites sur la surface interne (avec zoom)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.internal_surface.blit(sprite.image, offset_pos)

        # Redimensionner la surface interne vers la surface d'affichage
        zoomed_surface = pygame.transform.scale(self.internal_surface,
                                                self.display_surface.get_size())
        self.display_surface.blit(zoomed_surface, (0, 0))
