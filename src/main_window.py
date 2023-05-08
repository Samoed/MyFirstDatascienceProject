import json
import os
from collections import defaultdict

from pynput import keyboard
from PySide6 import QtGui
from PySide6.QtCore import QPointList, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow

from src.dialog_window import DialogWindow
from src.process_keyboard.keyboard_press import button_hook, keys_to_str, press_keyboard
from src.process_mouse.move_mouse import action_mouse, move_mouse
from src.thread import Thread
from src.ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    prev_label = None

    def __init__(self, file_name: str) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_name = file_name

        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.update_frame.connect(self.set_image)
        self.th.activate_key.connect(self.process_key)
        self.th.mouse_move.connect(self.process_mouse)
        self.th.update_label.connect(self.update_label)

        self.ui.one_combobox.currentTextChanged.connect(
            lambda text: self.combo_changed(text, combo_name="one_combobox")
        )
        self.ui.l_combobox.currentTextChanged.connect(lambda text: self.combo_changed(text, combo_name="l_combobox"))
        self.ui.two_fingers_near_combobox.currentTextChanged.connect(
            lambda text: self.combo_changed(text, combo_name="two_fingers_near_combobox")
        )

        self.ui.profile_combobox.currentTextChanged.connect(self.change_profile)
        self.ui.add_profile_button.clicked.connect(self.add_profile)

        self.key_values: dict[str, dict[str, list[keyboard.Key | keyboard.KeyCode]]] = {"default": defaultdict(list)}
        self.mouse_values: dict[str, dict[str, str]] = {"default": {}}
        self.mouse_gestures = [
            "two_fingers_near",
            "one",
            "l",
        ]
        self.gesture_buttons = [
            self.ui.two_button,
            self.ui.three_button,
            self.ui.four_button,
            self.ui.five_button,
            self.ui.ok_button,
            self.ui.c_button,
            self.ui.heavy_button,
            self.ui.hang_button,
            self.ui.palm_button,
            self.ui.like_button,
            self.ui.dislike_button,
        ]
        self.mouse_comboboxes = [
            self.ui.two_fingers_near_combobox,
            self.ui.one_combobox,
            self.ui.l_combobox,
        ]
        self.current_profile: str = "default"
        self.process_buttons()
        self.read_config()
        self.start()

    @Slot()
    def update_label(self):
        self.prev_label = None

    def change_profile(self, profile_name: str):
        self.current_profile = profile_name
        if profile_name not in self.mouse_values:
            self.mouse_values[profile_name] = {}
            self.key_values[profile_name] = defaultdict(list)
        self.update_gestures_text()

    def kill_thread(self) -> None:
        print("Finishing...")
        self.th.status = False
        self.th.wait()  # Wait for the thread to finish

    def start(self) -> None:
        print("Starting...")
        self.th.start()

    def process_buttons(self) -> None:
        for button in self.gesture_buttons:
            button.pressed.connect(lambda b=button: button_hook(b, self))

    @Slot(QImage)
    def set_image(self, image: QImage):
        self.ui.label_5.setPixmap(QPixmap.fromImage(image))

    @Slot(str)
    def process_key(self, label: str):
        if self.prev_label in self.mouse_gestures:
            action_mouse(self.mouse_values[self.current_profile], self.prev_label, is_start=False)

        print(label)
        print(self.key_values[self.current_profile][label])

        if self.prev_label == label or len(self.key_values[self.current_profile][label]) == 0:
            self.prev_label = label
            return
        self.prev_label = label
        try:
            press_keyboard(self.key_values[self.current_profile][label])
        except Exception as err:
            print(err)

    def add_profile(self):
        dlg = DialogWindow(self)
        if dlg.exec():
            text = dlg.ui.textEdit.toPlainText()
            self.ui.profile_combobox.addItem(text)
            self.ui.profile_combobox.setCurrentText(text)

    @Slot(str, QPointList)
    def process_mouse(self, label: str, point_history: QPointList) -> None:
        print(label)

        if self.prev_label != label:
            if self.prev_label in self.mouse_gestures:
                action_mouse(self.mouse_values[self.current_profile], self.prev_label, is_start=False)
            if label in self.mouse_gestures:
                action_mouse(self.mouse_values[self.current_profile], label)
        move_mouse(self.mouse_values[self.current_profile], point_history, label)
        self.prev_label = label

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.kill_thread()
        result_dict = {}
        for profile, keymap in self.key_values.items():
            result_dict[profile] = {}
            for gesture, keys in keymap.items():
                keys_str = []
                for key in keys:
                    match type(key):
                        case keyboard.Key:
                            keys_str.append(key.name)
                        case keyboard.KeyCode:
                            keys_str.append(key.char)
                result_dict[profile][gesture] = "+".join(keys_str)

        for profile, mouse_keymap in self.mouse_values.items():
            for gesture, mouse in mouse_keymap.items():
                result_dict[profile][gesture] = mouse

        json_string = json.dumps(result_dict)
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write(json_string)

    def combo_changed(self, text: str, combo_name: str) -> None:
        name = "_".join(combo_name.split("_")[:-1])
        self.mouse_values[self.current_profile][name] = text

    def read_config(self) -> None:
        if not os.path.exists(self.file_name):
            return
        try:
            with open(self.file_name, encoding="utf-8") as f:
                keymap = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            print("Error reading config")
            return

        for profile, keymap_val in keymap.items():
            keyboard_val, mouse_val = self.read_keymap(keymap_val)
            self.key_values[profile] = keyboard_val
            self.mouse_values[profile] = mouse_val

        self.ui.profile_combobox.removeItem(0)
        self.ui.profile_combobox.addItems(list(keymap.keys()))
        self.ui.profile_combobox.setCurrentText(list(self.key_values.keys())[0])
        self.update_gestures_text()
        print(self.key_values)

    def read_keymap(
        self, keymap_json: dict[str, str]
    ) -> tuple[dict[str, list[keyboard.KeyCode | keyboard.Key]], dict[str, str]]:
        keys = keyboard.Key.__members__.keys()
        key_values: dict[str, list[keyboard.Key | keyboard.KeyCode]] = defaultdict(list)
        mouse_values = {}
        for gesture, keymap_val in keymap_json.items():
            # TODO check if gesture is valid
            if gesture in self.mouse_gestures:
                mouse_values[gesture] = keymap_val
                continue
            for key in keymap_val.split("+"):
                if key == "":
                    continue
                if key in keys:
                    key_values[gesture].append(keyboard.Key[key])  # Key
                else:
                    key_values[gesture].append(keyboard.KeyCode.from_char(key))
        return key_values, mouse_values

    def update_gestures_text(self):
        self.update_buttons_text(self.key_values.get(self.current_profile, {}))
        self.update_como_text(self.mouse_values.get(self.current_profile, {}))

    def update_buttons_text(self, keymap: dict[str, list[keyboard.Key | keyboard.KeyCode]]):
        for button in self.gesture_buttons:
            button_gesture_name = "_".join(button.objectName().split("_")[:-1])
            if button_gesture_name in keymap and keymap[button_gesture_name] != "":
                button.setText(keys_to_str(keymap[button_gesture_name]))
            else:
                button.setText("Press button, then key")

    def update_como_text(self, keymap: dict[str, str]):
        for combo in self.mouse_comboboxes:
            button_gesture_name = "_".join(combo.objectName().split("_")[:-1])
            if button_gesture_name in keymap and keymap[button_gesture_name] != "":
                combo.setCurrentText(keymap[button_gesture_name])
            else:
                combo.setCurrentText("None")
