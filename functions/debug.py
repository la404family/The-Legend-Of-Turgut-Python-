import pygame
pygame.init()
font = pygame.font.Font(None, 36)

# cette fonction permet d'afficher des informations de debug sur l'écran


def debug(info, x=10, y=10):
    """
    Display debug information on the screen.

    :param info: The information to display.
    :param x: The x-coordinate for the text.
    :param y: The y-coordinate for the text.
    """
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, (255, 255, 255))
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, (0, 0, 0),
                     debug_rect.inflate(10, 10))  # Background rectangle
    display_surface.blit(debug_surf, debug_rect.topleft)
