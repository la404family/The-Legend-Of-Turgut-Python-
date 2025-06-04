import keyboard


class KeyEventHandler:
    def __init__(self):
        self.event_scan_code = None

    def on_key_event(self, event):
        self.event_scan_code = event.scan_code


handler = KeyEventHandler()
keyboard.on_press(handler.on_key_event)
"""
La fonction on_key_event est appelée à chaque fois qu'une touche est pressée.
Voici les codes des touches pour les claviers AZERTY  :
Pour LES MOUVEMENTS : 
Touche : q, Code : 30  -- Gauche
Touche : d, Code : 32  -- Droite
Touche : z, Code : 17  -- Haut
Touche : s, Code : 31  -- Bas
Pour LES ACTIONS :
Touche : u, Code : 22   -- touche X
Touche : i, Code : 23   -- touche B
Touche : o, Code : 24   -- touche A
Touche : p, Code : 25   -- touche Y
Touche : j, Code : 36   -- touche L
Touche : k, Code : 37   -- touche R
Touche : l, Code : 38   -- touche M
Touche : m, Code : 39   -- touche N
Pour LES TOUCHES DE FONCTION :
Touche : enter, Code : 28
Touche : espace, Code : 57
Touche : ctrl, Code : 29
Touche : maj, Code : 42
Touche : x, Code : 45
Touche : tab, Code : 15
Pour LES TOUCHES Numériques :
Touche : &, Code : 2
Touche : é, Code : 3
Touche : ", Code : 4
Touche : ', Code : 5
Touche : (, Code : 6
Pour le PAVÉ NUMÉRIQUE :
Touche : 0, Code : 82
Touche : 1, Code : 79
Touche : 2, Code : 80
Touche : 3, Code : 81
Touche : 4, Code : 75
Touche : 5, Code : 76
Touche : 6, Code : 77
Touche : 7, Code : 71
Touche : 8, Code : 72
Touche : 9, Code : 73
"""
