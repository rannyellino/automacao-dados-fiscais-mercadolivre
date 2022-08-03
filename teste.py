import pyautogui
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def teste():
    conta = 2
    time.sleep(3.5)
    #mouse = pyautogui.position()
    #print(mouse)

    pyautogui.click(x=710, y=186)
    um_segundo()
    if (conta == 1):  # Se for ScapJá
        pyautogui.click(x=807, y=373)  # Pinta de verde para indicar que é a conta SCAPJÁ
        um_segundo()
    elif (conta == 2):
        pyautogui.click(x=783, y=378)  # Pinta de amarelo para indicar que é a conta SoEscap
        um_segundo()


    """driver = webdriver.Chrome(executable_path=r"C:\chromedriver_win32\chromedriver.exe")
    driver.maximize_window()
    time.sleep(2)
    driver.get("http://google.com")
    time.sleep(5)"""

def um_segundo():
    time.sleep(1)

if __name__ == '__main__':
    teste()

