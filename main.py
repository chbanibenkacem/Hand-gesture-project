from collections import deque

import cv2
import mediapipe as mp

from gestures import get_fingers, get_gesture
from logger import GestureLogger

STABLE_FRAMES = 5  # gesture must stay the same for 5 frames


def main():
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open the camera.")
        return

    logger = GestureLogger()
    history = {"Left": deque(maxlen=STABLE_FRAMES),
               "Right": deque(maxlen=STABLE_FRAMES)}

    with mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    ) as hands:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)  # mirror
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            y = 40
            if results.multi_hand_landmarks:
                for hand_lms, handedness in zip(
                    results.multi_hand_landmarks, results.multi_handedness
                ):
                    # Frame is mirrored, so swap Left/Right
                    label = handedness.classification[0].label
                    label = "Left" if label == "Right" else "Right"

                    mp_draw.draw_landmarks(
                        frame, hand_lms, mp_hands.HAND_CONNECTIONS
                    )

                    fingers = get_fingers(hand_lms, label)
                    message = get_gesture(fingers)

                    # Stability check
                    history[label].append(message)
                    stable = (
                        len(history[label]) == STABLE_FRAMES
                        and len(set(history[label])) == 1
                    )

                    cv2.putText(frame, f"{label}: {message}", (20, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    y += 40

                    if stable:
                        logger.log(f"{label}: {message}")

            cv2.imshow("Hand Gestures", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
