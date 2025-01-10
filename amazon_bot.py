import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import navegador
import pandas as pd
import openpyxl
import pyautogui

_url_edit_1 = 'https://sellercentral.amazon.com.br/abis/listing/edit/offer?sku='
_url_edit_2 = '&asin='
_url_edit_3 = '&productType=AUTO_PART&marketplaceID=A2Q3Y263D00KWC&ref_=myp_1x1'
_url_edit_details = '#product_details'
_url_edit_offer = '#offer'

def main():
    archive = 'skus_asins_amazon-4.xlsx'

    sku_list, asin_list = get_skus_asin(archive)
    #edit_title_asin(sku_list, asin_list)
    edit_price(sku_list, asin_list)

def edit_price(sku_list, asin_list):
    user = "Administrator"  # Setando usuário
    primeiroCiclo = True

    if (sku_list.__len__() == asin_list.__len__()):
        print("Duas listas do mesmo tamanho")
        max = sku_list.__len__()
        i = 82

        # Abrindo navegador do usuário
        chrome = navegador.abrindo_navegador(user)
        chrome.maximize_window()

        # Começando loop de edição de título
        while (i <= max):
            find_price = False
            print("I: ", i)
            print("Asin: ", asin_list[i])
            edit = f'edit{i}'
            print(edit)

            __url = f'{_url_edit_1}{sku_list[i]}{_url_edit_2}{asin_list[i]}{_url_edit_offer}'
            #price_xpath = '/html/body/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[6]/section/div[1]/div/div/div[2]/div[1]/div[1]/div/section[2]/kat-input-group/kat-input'
            price_xpath = '/html/body/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[6]/section/div[3]/div/section[2]/kat-input-group/kat-input'
            button_save_xpath = '/html/body/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/kat-popover-trigger/kat-button//button'

            if (primeiroCiclo == True):
                chrome.execute_script("window.open('about:blank','blank');")
                chrome.switch_to.window('blank')

            chrome.execute_script(f"window.open('about:blank','{edit}');")
            pausa_curta()
            chrome.switch_to.window(f'{edit}')
            chrome.get(__url)
            pausa_longa()

            #Determinando um tempo de espera pro selenium para poder achar os elementos
            secs = 10
            while (find_price == False):
                find_price, price_xpath_correct = wait_selenium(chrome, price_xpath, secs)
                secs = secs+1

            try:
                #Achando o preço
                price_element = chrome.find_element(By.XPATH, price_xpath_correct)
                price = price_element.get_attribute('value')
                print(price)
                find_virgula = price.find(",")
                price = price[0: find_virgula:]
                print("price corrigido: ", price)
                price = price.replace('.','')
                price = float(price)
                price = int(price)

                print('Preço atual', price)

                if(price > 79):
                    price = price - 35
                    #price = int(price) + int(price * 0.05)
                else:
                    #price = int(price) + int(price * 0.05)
                    price = price

                print('Preço novo', price)

                pausa_curta()

                price_element.send_keys(Keys.CONTROL + "a")
                price_element.send_keys(Keys.DELETE)
                price_element.send_keys(price)

                pausa_curta()

                chrome.execute_script("window.scrollTo(0, 10000)")
                um()
                chrome.execute_script("window.scrollTo(0, 10000)")
                um()
                chrome.execute_script("window.scrollTo(0, 10000)")
                um()

                pyautogui.click(x=1661, y=786)
                pausa_longa()
                pyautogui.click(x=1661, y=786)
                pausa_curta()
                pyautogui.click(x=1000, y=786)
            except NoSuchElementException:
                print('Erro')

            chrome.close()
            chrome.switch_to.window("blank")
            primeiroCiclo = False
            i = i + 1

def edit_title_asin(sku_list, asin_list):
    user = "Administrator"  # Setando usuário
    primeiroCiclo = True

    if(sku_list.__len__() == asin_list.__len__()):
        print("Duas listas do mesmo tamanho")
        max = sku_list.__len__()
        i = 0

        # Abrindo navegador do usuário
        chrome = navegador.abrindo_navegador(user)
        chrome.maximize_window()

        #Começando loop de edição de título
        while (i <= max):
            print("I: ", i)
            print("Asin: ", asin_list[i])
            edit = f'edit{i}'
            print(edit)

            __url = f'{_url_edit_1}{sku_list[i]}{_url_edit_2}{asin_list[i]}{_url_edit_details}'
            title_xpath = '/html/body/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/section/div[1]/div/div[1]/div[1]/section[2]/kat-textarea'
            button_save_xpath = '/html/body/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/kat-popover-trigger/kat-button//button'

            if (primeiroCiclo == True):
                chrome.execute_script("window.open('about:blank','blank');")
                chrome.switch_to.window('blank')

            chrome.execute_script(f"window.open('about:blank','{edit}');")
            pausa_curta()
            chrome.switch_to.window(f'{edit}')
            chrome.get(__url)
            pausa_longa()

            try:
                title_element = chrome.find_element(By.XPATH, title_xpath)
                title_text = title_element.get_attribute('value')
                print(title_text)

                print('Titulo atual', title_text)

                title_text = title_text.replace('Genérico, ','')

                print('Titulo novo', title_text)

                pausa_curta()

                title_element.send_keys(Keys.CONTROL + "a")
                title_element.send_keys(Keys.DELETE)
                title_element.send_keys(title_text)

                pausa_curta()

                chrome.execute_script("window.scrollTo(0, 10000)")
                um()
                chrome.execute_script("window.scrollTo(0, 10000)")
                um()
                chrome.execute_script("window.scrollTo(0, 10000)")
                um()

                pyautogui.click(x=1661, y=786)
                pausa_longa()
                pyautogui.click(x=1661, y=786)
                pausa_curta()
                pyautogui.click(x=1000, y=786)
            except NoSuchElementException:
                print('Erro')

            chrome.close()
            chrome.switch_to.window("blank")
            primeiroCiclo = False
            i = i + 1


    else:
        print("Listas com tamanhos diferentes")

def get_skus_asin(archive):
    df_base = pd.read_excel(archive)
    print(df_base)
    rows = len(df_base.index)  # Pega a quantidade de linhas que tem na base de dados para usar como referencia no while
    i = 0  # Para o while que vai rodar a leitura de cada linha da base de dados

    #convertendo coluna para lista
    skus_list = df_base[df_base.columns[0]].values.tolist()
    asin_list = df_base[df_base.columns[1]].values.tolist()

    return skus_list, asin_list

def wait_selenium(chrome, price_xpath, i):
    price_xpath2 = '/html/body/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[4]/section/div[1]/div/section[2]/kat-input-group/kat-input'
    find_price = False

    try:
        if (i % 2 == 0):
            WebDriverWait(chrome, i).until(EC.presence_of_element_located((By.XPATH, price_xpath)))
            print("Achou preço")
            print(price_xpath)
            find_price = True
            return find_price, price_xpath
        else:
            WebDriverWait(chrome, i).until(EC.presence_of_element_located((By.XPATH, price_xpath2)))
            print("Achou preço")
            print(price_xpath2)
            find_price = True
            return find_price, price_xpath2
    except TimeoutException:
        print("Não achou o preço")
        chrome.find_element(By.XPATH, "//body").send_keys(Keys.F5)
        pyautogui.hotkey('f5')
        return find_price, price_xpath

def pausa_longa():
    time.sleep(5)

def pausa_curta():
    time.sleep(2.5)

def um():
    time.sleep(1)

if __name__ == '__main__':
    main()


