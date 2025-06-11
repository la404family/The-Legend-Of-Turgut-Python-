import tkinter as tk
from functions.get_screen_dimensions import get_screen_dimensions
from functions.get_os_adapted_path import get_os_adapted_path
# Ce fichier contient les paramètres de configuration du jeu {Variables globales}
root = tk.Tk()
UI_FONT = get_os_adapted_path("font", "retro.ttf")
UI_FONT_SIZE = 18
# Couleur de fond de l'UI
BAR_HEIGHT = 24  # Hauteur de la barre d'UI
# Calculer la taille de l'écran et ajuster les dimensions
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
# 40% de la taille de l'écran
HEALTH_BAR_WIDTH = int(SCREEN_WIDTH * 0.4)  # Largeur de la barre de vie
ENEGY_BAR_WIDTH = int(SCREEN_WIDTH * 0.4)  # Largeur de la barre de mana
ITEM_BOX_SIZE = 16  # Taille de la boîte d'objets
UI_BACKGROUND_COLOR = "#3E3E3E"
UI_BORDER_COLOR = "#7A5C17"  # Couleur de la bordure de l'UI
UI_TEXT_COLOR = "#DCD6D6"  # Couleur du texte de l'UI
HEALTH_BAR_COLOR = "#9C1E1E"  # Couleur de la barre de vie
ENERGY_BAR_COLOR = "#3B1C84"  # Couleur de la barre de mana
UI_BORDER_COLOR_ACTIVE = "gold"
# Utilisation de la fonction pour obtenir les dimensions de l'écran
WIDTH, HEIGHT = get_screen_dimensions()
# Images par seconde
FPS = 60
# Taille de la tuile
TILE_SIZE = 16
# Vitesse du joueur
PLAYER_SPEED = 2
PLAYER_RUN_SPEED = 4
PLAYER_NO_SPEED = 0
# Temps d'attaque en millisecondes
ATTACK_COOLDOWN1 = 500
ATTACK_COOLDOWN2 = 3500
ATTACK_COOLDOWN3 = 1000
ATTACK_COOLDOWN4 = 1250
# Décalage de la hitbox du joueur
PLAYER_HITBOX_OFFSET = 4
# Données X,Y du placement aléatoire du joueur sur la carte
PLAYER_START_POSITION = [(662, 615), (1591, 439), (1274, 817), (854, 1319), (1206, 1393), (913, 1587), (2287, 2139), (844, 2105), (1413, 2107), (1725, 1924), (1856, 2477), (2441, 31900), (
    2559, 2367), (1952, 3317)]
WEAPON_DATA = {
    "attack1": {  # Attaque en cercle
        "name": "Hache1",
        "damage": 25,
        "cooldown": ATTACK_COOLDOWN4,
        "sprite": get_os_adapted_path("assets", "hache.png"),
        "animation": {
            "type": "rotate",  # Toujours "rotate" mais maintenant c'est un cercle
            "rotation_speed": 35,
            "speed": 1,
            "max_distance": 360
        }
    },
    "attack2": {  # Attaque droite
        "name": "Hache2",
        "damage": 15,
        "cooldown": ATTACK_COOLDOWN3,
        "sprite": get_os_adapted_path("assets", "hache.png"),
        "animation": {
            "type": "swing",  # Toujours "swing" mais maintenant c'est droit
            "rotation_speed": 25,
            "speed": 2,
            "max_distance": 350,
            "swing_angle": 180,  # Gardé mais pas utilisé
            "circles": 2  # Gardé mais pas utilisé
        }
    },
    "attack3": {  # Attaque en dent de scie
        "name": "Hache3",
        "damage": 20,
        "cooldown": ATTACK_COOLDOWN1,
        "sprite": get_os_adapted_path("assets", "hache.png"),
        "animation": {
            "type": "stab",  # Toujours "stab" mais maintenant c'est une scie
            "speed": 3,
            "max_distance": 200,
            "return_speed": 0,  # Gardé mais pas utilisé
            "circles": 4,
            "rotation_speed": 35
        }
    },
    "attack4": {  # Attaque en S
        "name": "Hache4",
        "damage": 10,
        "cooldown": ATTACK_COOLDOWN2,
        "sprite": get_os_adapted_path("assets", "hache.png"),
        "animation": {
            "type": "spin",  # Toujours "spin" mais maintenant c'est un S
            "rotation_speed": 5,
            "speed": 50,
            "max_distance": 1720,
            "circles": 3,  # Rayon évolutif
        }
    }
}

