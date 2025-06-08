import pygame
from settings.settings import WEAPON_DATA
from functions.get_os_adapted_path import get_os_adapted_path


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(*groups)
        direction = player.status.split("_")[0]
        # image d'attaque
        self.image = pygame.Surface((16, 16))
        # mettre la surface en rouge pour la visualisation
        self.image = pygame.image.load(get_os_adapted_path(
            "assets", "hache.png")).convert_alpha()
        # définir la position de l'arme par rapport au joueur
        # si la direction contient "right", "left", "up" ou "down"
        if "right" in direction:
            self.rect = self.image.get_rect(
                midleft=player.rect.midright - pygame.Vector2(10, 0))
            # tourner l'image de 90 degrés vers la droite
            self.image = pygame.transform.rotate(
                self.image, -90)
        elif "left" in direction:
            self.rect = self.image.get_rect(
                midright=player.rect.midleft - pygame.Vector2(-10, 0))
            # tourner l'image de 90 degrés vers la gauche
            self.image = pygame.transform.rotate(
                self.image, 90)
        elif "up" in direction:
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop - pygame.Vector2(0, -10))
            # l'image reste dans la même orientation
        elif "down" in direction:
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom - pygame.Vector2(0, 10))
           # tourner l'image de 180 degrés
            self.image = pygame.transform.rotate(
                self.image, 180)
