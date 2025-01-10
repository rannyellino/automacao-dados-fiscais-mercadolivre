from __future__ import print_function

import os.path
import time

import google.auth
import pyautogui
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import navegador
from promocao import pausa_curta, pausa_longa
from preenchendo_dados_fiscais import um_segundo
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime
import requests
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '13TY9QrV-NFETPI1hDwytE2ppBcHMg0GuiqnbbL2xGdY'
SAMPLE_RANGE_NAME = 'Página1!A2:D10000'

# CREDENCIAIS SECONDS
LOGIN_SECONDS = 'rannyellino@gmail.com'
PASS_SECONDS = 'Trr12125'

def main():
    logado, chrome = openSeconds()
    print(logado)

    if(logado == "logado1"):
        chrome.get('https://app.seconds.com.br/ReportsSales/NewSalesProfit')
        trinta_sec()

    select_all_accounts(chrome)
    um_segundo()
    date = select_data(chrome)
    um_segundo()
    df = find_values(chrome)
    df2 = check_shipping(df)
    df3 = create_last_dataframe(df2, date)
    send_values(df3)

def send_values(df3):
    print("\n\n")
    print('DF3')
    print("\n\n")
    print(df3)
    rows2 = len(df3.index)
    i2= 0

    # if(rows1 == 0):
    #     range_sheet = 'A' + str(rows1 + 2) + ':''D' + str(rows1 + 2)
    #     sheet_range = "Página1!" + range_sheet
    # else:

    # Criando um loop para passar por cada linha da planilha de base de dados
    while i2 < rows2:
        df = getSheets(SAMPLE_RANGE_NAME)
        rows1 = len(df.index)
        range_sheet = 'A' + str(rows1 + 2) + ':''E' + str(rows1 + 2)
        sheet_range = "Página1!" + range_sheet
        # Guardando os valores de uma linha dentro de uma variavel
        linha = df3.loc[[i2]]
        print(linha)
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        print(lista)

        account = lista[0]
        cod_venda = lista[1]
        mlb = lista[2]
        frete = lista[3]
        date = lista[4]

        _values = [account, cod_venda, mlb, date, frete]

        update_values(SAMPLE_SPREADSHEET_ID, sheet_range, "USER_ENTERED", _values)

        i2 = i2 + 1

def create_last_dataframe(df, date):
    rows = len(df.index)
    i = 0

    accounts = []
    cods_sells = []
    mlbs = []
    fretes = []
    dates = []

    # Criando um loop para passar por cada linha da planilha de base de dados
    while i < rows:
        # Guardando os valores de uma linha dentro de uma variavel
        linha = df.loc[[i]]
        print(linha)
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        print(lista)

        cod_sell = lista[0]
        mlb = lista[1]
        frete = float(lista[2])
        account = get_api(mlb)

        accounts.append(account)
        cods_sells.append(cod_sell)
        mlbs.append(mlb)
        fretes.append(frete)
        dates.append(date)

        i = i+1

    df = {'Conta': accounts,'Cod Venda': cods_sells, 'MLBs': mlbs, 'Fretes': fretes, 'Datas': dates}
    dataframe = pd.DataFrame(df)
    print(dataframe)
    return dataframe

def get_api(mlb):
    account = ""

    # Configurando requisição GET para a API
    url = r"https://api.mercadolibre.com/items/MLB{}".format(mlb)
    print(url)

    response = requests.get(url)
    data = response.json()
    code = response.status_code

    print(response)
    print(data)
    print("STATUS CODE {}".format(code))

    # Caso a resposta da API seja um sucesso vamos começar a guardar as informações que queremos
    if (response.status_code == 200):
        # Salvando Conta
        if data["seller_id"] == 84058800:
            account = "ScapJá"
        elif data["seller_id"] == 142839488:
            account = "SoEscap"

    return account