# Teste de la carte du monde
WORLD_MAP_TEST = [
    ["x", "x", "x", "x", "x", "x", "x", "x", "x",
        "x", "x", "x", "x", "x", "x", "x", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", "p", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", " ", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", " ", " ", " ", "x"],
    ["x", "x", "x", "x", "x", "x", "x", "x", "x",
        "x", "x", "x", "x", "x", "x", "x", "x"]
]

TEXTES_DU_JEU = {
    "welcome": "Bienvenue dans le jeu !",
    "game_over": "Jeu terminé !",
    "level_up": "Niveau supérieur atteint !",
    "new_item": "Nouvel objet obtenu !",
    "quest_complete": "Quête terminée !",
    "error": "Une erreur est survenue !"
}
# Messages de l'unité turque
MESSAGES_UNITE_TURC = {
    "msgTR": [
        "Birlik güçtür.",
        "Biz tek yüreğiz.",
        "Birlikte yenilmeziz.",
        "Uyum büyüklüğü getirir.",
        "Gücümüz birliğimizden gelir.",
        "Birlikte geleceğe ilerliyoruz.",
        "Halkın birliği en büyük zenginliğidir.",
        "Birlikte her şeyin üstesinden gelebiliriz."
    ],
    "msgFR": [
        "L’unité fait la force.",
        "Nous sommes un seul cœur.",
        "Ensemble, nous sommes invincibles.",
        "L'harmonie crée la grandeur.",
        "Notre force vient de notre unité.",
        "Unis, nous avançons vers l’avenir.",
        "L’unité du peuple est sa plus grande richesse.",
        "Ensemble, nous pouvons surmonter tous les obstacles."
    ],
    "msgEN": [
        "Unity is strength.",
        "We are one heart.",
        "Together, we are invincible.",
        "Harmony brings greatness.",
        "Our strength comes from our unity.",
        "United, we move towards the future.",
        "The unity of the people is its greatest wealth.",
        "Together, we can overcome any obstacle."
    ],
    "msgDE": [
        "Einheit ist Stärke.",
        "Wir sind ein Herz.",
        "Gemeinsam sind wir unbesiegbar.",
        "Harmonie bringt Größe.",
        "Unsere Stärke kommt aus unserer Einheit.",
        "Vereint schreiten wir in die Zukunft.",
        "Die Einheit des Volkes ist sein größter Reichtum.",
        "Gemeinsam können wir jedes Hindernis überwinden."
    ],
    "msgES": [
        "La unidad es fuerza.",
        "Somos un solo corazón.",
        "Juntos, somos invencibles.",
        "La armonía trae grandeza.",
        "Nuestra fuerza proviene de nuestra unidad.",
        "Unidos, avanzamos hacia el futuro.",
        "La unidad del pueblo es su mayor riqueza.",
        "Juntos, podemos superar cualquier obstáculo."
    ],
    "msgIT": [
        "L'unità è forza.",
        "Siamo un solo cuore.",
        "Insieme, siamo invincibili.",
        "L'armonia porta grandezza.",
        "La nostra forza deriva dalla nostra unità.",
        "Uniti, ci muoviamo verso il futuro.",
        "L'unità del popolo è la sua più grande ricchezza.",
        "Insieme, possiamo superare ogni ostacolo."
    ],
    "msgPT": [
        "Unidade é força.",
        "Somos um só coração.",
        "Juntos, somos invencíveis.",
        "Harmonia traz grandeza.",
        "Nossa força vem da nossa unidade.",
        "Unidos, avançamos para o futuro.",
        "A unidade do povo é sua maior riqueza.",
        "Juntos, podemos superar qualquer obstáculo."
    ]
}
