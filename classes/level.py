import pygame
import random
from settings.settings import *
from functions.get_os_adapted_path import get_os_adapted_path
from functions.csv_reader import import_csv_layout
from classes.tile import *
from classes.player import *
from classes.camera import YsortCameraGroup
# Ensure this import matches the actual location of import_csv_layout


class Level:
    def __init__(self):
        self .display_surface = pygame.display.get_surface()
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        """Crée la carte du niveau à partir d'une image PNG d'obstacles"""
        # Charger l'image des obstacles
        obstacle_image = pygame.image.load(
            get_os_adapted_path("imagesOfMaps", "mapArbres.png")).convert_alpha()

        # # L'image est un obstacle sauf si elle est transparente (alpha = 0)
        # obstacle_tiles = []
        # for y in range(0, obstacle_image.get_height(), TILE_SIZE):
        #     for x in range(0, obstacle_image.get_width(), TILE_SIZE):
        #         tile_surface = obstacle_image.subsurface(
        #             (x, y, TILE_SIZE, TILE_SIZE))
        #         if tile_surface.get_alpha() != 0:
        #             # Si le tile n'est pas transparent, on le considère comme un obstacle
        #             obstacle_tile = Tile(
        #                 (x, y), [self.visible_sprites, self.obstacle_sprites], 'obstacle', tile_surface)
        #             obstacle_tiles.append(obstacle_tile)

        # faire un random sur le tableau PLAYER_START_POSITION
        random_position = random.choice(PLAYER_START_POSITION)
        self.player = Player(
            (random_position), [self.visible_sprites], self.obstacle_sprites)

        # # Importer les données de la carte depuis les fichiers CSV
        # terrain_layout = import_csv_layout(
        #     get_os_adapted_path("imagesOfMaps", "mapArbres_Floor.csv"))
        # details_layout = import_csv_layout(
        #     get_os_adapted_path("imagesOfMaps", "mapArbres_details.csv"))
        # obstacle_layout = import_csv_layout(
        #     get_os_adapted_path("imagesOfMaps", "mapArbres_arbres.csv"))

        # Positionner le joueur à une position aléatoire dans PLAYER_START_POSITION
        random_position = random.choice(PLAYER_START_POSITION)
        self.player = Player(
            (random_position), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        """Gère le rendu du niveau"""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
