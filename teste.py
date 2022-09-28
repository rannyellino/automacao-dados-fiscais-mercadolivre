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
from datetime import datetime

def teste():
    janela = Tk()
    s = Service(ChromeDriverManager().install()) #instala o drive do chrome que precisa
    options = Options()
    options.add_argument(r"user-data-dir=C:\Users\Rannyel\AppData\Local\Google\Chrome\User Data") #pega perfil do chrome
    chrome = webdriver.Chrome(service=s, options=options)
    chrome = chrome.get("https://myaccount.mercadolivre.com.br/fiscal-information/item/MLB2780157104") #abri navegador na url

    time.sleep(5)

    pyautogui.click(x=1272, y=325, clicks=3) # pega título do produto
    copiar() #copia o titulo
    titulo = janela.clipboard_get() #coloca a copia do titulo dentro de uma variavel

    titulo_pronto = titulo.casefold() #transforma toda string em minusculo
    print(titulo_pronto)
    titulo_split = titulo_pronto.rsplit(" ") #separa a string dentro de uma lista separando cada valor entre um espaço " "
    print(titulo_split)
    print(type(titulo_split))

    #Checa se algumas das palavras contem a palavra catalisador para saber se precisa trocar os valores fiscais
    for texto in titulo_split:
        if(texto == "catalisador"):
            print(texto)
            print("É catalisador")
        else:
            print(texto)
            print("não é catalisador")

    mouse = pyautogui.position()
    print(mouse)

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
    chrome.get("https://myaccount.mercadolivre.com.br/fiscal-information/item/MLB2780157104") #abri o chrome com o endereço indicado
    print(chrome)
    return chrome

def um_segundo():
    time.sleep(1)

def copiar():
    pyautogui.hotkey("ctrl", "c")

if __name__ == '__main__':
    teste2()