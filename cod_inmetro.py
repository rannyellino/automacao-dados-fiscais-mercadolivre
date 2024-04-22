import time
import pyautogui
from selenium.webdriver.common.by import By
import log
import navegador
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

def incluir_inmetro():
    user = "Rannyel"  # Setando usuário
    _url = "https://www.mercadolivre.com.br/anuncios/lista?filters=CHANNEL_MARKETPLACE_MSHOPS|CHANNEL_ONLY_MARKETPLACE|EXCLUSIVE_CHANNEL_NO_PROXIMITY_AND_NO_MP_MERCHANTS&page=1&search="
    _url2 = "&sort=DEFAULT"
    cod_inmetro = "C01-00-N / ISO 9001:2015"
    cods_mlbs = []
    cods_alterados = []
    status_list = []
    primeiroCiclo = True

    #Botões padrões do ML
    #search_x = '//*[@id="app-root-wrapper"]/div[1]/div/div[1]/div[4]/div/div/div/div/div/div[1]/div[1]/div/label/div/input'
    first_result_x = '//*[@id="app-root-wrapper"]/div[1]/div/div[1]/div[6]/div/div/div/div/div[3]/a'
    informacoes_regulatoria_x = '//*[@id="legal_requirements_header_container"]/div[1]/div[1]/h2'
    num_inmetro_x = '//*[@id="legal_requirements_task"]/div[2]/ul/div/div/div[1]/label/div[1]/input'
    confirm_x = '//*[@id="legal_requirements_task"]/div[2]/div[2]/button[1]'

    df_base = pd.read_excel('inmetro soescap.xlsx')
    print(df_base)
    rows = len(df_base.index)
    i = 0

    while i < rows:
        linha = df_base.loc[[i]]  # Localiza a linha referente ao indice 'i'
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        mlb = str(lista[0])
        mlb = mlb.replace(".0", "")

        cods_mlbs.append(mlb)  # Atribui a coluna 3 da linha 'i' a array cods_mlbs
        i = i + 1

    print(cods_mlbs)

    # Abrindo navegador do usuário
    chrome = navegador.abrindo_navegador(user)
    chrome.maximize_window()

    i = 4

    while i < cods_mlbs.__len__():
        newurl = _url + str(cods_mlbs[i]) + _url2
        pausa_curta()

        if (primeiroCiclo == True):
            chrome.execute_script("window.open('about:blank','blank');")
            chrome.switch_to.window('blank')

        chrome.execute_script("window.open('about:blank','promo{}');".format(i))
        pausa_curta()
        chrome.switch_to.window('promo{}'.format(i))
        chrome.get(newurl)
        pausa_longa()

        try:
            chrome.find_element(By.XPATH, first_result_x).click()
            print('Primeiro Resultado')
            pausa_curta()

            chrome.find_element(By.XPATH, informacoes_regulatoria_x).click()
            print('Informações Regulatoria')
            pausa_curta()
            #chrome.find_element(By.XPATH, num_inmetro_x).click()
            #print('Número inmetro')

            pyautogui.write(cod_inmetro)
            time.sleep(1)

            chrome.find_element(By.XPATH, confirm_x).click()
            print('Confirmação')
            pausa_longa()

            cods_alterados.append(cods_mlbs[i])
            status = 'Okay'
        except NoSuchElementException:
            cods_alterados.append(cods_mlbs[i])
            print('ERRO')
            status = 'Erro'

        status_list.append(status)
        chrome.close()
        primeiroCiclo = False
        chrome.switch_to.window('blank')
        i = i+1

    log.log_promo(status_list, cods_alterados)

def pausa_longa():
    time.sleep(4.5)

def pausa_curta():
    time.sleep(2)

if __name__ == '__main__':
    incluir_inmetro()