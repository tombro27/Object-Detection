import cv2

cap = cv2.VideoCapture('vdo.mp4') # replace 'vdo.mp4' with digits(0,1,2..) to use cameras attached. 0 for default webcam.
cap.set(3, 640)
cap.set(4,480)

classes = []
with open('coco.names','rt') as f:
    classes = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    success, img = cap.read()
    classIds, confs, bbox = net.detect(img, confThreshold=0.5)
    print(classIds, bbox)
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0,255,0), thickness=2)
            cv2.putText(img,classes[classId-1].capitalize(),(int((box[0]+box[2])/2),box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)
            cv2.putText(img,str(round(confidence*100,2)),(int((box[0]+box[2])/2+250),box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)
    cv2.imshow("Image",img)
    cv2.waitKey(1)