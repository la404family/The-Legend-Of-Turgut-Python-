import pygame
from settings.settings import WEAPON_DATA
from functions.get_os_adapted_path import get_os_adapted_path


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(*groups)
        self.player = player
        self.direction = player.status.split("_")[0]

        # Charger l'image originale
        self.original_image = pygame.image.load(get_os_adapted_path(
            "assets", "hache.png")).convert_alpha()
        self.image = self.original_image

        # Variables pour l'animation
        self.rotation_angle = 0
        self.rotation_speed = 35  # Vitesse de rotation
        self.speed = 8  # Vitesse de déplacement
        self.distance_traveled = 0
        self.max_distance = 100  # Distance maximale parcourue

        # Position initiale
        self.set_initial_position()

    def set_initial_position(self):
        """Définit la position initiale en fonction de la direction"""
        offset = 20  # Distance initiale par rapport au joueur

        if "right" in self.direction:
            self.rect = self.image.get_rect(
                midleft=self.player.rect.midright + pygame.Vector2(0, 0))
            self.direction_vector = pygame.Vector2(1, 0)
            self.initial_rotation = -90
        elif "left" in self.direction:
            self.rect = self.image.get_rect(
                midright=self.player.rect.midleft + pygame.Vector2(0, 0))
            self.direction_vector = pygame.Vector2(-1, 0)
            self.initial_rotation = 90
        elif "up" in self.direction:
            self.rect = self.image.get_rect(
                midbottom=self.player.rect.midtop + pygame.Vector2(0, 0))
            self.direction_vector = pygame.Vector2(0, -1)
            self.initial_rotation = 0
        elif "down" in self.direction:
            self.rect = self.image.get_rect(
                midtop=self.player.rect.midbottom + pygame.Vector2(0, 0))
            self.direction_vector = pygame.Vector2(0, 1)
            self.initial_rotation = 180

        # Appliquer la rotation initiale
        self.image = pygame.transform.rotate(
            self.original_image, self.initial_rotation)
        self.rotation_angle = self.initial_rotation

    def update(self):
        # Faire tourner l'image
        self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(
            self.original_image, self.rotation_angle)

        # Garder le centre de l'image après rotation
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

        # Déplacer l'arme dans la direction
        self.rect.center += self.direction_vector * self.speed
        self.distance_traveled += self.speed

        # Supprimer l'arme si elle a parcouru sa distance maximale
        if self.distance_traveled >= self.max_distance:
            self.kill()
