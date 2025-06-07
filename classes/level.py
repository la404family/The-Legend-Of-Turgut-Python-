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
        # Empêche de relancer la création de la carte si elle a déjà été faite
        if hasattr(self, 'map_created') and self.map_created:
            return  # On quitte immédiatement si la carte est déjà créée

        # Charger l'image des obstacles
        obstacle_image = pygame.image.load(
            get_os_adapted_path("imagesOfMaps", "mapArbres.png")).convert_alpha()
        taille_complete_de_limage = obstacle_image.get_size()

        # L'image est un obstacle seulement si elle contient des pixels non transparents
        obstacle_tiles = []
        for y in range(0, taille_complete_de_limage[1], TILE_SIZE):
            for x in range(0, taille_complete_de_limage[0], TILE_SIZE):
                tile_surface = obstacle_image.subsurface(
                    (x, y, TILE_SIZE, TILE_SIZE))

                # Vérifier si la tuile contient au moins un pixel non transparent
                has_obstacle = False
                for ty in range(TILE_SIZE):
                    for tx in range(TILE_SIZE):
                        alpha = tile_surface.get_at((tx, ty))[3]
                        if alpha > 0:
                            has_obstacle = True
                            break
                    if has_obstacle:
                        break

                if has_obstacle:
                    tile = Tile((x, y), [self.visible_sprites, self.obstacle_sprites],
                                'obstacle', tile_surface)
                    obstacle_tiles.append(tile)

        # Positionner le joueur à une position aléatoire
        random_position = random.choice(PLAYER_START_POSITION)
        self.player = Player(
            (random_position), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        """Gère le rendu du niveau"""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
