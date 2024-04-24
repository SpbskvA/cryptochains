import cv2
import keyboard

path = "C:\\Users\\Andrey\\PycharmProjects\\shorts-server"
web_num = 2

cap = cv2.VideoCapture(web_num)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def on_triggered():
    ret, frame = cap.read()
    cv2.imwrite(f'{path}\\frame.png', frame)
    ret, frame = cap.read()
    cv2.imwrite(f'{path}\\frame.png', frame)
    print(1)


keyboard.add_hotkey('ctrl+shift', on_triggered)
keyboard.wait('esc+ctrl+shift')
cap.release()
