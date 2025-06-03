import pygame

pygame.init()
_debug_font = pygame.font.Font(None, 24)

# Variable pour stocker un seul message de debug
debug_message = None
debug_start_time = None


def debug(info, x=10, y=10):
    """Affiche un message unique pendant 5 secondes."""
    global debug_message, debug_start_time
    surface = pygame.display.get_surface()

    if debug_message is None:  # Vérifie si un message est déjà affiché
        debug_message = str(info)
        debug_start_time = pygame.time.get_ticks()

    # Efface l'écran avant de redessiner
    surface.fill((0, 0, 0))

    if debug_message and pygame.time.get_ticks() - debug_start_time < 5000:
        text = _debug_font.render(debug_message, True, (255, 255, 255))
        rect = text.get_rect(topleft=(x, y))
        surface.blit(text, rect)

    pygame.display.flip()

    clear_debug()


def clear_debug():
    """Supprime le message après 5 secondes."""
    global debug_message, debug_start_time
    if debug_message and pygame.time.get_ticks() - debug_start_time >= 5000:
        debug_message = None
        debug_start_time = None
