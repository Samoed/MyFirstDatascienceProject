import cv2
import mediapipe as mp
import numpy as np
from mediapipe.framework.formats.classification_pb2 import ClassificationList
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList


def calc_bounding_rect(image: np.ndarray, landmarks: NormalizedLandmarkList) -> tuple[int, int, int, int]:
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv2.boundingRect(landmark_array)

    return x, y, x + w, y + h


def calc_landmark_list(landmarks: NormalizedLandmarkList) -> np.ndarray:
    landmark_list = landmarks.landmark
    # Get the position of the wrist landmark (Landmark.WRIST)
    wrist_position_x, wrist_position_y = (
        landmark_list[mp.solutions.hands.HandLandmark.WRIST].x,
        landmark_list[mp.solutions.hands.HandLandmark.WRIST].y,
    )

    # Normalize the landmarks relative to the wrist position
    normalized_landmarks = [
        (landmark.x - wrist_position_x, landmark.y - wrist_position_y) for landmark in landmark_list  # landmark.z
    ]
    normalized_landmarks = np.array(normalized_landmarks).flatten()
    normalized_landmarks /= max(abs(normalized_landmarks))
    return normalized_landmarks


def draw_bounding_rect(image: np.ndarray, brect: list[int]) -> np.ndarray:
    cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), (0, 0, 0), 1)
    return image


def draw_info_text(
    image: np.ndarray, brect: tuple[int, int, int, int], handedness: ClassificationList, hand_sign_text: str
) -> np.ndarray:
    cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22), (0, 0, 0), -1)

    info_text = handedness.classification[0].label[0:]
    if hand_sign_text != "":
        info_text = info_text + ":" + hand_sign_text
    cv2.putText(
        image,
        info_text,
        (brect[0] + 5, brect[1] - 4),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )
    return image
