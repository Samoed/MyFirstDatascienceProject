import copy
import json
import os
import pickle
import sys
from collections import defaultdict, deque

import cv2
import mediapipe as mp
import numpy as np
from pynput import keyboard
from pynput.mouse import Button, Controller
from PySide6 import QtGui
from PySide6.QtCore import QObject, QPoint, QPointList, Qt, QThread, Signal, Slot
from PySide6.QtGui import QDesktopServices, QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

import process_keyboard.keyboard_press
from app import (
    calc_bounding_rect,
    calc_landmark_list,
    draw_info_text,
    draw_point_history,
)
from process_keyboard.keyboard_press import press_keyboard
from process_keyboard.read_keyboard import ReadKeyboard
from ui import Ui_MainWindow

mouse = Controller()


class Thread(QThread):
    update_frame = Signal(QImage)
    activate_key = Signal(str)
    mouse_move = Signal(str, QPointList)

    def __init__(self, parent: QObject | None = None):
        QThread.__init__(self, parent)
        self.trained_file = None
        self.status = True
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
        self.point_history = QPointList()

        # Finger gesture history ################################################
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
        self.mouse_ids = [0, 1, 11]
        with open("model.pkl", "rb") as f:
            self.model = pickle.load(f)

    def draw_image(self, image: np.ndarray) -> None:
        h, w, ch = image.shape
        img = QImage(image.data, w, h, ch * w, QImage.Format_RGB888)
        scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)
        self.update_frame.emit(scaled_img)

    def run(self) -> None:
        cap = cv2.VideoCapture(1)
        start_mouse_x, start_mouse_y = mouse.position
        print(start_mouse_x, start_mouse_y)
        self.point_history.append(QPoint(0, 0))

        while self.status:
            ret, image = cap.read()
            if not ret:
                break
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            debug_image = copy.deepcopy(image)
            image.flags.writeable = False
            results = self.hands.process(image)
            image.flags.writeable = True

            if results.multi_hand_landmarks is None:
                self.point_history.append(QPoint(0, 0))
                # debug_image = draw_point_history(debug_image, self.point_history)
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
                max_score = max(self.model.predict_proba(landmark_list)[0])
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
                print(max_score, hand_sign_id, self.labels[hand_sign_id])
                if max_score < 0.6:
                    debug_image = draw_point_history(debug_image, self.point_history)
                    self.draw_image(debug_image)
                    continue

                if hand_sign_id in self.mouse_ids:
                    image_width, image_height = image.shape[1], image.shape[0]

                    landmark_x = min(int(hand_landmarks.landmark[8].x * image_width), image_width - 1)
                    landmark_y = min(int(hand_landmarks.landmark[8].y * image_height), image_height - 1)
                    self.point_history.append(QPoint(landmark_x, landmark_y))
                    self.mouse_move.emit(self.labels[hand_sign_id], self.point_history)
                else:
                    self.point_history.append(QPoint(0, 0))
                    self.activate_key.emit(self.labels[hand_sign_id])

                debug_image = draw_point_history(debug_image, self.point_history)
                self.draw_image(debug_image)
            if len(self.point_history) > self.history_length:
                self.point_history.removeFirst(len(self.point_history) - self.history_length)

        self.cap.release()
        cv2.destroyAllWindows()
        sys.exit(-1)


