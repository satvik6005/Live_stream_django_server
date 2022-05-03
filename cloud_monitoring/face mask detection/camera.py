from keras.models import load_model
import cv2 as cv
import cv2
import numpy as np

model = load_model('models/model10.model')

face_clsfr=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

source=cv2.VideoCapture(0)

labels_dict={0:'MASK',1:'NO MASK'}
color_dict={0:(0,255,0),1:(0,0,255)}

while(True):
    
    ret,img=source.read()
    print(img.shape)
    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    #cv.imshow("live",gray)
    print(gray.shape)
    faces=face_clsfr.detectMultiScale(gray,1.3,5)  

    for (x,y,w,h) in faces:
    
        face_img=gray[y:y+w,x:x+w]
        resized=cv2.resize(face_img,(128,128))
        normalized=resized/255.0
        reshaped=np.reshape(normalized,(1,128,128,1))
        result=model.predict(reshaped)

        label=np.argmax(result,axis=1)[0]
      
        cv.rectangle(img,(x,y),(x+w,y+h),color_dict[label],2)
        cv.rectangle(img,(x,y-40),(x+w,y),color_dict[label],-1)
        cv.putText(img, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        
        
    cv.imshow('LIVE VIDEO',img)
    key=cv.waitKey(1)
    
    if(key==27): 
        break
        
cv.destroyAllWindows()
source.release()