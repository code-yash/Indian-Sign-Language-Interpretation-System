import os
import numpy as np
import cv2

DATA_DIR = './data2'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 13  # Updated to 13 for 0 to 12 classes
dataset_size = 150

cap = cv2.VideoCapture(0)
class_to_collect = 12  # Set to the desired class (class 12 in this case)

if not os.path.exists(os.path.join(DATA_DIR, str(class_to_collect))):
    os.makedirs(os.path.join(DATA_DIR, str(class_to_collect)))

print('Collecting data for class {}'.format(class_to_collect))

done = False
while True:
    ret, frame = cap.read()
    cv2.putText(frame, 'Ready? Press "S" to Start Capturing ! :)', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    if cv2.waitKey(25) == ord('s'):
        break

counter = 0
while counter < dataset_size:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    cv2.waitKey(25)
    cv2.imwrite(os.path.join(DATA_DIR, str(class_to_collect), '{}.jpg'.format(counter)), frame)

    counter += 1

cap.release()
cv2.destroyAllWindows()
