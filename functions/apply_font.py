import pygame
from settings.settings import TILE_SIZE
from functions.get_os_adapted_path import get_os_adapted_path


def apply_font():
    try:
        pygame.font.init()  # Assure que le module de police est initialisé
        # Essaye d'abord d'obtenir la police par défaut
        font = pygame.font.get_default_font()
        # text_surface = font.render("Pixel Art", False, (255, 255, 255))
        if not font:  # Plus explicite que 'is None'
            raise ValueError("No default font available")

        return pygame.font.Font(font, 24)
    except (ValueError, pygame.error):
        try:
            # Si échec, essaie la police personnalisée
            return pygame.font.Font(
                get_os_adapted_path("font", "Jet.ttf"), 24)

        except (FileNotFoundError, pygame.error):
            # Fallback ultime
            return pygame.font.Font(None, 24)
