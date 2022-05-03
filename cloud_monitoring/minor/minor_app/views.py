import time

import cv2
import numpy as np
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from keras.models import load_model


def load_process():
    model = load_model(r'/home/abhimanyu/PycharmProjects/pythonProject/minor/minor_app/model10.model')
    face_clsfr = cv2.CascadeClassifier(
        r'/home/abhimanyu/PycharmProjects/pythonProject/minor/minor_app/haarcascade_frontalface_default.xml')
    labels_dict = {0: 'MASK', 1: 'NO MASK'}
    color_dict = {0: (0, 255, 0), 1: (0, 0, 255)}
    return model, face_clsfr, labels_dict, color_dict


def detection(img, model, face_clsfr, labels_dict, color_dict):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_clsfr.detectMultiScale(gray, 1.3, 5)


    for (x, y, w, h) in faces:
        face_img = gray[y:y + w, x:x + w]
        resized = cv2.resize(face_img, (128, 128))
        normalized = resized / 255.0
        reshaped = np.reshape(normalized, (1, 128, 128, 1))
        result = model.predict(reshaped)

        label = np.argmax(result, axis=1)[0]

        cv2.rectangle(img, (x, y), (x + w, y + h), color_dict[label], 2)
        cv2.rectangle(img, (x, y - 40), (x + w, y), color_dict[label], -1)
        cv2.putText(img, labels_dict[label], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    return img

path = r'/home/abhimanyu/PycharmProjects/pythonProject/minor/latest/latest.jpg'
var = None

model, face_clsfr, labels_dict, color_dict = load_process()


def index(request):
    return render(request, 'minor_app/index.html')


def gen():
    global var
    while True:
        try:
            time.sleep(0.04)
            print("retriving")
            # frame = cv2.imread(path)
            var = detection(var, model, face_clsfr, labels_dict, color_dict)
            jpeg = cv2.imencode('.jpg', var)[1]

            frame = jpeg.tobytes()

            print('sending')
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except:
            continue


def video_feed(request):
    print(request.method)
    return StreamingHttpResponse(gen(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


@csrf_exempt
def new(request):
    global var

    if request.method == 'POST':
        print("image recieved!")
        image = np.asarray(bytearray(request.body), dtype="uint8")

        var = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imwrite(path, var)

    return HttpResponse('did it')
