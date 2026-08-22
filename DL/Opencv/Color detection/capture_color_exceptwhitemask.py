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

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert the frame to HSV color space

    # Define the range for white color in HSV
    lower_white = np.array([0, 0, 200])  # Lower bound
    upper_white = np.array([180, 30, 255])  # Upper bound   

    # Create a mask for white color
    white_mask = cv2.inRange(hsv_frame, lower_white, upper_white)
    # Invert the mask to get everything except white
    except_white_mask = cv2.bitwise_not(white_mask)
    # Apply the mask to the original frame
    except_white_result = cv2.bitwise_and(frame, frame, mask=except_white_mask)
    cv2.imshow('Frame', frame)  # Display the original video frame
    cv2.imshow('Except White Mask', except_white_mask)  # Display the mask for everything except white
    cv2.imshow('Except White Result', except_white_result)  # Display the result with everything except white colors
    
    
    key = cv2.waitKey(1)
    if key == 27:  # Break the loop if 'esc' is pressed
        break