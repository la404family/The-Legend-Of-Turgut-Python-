import pygame
import math
import random
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

    def handle_rotate_animation(self):
        # Rotation continue avec déplacement
        self.rotation_angle = (self.rotation_angle +
                               self.animation_data["rotation_speed"]) % 360
        self.image = pygame.transform.rotate(
            self.original_image, self.rotation_angle)

        # Déplacement
        self.rect.center += self.direction_vector * \
            self.animation_data["speed"]
        self.distance_traveled += self.animation_data["speed"]

    def handle_swing_animation(self):
        # Rotation limitée avec déplacement
        if abs(self.rotation_angle - self.initial_rotation) < self.animation_data["swing_angle"]:
            self.rotation_angle = (
                self.rotation_angle + self.animation_data["rotation_speed"]) % 360
            self.image = pygame.transform.rotate(
                self.original_image, self.rotation_angle)

        # Déplacement
        self.rect.center += self.direction_vector * \
            self.animation_data["speed"]
        self.distance_traveled += self.animation_data["speed"]

    def handle_stab_animation(self):
        # Déplacement avant et retour
        if not self.is_returning:
            self.rect.center += self.direction_vector * \
                self.animation_data["speed"]
            self.distance_traveled += self.animation_data["speed"]

            if self.distance_traveled >= self.animation_data["max_distance"]:
                self.is_returning = True
        else:
            self.rect.center -= self.direction_vector * \
                self.animation_data["return_speed"]
            self.distance_traveled += self.animation_data["return_speed"]

    def handle_spin_animation(self):
        # Rotation rapide sur place
        self.rotation_angle = (self.rotation_angle +
                               self.animation_data["rotation_speed"]) % 360
        self.image = pygame.transform.rotate(
            self.original_image, self.rotation_angle)

        # Petit déplacement circulaire
        circle_progress = self.distance_traveled / \
            self.animation_data["max_distance"]
        angle = circle_progress * 2 * math.pi * self.animation_data["circles"]
        offset = pygame.Vector2(
            math.cos(angle) * 30,
            math.sin(angle) * 30
        )
        self.rect.center = self.player.rect.center + offset
        self.distance_traveled += self.animation_data["speed"]