def check_shipping(df):
    rows = len(df.index)
    i = 0

    # Criando um loop para passar por cada linha da planilha de base de dados
    while i < rows:
        # Guardando os valores de uma linha dentro de uma variavel
        linha = df.loc[[i]]
        print(linha)
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        print(lista)

        cod_sell = lista[0]
        mlb = lista[1]
        frete = float(lista[2])
        print('FRETE {}'.format(frete))
        print('TYPE FRETE {}'.format(type(frete)))

        if(frete < 40.00):
            print(frete < 40.00)
            print(i)
            df = df.drop(index=(i))

        i = i+1

    print("REMOVEU OS VALORES BAIXO DE FRETE")
    df = df.reset_index(drop=True)
    print(df)
    return df

def find_values(chrome):
    pausa_longa()
    pausa_longa()
    n = 2
    fretes = []
    mlbs = []
    cods_sells = []
    processo = True

    while(processo == True):
        try:
            print("N é {}".format(n))
            x_frete = '/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/table/tbody[1]/tr['+str(n)+']/td[5]/span'
            x_mlb = '/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/table/tbody[1]/tr['+str(n)+']/td[2]/span[3]'
            x_cod_sell = '/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/table/tbody[1]/tr['+str(n)+']/td[1]/span[1]/a'

            frete = chrome.find_element(By.XPATH, x_frete)
            mlb = chrome.find_element(By.XPATH, x_mlb)
            cod_sell = chrome.find_element(By.XPATH, x_cod_sell)
            um_segundo()

            frete = frete.text
            cod_sell = cod_sell.text
            mlb = mlb.text

            #Precisa limpar a string do cod MLB por vim com mais informações que o necessário
            find_cod_mlb = mlb.find("MLB")
            mlb = mlb[0: 0:] + mlb[find_cod_mlb::]
            find_cod_mlb = mlb.find("-")
            mlb = mlb[0: find_cod_mlb - 1:] + mlb[len(mlb) + 1::]
            mlb = mlb.replace('MLB', '')
            print(mlb)

            #Limpando o frete
            frete = frete.replace('R$ ', '')
            frete = frete.replace(',','.')

            print("Frete: {} | MLB: {} | Cod_Venda: {}".format(frete, mlb, cod_sell))

            fretes.append(frete)
            mlbs.append(mlb)
            cods_sells.append(cod_sell)
            n = n+1
        except NoSuchElementException:
            try:
                x_cart = '/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/table/tbody[1]/tr['+str(n)+']/td[1]/i'
                cart = chrome.find_element(By.XPATH, x_cart)
                n = n+1
                print('Compra de carrinho')
            except NoSuchElementException:
                print('Chegou no limite de vendas do dia')
                processo = False

    df = {'Cod Venda': cods_sells, 'MLBs': mlbs, 'Fretes':fretes}
    dataframe = pd.DataFrame(df)
    print(dataframe)
    chrome.close()
    chrome.quit()
    return dataframe

def select_data(chrome):
    #Definir o range da data pegando o dia atual e subtraindo um
    x_range_data = '/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[4]/input'
    range_data = chrome.find_element(By.XPATH, x_range_data)
    range_data.click()
    um_segundo()

    #DEFININDO DATA MANULAMENTE
    date_yesterday = ('07-05-2024')

    # date_actual = datetime.datetime.today()
    # date_yesterday = date_actual - datetime.timedelta(days=1)
    # date_yesterday = date_yesterday.strftime('%d-%m-%Y')
    print(date_yesterday)
    um_segundo()

    x_range1 = '/html/body/div[2]/div[1]/div[1]/input'
    x_range2 = '/html/body/div[2]/div[2]/div[1]/input'

    input_range1 = chrome.find_element(By.XPATH, x_range1)
    input_range2 = chrome.find_element(By.XPATH, x_range2)

    input_range1.send_keys(Keys.CONTROL + 'a')
    input_range1.send_keys(Keys.DELETE)
    um_segundo()
    input_range1.send_keys(date_yesterday)
    # pyautogui.hotkey('ctrl', 'a')
    # pyautogui.hotkey('delete')
    # pyautogui.write(date_yesterday)
    # pyautogui.hotkey('Enter')
    um_segundo()
    input_range2.send_keys(Keys.CONTROL + 'a')
    input_range2.send_keys(Keys.DELETE)
    um_segundo()
    input_range2.send_keys(date_yesterday)
    # pyautogui.hotkey('ctrl', 'a')
    # pyautogui.hotkey('delete')
    # pyautogui.write(date_yesterday)
    # pyautogui.hotkey('Enter')
    um_segundo()

    x_apply_date = '/html/body/div[2]/div[3]/div/button[1]'
    input_apply_date = chrome.find_element(By.XPATH, x_apply_date)
    input_apply_date.click()
    trinta_sec()
    return date_yesterday

