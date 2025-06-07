import pygame

from settings.settings import *
from functions.get_os_adapted_path import get_os_adapted_path
from classes.keyboard import handler
from classes.joystick import joystick_handler


pygame.init()
# Pour utiliser la fonction avec un hook


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = pygame.image.load(
            get_os_adapted_path("imagesOfTurgut", "row-6-column-1.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-PLAYER_HITBOX_OFFSET, -
                                        PLAYER_HITBOX_OFFSET)
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED
        self.attacking = False
        self.attack_cooldown = ATTACK_COOLDOWN1
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

    def input(self):
        """
        MOUVEMENT DU JOUEUR
        """

        """ initialisation des variables de direction du joueur"""
        global player_direction_up
        global player_direction_down
        global player_direction_left
        global player_direction_right
        global player_direction_stay
        global player_current_direction
        # Initialisation des variables de direction du joueur

        player_direction_up = False
        player_direction_down = False
        player_direction_left = False
        player_direction_right = False
        player_direction_stay = True
        player_current_direction = "stay"
        joystick_event_handler = None  # Initialisation de l'événement joystick
        # Récupère le scancode de l'événement

        """gestion du mouvement du joueur
        Touche : q, Code : 30  -- Gauche
        Touche : d, Code : 32  -- Droite
        Touche : z, Code : 17  -- Haut
        Touche : s, Code : 31  -- Bas"""
        if joystick_handler.joystick is not None:
            # Si une manette est connectée, on utilise les axes de la manette
            joystick_handler.handle_events()
        else:
            # Sinon, on utilise le clavier
            handler.handle_events()

        if handler.event_scan_code == 30 or joystick_handler.joystick.get_axis(0) < -0.5:
            self.direction.x = -1
            self.direction.y = 0  # Assurer aucun mouvement vertical
            player_current_direction = "left"

        elif handler.event_scan_code == 32 or joystick_handler.joystick.get_axis(0) > 0.5:
            self.direction.x = 1
            self.direction.y = 0  # Assurer aucun mouvement vertical
            player_current_direction = "right"
        elif handler.event_scan_code == 17 or joystick_handler.joystick.get_axis(1) < -0.5:

            self.direction.x = 0  # Assurer aucun mouvement horizontal
            self.direction.y = -1
            player_current_direction = "up"
        elif handler.event_scan_code == 31 or joystick_handler.joystick.get_axis(1) > 0.5:
            self.direction.x = 0  # Assurer aucun mouvement horizontal
            self.direction.y = 1
            player_current_direction = "down"
        # si aucune touche n'est pressée, le joueur reste en place
        elif handler.event_scan_code is None or handler.event_scan_code == 0:
            self.direction.x = 0
            self.direction.y = 0
            player_current_direction = "stay"
        else:
            self.direction = pygame.math.Vector2(0, 0)
            player_current_direction = "stay"

        """
        ACTIONS DU JOUEUR
        Touche : u, Code : 22   -- touche X
        Touche : i, Code : 23   -- touche Y
        Touche : o, Code : 24   -- touche LB
        Touche : p, Code : 25   -- touche RT
        Touche : j, Code : 36   -- touche A
        Touche : k, Code : 37   -- touche B
        Touche : l, Code : 38   -- touche RB
        Touche : m, Code : 39   -- touche RB
        """
        # dictionnaire pour les touches d'attaque
        attack_buttons = (
            # touches u, i, j, k
            handler.event_scan_code in {22, 23, 36, 37} or
            (joystick_handler.joystick is not None and (
                joystick_handler.joystick.get_button(0) or  # bouton A
                joystick_handler.joystick.get_button(1) or  # bouton B
                joystick_handler.joystick.get_button(2) or  # bouton X
                joystick_handler.joystick.get_button(3)     # bouton Y
            ))
        )
        # dictionnaire pour les touches de course
        run_buttons = (
            # touches o, p, l, m
            handler.event_scan_code in {24, 25, 38, 39} or
            (joystick_handler.joystick is not None and (
                joystick_handler.joystick.get_button(4) or  # bouton LB
                joystick_handler.joystick.get_button(5) or  # bouton RB
                joystick_handler.joystick.get_axis(4) > 0.2 or  # trigger LT
                joystick_handler.joystick.get_axis(5) > 0.2   # trigger RT
            ))
        )
        # Gestion de l'état d'attaque
        if attack_buttons and not self.attacking:
            self.attack_time = pygame.time.get_ticks()
            self.attack_cooldown = ATTACK_COOLDOWN1
            self.attacking = True
        elif not attack_buttons:
            self.attacking = False

        # Gestion de la vitesse du joueur
        if run_buttons and not self.attacking:
            self.speed = PLAYER_RUN_SPEED
        else:
            self.speed = PLAYER_NO_SPEED

    def move(self, speed):
        """déplacement du joueur"""
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        # Met à jour la position du rectangle de collision
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """vérification des collisions du joueur"""
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if hasattr(sprite, "hitbox") and sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if hasattr(sprite, "hitbox") and sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        """Gère le cooldown de l'attaque du joueur.
        Pendant l'attaque, le joueur ne peut pas bouger (NO_SPEED).
        Une fois le cooldown terminé, l'attaque s'arrête et la vitesse normale est rétablie.
        """

        if self.attack_time is None:
            self.attack_time = pygame.time.get_ticks()
        if self.attack_time:
            if pygame.time.get_ticks() - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.speed = PLAYER_SPEED
            if pygame.time.get_ticks() - self.attack_time < self.attack_cooldown:
                print("Attaque en cours, cooldown actif.")
                self.speed = PLAYER_NO_SPEED

    def update(self):
        """update du joueur"""
        self.input()
        self.cooldowns()
        self.move(self.speed)
