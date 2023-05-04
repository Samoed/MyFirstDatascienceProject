import copy
import json
import os
import pickle
import sys
import time
from collections import defaultdict, deque

import cv2
import mediapipe as mp
from pynput import keyboard
from pynput.mouse import Controller
from PySide6 import QtGui
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

import read_keyboard as app_setup
from app import (
    calc_bounding_rect,
    calc_landmark_list,
    draw_info_text,
    draw_point_history,
)
from ru_eng_keycodes import ru_eng_keycodes
from ui import Ui_MainWindow

mouse = Controller()


class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.trained_file = None
        self.status = True
        self.cap = None
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )
        self.mp_drawings = mp.solutions.drawing_utils

        # Coordinate history #################################################################
        self.history_length = 16
        self.point_history = deque(maxlen=self.history_length)

        # Finger gesture history ################################################
        self.finger_gesture_history = deque(maxlen=self.history_length)
        self.labels = [
            "two_fingers_near",
            "one",
            "two",
            "three",
            "four",
            "five",
            "ok",
            "c",
            "heavy",
            "hang",
            "palm",
            "l",
            "like",
            "dislike",
        ]
        with open("model.pkl", "rb") as f:
            self.model = pickle.load(f)

    def draw_image(self, image):
        h, w, ch = image.shape
        img = QImage(image.data, w, h, ch * w, QImage.Format_RGB888)
        scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)
        self.updateFrame.emit(scaled_img)

    def run(self):
        self.cap = cv2.VideoCapture(1)
        start_mouse_x, start_mouse_y = mouse.position
        print(start_mouse_x, start_mouse_y)

        while self.status:
            ret, image = self.cap.read()
            if not ret:
                break
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            debug_image = copy.deepcopy(image)
            image.flags.writeable = False
            results = self.hands.process(image)
            image.flags.writeable = True

            if results.multi_hand_landmarks is None:
                self.point_history.append([0, 0])
                debug_image = draw_point_history(debug_image, self.point_history)
                self.draw_image(debug_image)
                continue

            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # if handedness.classification[0].label == "Right":
                #     test_image = copy.deepcopy(image)
                #     test_image = cv2.flip(test_image, 1)
                #     mirrored_result = self.hands.process(test_image)
                #     hand_landmarks = mirrored_result.multi_hand_landmarks[0]

                # Bounding box calculation
                brect = calc_bounding_rect(debug_image, hand_landmarks)
                # Landmark calculation
                landmark_list = calc_landmark_list(hand_landmarks).reshape(1, -1)

                # Hand sign classification
                hand_sign_id = int(self.model.predict(landmark_list)[0])
                print(hand_sign_id)

                # Drawing part
                # debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                self.mp_drawings.draw_landmarks(
                    debug_image, results.multi_hand_landmarks[0], self.mp_hands.HAND_CONNECTIONS
                )
                debug_image = draw_info_text(
                    debug_image,
                    brect,
                    handedness,
                    self.labels[hand_sign_id],
                    "",
                )

            debug_image = draw_point_history(debug_image, self.point_history)
            self.draw_image(debug_image)
        self.cap.release()
        cv2.destroyAllWindows()
        sys.exit(-1)


class MainWindow(QMainWindow):
    file_name = "keymap.json"

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.set_image)

        self.ui.start_button.clicked.connect(self.start)
        self.ui.stop_button.clicked.connect(self.kill_thread)
        self.ui.stop_button.setEnabled(False)

        self.key_values: dict[str, list[keyboard.Key | keyboard.KeyCode]] = defaultdict(list)
        self.mouse_combo = [
            self.ui.two_fingers_combobox,
            self.ui.one_combobox,
            self.ui.l_combobox,
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
        self.process_buttons()
        self.read_config()

    @Slot()
    def kill_thread(self):
        print("Finishing...")
        self.ui.stop_button.setEnabled(False)
        self.ui.start_button.setEnabled(True)
        self.th.status = False
        self.th.wait()  # Wait for the thread to finish

    @Slot()
    def start(self):
        print("Starting...")
        self.ui.start_button.setEnabled(False)
        self.ui.stop_button.setEnabled(True)

        self.th.start()

    def process_buttons(self) -> None:
        for button in self.gesture_buttons:
            button.pressed.connect(lambda b=button: button_hook(b, self))

    @Slot(QImage)
    def set_image(self, image):
        self.ui.label_5.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        result_dict = {}
        for gesture, keys in self.key_values.items():
            keys_str = []
            # keys_vk = []
            for key in keys:
                match type(key):
                    case keyboard.Key:
                        keys_str.append(key.name)
                    case keyboard.KeyCode:
                        keys_str.append(key.char)
                        # keys_vk.append(key.vk)  # TODO test vk?
            result_dict[gesture] = "+".join(keys_str)
        # TODO dump all keymap
        json_string = json.dumps(result_dict)
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write(json_string)
        self.kill_thread()

    def read_config(self):
        if not os.path.exists(self.file_name):
            return
        with open(self.file_name, "r", encoding="utf-8") as f:
            keymap = json.loads(f.read())
        keys = keyboard.Key.__members__.keys()
        for gesture, keymap_val in keymap.items():
            # TODO check if gesture is valid
            for key in keymap_val.split("+"):
                if key in keys:
                    self.key_values[gesture].append(keyboard.Key[key])  # Key
                else:
                    self.key_values[gesture].append(keyboard.KeyCode.from_char(key))
        for button in self.gesture_buttons:
            if button.objectName() in keymap:
                button.setText(keymap[button.objectName()])
        # for combo in self.mouse_combo:
        #     combo.setText(keymap.get(combo.objectName(), "Press button, then key"))
        print(self.key_values)


def button_hook(button: QPushButton, app_window: MainWindow) -> None:
    # print(button.objectName())
    new_key_combo = app_setup.ReadKeyboard().read()
    new_text = keys_to_str(new_key_combo)
    button.setText(new_text)
    app_window.key_values[button.objectName()] = new_key_combo


def keys_to_str(keycodes: list[keyboard.Key | keyboard.KeyCode]) -> str:
    result = []
    for key in keycodes:
        match type(key):
            case keyboard.Key:
                result.append(key.name)
            case keyboard.KeyCode:
                result.append(key.char)
    return "+".join(result)


if __name__ == "__main__":
    app = QApplication()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
