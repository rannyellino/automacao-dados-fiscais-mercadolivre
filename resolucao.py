import navegador
import elementos
import log
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def pegando_resolucao_elementos(entry_user):
    user = entry_user.get() #Púxa o valor de Usuario do Chrome da interface
    print(user)
    chrome = navegador.abrindo_navegador(user) #Chama função para abrir o navegador
    chrome.maximize_window() #Maxima a Tela
    chrome.get("https://myaccount.mercadolivre.com.br/fiscal-information/item/MLB2780140143") # entra em um link de anuncio sem DADOS FISCAIS

    loc_um_produto = elementos.inicio_fiscais_elementos_location(chrome) #Chama função pra pegar a localização do botão "Possui apenas um produto"
    print(loc_um_produto)

    time.sleep(2)

    chrome.get("https://myaccount.mercadolivre.com.br/fiscal-information/item/MLB2709356074") #Entra no link de um anuncio com DADOS FISCAIS

    time.sleep(5)

    locations = elementos.fiscais_elementos_location(chrome)#Chama função pra pegar todos as localizações dos elementos dos dados fiscais
    print(locations)

    log.log_elementos(locations, loc_um_produto)





