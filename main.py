import cv2 as cv
import mediapipe as mp
import serial
import time

ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

def encenderLed(color, relleno):
    if relleno == -1:
        if color == (0,255,0):
            ser.write(b'G')
        elif color == (0,0,255):
            ser.write(b'R')
    else:
        ser.write(b'N')

def drawRect(x, y, color, hx, hy):
    limites = hx >= x and hx <= x+100 and hy >= y and hy <= y+40
    relleno = 2
    if(limites):
        relleno = -1 
    cv.rectangle(frame, (x,y), (x+100, y+40), color, relleno)
    encenderLed(color, relleno)

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# width = 640
# height = 480
cap = cv.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 2,
    min_detection_confidence = 0.5
) as hands:
    while True:
        ret, frame = cap.read()
        height, width, z = frame.shape
        frame = cv.flip(frame, 1)
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)
        drawRect(30, 50, (0, 255,0), 0, 0)
        drawRect(510, 50, (0, 0, 255), 0,0)
        if result.multi_hand_landmarks is not None:
            for hand_landmarks in result.multi_hand_landmarks:
                print(hand_landmarks)
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                for (i, points) in enumerate(hand_landmarks.landmark):
                    if i == 8:
                        x = int(points.x * width)
                        y = int(points.y * height)
                        drawRect(30, 50, (0, 255,0), x, y)
                        drawRect(510, 50, (0, 0, 255), x,y)
        
        cv.imshow("Frame", frame)

        if cv.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv.destroyAllWindows()