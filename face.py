import numpy as np
import cv2
import pickle



face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")


labels = {"person_name": 1}
with open("labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}





cap = cv2.VideoCapture(0)


while(True):
    #capture frame by frame
    ret , frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for(x,y,w,h) in faces:
        #print(x,y,w,h)
        #now we have to consider Region of interest , this saves only the portion we need
        roi_gray = gray[y:y+h , x:x+w] #(ycord_start , ycord_end)
        roi_color = frame[y:y+h , x:x+w]

        #this is on how to recognase, we can use deep leasrnig model like tensor flow

        id_,conf = recognizer.predict(roi_gray)
        if conf>=45 and conf <=85:
            print(id_)
            print(labels[id_])

        img_item =  "my-image.png"

        cv2.imwrite(img_item, roi_gray)# the are of interest will be saved in gray
        color = (0, 128, 0) #BGR 0-255 and 0 128 0 is for green, 256 0 0 for blue
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame , (x,y), (end_cord_x, end_cord_y), color,stroke)






    #display resulting frame
    cv2.imshow('frame' , frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


#When everything done , release the capture

cap.release()
cap.destroyAllWindoes()
