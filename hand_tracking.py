
import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Open webcam
camera = cv2.VideoCapture(0)

# Mouse settings
smooth_factor = 0.3
smooth_x, smooth_y = 0, 0
left_clicked = False
right_clicked = False

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while True:
        success, frame = camera.read()

        if not success:
            print("Cannot access webcam")
            break

        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                frame, hand, mp_hands.HAND_CONNECTIONS
            )

            # Get fingertip positions
            index_tip = hand.landmark[8]
            thumb_tip = hand.landmark[4]
            middle_tip = hand.landmark[12]

            # Map index finger to screen coordinates
            target_x = int(index_tip.x * screen_width)
            target_y = int(index_tip.y * screen_height)

            # Smooth cursor movement
            smooth_x += (target_x - smooth_x) * smooth_factor
            smooth_y += (target_y - smooth_y) * smooth_factor

            # Move mouse
            pyautogui.moveTo(
                int(smooth_x),
                int(smooth_y)
            )

            # Calculate finger distances
            left_distance = math.hypot(
                thumb_tip.x - index_tip.x,
                thumb_tip.y - index_tip.y
            )

            right_distance = math.hypot(
                thumb_tip.x - middle_tip.x,
                thumb_tip.y - middle_tip.y
            )

            # Left click: thumb + index finger
            if left_distance < 0.045 and not left_clicked:
                pyautogui.click()
                left_clicked = True
            elif left_distance >= 0.065:
                left_clicked = False

            # Right click: thumb + middle finger
            if right_distance < 0.045 and not right_clicked:
                pyautogui.rightClick()
                right_clicked = True
            elif right_distance >= 0.065:
                right_clicked = False

            # Display instructions
            cv2.putText(
                frame, "VIRTUAL MOUSE ACTIVE",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2
            )

            cv2.putText(
                frame, "Thumb + Index: Left Click",
                (20, 75), cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (255, 255, 0), 2
            )

            cv2.putText(
                frame, "Thumb + Middle: Right Click",
                (20, 105), cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (255, 255, 0), 2
            )

        cv2.imshow("Virtual Mouse", frame)

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()
 