import copy
import pickle
import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
from PySide6.QtCore import QObject, QPoint, QPointList, Qt, QThread, Signal
from PySide6.QtGui import QGuiApplication, QImage

from src.drawing import calc_bounding_rect, calc_landmark_list, draw_info_text


class Thread(QThread):
    update_frame = Signal(QImage)
    activate_key = Signal(str)
    mouse_move = Signal(str, QPointList)
    update_label = Signal()

    def __init__(self, device: int, parent: QObject | None = None):
        QThread.__init__(self, parent)
        self.device = device
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

        self.history_length = 16
        self.point_history = QPointList()

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
            "fist",
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
        cap = cv2.VideoCapture(self.device)
        self.point_history.append(QPoint(0, 0))
        fps_start_time = time.time()
        fps = 0
        frame_count = 0

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

            frame_count += 1

            if (time.time() - fps_start_time) > 1:
                fps = frame_count // (time.time() - fps_start_time)
                fps_start_time = time.time()
                frame_count = 0

            cv2.putText(debug_image, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

            if results.multi_hand_landmarks is None:
                self.point_history.append(QPoint(0, 0))
                self.update_label.emit()
                self.draw_image(debug_image)
                continue

            hand_landmarks = results.multi_hand_landmarks[0]
            handedness = results.multi_handedness[0]

            brect = calc_bounding_rect(debug_image, hand_landmarks)
            landmark_list = calc_landmark_list(hand_landmarks)
            is_right = handedness.classification[0].label == "Right"
            data = np.append(landmark_list, int(is_right)).reshape(1, -1)

            hand_sign_id = int(self.model.predict(data)[0])

            self.mp_drawings.draw_landmarks(debug_image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            debug_image = draw_info_text(
                debug_image,
                brect,
                handedness,
                self.labels[hand_sign_id],
            )

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
