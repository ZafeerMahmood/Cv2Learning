import cv2


def detect_movement_from_center(video_path):
    """
    Detects if the user moves away from the center of the video frame, tracks faces, and checks if the face is centered.

    Args:
        video_path (str): Path to the video file.

    Returns:
        None
    """

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    video = cv2.VideoCapture(video_path)

    while True:
        ret, frame = video.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces and check if they are centered
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Calculate the center coordinates of the face bounding box
            face_center_x = x + w // 2
            face_center_y = y + h // 2

            # Get the center coordinates of the video frame
            frame_center_x = frame.shape[1] // 2
            frame_center_y = frame.shape[0] // 2

            # Check if the face is centered within a threshold
            threshold = 50  # Adjust this value based on your requirement
            if abs(face_center_x - frame_center_x) <= threshold and abs(face_center_y - frame_center_y) <= threshold:
                cv2.putText(frame, 'Centered', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'Not Centered', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Display the frame
        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close the windows
    video.release()
    cv2.destroyAllWindows()


# Example usage
video_path = 'v1.mp4'
detect_movement_from_center(video_path)