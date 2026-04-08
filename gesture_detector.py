import cv2
import mediapipe as mp
from collections import deque
import time

def main():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                           min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    x_history = deque(maxlen=8)
    swipe_threshold = 0.18
    last_swipe_time = 0
    cooldown = 0.8

    print("Swipe detection prototype started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        gesture = None
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Index finger tip (landmark 8)
            current_x = hand_landmarks.landmark[8].x
            x_history.append(current_x)

            if len(x_history) == 8:
                dx = x_history[-1] - x_history[0]
                current_time = time.time()
                if current_time - last_swipe_time > cooldown:
                    if dx > swipe_threshold:
                        gesture = "SWIPE_RIGHT"
                        print("🚀 SWIPE RIGHT DETECTED")
                        last_swipe_time = current_time
                        x_history.clear()
                    elif dx < -swipe_threshold:
                        gesture = "SWIPE_LEFT"
                        print("🚀 SWIPE LEFT DETECTED")
                        last_swipe_time = current_time
                        x_history.clear()

        else:
            if x_history:
                x_history.clear()

        cv2.putText(frame, "Gesture Controlled Presentation", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        if gesture:
            cv2.putText(frame, f"{gesture} DETECTED!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        cv2.imshow("Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    hands.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()