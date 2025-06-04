import pygame
import ctypes
import locale

from functions.settings import *


def get_keyboard_type():
    """ Detects the keyboard type based on the system locale and returns it.
    Returns:
        str: The type of keyboard ('azerty', 'qwerty', 'qwertz', or 'unknown').
    """

    # Fichier config.py
    KEY_CONFIGS = {
        'AZERTY': {
            'up': 'z',
            'left': 'q',
            'down': 's',
            'right': 'd'
        },
        'QWERTY': {
            'up': 'w',
            'left': 'a',
            'down': 's',
            'right': 'd'
        }
    }
    try:
        # Get the current locale
        loc = locale.getdefaultlocale()[0]
        if loc is None:
            print("Locale is None, cannot determine keyboard type.")
            return "unknown"

        # Check for specific keyboard layouts
        if loc.startswith("fr_"):
            print("Detected French keyboard layout.")
            KEY_CONFIGS['current'] = KEY_CONFIGS['AZERTY']
            return "azerty"
        elif loc.startswith("en_") or loc.startswith("us_"):
            print("Detected English keyboard layout.")
            KEY_CONFIGS['current'] = KEY_CONFIGS['QWERTY']
            return "qwerty"
        else:
            KEY_CONFIGS['current'] = KEY_CONFIGS['QWERTY']
            print(f"Detected keyboard layout: {loc}. Defaulting to QWERTY.")
            return "qwerty"
    except Exception as e:
        print(f"Error detecting keyboard type: {e}")
        return "unknown"
