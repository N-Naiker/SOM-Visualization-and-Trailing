#######-------------------Library Imports Section------------------#######

# Import OpenCV for Video Capture
import cv2
from cv2 import sqrt

# Imports for Hand Detection
import mediapipe as mp

# Imports for Controling Mouse Cursor
import pyautogui as pag

#######-----------------------Set Up Section-----------------------#######

def main():
    # Create variable to caoture video using OpenCV
    # 0 for fast video source capture
    capture = cv2.VideoCapture(0)       

    # This has hand solutions usd for hand detection within video frames
    handDetector = mp.solutions.hands.Hands()

    # Variable used for drawing hand landmarks on live video
    drawing_utils = mp.solutions.drawing_utils

    # Variables to get computer screen dimentions
    sWidth, sHeight = pag.size()

    # Variable to set distance at which clicks occur
    pixel_dist = 40

    # Initializing index finger tracking coordinates 
    index_scaled_x = 0
    index_scaled_y = 0

    # Initializing middle finger tracking coordinates 
    middle_scaled_x = 0
    middle_scaled_y = 0

    # Initializing ring finger tracking coordinates 
    ring_scaled_x = 0
    ring_scaled_y = 0

    # Initializing pinky finger tracking coordinates
    pinky_scaled_x = 0
    pinky_scaled_y = 0

    '''
    #######------------------Distance Funtion Section------------------#######

    # Funtion that returns euclidean distance between 2 points
    def getDistance(x1, y1, x2, y2):
        x = (x2-x1)*(x2-x1)
        y = (y2-y1)*(y2-y1)
        dist = sqrt(x+y)
        return dist
    '''

