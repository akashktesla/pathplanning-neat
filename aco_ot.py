import cv2 as cv
import numpy as np
from aco import aco_tracking

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv.resize(frame,(500,500))
    target = cv.imread("target.png")
    target = cv.resize(target,(100,100))
    _index,confidence = aco_tracking(frame,target,loop_count=10)
    print(f"index:{_index}")
    # if confidence>0.5:
    #     cv.circle(frame, (_index[0], _index[1]), 5, (0, 255, 0), 2)
    #     print(frame.shape)

    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

