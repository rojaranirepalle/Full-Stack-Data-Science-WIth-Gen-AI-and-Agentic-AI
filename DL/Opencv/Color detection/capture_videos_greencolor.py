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

    lower_green = np.array([40, 100, 100])  # Lower bound for green color in HSV
    upper_green = np.array([80, 255, 255])  # Upper bound

    green_mask = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), lower_green, upper_green)  # Create a mask for green color
    green_result = cv2.bitwise_and(frame, frame, mask=green_mask)  # Apply the mask to the original frame

    cv2.imshow('Frame', frame)  # Display the original video frame
    cv2.imshow('Green Mask', green_mask)  # Display the green mask
    cv2.imshow('Green Result', green_result)  # Display the result with only green colors

    key = cv2.waitKey(1)
    if key == 27:  # Break the loop if 'esc' is pressed
        break