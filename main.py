import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from pyzbar.pyzbar import decode

input_dir = './data'

for j in sorted(os.listdir(input_dir)):
    img = cv2.imread(os.path.join(input_dir, j))
    
    qr_info = decode(img)

    #print (j, len(qr_info))

    for qr in qr_info:
        
        #features that we want
        data = qr.data
        rect = qr.rect
        polygon = qr.polygon

        print(data) # data
        print(rect) # size
        print(polygon) # location

        img = cv2.rectangle(img, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.width), 
                            (0,255,0), 5) 
        
        img = cv2.polylines(img, [np.array(polygon)], True, (255,0,0), 3) 

        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()