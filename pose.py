import cv2
import mediapipe as mp
import numpy as np
from imutils.video import VideoStream
from datetime import datetime, timedelta

class PoseDetector:
    def __init__(self, url, email):
        self.url = url
        self.email = email
        self.vs = None
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.angle_data = []
        self.frame_count = 0
        self.last_time = None
        self.stream_start_time = None
        self.stream_end_time = None
        self.monogdb_id= None

    def calculate_angle(self, a, b):
        a = np.array(a)  # Shoulder
        b = np.array(b)  # Hip

        radians = np.arctan2(b[1] - a[1], b[0] - a[0])
        angle = np.abs(radians * 180.0 / np.pi)

        return angle

    def start_stream(self):
        # Start video stream
        self.vs = VideoStream(src=self.url).start()

        # Record stream start time
        self.stream_start_time = datetime.now()

        # Setup mediapipe instance
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while True:
                frame = self.vs.read()

                if frame is None:
                    break

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

                    left_shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                     landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    right_shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                      landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    left_hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    right_hip = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                 landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                    # Calculate midpoints
                    shoulder_midpoint = [(left_shoulder[0] + right_shoulder[0]) / 2,
                                         (left_shoulder[1] + right_shoulder[1]) / 2]
                    hip_midpoint = [(left_hip[0] + right_hip[0]) / 2,
                                    (left_hip[1] + right_hip[1]) / 2]

                    # Calculate angle
                    angle = self.calculate_angle(shoulder_midpoint, hip_midpoint)

                    # Increment frame count
                    self.frame_count += 1

                    # Get current time
                    current_time = datetime.now()

                    # Check if it's a new second
                    if self.last_time is None or current_time.second != self.last_time.second:
                        # Store angle data
                        self.angle_data.append((current_time, angle))
                        self.last_time = current_time

                    # Visualize angle
                    cv2.putText(image, f'Angle: {angle:.2f} degrees',
                                (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    # Check if back is straight or bent down
                    if angle < 85 or angle > 105:
                        cv2.putText(image, 'Warning: Back not straight!',
                                    (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    else:
                        cv2.putText(image, 'Back is straight',
                                    (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                except:
                    pass

                # Render detections
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                               self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                               self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

                cv2.imshow('Mediapipe Feed', image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()
        self.vs.stop()

        # Record stream end time
        self.stream_end_time = datetime.now()

        # Print angle data at the end
        print("Angle Data:")
        for data in self.angle_data:
            timestamp = data[0]
            angle = data[1]
            print(f"Timestamp: {timestamp}, Angle: {angle:.2f} degrees")

        # Print stream start and end time
        print(f"Stream Start Time: {self.stream_start_time}")
        print(f"Stream End Time: {self.stream_end_time}")

# Example usage
url = 'http://192.168.100.24:8080'
email = 'example@gmail.com'

pose_detector = PoseDetector(url, email)
pose_detector.start_stream()
