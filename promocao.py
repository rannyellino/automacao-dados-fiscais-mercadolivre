import time

import pyautogui
from selenium.webdriver.common.by import By

import log
import navegador
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException

def incluir_promo():
    user = "Administrator"  # Setando usuario
    button_xpath = '/html/body/main/div/div/div[2]/div/div[1]/div/div[1]/div[6]/div/div/div[3]/div[1]/div[1]/div[4]/button' #Botão Participar
    button_xpath2 = '/html/body/main/div/div/div[2]/div/div[1]/div/div[1]/div[6]/div/div/div[3]/div[1]/div[2]/div[4]/button'
    button_xpath3 = '/html/body/main/div/div/div[2]/div/div[1]/div/div[1]/div[6]/div/div/div/div/div[4]/div[1]/div[3]/div/div[3]/button'
    #autoparts = '//*[@id="app-root-wrapper"]/div[1]/div/div[1]/div[5]/div/div/div/div/div[3]/div/div[1]/span'
    #ofertas = '//*[@id="app-root-wrapper"]/div[1]/div/div[1]/div[5]/div/div/div/div/div[3]/div/div[2]/span'
    _url = "https://www.mercadolivre.com.br/anuncios/lista/promos?filters=seller_campaign_offer-c-mlb961381&page=1&search="
    _url2 = "&task=c-mlb961381"
    em_processo = True
    cods_mlbs = []
    status_list = []
    status = ''
    cods_alterados = []
    have_autoparts = False

    df_base = pd.read_excel('promo catalisadores 20% scapja 08-04-24.xlsx')
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

        jump = False
        chrome.execute_script("window.open('about:blank','promo');")
        pausa_curta()
        chrome.switch_to.window('promo')
        chrome.get(newurl)
        pausa_longa()

        # try:
        #     paused_xpath = '/html/body/main/div/div/div[2]/div/div[1]/div/div[1]/div[6]/div/div/div/div/div[3]/p[1]'
        #     p_paused = chrome.find_element(By.XPATH, paused_xpath)
        #     jump = True
        #     i = i + 1
        # except NoSuchElementException:
        #     jump = False

        print("Jump: {}".format(jump))

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
        if(jump == False):
            try:
                button_participar = chrome.find_element(By.XPATH, button_xpath2)
                button_text = button_participar.text
                if(button_text == "Deixar de participar"):
                    status = 'Erro'
                else:
                    status = 'Okay'
                    print("button_xpath2")
            except NoSuchElementException:
                try:
                    button_participar = chrome.find_element(By.XPATH, button_xpath)
                    button_text = button_participar.text
                    if (button_text == "Deixar de participar"):
                        status = 'Erro'
                    else:
                        status = 'Okay'
                        print("button_xpath")
                except NoSuchElementException:
                    # try:
                    #     button_participar = chrome.find_element(By.XPATH, button_xpath)
                    #     status = 'Okay'
                    # except NoSuchElementException:
                         status = 'Erro'

            print(cods_mlbs[i])
            print(status)

            time.sleep(1)

            if(status == 'Okay'):
                try:
                    button_participar.click()
                except (StaleElementReferenceException, NoSuchElementException) as e:
                    status = 'Error'
                pausa_curta()
                button_click_x = '/html/body/div[6]/div/div/div[2]/div[3]/button[1]'
                try:
                    button_click = chrome.find_element(By.XPATH, button_click_x)
                    button_click.click()
                    status = 'Okay'
                except NoSuchElementException:
                    time.sleep(1.25)
                    try:
                        button_click = chrome.find_element(By.XPATH, button_click_x)
                        button_click.click()
                        status = 'Okay'
                    except NoSuchElementException:
                        status = 'Erro'
                except ElementClickInterceptedException:
                    print("ElementClickInterceptedException")
                    status = 'Erro'

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