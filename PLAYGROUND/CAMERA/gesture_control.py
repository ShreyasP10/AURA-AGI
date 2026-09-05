"""
6. Gesture Control — opencv hand gestures to control AURA
pip install mediapipe opencv-python
Gestures: open palm -> pause, fist -> stop TTS, ✋ -> stop, pinch -> volume
"""
import cv2
try:
    import mediapipe as mp
    mp_hands=mp.solutions.hands
    mp_draw=mp.solutions.drawing_utils
    def detect_gesture(frame):
        # placeholder: returns gesture string
        # real: use mp_hands.Hands() to detect landmarks
        return "none"

    def gesture_loop(on_gesture):
        cap=cv2.VideoCapture(0)
        hands=mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        print("Gesture control: show palm to pause, fist to stop")
        while True:
            ret, frame=cap.read()
            if not ret: break
            res=hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            gesture="none"
            if res.multi_hand_landmarks:
                for lm in res.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
                    # simple heuristic: if all fingers extended -> palm
                    gesture="palm"  # placeholder
                    on_gesture(gesture)
            cv2.imshow("AURA Gesture — ESC to exit", frame)
            if cv2.waitKey(1)==27: break
        cap.release(); cv2.destroyAllWindows()
except ImportError:
    def detect_gesture(f): return "none"
    def gesture_loop(cb): print("[pip install mediapipe]")

if __name__=="__main__":
    gesture_loop(lambda g: print("Gesture:",g))
