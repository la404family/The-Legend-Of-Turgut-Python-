import pygame
from csv import reader
import os
from settings.settings import *


def import_csv_layout(path):
    """Importe un fichier CSV et retourne une liste de listes"""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    terrain_map = []
    with open(path, encoding='utf-8', newline='') as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map


def import_folder(path):
    """Importe tous les fichiers d'un dossier et retourne une liste de surfaces.
    Returns:
        list: Liste de surfaces pygame.
    """
    surface_list = []
    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = f"{path}/{image}"
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list
