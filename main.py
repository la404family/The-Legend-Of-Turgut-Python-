import pygame
import sys

from functions.settings import *
from functions.debug import debug
from functions.get_os_adapted_path import get_os_adapted_path
from functions.apply_font import apply_font
from classes.level import Level
from classes.player import Player


class Game:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()

        # Configuration de la fenêtre
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self._setup_window()

        # Configuration de la police (une seule fois dans __init__)
        apply_font()

        # Configuration du jeu
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = Level()

    def _setup_window(self):
        """Configure l'icône et le titre de la fenêtre"""
        try:
            icon = pygame.image.load(
                get_os_adapted_path("assets", "favicon.png"))
            pygame.display.set_icon(icon)
        except:
            debug("Could not load favicon", 10, 10)

        pygame.display.set_caption("The Legend of Turgut")

    def run(self):
        """Boucle principale du jeu"""
        try:
            while self.running:
                self._handle_events()
                self._render()
                self.clock.tick(FPS)
        except Exception as e:
            debug(f"Error: {e}", 10, 30)
        finally:
            pygame.quit()
            sys.exit()

    def _handle_events(self):
        """Gère les événements du jeu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _render(self):
        """Gère le rendu du jeu"""
        self.screen.fill((0, 0, 0))
        self.level.run()
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
