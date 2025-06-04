import keyboard


def on_key_event(event):
    print(f"Touche : {event.name}, Code : {event.scan_code}")


keyboard.on_press(on_key_event)
