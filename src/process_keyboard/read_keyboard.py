from pynput import keyboard

from src.process_keyboard.ru_eng_keycodes import ru_eng_keycodes


class ReadKeyboard:
    pressed_key: list[keyboard.Key | keyboard.KeyCode] = []
    modifier_key: list[keyboard.Key] = [
        keyboard.Key.alt,
        keyboard.Key.alt_l,
        keyboard.Key.alt_r,
        keyboard.Key.alt_gr,
        keyboard.Key.ctrl,
        keyboard.Key.ctrl_l,
        keyboard.Key.ctrl_r,
        keyboard.Key.cmd,
        keyboard.Key.cmd_l,
        keyboard.Key.cmd_r,
    ]

    def __init__(self) -> None:
        self.pressed_key = []
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:  # type: ignore[arg-type]
            listener.join()
        print(self.pressed_key)

    def on_press(self, key: keyboard.Key | keyboard.KeyCode) -> None:
        self.pressed_key.append(key)

    def on_release(self, key: keyboard.Key) -> bool:
        return False
        # return key in self.modifier_key:

    def read(self) -> list[keyboard.Key | keyboard.KeyCode]:
        for i in range(len(self.pressed_key)):
            if type(self.pressed_key[i]) is keyboard.KeyCode:
                self.pressed_key[i] = ru_eng_keycodes.get(self.pressed_key[i].char, self.pressed_key[i])  # type: ignore
        return self.pressed_key
