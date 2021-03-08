import facial_emotion_recognition as EmotionRecognition
import cv2 as cv

er = EmotionRecognition(device='gpu', gpu_id=0)

cam = cv.VideoCapture(0)

success, frame = cam.read()

frame = er.recognise_emotion(frame, return_type='BGR')

cv.imshow("frame", frame)

while True:
    key = cv.waitKey(10)
    if key & 0xff == 27:
        break