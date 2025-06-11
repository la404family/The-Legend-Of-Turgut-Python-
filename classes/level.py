import pygame
import random
from settings.settings import *
from functions.get_os_adapted_path import get_os_adapted_path
from functions.csv_reader import import_csv_layout
from classes.tile import Tile
from classes.player import Player
from classes.camera import YsortCameraGroup
from classes.weapon import Weapon
from classes.ui import UI  # Assuming UI is defined in classes/ui.py


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.player = None
        self.create_map()
        self.ui = UI()  # Initialize UI, if needed later

    def create_map(self):
        # Only create the map once
        if getattr(self, 'map_created', False):
            return
        self.map_created = True

        try:
            # Load obstacle image with error handling
            obstacle_path = get_os_adapted_path(
                "imagesOfMaps", "mapArbres.png")
            obstacle_image = pygame.image.load(obstacle_path).convert_alpha()

            # Verify image was loaded properly
            if obstacle_image.get_size() == (0, 0):
                raise pygame.error("Image failed to load properly")

            img_width, img_height = obstacle_image.get_size()

            # Process the image tiles
            for y in range(0, img_height, TILE_SIZE):
                for x in range(0, img_width, TILE_SIZE):
                    try:
                        tile_surface = obstacle_image.subsurface(
                            (x, y, TILE_SIZE, TILE_SIZE))

                        # Check for any non-transparent pixels
                        has_obstacle = False
                        for tx in range(TILE_SIZE):
                            for ty in range(TILE_SIZE):
                                if tile_surface.get_at((tx, ty))[3] > 0:
                                    has_obstacle = True
                                    break
                            if has_obstacle:
                                break

                        if has_obstacle:
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                'obstacle',
                                tile_surface
                            )
                    except ValueError as e:
                        print(f"Error processing tile at ({x},{y}): {e}")
                        continue

        except pygame.error as e:
            print(f"Failed to load obstacle image at {obstacle_path}: {e}")
            # You might want to set map_created to False to retry next time
            self.map_created = False
        except Exception as e:
            print(f"Unexpected error processing map: {e}")
            self.map_created = False

        # Place player at random position
        random_position = random.choice(PLAYER_START_POSITION)
        self.player = Player(
            random_position,
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
            self.destroy_attack
        )

    def create_attack(self):
        if self.current_attack is None:
            self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
