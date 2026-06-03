import evdev
from evdev import InputDevice, categorize, ecodes

# Находим путь к джойстику
devices = [InputDevice(path) for path in evdev.list_devices()]
joystick = None
for dev in devices:
    if "Logitech" in dev.name: # Ищем наш Logitech
        joystick = dev
        break

if not joystick:
    print("Джойстик не найден!")
    exit()

print(f"Подключен: {joystick.name}")

try:
    for event in joystick.read_loop():
        if event.type == ecodes.EV_ABS:  # Если это движение стика (абсолютная ось)
            print(f"Ось {event.code}: {event.value}")
        elif event.type == ecodes.EV_KEY: # Если это кнопка
            print(f"Кнопка {event.code}: {event.value}")
except KeyboardInterrupt:
    print("\nТест завершен.")