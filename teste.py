import pyautogui
import time

def teste():
    time.sleep(3.5)
    mouse = pyautogui.position()
    print(mouse)

if __name__ == '__main__':
    teste()