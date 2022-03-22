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
        print(lm)
        cx, cy = int(lm[0] * w), int(lm[1] * h)
        cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
    return img


quaytrai_df = pd.read_csv("quaytrai.txt")
dataset = quaytrai_df.iloc[:,1:].values
n_sample = len(dataset)
print(dataset[0])
cap = cv2.VideoCapture(0)
for i in range (0,len(dataset)):
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)
    frame = draw_landmark_on_image(mpDraw, dataset[i], frame)
    cv2.imshow("image", frame)
    cv2.waitKey(100)
