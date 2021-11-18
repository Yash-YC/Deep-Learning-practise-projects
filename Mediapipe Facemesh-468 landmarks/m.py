import cv2
import mediapipe as mp
import streamlit as st
import time


## Load Face Mesh
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh()


## height
wCam, hCam = 640, 480
frame = st.empty()
st.title("Control Volume Through Pinch!!")
if st.button("stop"):
    st.write("Exit")
if st.button("Give Access To WebCam : Start" ):
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    pTime = 0

    while True:
        success, img = cap.read()
        if success is not True:
            break
        rgb_image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb_image)
        

        ## getting the landmarks
        if result.multi_face_landmarks:
            for landmarks in result.multi_face_landmarks:
                for i in range(0,468):
                    x = int(landmarks.landmark[i].x * wCam)
                    y = int(landmarks.landmark[i].y * hCam)
                    cv2.circle(img,(x,y), 1, (255,0,255), 1)
                    # cv2.putText(img,str(i),(x,y),0,0.2,(0,0,0))
        else:
            pass
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0, 0), 3)


        frame.image(img, channels="BGR")
        time.sleep(0.01)
