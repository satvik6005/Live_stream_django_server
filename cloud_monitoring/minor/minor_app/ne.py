import requests
import cv2
import numpy as np
from time import sleep


vid=cv2.VideoCapture(0)


while True:
    ret,frame=vid.read()
    img_encode = cv2.imencode('.jpg', frame)[1]
    data_encode = np.array(img_encode)
    str_encode = data_encode.tobytes()
    print(len(str_encode))
    url = 'http://127.0.0.1:8000/new'
    r = requests.post(url=url, data=str_encode)
    print(r)
    sleep(0.04)







