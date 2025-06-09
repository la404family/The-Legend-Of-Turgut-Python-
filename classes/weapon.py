import pygame
import math

from pygame.locals import *
from pygame import Vector2

from settings.settings import WEAPON_DATA
from functions.get_os_adapted_path import get_os_adapted_path


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(*groups)
        self.player = player
        self.attack_type = player.attack_type
        self.weapon_data = WEAPON_DATA[self.attack_type]
        self.direction = player.status.split("_")[0]

        # Charger l'image originale
        self.original_image = pygame.image.load(
            self.weapon_data["sprite"]).convert_alpha()
        self.image = self.original_image

        # Variables pour l'animation
        self.animation_data = self.weapon_data["animation"]
        self.rotation_angle = 0
        self.distance_traveled = 0
        self.is_returning = False

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

        # Appliquer la rotation initiale si nécessaire
        if self.animation_data["type"] in ["rotate", "swing", "spin"]:
            self.image = pygame.transform.rotate(
                self.original_image, self.initial_rotation)
            self.rotation_angle = self.initial_rotation

    def update(self):
        # Gérer les différents types d'animation
        if self.animation_data["type"] == "rotate":
            self.handle_rotate_animation()
        elif self.animation_data["type"] == "swing":
            self.handle_swing_animation()
        elif self.animation_data["type"] == "stab":
            self.handle_stab_animation()
        elif self.animation_data["type"] == "spin":
            self.handle_spin_animation()

        # Vérifier si l'arme doit être supprimée
        if self.distance_traveled >= self.animation_data["max_distance"] * (2 if self.is_returning else 1):
            self.player.destroy_attack()

    def handle_swing_animation(self):
        print("swing")
        # Rotation de l'arme
        self.rotation_angle = (self.rotation_angle +
                               self.animation_data["rotation_speed"]) % 360
        self.image = pygame.transform.rotate(
            self.original_image, self.rotation_angle)
        # avancer l'arme dans la direction du joueur
        self.rect.center += self.direction_vector * \
            self.animation_data["speed"]
        self.distance_traveled += self.animation_data["speed"]

    def handle_rotate_animation(self):
        print("rotate")
        # Rotation de l'arme
        self.rotation_angle = (self.rotation_angle +
                               self.animation_data["rotation_speed"]) % 360
        self.image = pygame.transform.rotate(
            self.original_image, self.rotation_angle)
        # avancer l'arme dans la direction du joueur
        self.rect.center += self.direction_vector * \
            self.animation_data["speed"]
        self.distance_traveled += self.animation_data["speed"]

    def handle_stab_animation(self):
        print("stab")
        amplitude = 0.5
        frequency = 50  # Amplitude et fréquence pour l'oscillation

        # alterner entre la droite et la gauche de manière plus régulière
        direction = 1 if int(self.distance_traveled *
                             frequency) % 2 == 0 else -1
        offset = self.direction_vector.rotate(
            90 * direction) * math.sin(self.distance_traveled * frequency) * amplitude

        self.rect.center += self.direction_vector * \
            self.animation_data["speed"] + offset
        self.distance_traveled += self.animation_data["speed"]

        # rotation
        self.rotation_angle = (self.rotation_angle +
                               self.animation_data["rotation_speed"]) % 360
        self.image = pygame.transform.rotate(
            self.original_image, self.rotation_angle)

    def handle_spin_animation(self):

        print("spin")

        # Initialisations si nécessaires
        if not hasattr(self, 'current_radius'):
            self.current_radius = 20  # Rayon initial

        if not hasattr(self, 'orbit_angle'):
            self.orbit_angle = 0  # Angle pour la rotation autour du joueur

        if not hasattr(self, 'self_spin_angle'):
            self.self_spin_angle = 0  # Angle pour la rotation sur elle-même

        # Augmenter le rayon progressivement
        self.current_radius += 0.3  # Ou un autre incrément selon l'effet souhaité

        # Mise à jour de l'angle orbital
        self.orbit_angle = (self.orbit_angle +
                            self.animation_data["rotation_speed"]) % 360
        angle_rad = math.radians(self.orbit_angle)

        # Calcul de l'offset pour tourner autour du joueur
        offset = pygame.Vector2(
            math.cos(angle_rad) * self.current_radius,
            math.sin(angle_rad) * self.current_radius
        )

        # Mise à jour de la position
        self.rect.center = self.player.rect.center + offset

        # Mise à jour de la rotation sur elle-même
        # Vitesse de rotation propre
        self.self_spin_angle = (self.self_spin_angle + 10) % 360
        self.image = pygame.transform.rotate(
            self.original_image, self.self_spin_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
