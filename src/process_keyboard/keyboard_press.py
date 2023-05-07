from typing import TYPE_CHECKING

from pynput import keyboard
from PySide6.QtWidgets import QPushButton

from src.process_keyboard.read_keyboard import ReadKeyboard

if TYPE_CHECKING:
    from src.main_window import MainWindow

keyboard_controller = keyboard.Controller()


def press_keyboard(keys: list[keyboard.Key | keyboard.KeyCode]) -> None:
    for key in keys[:-1]:
        keyboard_controller.press(key)
    keyboard_controller.tap(keys[-1])
    for key in keys[:-1]:
        keyboard_controller.release(key)


def button_hook(button: QPushButton, app_window: "MainWindow") -> None:
    new_key_combo = ReadKeyboard().read()
    new_text = keys_to_str(new_key_combo)
    button.setText(new_text)
    gesture = "_".join(button.objectName().split("_")[:-1])
    app_window.key_values[app_window.current_profile][gesture] = new_key_combo


def keys_to_str(keycodes: list[keyboard.Key | keyboard.KeyCode]) -> str:
    result = []
    for key in keycodes:
        match type(key):
            case keyboard.Key:
                result.append(key.name)
            case keyboard.KeyCode:
                result.append(key.char)
    return "+".join(result)
