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
    tabela = ["SÃO PAULO", "47,00", "SANTA CATARINA", "56,90", "PARANA", "56,90", "DISTRITO FEDERAL", "67,90",
              "MINAS GERAIS", "67,90", "RIO DE JANEIRO", "67,90", "ESPIRITO SANTO", "67,90", "RIO GRANDE DO SUL", "67,90", "MATO GROSSO DO SUL",
              "82,90", "PE - BA - SE","93,00", "CE - GO - MT - RN - PB - AL", "105,90", "MA - PI", "115,00",
              "DEMAIS ESTADOS FAZER COTAÇÃO NAS PERGUNTAS","R$999,99"]  # TABELA DE FRETE PARA ADICIONAR NOS ANUNCIOS
    user = "Rannyel"
    chrome = abrindo_navegador(user)
    chrome.maximize_window()
    estado_xpath = "//*[@id='shipping_task']//div[2]//div[1]//div//div[2]//div[2]//div//div[2]//div[2]//div//ul//li[{}]//div//label[1]//div[1]//input"
    valor_xpath = "//*[@id='shipping_task']//div[2]//div[1]//div//div[2]//div[2]//div//div[2]//div[2]//div//ul//li[{}]//div//label[2]//div[1]//input"
    i_estado = 1
    i_valor = 1
    time.sleep(5)

    # Agora iremos começar a preencher de fato a tabela de frete, mas antes precisamos fazer alguns clicks em alguns elementos do HTML para poder ter a tabela
    try:
        chrome.find_element(By.XPATH,
                            "//*[@id='shipping_header_container']//div//div[1]//h2").click()  # Faz o primeiro clique em 'Forma de entrega'
        print("Clicou pela 1x")
        um_segundo()
        element2 = chrome.find_element(By.XPATH,
                                       "//*[@id='shipping_task']//div[2]//div[1]//div//div[2]//div[1]//label//span[1]")  # Apenas acha o elemento para clicar depois
        um_segundo()
        chrome.execute_script("arguments[0].click();", element2)  # Faz o segundo clique em 'Faço envio por minha conta'
        print("Clicou pela 2x")
        element3 = chrome.find_element(By.XPATH,
                                       "//*[@id='shipping_task']//div[2]//div[1]//div//div[2]//div[2]//div//div[2]//div[1]//label//span")  # Apenas acha o elemento para clicar depois
        um_segundo()
        chrome.execute_script("arguments[0].click();", element3)  # Faz o terceiro clique em 'Por conta do comprador'
        print("Clicou pela 3x")
        # AGORA FALTA ADICIONAR TODOS OS CAMPOS NECESSARIOS E PREENCHE-LOS
        for i in range(10):
            adicionar = chrome.find_element(By.XPATH,
                                            "//*[@id='shipping_task']//div[2]//div[1]//div//div[2]//div[2]//div//div[2]//div[2]//div//a")
            chrome.execute_script("arguments[0].click();", adicionar)
            um_segundo()
        i = 0  # Esse servira como indice tanto pro nosso laço quanto pra saber qual valor da tabela ele tem que pegar e colocar nos campos do frete
        while i < 26:
            estado = chrome.find_element(By.XPATH, estado_xpath.format(
                i_estado))  # pega o elemento que será o estado na tabela de frete
            estado.send_keys(tabela[i])  # coloca o valor correto do estado nesse campo
            i = i + 1  # adiciona mais 1 no indice para saber que agora terá que usar o proximo valor da nossa lista 'tabela'
            um_segundo()
            valor = chrome.find_element(By.XPATH, valor_xpath.format(
                i_valor))  # pega o elemento que será o valor de custo na tabela de frete
            valor.send_keys(tabela[i])  # coloca o valor correto  nesse campo
            i = i + 1  # adiciona mais 1 no indice para saber que agora terá que usar o proximo valor da nossa lista 'tabela'
            i_estado = i_estado + 1  # Faz soma pra ir pro proximo 'li' do html
            i_valor = i_valor + 1  # Faz soma pra ir pro proximo 'li' do html
        i_estado = 1  # Será usado para saber qual é o 'li' que estamos usando na lista/tabela de html do frete
        i_valor = 1  # Será usado para saber qual é o 'li' que estamos usando na lista/tabela de html do frete
        um_segundo()
        print("Finalizou de preencher")
        time.sleep(5)
    except NoSuchElementException:
        print("Não achou o ELEMENTO")

def teste2():
    tabela = ["SÃO PAULO", "47,00", "SANTA CATARINA", "56,90", "PARANA", "56,90", "DISTRITO FEDERAL", "67,90",
              "MINAS GERAIS", "67,90", "RIO DE JANEIRO", "67,90", "ESPIRITO SANTO", "67,90", "RIO GRANDE DO SUL",
              "67,90", "MATO GROSSO DO SUL",
              "82,90", "PE - BA - SE", "93,00", "CE - GO - MT - RN - PB - AL", "105,90", "MA - PI", "115,00",
              "DEMAIS ESTADOS FAZER COTAÇÃO NAS PERGUNTAS", "R$999,99"]  # TABELA DE FRETE PARA ADICIONAR NOS ANUNCIOS
    tamanho = tabela.__len__()
    print(tamanho)

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