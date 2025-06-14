import cv2
import numpy as np
import HandTracking_module as htm
import time
import autopy



# Camera - Screen Size Declaration
cam_width, cam_height = 640, 480
screen_width, screen_height = autopy.screen.size()

# Capture - Initialization
cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

# FPS - Initialization
pTime = 0

# Hand Detector - Declaration
detector = htm.handDetector(maxHands=1)

# Object - Initialization
fingers = []



while True:

# Landmarks - Hand
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if not success:
        print("Debug: Failed to capture frame from camera.")
        time.sleep(1) # Delay before retrying capture
        continue

    img = detector.findHands(img)
    Landmark_list, bbox = detector.findPosition(img)

# Landmarks - Each Finger
    if len(Landmark_list) != 0:
        x1, y1 = Landmark_list [8][1:]   # Index Finger
        x2, y2 = Landmark_list [12][1:]   # Middle Finger
        x3, y3 = Landmark_list [16][1:]   # Ring Finger
        x4, y4 = Landmark_list [20][1:]   # Little Finger
        x5, y5 = Landmark_list [4][1:]   # Thumb
        #print(f'Thumb:{(x5,y5)}, Index{(x1,y1)}, Middle:{(x2,y2)}, Ring:{(x3,y3)}, Little:{(x4,y4)}')

# Checking which finger is up
        fingers = detector.fingersUp()
        #print(fingers)

# Counting Fingers - When up
    if len(fingers) >= 5:
        fingers_count = []

        # Thumb
        if fingers[0] == 0:
            fingers.insert(1, 1)
        else:
            fingers.insert(1, 0)

        # Other fingers
        for f in fingers[1:]:
            if f == 1:
                fingers_count.append(1)
            else:
                fingers_count.append(0)

        #print(fingers_count)

        # Sum - Fingers up
        _sum = 0
        for i in fingers_count:
            if i == 1:
                _sum+=1
        
# On Screen Text 
    # Total Fingers up - Displaying
        cv2.putText(img, 
                    f'Count of Fingers: {_sum}', 
                    (230, 30),   # Position
                    cv2.FONT_HERSHEY_DUPLEX,   # Font
                    0.5,   # Scale
                    (255, 255, 255),   # Color
                    1,   # Thickness
        )

    # FPS - Configurations
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # FPS Text - Displaying
    cv2.putText(img, 
                f'FPS: {int(fps)}', 
                (20, 50),   # Position
                cv2.FONT_HERSHEY_DUPLEX,   # Font
                0.5,   # Scale
                (255, 255, 255),   # Color
                1,   # Thickness
    )

# Product 
    # Result Image - Display
    cv2.imshow('Image', img)

    # Capture termination 'Q'
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break



# CLEANUP - Release resources and close windows
cap.release()
cv2.destroyAllWindows()