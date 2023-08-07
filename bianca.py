import time

import pyautogui
from selenium.webdriver.common.by import By
from tkinter import *

import log
import navegador
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

def adicionar_contato(account, cod_sell, id_contact, user, janela):
    em_processo = True
    janela = janela
    user = user
    num_page = 1
    offset = 0
    start_div = 2
    found_sell = False
    sales = []
    sells_noted = []
    phone_noted = []
    links_noted = []
    ids_noted = []

    link_google = "https://contacts.google.com/new"
    link_ml_sales = "https://www.mercadolivre.com.br/vendas/omni/lista?startPeriod=WITH_DATE_CLOSED_6M_OLD&sort=DATE_CLOSED_DESC&search=&limit=50&offset="+ str(offset) +"&page="+ str(num_page) +"#"

    last_sell = cod_sell

    # Abrindo navegador do usuário
    chrome = navegador.abrindo_navegador(user)
    chrome.execute_script("window.open('about:blank','blank');")
    pausa_curta()
    chrome.switch_to.window('blank')

    sales = identify_sell(chrome, last_sell, sales)

    print("Vai printar as vendas")
    print(sales)

    while(sales.__len__() > 0):
        last_number = int(id_contact)
        account = account

        while(em_processo == True):
            print("COPIA1: {}".format(janela.clipboard_get()))
            print("Tamanho da array SALES: {}".format(sales.__len__()))
            link_sell = "https://www.mercadolivre.com.br/vendas/"+sales[sales.__len__()-1]+"/detalhe?callbackUrl=https%3A%2F%2Fwww.mercadolivre.com.br%2Fvendas%2Fomni%2Flista%3Fplatform.id%3DML%26channel%3Dmarketplace%26filters%3D%26sort%3DDATE_CLOSED_DESC%26page%3D1%26search%3D%26startPeriod%3DWITH_DATE_CLOSED_6M_OLD%26toCurrent%3D%26fromCurrent%3D"
            sell = sales[sales.__len__()-1]
            print(sales[sales.__len__()-1])
            id = str(sales.__len__()-1)
            print(id)

            pausa_curta()
            chrome.execute_script("window.open('about:blank','{}');".format(id))
            pausa_curta()
            chrome.switch_to.window("{}".format(id))
            chrome.get(link_sell)
            pausa_longa()

            name_sell_x = '//*[@id="root-app"]/div/div[1]/div/div[3]/div/div/div[2]/div/div[1]/div'
            name_sell = chrome.find_element(By.XPATH, name_sell_x)
            name_sell = name_sell.text

            name = r"{} - {} {} {}".format(str(last_number+1), name_sell, account, sell)

            print(name)

            phone = ""

            phone = identify_phone(phone, chrome, sell)

            print("TELEFONE1: {}".format(phone))
            print("TAMANHO TELEFONE: {}".format(phone.__len__()))

            pausa_curta()

            chrome.execute_script("window.open('about:blank','add_contact');")
            pausa_curta()
            chrome.switch_to.window('add_contact')
            chrome.get(link_google)
            pausa_longa()

            pyautogui.write(name)
            time.sleep(1)

            pyautogui.hotkey("tab")
            pyautogui.hotkey("tab")
            pyautogui.hotkey("tab")
            pyautogui.hotkey("tab")
            pyautogui.hotkey("tab")
            pyautogui.hotkey("tab")
            pyautogui.hotkey("tab")
            pyautogui.hotkey("tab")
            time.sleep(1)

            pyautogui.write(phone)

            #TERA QUE SER UM CLICK BASEADO NA RESOLUÇÃO DO MONITOR
            #chrome.find_element(By.XPATH, button_save_contact_x).click()
            pyautogui.click(x=1188, y=372)
            pausa_longa()

            chrome.close()
            pausa_curta()
            chrome.switch_to.window("{}".format(id))
            pausa_curta()
            chrome.close()
            chrome.switch_to.window("identify_sell")
            pausa_curta()

            sells_noted.append(sales[int(id)])
            # if(phone == "" or phone == None):
            #     phone = 61999999999
            phone_noted.append(phone)
            links_noted.append(link_sell)
            ids_noted.append(last_number)
            sales.pop(int(id))
            last_number = last_number+1
            if(sales.__len__() == 0):
                em_processo = False
                log.log_bianca(sells_noted, phone_noted, ids_noted)
                sales = []
            print(sales)

def identify_sell(chrome, last_sell, sales):
    offset = 0
    num_page = 1
    start_div = 2
    found_sell = False
    first_cicle = True

    while (found_sell == False):
        if(first_cicle == True):
            link_ml_sales = "https://www.mercadolivre.com.br/vendas/omni/lista?startPeriod=WITH_DATE_CLOSED_6M_OLD&sort=DATE_CLOSED_DESC&search=&limit=50&offset=" + str(
                offset) + "&page=" + str(num_page) + "#"

            chrome.execute_script("window.open('about:blank','identify_sell');")
            pausa_curta()
            chrome.switch_to.window('identify_sell')
            chrome.get(link_ml_sales)
            pausa_longa()
            first_cicle = False

        try:
            identify_sell_x = '//*[@id="desktop"]/div[1]/div/div[2]/div/div[3]/div[' + str(
                start_div) + ']/div/div[1]/div[1]/div[2]'

            identify_sell = chrome.find_element(By.XPATH, identify_sell_x)
            identify_sell = identify_sell.text

            if (identify_sell == last_sell):
                found_sell = True
                print("Achou a Venda")
            else:
                identify_sell = identify_sell.replace("#", "")
                print(identify_sell)
                sales.append(identify_sell)
                start_div = start_div + 1
        except NoSuchElementException:
            print("Não achou a venda na página, precisa alterar de página")
            start_div = 2
            offset = offset+50
            num_page = num_page+1
            chrome.close()
            chrome.switch_to.window('blank')
            first_cicle = True
            pausa_curta()

    return sales

def identify_phone(phone, chrome, sell):
    find_phone = ""

    try:
        div_phone = '//*[@id="row_{}_{}"]/div[3]/div[2]/div'.format(sell, sell)
        phone_element = chrome.find_element(By.XPATH, div_phone)
        phone_element = phone_element.text
        print("Phone Element: {}".format(phone_element))
        find_phone = phone_element.find("Tel")
    except NoSuchElementException:
        print("Não achou telefone")
        phone = "61999999999"

    if (find_phone == None or find_phone == ""):
        print("Não achou telefone")
        phone = "61999999999"
    else:
        # Vamos começar a limpar agora a string do telefone
        if len(phone_element) > find_phone:
            phone = phone_element[0: 0:] + phone_element[find_phone + 6::]
            print("Phone: {}".format(phone))

    if(phone.__len__() != 11):
        phone = "61999999999"

    return phone

def pausa_longa():
    time.sleep(4.5)

def pausa_curta():
    time.sleep(2)

if __name__ == '__main__':
    adicionar_contato()
