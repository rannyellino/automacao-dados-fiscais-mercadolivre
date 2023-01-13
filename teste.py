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
    df_base = pd.read_excel('DESC_TESTE2.xlsx')
    print(df_base)

    #Guardando os valores de uma linha dentro de uma variavel
    linha = df_base.loc[[4]]
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

    # Continua eliminando caracteres a mais que não sejam códigos
    codigos = codigos.replace(":", "")
    codigos = codigos.replace("(Brinde)", "")
    codigos = codigos.replace(" ", "")
    codigos = codigos.replace("LinhaPesada", "")
    codigos = codigos.replace("+", ",")

    # Após limpar toda a string e deixar apenas os códigos separados por "," vamos guardar os códigos como uma lista
    lista_codigos = codigos.split(",")
    print(lista_codigos.__len__())

    print("Lista Códigos", lista_codigos)
    print(type(lista_codigos))

def teste2():
    df_base = pd.read_excel('DESC_TESTE8.xlsx')
    linha = df_base.loc[[2]]
    lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
    print(lista)

    desc = str(lista[4])

    have_zx = False
    have_px = False
    zx = "ZX"
    px = "PX"
    acoes = []
    zx_cods = []
    px_cods = []
    lista_zx_real = []
    lista_px_real = []
    px_real_string = ""
    zx_real_string = ""
    print(acoes)

    #Adicionar números das ações
    for i in range(50):
        acoes.append(i)

        # Agora começa a procurar códigos ZX e PX dentro da descrição e adiciona eles em uma lista para dar como feedback depois
        for i in range(50):
            have_zx = False
            have_px = False
            # Atribui o número de "i" para as nomeclaturas de ações ZX e PX
            zx_real = zx + str(acoes[i])
            px_real = px + str(acoes[i])

            # Começa a checar agora os códigos ZX
            if (desc.find(zx_real) != -1):  # Checa se na descrição achou algum código ZX
                # As três linhas abaixo são para limpar a string 'desc' para ficar apenas os códigos ZX caso tenha achado
                indice_desc_zx = desc.find(zx_real)
                zx_real_string = desc[0: 0:] + desc[indice_desc_zx::]
                print(zx_real_string)

                # Caso tenha mais de um código vamos transformar esses códigos em lista para checar depois quais são esses códigos ZX
                if (zx_real_string.find(" ") != -1):
                    zx_replace = zx_real_string.replace(" ", ",")
                    lista_zx_real = zx_replace.split(",")
                    print(lista_zx_real)

                # Caso realmente tenha mais de um código e tenha transformado em uma lista esses códigos ZX ele vai checar se o valor da lista
                # É igual o valor da variavel 'zx_real', isso porque as vezes o código zx_real = ZX1 e ele achando duas vezes ou mais na descrição valores
                # Com o valor ZX1, Exemplo: 'ZX1', 'ZX11', 'ZX12', etc. Com isso acontecendo o if e for abaixo resolve isso pois ele vai checar qual desses códigos
                # Está de fato certo
                if (lista_zx_real.__len__() > 0):
                    for i in range(lista_zx_real.__len__()):
                        if (lista_zx_real[i] == zx_real):
                            zx_cods.append(zx_real)
                            have_zx = True
                elif (zx_real_string == zx_real):
                    zx_cods.append(zx_real)
                    have_zx = True

            # Começa a checar agora os códigos PX
            if (desc.find(px_real) != -1):  # Checa se na descrição achou algum código ZX
                # As três linhas abaixo são para limpar a string 'desc' para ficar apenas os códigos ZX caso tenha achado
                indice_desc_px = desc.find(px_real)
                px_real_string = desc[0: 0:] + desc[indice_desc_px::]
                print(px_real_string)

                # Caso tenha mais de um código vamos transformar esses códigos em lista para checar depois quais são esses códigos ZX
                if (px_real_string.find(" ") != -1):
                    px_replace = px_real_string.replace(" ", ",")
                    lista_px_real = px_replace.split(",")
                    print(lista_px_real)

                # Caso realmente tenha mais de um código e tenha transformado em uma lista esses códigos ZX ele vai checar se o valor da lista
                # É igual o valor da variavel 'zx_real', isso porque as vezes o código zx_real = ZX1 e ele achando duas vezes ou mais na descrição valores
                # Com o valor ZX1, Exemplo: 'ZX1', 'ZX11', 'ZX12', etc. Com isso acontecendo o if e for abaixo resolve isso pois ele vai checar qual desses códigos
                # Está de fato certo
                if (lista_px_real.__len__() > 0):
                    for i in range(lista_px_real.__len__()):
                        if (lista_px_real[i] == px_real):
                            px_cods.append(px_real)
                            have_px = True
                elif (px_real_string == px_real):
                    px_cods.append(px_real)
                    have_px = True

        # if(lista_px_real.__len__() <= 0 and px_real_string != px_real):
        # px_cods.append("None")
        # if(lista_zx_real.__len__() <= 0 and zx_real_string != zx_real):
        # zx_cods.append("None")
        if (have_zx == False):
            zx_cods.append("None")
        if (have_px == False):
            px_cods.append("None")

        print("Codigos ZX achados:", zx_cods)
        print("Codigos PX achados:", px_cods)

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
    teste2()