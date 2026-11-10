# Fingers order: thumb, index, middle, ring, pinky
TIP_IDS = [4, 8, 12, 16, 20]

# Easy to edit: finger pattern -> message
GESTURES = {
    (0, 0, 0, 0, 0): "Fist",
    (1, 1, 1, 1, 1): "Hello",
    (1, 0, 0, 0, 0): "Like",
    (0, 1, 0, 0, 0): "One",
    (0, 1, 1, 0, 0): "Peace",
    (0, 1, 1, 1, 0): "Three",
    (0, 1, 1, 1, 1): "Four",
    (1, 0, 0, 0, 1): "Call me",
    (0, 1, 0, 0, 1): "Rock",
}


def get_fingers(hand_landmarks, label):
    """Return [thumb, index, middle, ring, pinky] with 1 = up, 0 = down."""
    lm = hand_landmarks.landmark
    fingers = []

    # Thumb: compare on the X axis (depends on left/right hand)
    if label == "Right":
        fingers.append(1 if lm[TIP_IDS[0]].x < lm[TIP_IDS[0] - 1].x else 0)
    else:
        fingers.append(1 if lm[TIP_IDS[0]].x > lm[TIP_IDS[0] - 1].x else 0)

    # Other fingers: tip above the joint on the Y axis = up
    for i in range(1, 5):
        fingers.append(1 if lm[TIP_IDS[i]].y < lm[TIP_IDS[i] - 2].y else 0)

    return fingers


def get_gesture(fingers):
    """Convert a finger pattern into a message."""
    return GESTURES.get(tuple(fingers), f"{sum(fingers)} fingers up")
