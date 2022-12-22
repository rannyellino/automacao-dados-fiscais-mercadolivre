import pyautogui
import pyperclip
import time
import webbrowser
from tkinter import *
from selenium import webdriver
import pandas as pd
import openpyxl
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

    #Lendo a tabela
    df_base = pd.read_excel('DESC_TESTE.xlsx')
    print(df_base)

    #Guardando os valores de uma linha dentro de uma variavel
    linha = df_base.loc[[1]]
    print(linha)
    lista = list(linha.values.flatten())
    print(lista)

    #LISTA
    #0 = CONTA, 1 = Código do Anúncio, 4 = Descrição, 7 = Preço de Venda
    conta = str(lista[0])
    cod = str(lista[1])
    desc = str(lista[4])
    preco = int(lista[7])

    #PROCURANDO CÓDIGO DAS PEÇAS
    variation_cod = 0 # 1 = "Código:", 2 = "Códigos"

    #Vai tentar achar a posição da palavra "Código:" se não achar vai tentar procurar a palavra "Códigos:", pois são os dois padrões que usamos
    find_cod = desc.find("Código:")
    variation_cod = 1
    if(find_cod == None or find_cod == -1):
        find_cod = desc.find("Códigos:")
        variation_cod = 2

    #Transforma em int para poder funcionar no método de exclusão de string atraves de index
    find_cod = int(find_cod)

    #Aqui adiciona mais index de acordo com a palavra achada se foi no singular ou no plural a palavra Código
    if(find_cod != None and variation_cod == 1):
        find_cod = find_cod + 5
    elif(find_cod != None and variation_cod == 2):
        find_cod = find_cod + 6
    print("Find Cod:", find_cod)

    #Vamos limpar agora a string da descrição do anúncio para ter apenas os códigos das peças
    if len(desc) > find_cod:
        codigos = desc[0: 0:] + desc[find_cod + 1::]
        codigos_len = len(codigos)
        codigos_len = int(codigos_len)

    print("Códigos:", codigos)
    print("Len Tamanho:", codigos_len)

    #Agora precisamos achar onde vai começar novamente a exclusão da string que vai ser pelas duas palavras "Para" ou "Linha" o que sobrar serão os códigos das peças mais alguns caracteres
    find_last = codigos.find("Para")
    if (find_last == None or find_last == -1):
        find_last = codigos.find("Linha")

    find_last = int(find_last)
    print("Find Last:", find_last)

    #Aqui começa a exclusão de caracteres da string baseado na posição dos caracteres
    if len(codigos) > find_last:
        codigos = codigos[0: find_last:] + codigos[codigos_len + 1::]

    print("Códigos:", codigos)

    #Continua eliminando caracteres a mais que não sejam códigos
    codigos = codigos.replace(":", "")
    codigos = codigos.replace("(Brinde)", "")
    codigos = codigos.replace(" ", "")
    codigos = codigos.replace("+", ",")
    lista_codigos = codigos.split(",")

    print("Lista Códigos", lista_codigos)
    print(type(lista_codigos))

def teste2():
    df_base = pd.read_excel('Peças-Preços.xlsx')
    print(df_base)

    df_base = pd.read_excel('Peças-Preços.xlsx')
    print(df_base)

    filtro = df_base.loc[df_base["Cod Peça"] == "13033"]  # Procura a linha com o código da peça
    print("Filtro {}".format(filtro))
    lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
    print("Lista {}".format(lista))


def abrindo_navegador(user):
    # Abrindo Chrome(NAVEGADOR PADRÃO DO WINDOWS)
    s = Service(ChromeDriverManager().install())
    options = Options() #Para poder pegar o perfil do chrome
    options.add_argument(r"user-data-dir=C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(user)) #Indicado diretorio do perfil do chrome
    chrome = webdriver.Chrome(service=s, options=options) #Passando parametros do chrome
    chrome.maximize_window()
    chrome.get("https://www.mercadolivre.com.br/anuncios/MLB2833792731/modificar/") #abri o chrome com o endereço indicado
    print(chrome)
    return chrome

def um_segundo():
    time.sleep(1)

def copiar():
    pyautogui.hotkey("ctrl", "c")

if __name__ == '__main__':
    teste()