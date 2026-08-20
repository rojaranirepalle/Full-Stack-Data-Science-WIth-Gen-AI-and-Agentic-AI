import numpy as np
import cv2

print(cv2.__version__)
print(cv2.__file__)
print(hasattr(cv2, "CascadeClassifier"))

# Load the Haar Cascade for face detection
body_classifier = cv2.CascadeClassifier("/Users/rojarani/Documents/AIML/GitAIML/Full-Stack-Data-Science-WIth-Gen-AI-and-Agentic-AI/DL/Opencv/Haar Cascades Classifier/haarcascade_fullbody.xml")# Load the image
if body_classifier.empty():
    print("Error: Could not load Haar Cascade classifier for body detection.")
    exit()  # Exit if the classifier is not loaded

video = cv2.VideoCapture("/Users/rojarani/Documents/AIML/GitAIML/Full-Stack-Data-Science-WIth-Gen-AI-and-Agentic-AI/DL/images/training/Happy/videos/mango.mp4")

if not video.isOpened():
    print("Error: Could not open video file.")
    exit()  # Exit if the video file is not opened

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        print("Error: Could not read frame from video.")
        break  # Exit the loop if the frame is not read

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect bodies in the frame
    bodies = body_classifier.detectMultiScale(gray, 1.3, 5)

    # Draw rectangles around the detected bodies
    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (127, 0, 255), 2)

    # Display the output frame
    cv2.imshow('Body Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break