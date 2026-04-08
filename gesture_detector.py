import cv2
import mediapipe as mp
from collections import deque
import time

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False, max_num_hands=1,
            min_detection_confidence=0.7, min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.x_history = deque(maxlen=8)
        self.swipe_threshold = 0.18
        self.last_swipe_time = 0
        self.cooldown = 0.8

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        gesture = None

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            self.mp_draw.draw_landmarks(
                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2),
                self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
            )

            current_x = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            self.x_history.append(current_x)

            if len(self.x_history) == 8:
                dx = self.x_history[-1] - self.x_history[0]
                current_time = time.time()
                if current_time - self.last_swipe_time > self.cooldown:
                    if dx > self.swipe_threshold:
                        gesture = "SWIPE_RIGHT"
                        self.last_swipe_time = current_time
                        self.x_history.clear()
                    elif dx < -self.swipe_threshold:
                        gesture = "SWIPE_LEFT"
                        self.last_swipe_time = current_time
                        self.x_history.clear()
        else:
            if self.x_history:
                self.x_history.clear()

        return frame, gesture

    def release(self):
        self.hands.close()