import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import streamlit as st


st.title("Distance and EyeBlink detection")
frame = st.empty()

col1,col2 = st.columns(2)

if col2.button("stop"):
    frame = st.empty()
if col1.button("Start Video" ):
    FRAME_WINDOW = st.image([])
    FRAME_WINDOW1 = st.image([])

    cap = cv2.VideoCapture('Blink.mp4')

    detector = FaceMeshDetector(maxFaces = 1)


    plotY = LivePlot(640,360,[25,50],invert = True)
    idList = [22, 23, 24 ,26, 110 ,157, 158 , 159 ,160 ,161, 130, 243]

    ratioList = []
    BlinkCounter = 0
    counter = 0
    color = (255, 0, 255 )

    while True:

        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        success,img = cap.read()
        if not success:
            break
        img, faces = detector.findFaceMesh(img, draw = False)

        if faces:
            face = faces[0]
            pointLeft = face[145]
            pointRight = face[374]
            leftup = face[159]
            leftdown  = face[23]
            leftLeft = face[130]
            leftright = face[243]
            lenVer,_ = detector.findDistance(leftup, leftdown)
            lenhor,_ = detector.findDistance(leftLeft, leftright)

            ratio = (lenVer/lenhor)*100
            ratioList.append((ratio))
            if len(ratioList)>3:
                ratioList.pop(0)
            ratioAvg = sum(ratioList) / len(ratioList)

            if ratioAvg < 36 and counter == 0:
                BlinkCounter +=1 
                color = (0,200,0)
                counter = 1
            if counter != 0 :
                counter +=1 
                if counter > 15:
                    counter = 0
                    color = (255,0,255)

            cvzone.putTextRect(img, f"BlinkCount:{BlinkCounter}", (10,50),colorR=color)
            imgplot = plotY.update(ratioAvg,color)        
        
            w,_ = detector.findDistance(pointLeft , pointRight)
            W = 6.3 #average value for male,Female
            # d = 50
            # f = (w*d)/W
            # print(f)   

            f = 700
            d = (W*f)/w

            cvzone.putTextRect(img , f"Dept: {int(d)}cm ",(face[10][0]-100, face[10][1] - 20 ),scale = 2)
            img = cv2.resize(img, (640, 360))
            img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
            # FRAME_WINDOW.image(img, use_column_width=True)
            # FRAME_WINDOW1.image(imgplot,use_column_width=True)
            FRAME_WINDOW.image(img, use_column_width=True)
            FRAME_WINDOW1.image(imgplot,use_column_width=True)

    
        else:
            st.write("stopped")
        cv2.waitKey(1)

