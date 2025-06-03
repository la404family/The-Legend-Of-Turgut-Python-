import pygame
import sys
from functions.settings import *
from functions.debug import debug
from functions.get_os_adapted_path import get_os_adapted_path
from classes.level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # favicon de l'application
        icon = pygame.image.load(
            get_os_adapted_path("assets", "favicon.png"))
        pygame.display.set_icon(icon)

        pygame.display.set_caption(
            "The Legend of Turgut")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = Level()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            self.level.run()
            debug("Game is running", 10, 10)
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except Exception as e:
        debug(f"Error: {e}", 10, 30)
    finally:
        pygame.quit()
        sys.exit()
