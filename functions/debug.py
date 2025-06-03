import pygame
from functions.get_os_adapted_path import get_os_adapted_path

# Initialisation des ressources une seule fois
pygame.font.init()
_debug_font = None  # Cache pour la police


def _get_debug_font():
    """Obtient la police de debug avec lazy loading"""
    global _debug_font
    if _debug_font is None:
        try:
            _debug_font = pygame.font.Font(
                get_os_adapted_path("font", "Jet.ttf"), 24)
        except:
            _debug_font = pygame.font.Font(None, 24)  # Fallback
    return _debug_font


def debug(info, x=10, y=10):
    """
    Affiche des informations de debug sur l'écran.

    Args:
        info: Information à afficher (sera converti en string)
        x: Position horizontale (par défaut 10)
        y: Position verticale (par défaut 10)
    """
    display_surface = pygame.display.get_surface()
    font = _get_debug_font()

    # Préparation du texte
    text_surf = font.render(str(info), True, (255, 255, 255))
    text_rect = text_surf.get_rect(topleft=(x, y))

    # Dessin du fond
    bg_rect = text_rect.inflate(10, 10)
    pygame.draw.rect(display_surface, (0, 0, 0), bg_rect)

    # Affichage du texte
    display_surface.blit(text_surf, text_rect)
