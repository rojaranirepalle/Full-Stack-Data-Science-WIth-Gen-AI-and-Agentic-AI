import numpy as np
import cv2

print(cv2.__version__)
print(cv2.__file__)
print(hasattr(cv2, "CascadeClassifier"))

# Load the Haar Cascade for face detection
face_classifier = cv2.CascadeClassifier("/Users/rojarani/Documents/AIML/GitAIML/Full-Stack-Data-Science-WIth-Gen-AI-and-Agentic-AI/DL/Opencv/Haar Cascades Classifier/haarcascade_frontalface_default.xml")# Load the image
eye_classifier = cv2.CascadeClassifier("/Users/rojarani/Documents/AIML/GitAIML/Full-Stack-Data-Science-WIth-Gen-AI-and-Agentic-AI/DL/Opencv/Haar Cascades Classifier/haarcascade_eye.xml")# Load the image
video = cv2.VideoCapture(0)  # Use 0 for the default camera, or provide a video file path

if not video.isOpened():
    print("Error: Could not open video source.")
    exit()  # Exit if the video source is not opened

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        print("Error: Could not read frame from video.")
        break  # Exit the loop if the frame is not read

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    eyes = eye_classifier.detectMultiScale(gray, 1.3, 5)

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (127, 0, 255), 2)

    # Draw rectangles around the detected eyes
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    # Display the output frame
    cv2.imshow('Face and Eye Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
