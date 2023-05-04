from pynput import keyboard


class ReadKeyboard:
    pressed_key: list[keyboard.Key | keyboard.KeyCode] = []
    modifier_key: list[keyboard.Key] = [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt_gr,
                                        keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.cmd,
                                        keyboard.Key.cmd_l, keyboard.Key.cmd_r]

    def on_press(self, key: keyboard.Key) -> None:
        self.pressed_key.append(key)

    def on_release(self, key: keyboard.Key) -> bool:
        return False
        # return key in self.modifier_key:

    def read(self) -> list[keyboard.Key]:
        return self.pressed_key

    def __init__(self) -> None:
        self.pressed_key = []
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        print(self.pressed_key)