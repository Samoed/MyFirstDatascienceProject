import copy
import pickle

import cv2
import mediapipe as mp
import numpy as np
from PySide6.QtCore import QThread, Signal, QPointList, QObject, Qt, QPoint
from PySide6.QtGui import QImage, QGuiApplication
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark

from src.drawing import calc_bounding_rect, calc_landmark_list, draw_info_text


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
        self.cam_width = 640
        self.cam_height = 480

    def draw_image(self, image: np.ndarray) -> None:
        h, w, ch = image.shape
        img = QImage(image.data, w, h, ch * w, QImage.Format_RGB888)
        scaled_img = img.scaled(self.cam_width, self.cam_height, Qt.KeepAspectRatio)
        self.update_frame.emit(scaled_img)

    def run(self) -> None:
        cap = cv2.VideoCapture(1)
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

            hand_landmarks = results.multi_hand_landmarks[0]
            handedness = results.multi_handedness[0]
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
            )
            print(max_score, hand_sign_id, self.labels[hand_sign_id])
            if max_score < 0.6:
                self.draw_image(debug_image)
                continue

            if hand_sign_id in self.mouse_ids:
                # 8 is index of index point finger
                move_x, move_y = self.mouse_move_size(hand_landmarks.landmark[8])

                self.point_history.append(QPoint(move_x, move_y))
                self.mouse_move.emit(self.labels[hand_sign_id], self.point_history)
            else:
                self.point_history.append(QPoint(0, 0))
                self.activate_key.emit(self.labels[hand_sign_id])

            self.draw_image(debug_image)

            if len(self.point_history) > self.history_length:
                self.point_history.removeFirst(len(self.point_history) - self.history_length)

        cap.release()
        cv2.destroyAllWindows()

    def mouse_move_size(self, landmark: NormalizedLandmark) -> tuple[int, int]:
        landmark_x = min(int(landmark.x * self.cam_width), self.cam_width - 1)
        landmark_y = min(int(landmark.y * self.cam_height), self.cam_height - 1)

        percent_web_x = min(landmark_x / (self.cam_width * 0.8), 100)
        percent_web_y = min(landmark_y / (self.cam_height * 0.8), 100)

        display = QGuiApplication.primaryScreen().size()

        move_x = int(display.width() * percent_web_x)
        move_y = int(display.height() * percent_web_y)
        return move_x, move_y
