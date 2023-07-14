import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b):
    a = np.array(a)  # Shoulder
    b = np.array(b)  # Hip

    radians = np.arctan2(b[1] - a[1], b[0] - a[0])
    angle = np.abs(radians * 180.0 / np.pi)

    return angle

cap = cv2.VideoCapture('bike1.mp4')

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            # shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
            #             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            # hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
            #        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]


            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            # Calculate midpoints
            shoulder_midpoint = [(left_shoulder[0] + right_shoulder[0]) / 2,
                                 (left_shoulder[1] + right_shoulder[1]) / 2]
            hip_midpoint = [(left_hip[0] + right_hip[0]) / 2,
                            (left_hip[1] + right_hip[1]) / 2]


        
            # Calculate angle
            angle = calculate_angle(shoulder_midpoint, hip_midpoint)

            # Visualize angle
            cv2.putText(image, f'Angle: {angle:.2f} degrees',
                        (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Check if back is straight or bent down
            if angle < 160:
                cv2.putText(image, 'Warning: Back not straight!',
                            (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        except:
            pass

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        # Only continue iterating to the next frame if the user presses 'w'
        while cv2.waitKey(10) & 0xFF != ord('w'):
            pass

cap.release()
cv2.destroyAllWindows()
