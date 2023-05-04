import argparse
import copy
import csv
import itertools
import pickle
from collections import Counter, deque

import cv2
import mediapipe as mp
import numpy as np
from pynput.mouse import Button, Controller

mouse = Controller()


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help="cap width", type=int, default=960)
    parser.add_argument("--height", help="cap height", type=int, default=540)

    parser.add_argument("--use_static_image_mode", action="store_true")
    parser.add_argument(
        "--min_detection_confidence",
        help="min_detection_confidence",
        type=float,
        default=0.7,
    )
    parser.add_argument(
        "--min_tracking_confidence",
        help="min_tracking_confidence",
        type=int,
        default=0.5,
    )

    args = parser.parse_args()

    return args


def main():
    # Argument parsing #################################################################
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    use_brect = True

    # Camera preparation ###############################################################
    cap = cv2.VideoCapture(1)  # cap_device

    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    # Model load #############################################################
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=1,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )
    mp_drawing = mp.solutions.drawing_utils

    # Read labels ###########################################################
    labels = [
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
        model = pickle.load(f)

    # Coordinate history #################################################################
    history_length = 16
    point_history = deque(maxlen=history_length)
    #  ########################################################################
    mode = 0
    # start_mouse_x, start_mouse_y = pyautogui.position()
    # print(start_mouse_x, start_mouse_y)
    start_mouse_x, start_mouse_y = mouse.position
    print(start_mouse_x, start_mouse_y)
    while True:
        # Process Key (ESC: end) #################################################
        key = cv2.waitKey(10)
        if key == 27:  # ESC
            break

        # Camera capture #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv2.flip(image, 1)  # Mirror display
        debug_image = copy.deepcopy(image)

        # Detection implementation #############################################################
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks is None:
            point_history.append([0, 0])
            debug_image = draw_point_history(debug_image, point_history)
            cv2.imshow("Hand Gesture Recognition", debug_image)
            continue

        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Bounding box calculation
            brect = calc_bounding_rect(debug_image, hand_landmarks)
            # Landmark calculation
            landmark_list = calc_landmark_list(debug_image, hand_landmarks)

            # Hand sign classification
            hand_sign_id = int(model.predict([landmark_list])[0])
            print(hand_sign_id)
            # if hand_sign_id == 1:  # Point gesture
            #     point_history.append((landmark_list[8], landmark_list[9]))
            #     if len(point_history) > 2 and point_history[-1][0] != 0 and point_history[-2][0] != 0 and \
            #             point_history[-1][1] != 0 and point_history[-2][1] != 0:
            #         start_mouse_x += point_history[-1][0] - point_history[-2][0]
            #         start_mouse_y += point_history[-1][1] - point_history[-2][1]
            #         print(point_history[-1][0] - point_history[-2][0], point_history[-1][1] - point_history[-2][1])
            #         mouse.move(point_history[-1][0] - point_history[-2][0], point_history[-1][1] - point_history[-2][1])
            #         # pyautogui.moveTo(start_mouse_x, start_mouse_y)
            # else:
            #     point_history.append([0, 0])

            # Drawing part
            # debug_image = draw_bounding_rect(use_brect, debug_image, brect)
            mp_drawing.draw_landmarks(debug_image, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
            debug_image = draw_info_text(
                debug_image,
                brect,
                handedness,
                labels[hand_sign_id],
                "",
            )

        debug_image = draw_point_history(debug_image, point_history)

        # Screen reflection #############################################################
        cv2.imshow("Hand Gesture Recognition", debug_image)

    cap.release()
    cv2.destroyAllWindows()


def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv2.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def calc_landmark_list(landmarks):
    landmarks = landmarks.landmark

    # Get the position of the wrist landmark (Landmark.WRIST)
    wrist_position_x, wrist_position_y = (
        landmarks[mp.solutions.hands.HandLandmark.WRIST].x,
        landmarks[mp.solutions.hands.HandLandmark.WRIST].y,
    )

    # Normalize the landmarks relative to the wrist position
    normalized_landmarks = [
        (landmark.x - wrist_position_x, landmark.y - wrist_position_y) for landmark in landmarks  # landmark.z
    ]
    normalized_landmarks = np.array(normalized_landmarks).flatten()
    normalized_landmarks /= max(abs(normalized_landmarks))
    return normalized_landmarks


def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        # Outer rectangle
        cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), (0, 0, 0), 1)

    return image


def draw_info_text(image, brect, handedness, hand_sign_text, finger_gesture_text):
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

    if finger_gesture_text != "":
        cv2.putText(
            image,
            "Finger Gesture:" + finger_gesture_text,
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 0),
            4,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            "Finger Gesture:" + finger_gesture_text,
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    return image


def draw_point_history(image, point_history):
    for index, point in enumerate(point_history):
        if point[0] != 0 and point[1] != 0:
            cv2.circle(image, (point[0], point[1]), 1 + int(index / 2), (152, 251, 152), 2)

    return image


if __name__ == "__main__":
    main()