class MainWindow(QMainWindow):
    file_name = "keymap.json"
    prev_label = None
    mouse_move = False

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.update_frame.connect(self.set_image)
        self.th.activate_key.connect(self.process_key)
        self.th.mouse_move.connect(self.process_mouse)

        self.ui.start_button.clicked.connect(self.start)
        self.ui.stop_button.clicked.connect(self.kill_thread)
        self.ui.stop_button.setEnabled(False)

        self.ui.one_combobox.currentTextChanged.connect(
            lambda text: self.combo_changed(text, combo_name="one_combobox")
        )
        self.ui.l_combobox.currentTextChanged.connect(lambda text: self.combo_changed(text, combo_name="l_combobox"))
        self.ui.two_fingers_near_combobox.currentTextChanged.connect(
            lambda text: self.combo_changed(text, combo_name="two_fingers_near_combobox")
        )

        self.key_values: dict[str, list[keyboard.Key | keyboard.KeyCode]] = defaultdict(list)
        self.mouse_values: dict[str, str] = {}
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
        self.process_buttons()
        self.read_config()

    @Slot()
    def kill_thread(self) -> None:
        print("Finishing...")
        self.ui.stop_button.setEnabled(False)
        self.ui.start_button.setEnabled(True)
        self.th.status = False
        self.th.wait()  # Wait for the thread to finish

    @Slot()
    def start(self) -> None:
        print("Starting...")
        self.ui.start_button.setEnabled(False)
        self.ui.stop_button.setEnabled(True)

        self.th.start()

    def process_buttons(self) -> None:
        for button in self.gesture_buttons:
            button.pressed.connect(lambda b=button: button_hook(b, self))

    @Slot(QImage)
    def set_image(self, image: QImage):
        self.ui.label_5.setPixmap(QPixmap.fromImage(image))

    def action_mouse(self, label: str, is_start: bool = True) -> None:
        action = self.mouse_values.get(label, None)
        if action is None:
            return
        # TODO create enum for actions
        match action:
            case "Mouse move":
                return
            case "Left mouse (LMB)":
                button = Button.left
            case "Right mouse":
                button = Button.right
            case _:
                return
        if is_start:
            mouse.press(button)
        else:
            mouse.release(button)

    @Slot(str)
    def process_key(self, label: str):
        if self.prev_label in self.mouse_gestures:
            self.action_mouse(self.prev_label, is_start=False)

        print(label)
        print(self.key_values[label])
        self.mouse_move = False

        if self.prev_label == label or len(self.key_values[label]) == 0:
            self.prev_label = label
            return
        self.prev_label = label
        try:
            press_keyboard(self.key_values[label])
        except TypeError as e:
            print(e)

    @Slot(str, QPointList)
    def process_mouse(self, label: str, point_history: QPointList) -> None:
        print(label)
        # a = QtGui.QScreen.availableGeometry(self)
        # QtGui.QGuiApplication.primaryScreen().size()
        # QtGui.QGuiApplication.screens()[1].geometry()
        # height
        # width
        if self.prev_label != label:
            if self.prev_label in self.mouse_gestures:
                self.action_mouse(self.prev_label, is_start=False)
            if label in self.mouse_gestures:
                self.action_mouse(label)
        action = self.mouse_values.get(label, "None")
        if (
            action != "None"
            and len(point_history) > 2
            and (point_history[-1].x() + point_history[-1].y()) != 0
            and (point_history[-2].x() + point_history[-2].y()) != 0
        ):
            diff_x = point_history[-1].x() - point_history[-2].x()
            diff_y = point_history[-1].y() - point_history[-2].y()
            print(diff_x, diff_y)
            mouse.move(diff_x, diff_y)
        # print(self.mouse_values[label])
        # if self.mouse_values[label] == [''] or self.prev_label == label:
        #     return
        # process_keyboard.keyboard_press.press_mouse(self.key_values[label])
        self.prev_label = label

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        # TODO mouse
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

    def combo_changed(self, text: str, combo_name: str) -> None:
        name = "_".join(combo_name.split("_")[:-1])
        self.mouse_values[name] = text

    def read_config(self) -> None:
        if not os.path.exists(self.file_name):
            return
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                keymap = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            print("Error reading config")
            return
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
    new_key_combo = ReadKeyboard().read()
    new_text = keys_to_str(new_key_combo)
    button.setText(new_text)
    gesture = "_".join(button.objectName().split("_")[:-1])
    app_window.key_values[gesture] = new_key_combo


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
