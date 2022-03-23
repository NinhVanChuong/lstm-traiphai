import cv2
import mediapipe as mp
import pandas as pd


# Khởi tạo thư viện mediapipe
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

def make_landmark_timestep(results):
    #print(results.pose_landmarks.landmark)
    c_lm = []
    for id, lm in enumerate(results.pose_landmarks.landmark):
        c_lm.append(lm.x)
        c_lm.append(lm.y)
        c_lm.append(lm.z)
        c_lm.append(lm.visibility)
    return c_lm

def draw_landmark_on_image(mpDraw, results, img):
    # Vẽ các đường nối
    mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

    # Vẽ các điểm nút
    for id, lm in enumerate(results.pose_landmarks.landmark):
        h, w, c = img.shape
        print(id, lm)
        cx, cy = int(lm.x * w), int(lm.y * h)
        cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
    return img


def frames_extraction(video_path):
    # Declare a list to store video frames.
    frames_list = []

    # Read the Video File using the VideoCapture object.
    cap = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video.
    video_frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for i in range(0,video_frames_count):
        # Nhận diện pose
        cap.set(cv2.CAP_PROP_POS_FRAMES,i)
        ret,frame=cap.read()
        cv2.imshow()
        frame = cv2.resize(frame,(720,1280))
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frameRGB)

        if results.pose_landmarks:
            # Vẽ khung xương lên ảnh
            frame = draw_landmark_on_image(mpDraw, results, frame)
            cv2.imshow("image", frame)
            key = cv2.waitKeyEx(1)  # waitKey(300)
            if key == 2424832:  # left arrow
                i=i-2
            elif key == 2555904:  # right arrow
                continue
            elif key == ord(' '):  # space
                lm = make_landmark_timestep(results)
                frames_list.append(lm)
            elif key == ord('q'):
                break


    # Return the frames list.
    return frames_list

label="annut"
lm_list=[]
lm_list=frames_extraction('../bamnut.mp4')

# Write vào file csv
df = pd.DataFrame(lm_list)
df.to_csv(label + ".txt")
