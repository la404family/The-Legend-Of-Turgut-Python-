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
        self.import_player_assets()
        self.status = "down_idle"  # Statut initial du joueur
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED
        self.attacking = False
        self.attack_cooldown = ATTACK_COOLDOWN1
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        self._setup_controls()

    def import_player_assets(self):
        """Importe les assets du joueur"""
        player_assets = {
            "up1": get_os_adapted_path("imagesOfTurgut", "row-1-column-4.png"),
            "down1": get_os_adapted_path("imagesOfTurgut", "row-2-column-6.png"),
            "left1": get_os_adapted_path("imagesOfTurgut", "row-3-column-6.png"),
            "right1": get_os_adapted_path("imagesOfTurgut", "row-3-column-8.png"),

            "up2": get_os_adapted_path("imagesOfTurgut", "row-1-column-5.png"),
            "down2": get_os_adapted_path("imagesOfTurgut", "row-2-column-7.png"),
            "left2": get_os_adapted_path("imagesOfTurgut", "row-6-column-3.png"),
            "right2": get_os_adapted_path("imagesOfTurgut", "row-3-column-7.png"),

            "up_attack": get_os_adapted_path("imagesOfTurgut", "row-7-column-4.png"),
            "down_attack": get_os_adapted_path("imagesOfTurgut", "row-7-column-3.png"),
            "left_attack": get_os_adapted_path("imagesOfTurgut", "row-7-column-5.png"),
            "right_attack": get_os_adapted_path("imagesOfTurgut", "row-7-column-6.png"),

            "up_idle": get_os_adapted_path("imagesOfTurgut", "row-3-column-3.png"),
            "down_idle": get_os_adapted_path("imagesOfTurgut", "row-2-column-8.png"),
            "left_idle": get_os_adapted_path("imagesOfTurgut", "row-3-column-6.png"),
            "right_idle": get_os_adapted_path("imagesOfTurgut", "row-3-column-7.png"),

            "up_hit": get_os_adapted_path("imagesOfTurgut", "row-6-column-4.png"),
            "down_hit": get_os_adapted_path("imagesOfTurgut", "row-6-column-3.png"),
            "left_hit": get_os_adapted_path("imagesOfTurgut", "row-6-column-5.png"),
            "right_hit": get_os_adapted_path("imagesOfTurgut", "row-6-column-6.png"),

            "up_dead": get_os_adapted_path("imagesOfTurgut", "row-5-column-6.png"),
            "down_dead": get_os_adapted_path("imagesOfTurgut", "row-5-column-6.png"),
            "left_dead": get_os_adapted_path("imagesOfTurgut", "row-5-column-7.png"),
            "right_dead": get_os_adapted_path("imagesOfTurgut", "row-5-column-8.png"),

            "up_protect": get_os_adapted_path("imagesOfTurgut", "row-4-column-7.png"),
            "down_protect": get_os_adapted_path("imagesOfTurgut", "row-4-column-4.png"),
            "left_protect": get_os_adapted_path("imagesOfTurgut", "row-5-column-5.png"),
            "right_protect": get_os_adapted_path("imagesOfTurgut", "row-4-column-8.png"),

            "take_item": get_os_adapted_path("imagesOfTurgut", "row-6-column-2.png")
        }
        # Convertir les chemins en images
        for key, path in player_assets.items():
            converted_image = pygame.image.load(path).convert_alpha()
            player_assets[key] = converted_image
            self.animations = player_assets
            print(self.animations)

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
            self.status = "left"
        elif keys[self.key_mappings['right']]:
            self.direction.x = 1
            self.status = "right"
        elif keys[self.key_mappings['up']]:
            self.direction.y = -1
            self.status = "up"
        elif keys[self.key_mappings['down']]:
            self.direction.y = 1
            self.status = "down"

        # Détection des axes du joystick (si connecté et aucune touche clavier pressée)
        if joystick and self.direction.length() == 0:
            joystick_x = joystick.get_axis(0)
            joystick_y = joystick.get_axis(1)

            if abs(joystick_x) > abs(joystick_y):  # Priorité à l'axe dominant
                if joystick_x < -0.5:
                    self.direction.x = -1
                    self.status = "left"
                elif joystick_x > 0.5:
                    self.direction.x = 1
                    self.status = "right"
            else:
                if joystick_y < -0.5:
                    self.direction.y = -1
                    self.status = "up"
                elif joystick_y > 0.5:
                    self.direction.y = 1
                    self.status = "down"

        # Normalisation pour éviter les vecteurs diagonaux
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        # Gestion de l'état d'attaque
        attack_pressed = any(keys[btn] for btn in self.key_mappings['attack']) or (
            joystick and any(joystick.get_button(btn)
                             for btn in self.joystick_buttons['attack'])
        )
        if attack_pressed and self.status.startswith("down"):
            self.status = "down_attack"
        if attack_pressed and self.status.startswith("up"):
            self.status = "up_attack"
        if attack_pressed and self.status.startswith("left"):
            self.status = "left_attack"
        if attack_pressed and self.status.startswith("right"):
            self.status = "right_attack"

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

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status:
                if "attack" in self.status:
                    self.status = self.status.replace("attack", "idle")
                elif "hit" in self.status:
                    self.status = self.status.replace("hit", "idle")
                elif "dead" in self.status:
                    self.status = self.status.replace("dead", "idle")
                elif "protect" in self.status:
                    self.status = self.status.replace("protect", "idle")
                else:
                    self.status = f"{self.status}_idle"

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
            self.status = self.status + "_attack"
        else:
            self.attacking = False

    def animate(self):
        animation = self.animations[self.status]
        if not animation:
            print(f"Animation not found for status: {self.status}")
            return

        """Animation du joueur en fonction de son statut."""
        if self.status.endswith("_idle"):
            self.image = self.animations[self.status]
        elif self.status.endswith("_attack"):
            self.image = self.animations[self.status]
        elif self.status.endswith("_hit"):
            self.image = self.animations[self.status]
        elif self.status.endswith("_dead"):
            self.image = self.animations[self.status]
        elif self.status.endswith("_protect"):
            self.image = self.animations[self.status]
        else:
            # # Animation de marche est composée de deux images
            # if self.status.startswith("up"):
            #     self.image = self.animations["up1"] if self.direction.y < 0 else self.animations["up2"]
            # elif self.status.startswith("down"):
            #     self.image = self.animations["down1"] if self.direction.y > 0 else self.animations["down2"]
            # elif self.status.startswith("left"):
            #     self.image = self.animations["left1"] if self.direction.x < 0 else self.animations["left2"]
            # elif self.status.startswith("right"):
            #     self.image = self.animations["right1"] if self.direction.x > 0 else self.animations["right2"]
            print(f"Unhandled status: {self.status}")

    def update(self):
        """Mise à jour du joueur."""
        self.input()
        self.cooldowns()
        self.get_status()
        # self.animate()
        print(f"Player status: {self.status}")  # Debugging line
        self.move()
