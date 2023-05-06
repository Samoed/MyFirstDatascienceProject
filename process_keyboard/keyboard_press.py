from pynput import keyboard

keyboard_controller = keyboard.Controller()


def press_keyboard(keys: list[keyboard.Key | keyboard.KeyCode]) -> None:
    for key in keys[:-1]:
        keyboard_controller.press(key)
    keyboard_controller.tap(keys[-1])
    for key in keys[:-1]:
        keyboard_controller.release(key)