#######-------------------Virtual Mouse Section--------------------#######

    # Want Capture to run continuously. Thus, use while loop
    while True:
        # Capture Frame of Video
        # _ is first variable and frame is second variable  # for reading 
        # from video capture
        _, frame = capture.read()      

        # Video capture frame must be flipped/mirrored to correspond to 
        # movements. This is because the default capturing mode acts as 
        # an invertion of what is captured
        frame = cv2.flip(frame, 1)

        # Getting dimentions of frame, this will be important for getting
        # accurate tracking results with regards to the hands relative 
        # position
        fHeight, fWidth, _ = frame.shape

        # Converts colour of frame using OpenCV from BRg to RGB
        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Output variable to use handDetector variable from Mediapipe 
        # library to process video to detect hands in frame
        detection = handDetector.process(rgbFrame)

        # Hands detected from processing of video frames
        outputHands = detection.multi_hand_landmarks

        # Check if hands have been detected using the 21 land marks. If so, 
        # draw hands landmarks on subject frame
        if outputHands:
            for hand in outputHands:
                # Draw hand landmarks on hands within fram
                drawing_utils.draw_landmarks(frame, hand) 

                # Get landmarks of hand
                handLandmarks = hand.landmark

                # Iterate over lnadmarks to get index of each landmarks.To 
                # do this, the lands marks variable must first be converted 
                # into an enumerate array. Index and their values can be
                # found on the internet
                for id, landmark in enumerate(handLandmarks):
                    # Getting x & y co-ordinates of tracked hand. This 
                    # returns a percentage based value (a value between 
                    # 0 & 1). This it must be multiplied by the frame's 
                    # dimentions to get its actuale distance change
                    # Note that the number is also rounded and converted 
                    # to int for the purpose of using it as a cooridinate 
                    # tracking
                    x = int(round(landmark.x*fWidth, 0))
                    y = int(round(landmark.y*fHeight, 0))

                    # Check if index finger has been detected
                    if id == 8:
                        # Draw circle around index finger to show tracking
                        # of it on frame using its positional coordinates
                        cv2.circle(img=frame, center=(x,y), radius=12, 
                                color=(100, 100, 0))

                        # Scale frame to whole screen so mouse cursor can 
                        # frealy move
                        index_scaled_x = (sWidth/fWidth)*x
                        index_scaled_y = (sHeight/fHeight)*y

                        # Move mouse cursor to position of index finger 
                        # using scaled positional coordinates
                        pag.moveTo(index_scaled_x, index_scaled_y)

                        # Print mouse cursor coordinates
                        print(index_scaled_x, index_scaled_y)

                    # Check if middle finger has been detected
                    if id == 12:
                        # Draw circle around middle finger to show tracking
                        # of it on frame using its positional coordinates
                        cv2.circle(img=frame, center=(x,y), radius=12, 
                                color=(100, 100, 0))

                        # Scale frame to whole screen
                        middle_scaled_x = (sWidth/fWidth)*x
                        middle_scaled_y = (sHeight/fHeight)*y

                    # Check if ring finger has been detected
                    if id == 16:
                        # Draw circle around ring finger to show tracking
                        # of it on frame using its positional coordinates
                        cv2.circle(img=frame, center=(x,y), radius=12, 
                                color=(100, 100, 0))

                        # Scale frame to whole screen
                        ring_scaled_x = (sWidth/fWidth)*x
                        ring_scaled_y = (sHeight/fHeight)*y

                    # Check if pinky finger has been detected
                    if id == 20:
                        # Draw circle around pinky finger to show tracking
                        # of it on frame using its positional coordinates
                        cv2.circle(img=frame, center=(x,y), radius=12, 
                                color=(100, 100, 0))

                        # Scale frame to whole screen
                        pinky_scaled_x = (sWidth/fWidth)*x
                        pinky_scaled_y = (sHeight/fHeight)*y

                    # Check if thumb has been detected
                    if id == 4:
                        # Draw circle around thumb to show tracking of it 
                        # on frame using its positional coordinates
                        cv2.circle(img=frame, center=(x,y), radius=12, 
                                color=(100, 100, 0))

                        # Scale frame to whole screen so mouse cursor can
                        thumb_scaled_x = (sWidth/fWidth)*x
                        thumb_scaled_y = (sHeight/fHeight)*y

                        # Getting distance between thumb and index
                        thumb_index_x = abs(thumb_scaled_x-index_scaled_x)
                        thumb_index_y = abs(thumb_scaled_y-index_scaled_y)

                        '''
                        # Print Thumb Index Distance for data captue
                        print('Thumb Index Dist: ', thumb_index_x)
                        '''

                        # Getting distance between thumb and middle
                        thumb_middle_x = abs(thumb_scaled_x-middle_scaled_x)
                        thumb_middle_y = abs(thumb_scaled_y-middle_scaled_y)

                        '''
                        # Print Thumb Middle Distance for data captue
                        print('Thumb Middle Dist: ', thumb_middle_x)
                        '''

                        # Getting distance between thumb and ring
                        thumb_ring_x = abs(thumb_scaled_x-ring_scaled_x)
                        thumb_ring_y = abs(thumb_scaled_y-ring_scaled_y)

                        '''
                        # Print Thumb Ring Distance for data captue
                        print('Thumb Ring Dist: ', thumb_ring_x)
                        '''

                        # Getting distance between thumb and pinky
                        thumb_pinky_x = abs(thumb_scaled_x-pinky_scaled_x)
                        thumb_pinky_y = abs(thumb_scaled_y-pinky_scaled_y)

                        '''
                        # Print Thumb Pinky Distance for data captue
                        print('Thumb Pinky Dist: ', thumb_pinky_x)
                        '''

                        '''
                        # Next
                        # Check that distance is less that of pixel_dist 
                        # Note that this pixel distance depends on the 
                        # distance between the user and the video camera. 
                        # Further distances require a smaller number of pixels 
                        # where as a closer distance requires a higher number
                        '''

                        # Left click with index to thumb
                        if thumb_index_x < pixel_dist and thumb_index_y < pixel_dist:
                            # Print whether single left click has occured
                            print('left click detected')

                            # Perform single left click when requirements are met
                            pag.leftClick()

                            # Add delay to prevent continuous click
                            pag.sleep(1)

                        # Right click with middle to thumb
                        if thumb_middle_x < pixel_dist and thumb_middle_y < pixel_dist:
                            # Print whether right click has occured
                            print('right click detected')

                            # Perform single right click when requirements are met
                            pag.rightClick()

                            # Add delay to prevent continuous click
                            pag.sleep(1)

                        # Left click hold with ring to thumb
                        if thumb_ring_x < pixel_dist and thumb_ring_y < pixel_dist:
                            # Print whether Left click hold has occured
                            print('mouse down detected')

                            # Perform Left click hold when requirements are met
                            pag.mouseDown()

                        # Left click release with pinky to thumb
                        if thumb_pinky_x < pixel_dist and thumb_pinky_y < pixel_dist:
                            # Print whether Left click release has occured
                            print('mouse up detected')

                            # Perform single right click when requirements are met
                            pag.mouseUp()                       

        # Show Captured Image 
        # Uses imshow to display capture with frames name and the frame 
        # itself
        cv2.imshow('Virtual Mouse', frame)

        # Establish Wait Time
        # The waitKey method will display the frame for 1 ms, after which 
        # display will be automatically closed.
        cv2.waitKey(10)

main()

#######--------------------------File End--------------------------#######