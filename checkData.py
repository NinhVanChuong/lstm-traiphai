import cv2
import numpy as np
import pandas as pd
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils


def draw_landmark_on_image(mpDraw, results, img):
    # Vẽ các điểm nút
    adu=[]
    adus=[]
    for i in range(len(results)):
        adu.append(results[i])
        if (i+1)%4==0:
            adus.append(adu)
            adu=[]
    for lm in adus:
        h, w, c = img.shape
        # print(lm)
        cx, cy = int(lm[0] * w), int(lm[1] * h)
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
    return img


quaytrai_df = pd.read_csv("quaytrai.txt")
dataset = quaytrai_df.iloc[:,1:].values
n_sample = len(dataset)
print(n_sample)
# print(dataset[0])

# cap = cv2.VideoCapture(0)
# for i in range (0,len(dataset)):
#     frame = np.ones((480, 640, 3), np.uint8) * 0
#     # ret, frame = cap.read()
#     # frame=cv2.flip(frame,1)
#     frame = draw_landmark_on_image(mpDraw, dataset[i], frame)
#     cv2.imshow("image", frame)
#     cv2.waitKey(100)
i = 0
list_frame=[]
frame = np.ones((480, 640, 3), np.uint8) * 0

while True:

    frame = np.ones((480, 640, 3), np.uint8) * 0
    # ret, frame = cap.read()
    # frame=cv2.flip(frame,1)
    frame = draw_landmark_on_image(mpDraw, dataset[i], frame)
    cv2.putText(frame,str(i),(30,50),4,2,(0,255,0),2);
    cv2.imshow("image", frame)
    # print(i)
    key = cv2.waitKeyEx(1)  # waitKey(300)

    if key == 2424832: #left arrow
        # print(i)
        if i>0: i=i-1
    elif key == 2555904:  #right arrow
        # print(i)
        if i < n_sample: i = i + 1
    elif key==ord(' '):  #space
        list_frame.append(i)
    elif key==ord('q'):
        break
    if i > n_sample:
        break
print(list_frame)