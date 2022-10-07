import pyautogui
import pyperclip
import time
import webbrowser
from tkinter import *
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def teste():
    janela = Tk()
    user = "Rannyel"
    chrome = abrindo_navegador(user)
    chrome.maximize_window()
    time.sleep(10)
    pyautogui.scroll(-1000)
    try:
        #print(chrome.page_source)
        time.sleep(10)
        chrome.switch_to.frame(chrome.find_element(By.XPATH, "//html//body//div[1]//div//div[3]//div[1]//div//div[2]//div//iframe[@id='centro']"))
        print("Entrou no iframe")
        time.sleep(2)
        ean_element = chrome.find_element(By.XPATH, "//input[@id='ProductEan']")
        ean_preenchido = ean_element.get_attribute('value')
        ean_preenchido = str(ean_preenchido)
        time.sleep(2)
        print("Meu EAN: {}".format(ean_preenchido))
        print("Achou EAN")
    except TimeoutException:
        print("Não achou o EAN")
    time.sleep(2)

def teste2():
    janela = Tk()
    user = "Rannyel"
    conta = "1"
    chrome = abrindo_navegador(user)
    locations = []

    with open("Loc Elementos.txt", 'r') as arquivo:
        for linha in arquivo:
            linha = linha.replace("(","").replace(")","").replace("\n","")
            print(linha)
            locations.append(linha)
    arquivo.close()

    #locations = dict(locations)
    print(locations)
    print(type(locations))
    time.sleep(2)


    um_produto = str(locations[9]).replace(",","\n")
    um_produto = um_produto.split('\n')
    firstTime = 0
    for linha in um_produto:
        print(linha)
        if(firstTime == 0):
            um_produto_loc_x = linha.strip()
            firstTime = 1
        um_produto_loc_y = linha.strip()
    firstTime = 0
    print('X {}'.format(um_produto_loc_x))
    print('Y {}'.format(um_produto_loc_y))
    um_produto_loc_x = int(um_produto_loc_x)
    um_produto_loc_y = int(um_produto_loc_y)

    pyautogui.click(um_produto_loc_x, um_produto_loc_y)

    time.sleep(5)

    pyautogui.click(locations[0]) #Clica nos valores de X e Y do elemento
    time.sleep(1)
    pyautogui.hotkey("ctrl", "a")
    copiar()
    sku = janela.clipboard_get()
    print(sku)
    time.sleep(1)
    mouse = pyautogui.position()
    print(mouse)

def abrindo_navegador(user):
    # Abrindo Chrome(NAVEGADOR PADRÃO DO WINDOWS)
    s = Service(ChromeDriverManager().install())
    options = Options() #Para poder pegar o perfil do chrome
    options.add_argument(r"user-data-dir=C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(user)) #Indicado diretorio do perfil do chrome
    chrome = webdriver.Chrome(service=s, options=options) #Passando parametros do chrome
    chrome.maximize_window()
    chrome.get("https://www.scapja.com.br/admin/#/mvc/adm/products/edit/3") #abri o chrome com o endereço indicado
    print(chrome)
    return chrome

def um_segundo():
    time.sleep(1)

def copiar():
    pyautogui.hotkey("ctrl", "c")

if __name__ == '__main__':
    teste()