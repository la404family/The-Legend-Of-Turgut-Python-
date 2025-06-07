import pygame
from settings.settings import *
from functions.get_os_adapted_path import get_os_adapted_path
from classes.joystick import joystick_handler

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(
            get_os_adapted_path("imagesOfTurgut", "row-6-column-1.png")
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-PLAYER_HITBOX_OFFSET, -
                                        PLAYER_HITBOX_OFFSET)
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED
        self.attacking = False
        self.attack_cooldown = ATTACK_COOLDOWN1
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        self._setup_controls()

    def _setup_controls(self):
        """Initialisation des contrôles clavier et manette."""
        self.key_mappings = {
            'left': pygame.K_q,
            'right': pygame.K_d,
            'up': pygame.K_z,
            'down': pygame.K_s,
            'attack': [pygame.K_u, pygame.K_i, pygame.K_j, pygame.K_k],
            'run': [pygame.K_o, pygame.K_p, pygame.K_l, pygame.K_m]
        }

        self.joystick_buttons = {
            'attack': [0, 1, 2, 3],
            'run': [4, 5],
            'run_axes': [4, 5]
        }

    def input(self):
        """Gestion du mouvement du joueur sans déplacement diagonal, avec support pour la manette."""
        keys = pygame.key.get_pressed()
        joystick = getattr(joystick_handler, "joystick", None)

        # Réinitialisation de la direction
        self.direction.x, self.direction.y = 0, 0

        # Détection des touches clavier (priorité aux touches pressées)
        if keys[self.key_mappings['left']]:
            self.direction.x = -1
        elif keys[self.key_mappings['right']]:
            self.direction.x = 1
        elif keys[self.key_mappings['up']]:
            self.direction.y = -1
        elif keys[self.key_mappings['down']]:
            self.direction.y = 1

        # Détection des axes du joystick (si connecté et aucune touche clavier pressée)
        if joystick and self.direction.length() == 0:
            joystick_x = joystick.get_axis(0)
            joystick_y = joystick.get_axis(1)

            if abs(joystick_x) > abs(joystick_y):  # Priorité à l'axe dominant
                if joystick_x < -0.5:
                    self.direction.x = -1
                elif joystick_x > 0.5:
                    self.direction.x = 1
            else:
                if joystick_y < -0.5:
                    self.direction.y = -1
                elif joystick_y > 0.5:
                    self.direction.y = 1

        # Normalisation pour éviter les vecteurs diagonaux
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        # Gestion de l'état d'attaque
        attack_pressed = any(keys[btn] for btn in self.key_mappings['attack']) or (
            joystick and any(joystick.get_button(btn)
                             for btn in self.joystick_buttons['attack'])
        )

        if attack_pressed and not self.attacking:
            self.attack_time = pygame.time.get_ticks()
            self.attacking = True

        # Gestion de l'état de course
        run_pressed = any(keys[btn] for btn in self.key_mappings['run']) or (
            joystick and (
                any(joystick.get_button(btn) for btn in self.joystick_buttons['run']) or
                any(joystick.get_axis(axis) >
                    0.2 for axis in self.joystick_buttons['run_axes'])
            )
        )

        self.speed = PLAYER_RUN_SPEED if run_pressed else PLAYER_SPEED

    def move(self):
        """Déplacement du joueur avec gestion des collisions."""
        if self.direction.length() > 0:
            self.hitbox.x += self.direction.x * self.speed
            self.collision("horizontal")
            self.hitbox.y += self.direction.y * self.speed
            self.collision("vertical")
            self.rect.center = self.hitbox.center

    def collision(self, direction):
        """Vérification des collisions du joueur."""
        for sprite in self.obstacle_sprites:
            if hasattr(sprite, "hitbox") and sprite.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:  # Vers la droite
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # Vers la gauche
                        self.hitbox.left = sprite.hitbox.right
                elif direction == "vertical":
                    if self.direction.y > 0:  # Vers le bas
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # Vers le haut
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        """Gestion du cooldown des attaques."""
        current_time = pygame.time.get_ticks()
        if self.attacking and current_time - self.attack_time < self.attack_cooldown:
            self.speed = PLAYER_NO_SPEED
        else:
            self.attacking = False

    def update(self):
        """Mise à jour du joueur."""
        self.input()
        self.cooldowns()
        self.move()
