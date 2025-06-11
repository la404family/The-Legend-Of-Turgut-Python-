import pygame
from settings.settings import *
from functions.get_os_adapted_path import get_os_adapted_path


class Entity:
    def __init__(self, name, health, damage, attack_radius, notice_radius, attack_sound, resistance, speed):
        self.name = name
        self.health = health
        self.damage = damage
        self.attack_radius = attack_radius
        self.notice_radius = notice_radius
        self.attack_sound = pygame.mixer.Sound(attack_sound)
        self.resistance = resistance
        self.speed = speed

    def attack(self):
        """Simule une attaque de l'entité."""
        self.attack_sound.play()
        return self.damage

    def take_damage(self, amount):
        """Réduit la santé de l'entité."""
        effective_damage = max(0, amount - self.resistance)
        self.health -= effective_damage
        return effective_damage

    def is_alive(self):
        """Vérifie si l'entité est encore en vie."""
        return self.health > 0
