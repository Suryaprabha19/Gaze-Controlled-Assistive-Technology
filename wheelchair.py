import cv2
import numpy as np
import dlib

# Load face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Define control keys
keyboard_keys = ["Front", "Reverse", "Left", "Right"]

# Keyboard layout positions (center of screen)
screen_width, screen_height = 640, 480  # Adjust based on your webcam resolution
keyboard_center_x, keyboard_center_y = screen_width // 2, screen_height // 2

key_size = 100  # Square key size
key_positions = {
    "Front": (keyboard_center_x - key_size // 2, keyboard_center_y - key_size - 50),
    "Reverse": (keyboard_center_x - key_size // 2, keyboard_center_y + key_size - 40),
    "Left": (keyboard_center_x - key_size - 90, keyboard_center_y - key_size // 2),
    "Right": (keyboard_center_x + key_size - 10, keyboard_center_y - key_size // 2),
}

# Blink detection variables
blink_count = 0
blink_threshold = 2  # Double blink to select
selected_key = None
key_selected = False  # Prevent multiple selections on one blink

def draw_keyboard(frame):
    """Draws a transparent keyboard layout in a cross shape."""
    for key, (x, y) in key_positions.items():
        cv2.rectangle(frame, (x, y), (x + key_size, y + key_size), (255, 255, 255), 2)
        cv2.putText(frame, key, (x + 15, y + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

def eye_aspect_ratio(eye):
    """Calculates the Eye Aspect Ratio (EAR) for blink detection."""
    eye = np.array([(p.x, p.y) for p in eye])
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

# Open the webcam
cap = cv2.VideoCapture(0)
cap.set(3, screen_width)  # Set width
cap.set(4, screen_height)  # Set height

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # 🔄 Mirror the camera feed
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Extract eye landmarks
        left_eye = landmarks.parts()[36:42]
        right_eye = landmarks.parts()[42:48]

        # Compute EAR for blink detection
        left_EAR = eye_aspect_ratio(left_eye)
        right_EAR = eye_aspect_ratio(right_eye)
        EAR = (left_EAR + right_EAR) / 2.0

        # Blink detection
        if EAR < 0.2:  # Eyes closed
            blink_count += 1
            key_selected = False  # Allow selection after blink
        else:
            if blink_count >= blink_threshold and selected_key and not key_selected:
                print(f'Key Pressed: {selected_key}')  # Simulate key press
                key_selected = True  # Prevent multiple selections on one blink
            blink_count = 0  # Reset blink counter

        # Find center of the eyes
        left_eye_center = np.mean([(p.x, p.y) for p in left_eye], axis=0).astype(int)
        right_eye_center = np.mean([(p.x, p.y) for p in right_eye], axis=0).astype(int)
        eye_x, eye_y = (left_eye_center + right_eye_center) // 2  # Average both eyes

        # *Fix the mirrored tracking issue*
        mirrored_eye_x = eye_x  # ✅ Corrected: Now moves naturally with head movement

        # Draw tracking dot at corrected position
        frame = cv2.circle(frame, (mirrored_eye_x, eye_y), 5, (0, 255, 0), -1)

        # Map gaze to keyboard correctly after mirroring
        for key, (x, y) in key_positions.items():
            if x < mirrored_eye_x < x + key_size and y < eye_y < y + key_size:
                selected_key = key

    draw_keyboard(frame)

    cv2.imshow("Eye Tracking Virtual Keyboard", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
