import pygame

# Récuperation des événements du joystick


class JoystickEventHandler:
    def __init__(self):
        self.joystick = None
        self.axis_values = {}

    def init_joystick(self):
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick initialized: {self.joystick.get_name()}")

    def on_axis_event(self, event):
        self.axis_values[event.axis] = event.value
        print(f"Axis {event.axis} value: {event.value}")

    def on_button_event(self, event):
        print(
            f"Button {event.button} {'pressed' if event.type == pygame.JOYBUTTONDOWN else 'released'}")


JoystickEventHandler = JoystickEventHandler()
JoystickEventHandler.init_joystick()
