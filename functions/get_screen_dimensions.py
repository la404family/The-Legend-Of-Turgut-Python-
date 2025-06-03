# Calculer la taille de l'ecran
import tkinter as tk

# Calculer la taille de l'écran et ajuster les dimensions


def get_screen_dimensions():
    root = tk.Tk()
    try:
        # Obtenir la taille totale de l'écran
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()  # Fermer la fenêtre tkinter
        # Soustraire 5 pixels de chaque dimension
        WIDTH = max(screen_width - 100, 1)  # Au moins 1 pixel
        HEIGHT = max(screen_height - 100, 1)  # Au moins 1 pixel
    except Exception as e:
        print(f"Error getting screen dimensions: {e}")
        # En cas d'erreur, utiliser des dimensions par défaut
        root.destroy()

        WIDTH, HEIGHT = 800, 450
    return WIDTH, HEIGHT