def select_all_accounts(chrome):
    #Selecionar todas as contas para poder pesquisar o frete e também alterar a data pra o dia anterior
    x_all_accounts = '/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[3]/h6/input'

    checkbox_all_accounts = chrome.find_element(By.XPATH, x_all_accounts)
    checkbox_all_accounts.click()
    um_segundo()

def openSeconds():
    #Primeira etapa é abrir a url da Seconds para ver se está logado
    urlSeconds = 'https://app.seconds.com.br/ReportsSales/NewSalesProfit'
    x_email = '/html/body/div/div[1]/div[2]/div/div/div/div/div/div/div/div/section/form/div[1]/div/input'
    x_password = '/html/body/div/div[1]/div[2]/div/div/div/div/div/div/div/div/section/form/div[2]/div/input'
    x_login_button = '/html/body/div/div[1]/div[2]/div/div/div/div/div/div/div/div/section/form/div[3]/div/input'

    chrome = navegador.abrindo_navegador('Administrator')
    chrome.maximize_window()

    chrome.execute_script("window.open('about:blank','seconds1');")
    pausa_curta()
    chrome.switch_to.window('seconds1')
    chrome.get(urlSeconds)
    um_minuto()

    try:
        #Identificando os 3 campos para fazer login na Seconds
        input_email = chrome.find_element(By.XPATH, x_email)
        input_password = chrome.find_element(By.XPATH, x_password)
        input_login = chrome.find_element(By.XPATH, x_login_button)

        input_email.send_keys(Keys.CONTROL + 'a')
        input_email.send_keys(Keys.DELETE)
        um_segundo()
        input_email.send_keys(LOGIN_SECONDS)
        input_password.send_keys(Keys.CONTROL + 'a')
        input_password.send_keys(Keys.DELETE)
        um_segundo()
        input_password.send_keys(PASS_SECONDS)
        um_segundo()
        input_login.click()
        pausa_curta()

        x_indicadores = '/html/body/div/div[1]/div[1]/ul/li[2]/a/span'
        chrome.find_element(By.XPATH, x_indicadores)
        print("Logado")
        return "logado1", chrome
    except NoSuchElementException:
        #Provavelmente já está logado
        x_indicadores = '/html/body/div/div[1]/div[1]/ul/li[2]/a/span'
        chrome.find_element(By.XPATH, x_indicadores)
        print("Logado")
        return "logado2", chrome

def getSheets(SAMPLE_RANGE_NAME):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token-frete.json'):
        creds = Credentials.from_authorized_user_file('token-frete.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials-frete.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token-frete.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        df = pd.DataFrame(values, columns=['Conta', 'Cods', 'MLB', 'Frete'])
        print(df)
        return df

    except HttpError as err:
        print(err)

def update_values(spreadsheet_id, range_name, value_input_option,_values):
    print(spreadsheet_id)
    print(range_name)
    print(_values)
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token-frete.json'):
        creds = Credentials.from_authorized_user_file('token-frete.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials-frete.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token-frete.json', 'w') as token:
            token.write(creds.to_json())

    try:

        service = build('sheets', 'v4', credentials=creds)
        values = [
            [
                _values[0],
                _values[1],
                _values[2],
                _values[3],
                _values[4]
            ],
            # Additional rows ...
        ]
        body = {
            'values': values
        }
        print(spreadsheet_id)
        print(range_name)
        print(value_input_option)
        print(body)
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def um_minuto():
    time.sleep(60)

def trinta_sec():
    time.sleep(30)

if __name__ == '__main__':
    main()

