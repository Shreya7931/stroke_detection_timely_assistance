import cv2
import mediapipe as mp
import numpy as np
import time

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return np.linalg.norm(np.array(point1) - np.array(point2))

# Video capture setup
cap = cv2.VideoCapture(0)  # Open webcam
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('arm_symmetry_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, (frame_width, frame_height))

# Timing for 15-second recording
start_time = time.time()
duration = 15  # seconds

symmetrical_frames = 0
total_frames = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Get keypoints
        left_shoulder = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * frame.shape[1]),
                         int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * frame.shape[0]))
        right_shoulder = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * frame.shape[1]),
                          int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * frame.shape[0]))
        left_wrist = (int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * frame.shape[1]),
                      int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * frame.shape[0]))
        right_wrist = (int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * frame.shape[1]),
                       int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * frame.shape[0]))

        # Calculate vertical midline
        mid_x = (left_shoulder[0] + right_shoulder[0]) // 2
        mid_y_top = min(left_shoulder[1], right_shoulder[1]) - 50  # Slightly above shoulders
        mid_y_bottom = max(left_shoulder[1], right_shoulder[1]) + 100  # Below chest

        # Calculate distances from symmetry line
        left_wrist_dist = abs(left_wrist[0] - mid_x)
        right_wrist_dist = abs(right_wrist[0] - mid_x)

        # Define a symmetry threshold
        threshold = 20  # Pixels tolerance
        if abs(left_wrist_dist - right_wrist_dist) > threshold:
            symmetry_text = "Arms are symmetrical"
            color = (0, 255, 0)  # Green
            symmetrical_frames += 1
        else:
            symmetry_text = "Arms are NOT symmetrical"
            color = (0, 0, 255)  # Red

        total_frames += 1

        # Draw symmetry line
        cv2.line(frame, (mid_x, mid_y_top), (mid_x, mid_y_bottom), (255, 255, 0), 2)

        # Draw wrist points
        cv2.circle(frame, left_wrist, 8, (0, 255, 0), -1)
        cv2.circle(frame, right_wrist, 8, (0, 0, 255), -1)

        # Display symmetry assessment
        cv2.putText(frame, symmetry_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

    # Write frame to video
    out.write(frame)

    # Show the frame
    cv2.imshow("Arm Symmetry Detection", frame)

    # Stop recording after 15 seconds
    if time.time() - start_time > duration:
        break

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# Final decision after 15 seconds
symmetry_percentage = (symmetrical_frames / total_frames) * 100
print(f"Final Symmetry Analysis: {symmetry_percentage:.2f}% frames were symmetrical.")

if symmetry_percentage > 70:  # If 70% of frames show symmetry, consider arms symmetrical
    print("Final Result: Arms are symmetrical.")
else:
    print("Final Result: Arms are NOT symmetrical.")
