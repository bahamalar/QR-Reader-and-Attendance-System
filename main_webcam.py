import os
import datetime
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

from pyzbar.pyzbar import decode

with open('./whitelist.txt','r') as f:
    authorized_users = [l.strip() for l in f.readlines() if len(l) > 2]

log_path = './log.txt'
most_recent_access = {}
time_between_logs_th = 5

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    qr_info = decode(frame)

    if len(qr_info) > 0:
        qr = qr_info[0]

        #features that we want
        data = qr.data # data, bytes formatında
        rect = qr.rect # size
        polygon = qr.polygon # location

        if data.decode() in authorized_users:
            cv2.putText(frame, 'ACCESS GRANTED', (rect.left, rect.top-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,225,0), 3)
            
            if data.decode() not in most_recent_access.keys() \
                    or time.time() - most_recent_access[data.decode()] > time_between_logs_th:
                most_recent_access[data.decode()] = time.time()
                with open(log_path, 'a') as f:
                    f.write('{},{}\n'.format(data.decode(), datetime.datetime.now()))
        else:
            cv2.putText(frame, 'ACCESS DENIED', (rect.left, rect.top-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,225), 3)

        frame = cv2.rectangle(frame, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.width), 
                            (0,255,0), 5) 
        
        frame = cv2.polylines(frame, [np.array(polygon)], True, (255,0,0), 3) 

    cv2.imshow('webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()