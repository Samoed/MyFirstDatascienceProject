import copy
import pickle
import sys
import time
from collections import deque

import cv2
import mediapipe as mp
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton)
from pynput import keyboard
from pynput.mouse import Controller

import read_keyboard as app_setup
from app_test import (calc_bounding_rect, calc_landmark_list, draw_info_text, draw_point_history, )
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
        self.labels = ['two_fingers_near', 'one', 'two', 'three', 'four', 'five', 'ok', 'c', 'heavy', 'hang', 'palm',
                       'l',
                       'like', 'dislike']
        with open("model.pkl", "rb") as f:
            self.model = pickle.load(f)

    def run(self):
        self.cap = cv2.VideoCapture(1)
        start_mouse_x, start_mouse_y = mouse.position
        print(start_mouse_x, start_mouse_y)

        while self.status:

            # Camera capture #####################################################
            ret, image = self.cap.read()
            if not ret:
                break
            image = cv2.flip(image, 1)  # Mirror display
            debug_image = copy.deepcopy(image)

            # Detection implementation #############################################################
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            image.flags.writeable = False
            results = self.hands.process(image)
            image.flags.writeable = True

            if results.multi_hand_landmarks is None:
                self.point_history.append([0, 0])
                debug_image = draw_point_history(debug_image, self.point_history)
                debug_image = cv2.cvtColor(debug_image, cv2.COLOR_RGB2BGR)
                h, w, ch = debug_image.shape
                img = QImage(debug_image.data, w, h, ch * w, QImage.Format_RGB888)
                scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)
                self.updateFrame.emit(scaled_img)
                continue

            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Bounding box calculation
                brect = calc_bounding_rect(debug_image, hand_landmarks)
                # Landmark calculation
                landmark_list = calc_landmark_list(debug_image, hand_landmarks).reshape(1, -1)

                # Hand sign classification
                hand_sign_id = int(self.model.predict(landmark_list)[0])
                print(hand_sign_id)

                # Drawing part
                # debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                self.mp_drawings.draw_landmarks(
                    debug_image,
                    results.multi_hand_landmarks[0],
                    self.mp_hands.HAND_CONNECTIONS
                )
                debug_image = draw_info_text(
                    debug_image,
                    brect,
                    handedness,
                    self.labels[hand_sign_id],
                    "",
                )

            debug_image = draw_point_history(debug_image, self.point_history)

            # Screen reflection #############################################################
            # cv2.imshow("Hand Gesture Recognition", debug_image)
            # Creating and scaling QImage
            h, w, ch = debug_image.shape
            debug_image = cv2.cvtColor(debug_image, cv2.COLOR_RGB2BGR)
            img = QImage(debug_image.data, w, h, ch * w, QImage.Format_RGB888)
            scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)

            # Emit signal
            self.updateFrame.emit(scaled_img)
        sys.exit(-1)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        self.ui.start_button.clicked.connect(self.start)
        self.ui.stop_button.clicked.connect(self.kill_thread)
        self.ui.stop_button.setEnabled(False)

        self.key_values: dict[str, list[keyboard.Key | keyboard.KeyCode]] = {}
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
            self.ui.dislike_button
        ]
        self.process_buttons()

    @Slot()
    def kill_thread(self):
        print("Finishing...")
        self.ui.stop_button.setEnabled(False)
        self.ui.start_button.setEnabled(True)
        self.th.cap.release()
        cv2.destroyAllWindows()
        self.status = False
        self.th.terminate()
        # Give time for the thread to finish
        time.sleep(1)

    @Slot()
    def start(self):
        print("Starting...")
        self.ui.start_button.setEnabled(True)
        self.ui.stop_button.setEnabled(False)

        # self.th.set_file(self.combobox.currentText())
        self.th.start()

    def process_buttons(self) -> None:
        for button in self.gesture_buttons:
            button.pressed.connect(lambda b=button: button_hook(b, self))

    @Slot(QImage)
    def setImage(self, image):
        self.ui.label_5.setPixmap(QPixmap.fromImage(image))


def button_hook(button: QPushButton, app: MainWindow) -> None:
    # print(button.objectName())
    new_key_combo = app_setup.ReadKeyboard().pressed_key
    new_text = ""
    for key in new_key_combo[:-1]:
        new_text += key.name + "+"
    button.setText(new_text + new_key_combo[-1].char)
    app.key_values[button.objectName()] = new_key_combo


if __name__ == "__main__":
    app = QApplication()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
