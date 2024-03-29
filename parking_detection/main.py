import base64

import cv2
import pickle
import cvzone
import numpy as np
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path
carparkpos_path = os.path.join(current_dir, 'CarParkPos')
video_path = os.path.join(current_dir, 'carPark.mp4')
cap = cv2.VideoCapture(video_path)
# cap = cv2.VideoCapture('cars.mp4')
# cap = cv2.VideoCapture('parkinglot_1_480p.mp4')

width, height = 103, 43
with open(carparkpos_path, 'rb') as f:
    posList = pickle.load(f)


def empty(a):
    pass


def check_spaces():
    print("checking")
    # Get image frame
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    # img = cv2.imread('img.png')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    # ret, imgThres = cv2.threshold(imgBlur, 150, 255, cv2.THRESH_BINARY)

    val1 = 25
    val2 = 14
    val3 = 5
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1
    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, val1, val2)
    imgThres = cv2.medianBlur(imgThres, val3)
    kernel = np.ones((3, 3), np.uint8)
    imgThres = cv2.dilate(imgThres, kernel, iterations=1)
    spaces = 0
    for pos in posList:
        x, y = pos
        w, h = width, height

        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 200, 0)
            thic = 5
            spaces += 1

        else:
            color = (0, 0, 200)
            thic = 2

        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)

        cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,
                    color, 2)

    cvzone.putTextRect(img, f'Free: {spaces}/{len(posList)}', (50, 60), thickness=3, offset=20,
                       colorR=(0, 200, 0))
    # your existing code to capture frame
    ret, frame = cap.read()
    # your existing code to process the frame
    ret, buffer = cv2.imencode('.jpg', img)
    frame_str = base64.b64encode(buffer).decode()
    #return [spaces, frame_str]

    return spaces


# while True:

#def disp():
#    cv2.imshow("Image", img)

    # checkSpaces()

    # cv2.imshow("Image", img)
    # cv2.imshow("ImageGray", imgThres)
    # # cv2.imshow("ImageBlur", imgBlur)
    # key = cv2.waitKey(1)
    # if key == ord('r'):
    #     pass
