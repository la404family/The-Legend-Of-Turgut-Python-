import pygame
from settings.settings import *
from functions.get_os_adapted_path import get_os_adapted_path


class UI:
    def __init__(self):
        # Assurez-vous d'avoir importé pygame correctement
        self.energy_icon = pygame.image.load(
            get_os_adapted_path("assets", "energy.png")).convert_alpha()
        self.health_icon = pygame.image.load(
            get_os_adapted_path("assets", "energy.png")).convert_alpha()

        # Redimensionner les images si nécessaire (16x16)
        self.health_icon = pygame.transform.scale(self.health_icon, (16, 16))
        self.energy_icon = pygame.transform.scale(self.energy_icon, (16, 16))
        self.display_surface = pygame.display.get_surface()
        # Default font, can be changed later
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # barre d'UI
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.cay_bar_rect = pygame.Rect(10, 36, ENEGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw background with border
        border_rect = bg_rect.copy()
        border_rect.inflate_ip(6, 6)  # 2 pixels de chaque côté (2*2=4)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, border_rect)
        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, bg_rect)

        # convertir stats en pixels
        ratio = current / max_amount
        current_width = int(bg_rect.width * ratio)
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)

    def display(self, player):
        # health bar
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, HEALTH_BAR_COLOR
        )
        # energy bar
        self.show_bar(
            player.energy, player.stats['energy'], self.cay_bar_rect, ENERGY_BAR_COLOR
        )
