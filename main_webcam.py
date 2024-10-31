import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    qr_info = decode(frame)

    if len(qr_info) > 0:
        qr = qr_info[0]

        #features that we want
        data = qr.data # data
        rect = qr.rect # size
        polygon = qr.polygon # location

        frame = cv2.rectangle(frame, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.width), 
                            (0,255,0), 5) 
        
        frame = cv2.polylines(frame, [np.array(polygon)], True, (255,0,0), 3) 

    cv2.imshow('webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()