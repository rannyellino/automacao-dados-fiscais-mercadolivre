import pyautogui
import pyperclip
import time
import webbrowser
from tkinter import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def teste():
    janela = Tk()
    time.sleep(3)
    mouse = pyautogui.position()
    print(mouse)
    s = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument(r"user-data-dir=C:\Users\Rannyel\AppData\Local\Google\Chrome\User Data")
    chrome = webdriver.Chrome(service=s, options=options)
    chrome = chrome.get("https://google.com.br")
    time.sleep(3)

def um_segundo():
    time.sleep(1)

if __name__ == '__main__':
    teste()

