import time

import pyautogui
from selenium.webdriver.common.by import By

import log
import navegador
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

def incluir_promo():
    user = "ranny"  # Setando usuário
    button_xpath = '//*[@id="app-root-wrapper"]/div[1]/div/div[1]/div[6]/div/div/div/div/div[3]/div/div[1]/div/div[3]/button' #Botão Participar
    button_xpath2 = '//*[@id="app-root-wrapper"]/div[1]/div/div[1]/div[6]/div/div/div/div/div[3]/div/div[2]/div[2]/div[3]/button'
    #autoparts = '//*[@id="app-root-wrapper"]/div[1]/div/div[1]/div[5]/div/div/div/div/div[3]/div/div[1]/span'
    #ofertas = '//*[@id="app-root-wrapper"]/div[1]/div/div[1]/div[5]/div/div/div/div/div[3]/div/div[2]/span'
    _url = "https://www.mercadolivre.com.br/anuncios/lista/promos?page=1&search="
    _url2 = ""
    em_processo = True
    cods_mlbs = []
    status_list = []
    status = ''
    cods_alterados = []
    have_autoparts = False

    df_base = pd.read_excel('promo catalisadores zx49 soescap.xlsx')
    print(df_base)
    rows = len(df_base.index)
    i = 0

    while i < rows:
        linha = df_base.loc[[i]] #Localiza a linha referente ao indice 'i'
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        mlb = str(lista[0])
        mlb = mlb.replace(".0","")

        cods_mlbs.append(mlb) #Atribui a coluna 3 da linha 'i' a array cods_mlbs
        i = i+1

    print(cods_mlbs)

    # Abrindo navegador do usuário
    chrome = navegador.abrindo_navegador(user)
    chrome.maximize_window()

    i = 0

    while i < cods_mlbs.__len__():
        newurl = _url + str(cods_mlbs[i]) + _url2

        chrome.execute_script("window.open('about:blank','promo');")
        pausa_curta()
        chrome.switch_to.window('promo')
        chrome.get(newurl)
        pausa_longa()


        # try:
        #     autoparts_span = chrome.find_element(By.XPATH, autoparts)
        #     have_autoparts = True
        # except NoSuchElementException:
        #     have_autoparts = False

        # try:
        #     ofertas_span = chrome.find_element(By.XPATH, ofertas)
        #     have_ofertas = True
        # except NoSuchElementException:
        #     have_ofertas = False

        # print(have_autoparts)

        # if(have_autoparts == True and have_ofertas == True):
        try:
            button_participar = chrome.find_element(By.XPATH, button_xpath2)
            status = 'Okay'
        except NoSuchElementException:
            try:
                button_participar = chrome.find_element(By.XPATH, button_xpath)
                status = 'Okay'
            except NoSuchElementException:
                status = 'Erro'

        print(cods_mlbs[i])
        print(status)

        time.sleep(1)

        if(status == 'Okay'):
            button_participar.click()
            pausa_curta()
            pyautogui.click(x=562, y=832)

        status_list.append(status)
        cods_alterados.append(cods_mlbs[i])

        pausa_longa()

        i = i+1

    log.log_promo(status_list, cods_alterados)

def pausa_longa():
    time.sleep(4.5)

def pausa_curta():
    time.sleep(2)

if __name__ == '__main__':
    incluir_promo()