import pickle

import cv2
import mediapipe as mp
import numpy as np

model_dict1 = pickle.load(open('./model1.p', 'rb'))
model_dict2 = pickle.load(open('./model2.p', 'rb'))
model1 = model_dict1['model1']
model2 = model_dict2['model2']

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)


# labels_dict1 = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 11: 'C', 18: 'I',
#                   21: 'L', 24: 'O', 30: 'U', 31: 'V', 9: 'A', 10: 'B', 12: 'D', 13: 'E', 14: 'F', 15: 'G',
#                   16: 'H', 19: 'J', 20: 'K', 22: 'M', 23: 'N', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T',
#                   32: 'W', 33: 'X', 34: 'Y', 35: 'Z'}

labels_dict1 = {}

for i in range(36):
    if i < 9:
        value = str(i + 1)
    else:
        value = chr(i - 9 + ord('A'))
    labels_dict1[i] = value

# print(labels_dict1)
# labels_dict2 = labels_dict1

while True:

    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        n = len(results.multi_hand_landmarks)
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        if n == 1:

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            prediction1 = model1.predict([np.asarray(data_aux)])
            print(prediction1[0])

            predicted_character1 = labels_dict1[int(prediction1[0])]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character1, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)
        else:
            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            prediction2 = model2.predict([np.asarray(data_aux)])
            print(prediction2[0])

            predicted_character2 = labels_dict1[int(prediction2[0])]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character2, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)

    cv2.imshow('frame', frame)
    cv2.waitKey(25)

cap.release()
cv2.destroyAllWindows()
