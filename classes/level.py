import pygame
import random
from settings.settings import *
from functions.get_os_adapted_path import get_os_adapted_path
from functions.csv_reader import import_csv_layout
from classes.tile import Tile
from classes.player import Player
from classes.camera import YsortCameraGroup
from classes.weapon import Weapon


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.player = None
        self.create_map()

    def create_map(self):
        # Only create the map once
        if getattr(self, 'map_created', False):
            return
        self.map_created = True

        # Load obstacle image once
        obstacle_image = pygame.image.load(
            get_os_adapted_path("imagesOfMaps", "mapArbres.png")
        ).convert_alpha()
        img_width, img_height = obstacle_image.get_size()

        # Only create tiles for non-transparent areas
        for y in range(0, img_height, TILE_SIZE):
            for x in range(0, img_width, TILE_SIZE):
                tile_surface = obstacle_image.subsurface(
                    (x, y, TILE_SIZE, TILE_SIZE))
                if any(tile_surface.get_at((tx, ty))[3] > 0 for tx in range(TILE_SIZE) for ty in range(TILE_SIZE)):
                    Tile(
                        (x, y),
                        [self.visible_sprites, self.obstacle_sprites],
                        'obstacle',
                        tile_surface
                    )

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
