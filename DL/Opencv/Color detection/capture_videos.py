import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # Capture video from the default camera
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()  # Exit if the video source is not opened    

while True:
    _, frame = cap.read()  # Read a frame from the video capture
    if frame is None:
        print("Error: Could not read frame from video.")
        break  # Exit the loop if the frame is not read

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert the frame to HSV color space
    cv2.imshow('HSV Video', hsv)  # Display the HSV video frame
    cv2.imshow('Frame', frame)  # Display the original video frame

    key = cv2.waitKey(1)
    if key == 27:  # Break the loop if 'esc' is pressed
        break