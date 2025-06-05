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

        # Charger l'image des obstacles
        obstacle_image = pygame.image.load(
            get_os_adapted_path("imagesOfMaps", "mapArbres.png")).convert_alpha()

        # L'image est un obstacle seulement si elle contient des pixels non transparents
        # sur toute la zone 16x16 de la tuile
        obstacle_tiles = []
        for y in range(0, obstacle_image.get_height(), TILE_SIZE):
            for x in range(0, obstacle_image.get_width(), TILE_SIZE):
                tile_surface = obstacle_image.subsurface(
                    (x, y, TILE_SIZE, TILE_SIZE))

                # Vérifier si la tuile contient au moins un pixel non transparent
                has_obstacle = False
                for ty in range(TILE_SIZE):
                    for tx in range(TILE_SIZE):
                        # Obtenir la valeur alpha du pixel (tx, ty)
                        alpha = tile_surface.get_at((tx, ty))[3]
                        if alpha > 0:  # Si alpha > 0, pixel non transparent
                            has_obstacle = True
                            break
                    if has_obstacle:
                        break

                if has_obstacle:
                    # Si la tuile contient au moins un pixel non transparent, on la considère comme un obstacle
                    tile = Tile((x, y), [self.visible_sprites, self.obstacle_sprites],
                                'obstacle', tile_surface)
                    obstacle_tiles.append(tile)

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
