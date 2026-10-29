import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import math

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Mouse settings
pyautogui.FAILSAFE = True
screen_width, screen_height = pyautogui.size()

# Keyboard layout
keys = [
    list("1234567890"),
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM"),
    ["SPACE", "BACKSPACE", "ENTER"]
]

key_width = 65
key_height = 55
gap = 8
start_y = 150

typed_text = ""
last_click_time = 0
click_cooldown = 0.6
pinch_was_active = False

# Open webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Cannot access webcam.")
    raise SystemExit

try:
    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    ) as hands:

        while True:
            success, frame = camera.read()

            if not success:
                print("Cannot read webcam.")
                break

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape

            # Detect hand
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            # Create keyboard
            keyboard = np.full(
                (height, width, 3),
                245,
                dtype=np.uint8
            )

            cv2.putText(
                keyboard, "VIRTUAL KEYBOARD",
                (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (180, 70, 30), 2
            )

            # Text display
            cv2.rectangle(
                keyboard,
                (10, 60), (width - 10, 125),
                (255, 255, 255), -1
            )

            cv2.rectangle(
                keyboard,
                (10, 60), (width - 10, 125),
                (180, 70, 30), 2
            )

            display_text = typed_text.split("\n")[-1][-35:]

            cv2.putText(
                keyboard, display_text,
                (20, 100), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (30, 30, 30), 2
            )

            # Draw keyboard keys
            key_positions = []

            for row_index, row in enumerate(keys):

                if row_index == 4:
                    special_widths = {
                        "SPACE": 150,
                        "BACKSPACE": 180,
                        "ENTER": 120
                    }

                    total_width = sum(
                        special_widths[k] + gap for k in row
                    ) - gap
                else:
                    total_width = (
                        len(row) * (key_width + gap) - gap
                    )

                row_start_x = max(
                    10, (width - total_width) // 2
                )

                row_y = start_y + row_index * (key_height + gap)
                x = row_start_x

                for key in row:

                    w = (
                        special_widths[key]
                        if row_index == 4 else key_width
                    )
                    h = key_height

                    cv2.rectangle(
                        keyboard,
                        (x, row_y), (x + w, row_y + h),
                        (220, 230, 245), -1
                    )

                    cv2.rectangle(
                        keyboard,
                        (x, row_y), (x + w, row_y + h),
                        (180, 70, 30), 2
                    )

                    font_scale = 0.45 if len(key) > 1 else 0.65

                    text_size = cv2.getTextSize(
                        key, cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, 1
                    )[0]

                    text_x = x + (w - text_size[0]) // 2
                    text_y = row_y + (h + text_size[1]) // 2

                    cv2.putText(
                        keyboard, key, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, (30, 30, 30), 1
                    )

                    key_positions.append(
                        (key, x, row_y, w, h)
                    )

                    x += w + gap

            pinch_active = False

            if result.multi_hand_landmarks:

                hand = result.multi_hand_landmarks[0]

                mp_draw.draw_landmarks(
                    frame, hand, mp_hands.HAND_CONNECTIONS
                )

                index_tip = hand.landmark[8]
                thumb_tip = hand.landmark[4]

                # Camera coordinates
                finger_x = int(index_tip.x * width)
                finger_y = int(index_tip.y * height)

                thumb_x = int(thumb_tip.x * width)
                thumb_y = int(thumb_tip.y * height)

                # Map camera coordinates to screen coordinates
                mouse_x = int(index_tip.x * screen_width)
                mouse_y = int(index_tip.y * screen_height)

                # Move the real mouse cursor
                pyautogui.moveTo(mouse_x, mouse_y, duration=0)

                cv2.circle(
                    frame,
                    (finger_x, finger_y),
                    10, (0, 255, 0), -1
                )

                # Calculate pinch distance
                distance = math.hypot(
                    finger_x - thumb_x,
                    finger_y - thumb_y
                )

                pinch_active = distance < 35

                cv2.putText(
                    frame,
                    "PINCH" if pinch_active else "MOVE INDEX FINGER",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2
                )

                current_time = time.time()

                # Select a key using the fingertip coordinates
                if (
                    pinch_active
                    and not pinch_was_active
                    and current_time - last_click_time > click_cooldown
                ):

                    for key, x, y, w, h in key_positions:

                        if (
                            x <= finger_x < x + w
                            and y <= finger_y < y + h
                        ):

                            if key == "SPACE":
                                typed_text += " "
                            elif key == "BACKSPACE":
                                typed_text = typed_text[:-1]
                            elif key == "ENTER":
                                typed_text += "\n"
                            else:
                                typed_text += key

                            last_click_time = current_time
                            break

                pinch_was_active = pinch_active

            else:
                pinch_was_active = False

            # Display windows
            cv2.imshow("Hand Tracking", frame)
            cv2.imshow("Virtual Keyboard", keyboard)

            # Press Q to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

finally:
    camera.release()
    cv2.destroyAllWindows()