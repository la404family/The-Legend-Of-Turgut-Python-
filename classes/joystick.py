import pygame
import sys

# Initialisation de pygame
pygame.init()


class JoystickEventHandler:
    def __init__(self):
        self.joystick = None
        self.axis_values = {}
        self.button_states = {}

    def init_joystick(self):
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Manette détectée: {self.joystick.get_name()}")
            print(f"Nombre d'axes: {self.joystick.get_numaxes()}")
            print(f"Nombre de boutons: {self.joystick.get_numbuttons()}")

            # Initialiser les valeurs des axes
            for i in range(self.joystick.get_numaxes()):
                self.axis_values[i] = 0.0

            # Initialiser les états des boutons
            for i in range(self.joystick.get_numbuttons()):
                self.button_states[i] = False
        else:
            print("Aucune manette détectée!")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Gestion des axes
            elif event.type == pygame.JOYAXISMOTION:
                self.axis_values[event.axis] = event.value
                print(f"Axe {event.axis}: {event.value:.2f}")

            # Gestion des boutons
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_states[event.button] = True
                print(f"Bouton {event.button} pressé")
            elif event.type == pygame.JOYBUTTONUP:
                self.button_states[event.button] = False
                print(f"Bouton {event.button} relâché")

        return True


# Création de l'instance
joystick_handler = JoystickEventHandler()
joystick_handler.init_joystick()
