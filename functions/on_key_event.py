import keyboard


def on_key_event(event):
    if keyboard.on_press():
        print(f"Touche : {event.name}, Code : {event.scan_code}")
