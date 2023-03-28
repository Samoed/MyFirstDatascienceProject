import copy
import csv
import sys
import time
from collections import Counter, deque

import cv2
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)
import mediapipe as mp

from app import (calc_bounding_rect, calc_landmark_list, draw_bounding_rect, draw_info, draw_info_text, draw_landmarks,
                 draw_point_history, logging_csv,
                 pre_process_landmark,
                 pre_process_point_history, select_mode, )
from model.keypoint_classifier.keypoint_classifier import KeyPointClassifier
from model.point_history_classifier.point_history_classifier import PointHistoryClassifier
from ui import Ui_MainWindow
from pynput.mouse import Button, Controller

mouse = Controller()


class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.trained_file = None
        self.status = True
        self.cap = True
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )

        self.keypoint_classifier = KeyPointClassifier()

        self.point_history_classifier = PointHistoryClassifier()

        # Read labels ###########################################################
        with open("model/keypoint_classifier/keypoint_classifier_label.csv", encoding="utf-8-sig") as f:
            keypoint_classifier_labels = csv.reader(f)
            self.keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]
        with open(
                "model/point_history_classifier/point_history_classifier_label.csv",
                encoding="utf-8-sig",
        ) as f:
            point_history_classifier_labels = csv.reader(f)
            self.point_history_classifier_labels = [row[0] for row in point_history_classifier_labels]

        # Coordinate history #################################################################
        self.history_length = 16
        self.point_history = deque(maxlen=self.history_length)

        # Finger gesture history ################################################
        self.finger_gesture_history = deque(maxlen=self.history_length)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        start_mouse_x, start_mouse_y = mouse.position
        print(start_mouse_x, start_mouse_y)
        use_brect = True
        mode = 0

        while self.status:
            # key = cv2.waitKey(10)
            # if key == 27:  # ESC
            #     break
            # number, mode = select_mode(key, mode)

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
                # debug_image = draw_info(debug_image, mode, number)
                # cv2.imshow("Hand Gesture Recognition", debug_image)
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
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                pre_processed_point_history_list = pre_process_point_history(debug_image, self.point_history)
                # Write to the dataset file
                # logging_csv(
                #     number,
                #     mode,
                #     pre_processed_landmark_list,
                #     pre_processed_point_history_list,
                # )

                # Hand sign classification
                hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list)
                if hand_sign_id == 2:  # Point gesture
                    self.point_history.append(landmark_list[8])
                    if len(self.point_history) > 2 and self.point_history[-1][0] != 0 and self.point_history[-2][0] != 0 and \
                            self.point_history[-1][1] != 0 and self.point_history[-2][1] != 0:
                        start_mouse_x += self.point_history[-1][0] - self.point_history[-2][0]
                        start_mouse_y += self.point_history[-1][1] - self.point_history[-2][1]
                        print(self.point_history[-1][0] - self.point_history[-2][0], self.point_history[-1][1] - self.point_history[-2][1])
                        mouse.move(self.point_history[-1][0] - self.point_history[-2][0],
                                   self.point_history[-1][1] - self.point_history[-2][1])
                        # pyautogui.moveTo(start_mouse_x, start_mouse_y)
                elif hand_sign_id == 3:
                    mouse.click(Button.left)
                else:
                    self.point_history.append([0, 0])

                # Finger gesture classification
                finger_gesture_id = 0
                point_history_len = len(pre_processed_point_history_list)
                if point_history_len == (self.history_length * 2):
                    finger_gesture_id = self.point_history_classifier(pre_processed_point_history_list)

                # Calculates the gesture IDs in the latest detection
                self.finger_gesture_history.append(finger_gesture_id)
                most_common_fg_id = Counter(self.finger_gesture_history).most_common()

                # Drawing part
                debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                debug_image = draw_landmarks(debug_image, landmark_list)
                debug_image = draw_info_text(
                    debug_image,
                    brect,
                    handedness,
                    self.keypoint_classifier_labels[hand_sign_id],
                    self.point_history_classifier_labels[most_common_fg_id[0][0]],
                )

            debug_image = draw_point_history(debug_image, self.point_history)
            # debug_image = draw_info(debug_image, mode, number)

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

        self.ui.pushButton.clicked.connect(self.start)
        self.ui.pushButton_2.clicked.connect(self.kill_thread)
        self.ui.pushButton_2.setEnabled(False)

    @Slot()
    def kill_thread(self):
        print("Finishing...")
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton.setEnabled(True)
        self.th.cap.release()
        cv2.destroyAllWindows()
        self.status = False
        self.th.terminate()
        # Give time for the thread to finish
        time.sleep(1)

    @Slot()
    def start(self):
        print("Starting...")
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton.setEnabled(False)
        # self.th.set_file(self.combobox.currentText())
        self.th.start()

    @Slot(QImage)
    def setImage(self, image):
        self.ui.label_5.setPixmap(QPixmap.fromImage(image))


if __name__ == "__main__":
    app = QApplication()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
