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
from datetime import datetime

def teste():
    janela = Tk()
    s = Service(ChromeDriverManager().install()) #instala o drive do chrome que precisa
    options = Options()
    options.add_argument(r"user-data-dir=C:\Users\Rannyel\AppData\Local\Google\Chrome\User Data") #pega perfil do chrome
    chrome = webdriver.Chrome(service=s, options=options)
    chrome = chrome.get("https://myaccount.mercadolivre.com.br/fiscal-information/item/MLB2762589755") #abri navegador na url

    time.sleep(10)

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
    cod_finalizados = []
    cod_erros = []
    print(cod_finalizados)
    print(cod_erros)
    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S')  # Pega a data e hora atual e já formata
    nome_arquivo = 'Log ' + str(data_hora) + '.txt'  # Salva a data e hora atual formatada em STRING e adiciona a extensão que quero do arquivo TXT

    if(cod_finalizados != []):
        with open(nome_arquivo,"w") as arquivo:  # Cria o arquivo TXT com o nome certo e começa a escrever em cada linha os códigos que ele finalizou o processo
            for valor in cod_finalizados:
                arquivo.write(str(valor)+" FINALIZADO" + "\n")
    else:
        print("Não tem códigos finalizados")

    if(cod_erros != []):
        with open(nome_arquivo, "a") as arquivo:
            for valor in cod_erros:
                arquivo.write(str(valor)+" VERIFICAR" + "\n")
    else:
        print("Não tem códigos com erros")

def um_segundo():
    time.sleep(1)

def copiar():
    pyautogui.hotkey("ctrl", "c")

if __name__ == '__main__':
    teste()

