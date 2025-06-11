import pygame
from settings.settings import *
from functions.get_os_adapted_path import get_os_adapted_path


class UI:
    def __init__(self):
        # Initialisation des icônes
        self.energy_icon = pygame.image.load(
            get_os_adapted_path("assets", "energy.png")).convert_alpha()
        self.health_icon = pygame.image.load(
            get_os_adapted_path("assets", "health.png")).convert_alpha()

        # Redimensionnement
        self.health_icon = pygame.transform.scale(self.health_icon, (48, 48))
        self.energy_icon = pygame.transform.scale(self.energy_icon, (48, 48))

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Position des barres (décalées à droite pour laisser de la place aux icônes)
        ICON_OFFSET = 26  # 16px pour l'icône + 10px de marge
        self.health_bar_rect = pygame.Rect(
            10 + ICON_OFFSET, 14, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10 + ICON_OFFSET, 50, ENEGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # Bordure + fond
        border_rect = bg_rect.copy()
        border_rect.inflate_ip(6, 6)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, border_rect)
        pygame.draw.rect(self.display_surface, UI_BACKGROUND_COLOR, bg_rect)

        # Barre de progression
        ratio = current / max_amount
        current_rect = bg_rect.copy()
        current_rect.width = int(bg_rect.width * ratio)
        pygame.draw.rect(self.display_surface, color, current_rect)

        # Ajout du texte centré dans la barre
        if bg_rect == self.health_bar_rect:
            text = "SANTE DE TURGUT"
        else:
            text = "ÇAY DANS LE SANG"

        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(text_surf, text_rect)

    def display(self, player):
        # Position des icônes (à gauche des barres)
        health_icon_pos = (self.health_bar_rect.left-45,
                           self.health_bar_rect.centery - 28)
        energy_icon_pos = (self.energy_bar_rect.left-45,
                           self.energy_bar_rect.centery - 24)

        # Affichage des icônes
        self.display_surface.blit(self.health_icon, health_icon_pos)
        self.display_surface.blit(self.energy_icon, energy_icon_pos)

        # Affichage des barres (le texte est maintenant géré dans show_bar)
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, HEALTH_BAR_COLOR)
        self.show_bar(
            player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_BAR_COLOR)
