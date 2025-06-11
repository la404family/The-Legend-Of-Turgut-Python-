import pygame
from settings.settings import *
from functions.get_os_adapted_path import get_os_adapted_path


class UI:
    def __init__(self):
        # Initialisation des icônes
        self.energy_icon = pygame.image.load(
            get_os_adapted_path("assets", "energy.png")).convert_alpha()
        self.health_icon = pygame.image.load(
            get_os_adapted_path("assets", "health.png")).convert_alpha()

        # Redimensionnement
        self.health_icon = pygame.transform.scale(self.health_icon, (48, 48))
        self.energy_icon = pygame.transform.scale(self.energy_icon, (48, 48))

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Position des barres (décalées à droite pour laisser de la place aux icônes)
        ICON_OFFSET = 26  # 16px pour l'icône + 10px de marge
        self.health_bar_rect = pygame.Rect(
            10 + ICON_OFFSET, 14, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10 + ICON_OFFSET, 50, ENEGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # Bordure + fond
        border_rect = bg_rect.copy()
        border_rect.inflate_ip(6, 6)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         border_rect, border_radius=5)
        pygame.draw.rect(self.display_surface,
                         UI_BACKGROUND_COLOR, bg_rect, border_radius=5)

        # Barre de progression
        ratio = current / max_amount
        current_rect = bg_rect.copy()
        current_rect.width = int(bg_rect.width * ratio)
        pygame.draw.rect(self.display_surface, color, current_rect)

        # Ajout du texte centré dans la barre
        if bg_rect == self.health_bar_rect:
            text = "SANTE DE TURGUT"
        else:
            text = "ÇAY DANS LE SANG"

        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(text_surf, text_rect)

    def show_kill_count(self, kill_count):
        # Police pour le titre (peut utiliser la même ou une plus petite)
        # ou pygame.font.Font(None, 24) pour une taille différente
        title_font = self.font

        # Texte du compteur de kills
        count_text = f"{kill_count}"
        count_surf = self.font.render(count_text, True, "#D2D42B")
        # déplacement du rectangle compteur
        count_rect = count_surf.get_rect(
            midbottom=(self.display_surface.get_width() - 130,
                       self.display_surface.get_height() - 20))

        # Texte du titre
        title_text = "COMPTEUR DE KILLS"
        title_surf = title_font.render(title_text, True, "white")

        # déplacement du rectangle titre
        title_rect = title_surf.get_rect(
            midbottom=(self.display_surface.get_width() - 130,
                       self.display_surface.get_height() - 50))

        # Calcul du rectangle englobant pour le fond
        combined_rect = count_rect.union(
            title_rect)  # Combine les deux rectangles
        bg_rect = combined_rect.inflate(20, 20)  # Marge autour
        border_rect = bg_rect.inflate(6, 6)  # Bordure extérieure
        # déplacement du rectangle de fond pour le centrer
        bg_rect.center = (self.display_surface.get_width() - 130,
                          self.display_surface.get_height() - 47)

        # Dessiner les éléments
        # Bordure
        pygame.draw.rect(self.display_surface, "#7A5C17",
                         border_rect, 0, border_radius=5)  # surface, couleur, épaisseur, rayon de bordure
        # Fond noir
        pygame.draw.rect(self.display_surface, "black",
                         bg_rect, 0, border_radius=4)
        # Titre
        self.display_surface.blit(title_surf, title_rect)
        # Compteur
        self.display_surface.blit(count_surf, count_rect)

    def display(self, player):
        # Position des icônes (à gauche des barres)
        health_icon_pos = (self.health_bar_rect.left-45,
                           self.health_bar_rect.centery - 28)
        energy_icon_pos = (self.energy_bar_rect.left-45,
                           self.energy_bar_rect.centery - 24)

        # Affichage des icônes
        self.display_surface.blit(self.health_icon, health_icon_pos)
        self.display_surface.blit(self.energy_icon, energy_icon_pos)

        # Affichage des barres (le texte est maintenant géré dans show_bar)
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, HEALTH_BAR_COLOR)
        self.show_bar(
            player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_BAR_COLOR)
        self.show_kill_count(player.kill_count)
