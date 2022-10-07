import time

import pyautogui
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
# 0 = Sku
# 1 = EAN
# 2 = Nome_Produto
# 3 = NCM
# 4 = CEST
# 5 = Tipo de Origem
# 6 = Último Dado Para Preencher
# 7 = Botão para Salvar
# 8 = Título do Anúncio
# 9 = Botão "Possui apenas um produto"
# 10 = Botão entrar da TRAY

def read_elementos():
    locations = []
    um_produto_x = 0
    um_produto_y = 0
    sku_x = 0
    sku_y = 0
    botao_salvar_x = 0
    botao_salvar_y = 0
    titulo_x = 0
    titulo_y = 0
    nome_x = 0
    nome_y = 0
    origem_x = 0
    origem_y = 0

    with open("Loc Elementos.txt", 'r') as arquivo:
        for linha in arquivo:
            linha = linha.replace("(", "").replace(")", "").replace("\n", "")
            print(linha)
            locations.append(linha)
    arquivo.close()

    i = 0
    while(i < 6):
        um_produto = str(locations[9]).replace(",", "\n").split('\n')
        sku = str(locations[0]).replace(",", "\n").split('\n')
        botao_salvar = str(locations[7]).replace(",", "\n").split('\n')
        titulo = str(locations[8]).replace(",", "\n").split('\n')
        nome = str(locations[2]).replace(",", "\n").split('\n')
        origem = str(locations[5]).replace(",", "\n").split('\n')
        locs = [um_produto, sku, botao_salvar, titulo, nome, origem]
        firstTime = 0


        for linha in locs[i]:
            print(linha)
            if(i == 0):
                if (firstTime == 0):
                    um_produto_loc_x = linha.strip()
                    um_produto_x = int(um_produto_loc_x)
                    firstTime = 1
                um_produto_loc_y = linha.strip()
                um_produto_y = int(um_produto_loc_y)
            if (i == 1):
                if (firstTime == 0):
                    sku_loc_x = linha.strip()
                    sku_x = int(sku_loc_x)
                    firstTime = 1
                sku_y = linha.strip()
                sku_y = int(sku_y)
            if (i == 2):
                if (firstTime == 0):
                    botao_salvar_loc_x = linha.strip()
                    botao_salvar_x = int(botao_salvar_loc_x)
                    firstTime = 1
                botao_salvar_loc_y = linha.strip()
                botao_salvar_y = int(botao_salvar_loc_y)
            if (i == 3):
                if (firstTime == 0):
                    titulo_loc_x = linha.strip()
                    titulo_x = int(titulo_loc_x)
                    firstTime = 1
                titulo_loc_y = linha.strip()
                titulo_y = int(titulo_loc_y)
            if (i == 4):
                if (firstTime == 0):
                    nome_loc_x = linha.strip()
                    nome_x = int(nome_loc_x)
                    firstTime = 1
                nome_loc_y = linha.strip()
                nome_y = int(nome_loc_y)
            if (i == 5):
                if (firstTime == 0):
                    origem_loc_x = linha.strip()
                    origem_x = int(origem_loc_x)
                    firstTime = 1
                origem_loc_y = linha.strip()
                origem_y = int(origem_loc_y)
        firstTime = 0
        i = i+1

    return um_produto_x, um_produto_y, sku_x, sku_y, botao_salvar_x, botao_salvar_y, titulo_x, titulo_y, nome_x, nome_y, origem_x, origem_y


def fiscais_elementos_location(chrome):
    sku_loc = 0, 0
    ean_loc = 0, 0
    nome_produto_loc = 0, 0
    cest_loc = 0, 0
    tipo_origem_loc = 0, 0
    ultima_loc = 0, 0
    salvar_loc = 0, 0
    name_loc = 0, 0

    # Pega elemento SKU e a sua posição na tela
    try:
        sku = chrome.find_element(By.XPATH, "//input[@name='sku']")  # Acha elemento
        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')  # Pega o Y da tela
        sku_loc_x = sku.location['x']  # pega o valor de X do elemento
        sku_y = sku.location['y']  # pegao valor de Y do elemento
        sku_loc_y = sku_y + panel_height  # pega o valor de Y do elemento mas sendo o valor absoluto referente a resolução da tela
        sku_loc = sku_loc_x, sku_loc_y  # Coloca os valores de X e Y absolutos dentro de uma variavel para usar o comando de click posteriomente
        print(sku_loc)
    except NoSuchElementException:
        print(sku_loc)

    # Pega elemento EAN e a sua posição na tela
    try:
        ean = chrome.find_element(By.XPATH, "//input[@name='ean']")
        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        ean_loc_x = ean.location['x']
        ean_y = ean.location['y']
        ean_loc_y = ean_y + panel_height
        ean_loc = ean_loc_x, ean_loc_y
        print(ean_loc)
    except NoSuchElementException:
        print(ean_loc)

    # Pega elemento Nome do Produto e a sua posição na tela
    try:
        nome_produto = chrome.find_element(By.XPATH, "//input[@name='name']")
        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        nome_produto_loc_x = nome_produto.location['x']
        nome_produto_y = nome_produto.location['y']
        nome_produto_loc_y = nome_produto_y + panel_height
        nome_produto_loc = nome_produto_loc_x, nome_produto_loc_y
        print(nome_produto_loc)
    except NoSuchElementException:
        print(nome_produto_loc)

    # Pega elemento NCM e a sua posição na tela
    try:
        ncm = chrome.find_element(By.XPATH, "//input[@name='ean']")
        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        ncm_loc_x = ncm.location['x']
        ncm_y = ncm.location['y']
        ncm_loc_y = ncm_y + panel_height
        ncm_loc = ncm_loc_x, ncm_loc_y
        print(ncm_loc)
    except NoSuchElementException:
        print(ncm_loc)

    # Pega elemento CEST e a sua posição na tela
    try:
        cest = chrome.find_element(By.XPATH, "//input[@class='tax-information-dropdown-input__input']")
        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        cest_loc_x = cest.location['x']
        cest_y = cest.location['y']
        cest_loc_y = cest_y + panel_height
        cest_loc = cest_loc_x, cest_loc_y
        print(cest_loc)
    except NoSuchElementException:
        print(cest_loc)

    # Pega elemento Tipo de Origem e a sua posição na tela
    try:
        tipo_origem = chrome.find_element(By.XPATH,"//button[@aria-label='Seleção de originType ']//span[@class='andes-form-control__placeholder']")
        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        tipo_origem_loc_x = tipo_origem.location['x']
        tipo_origem_y = tipo_origem.location['y']
        tipo_origem_loc_y = tipo_origem_y + panel_height
        tipo_origem_loc = tipo_origem_loc_x, tipo_origem_loc_y
        print(tipo_origem_loc)
    except NoSuchElementException:
        tipo_origem = chrome.find_element(By.XPATH,"//button[@aria-label='Seleção de originType ']//span[@class='andes-dropdown__display-values']")
        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        tipo_origem_loc_x = tipo_origem.location['x']
        tipo_origem_y = tipo_origem.location['y']
        tipo_origem_loc_y = tipo_origem_y + panel_height
        tipo_origem_loc = tipo_origem_loc_x, tipo_origem_loc_y
        print(tipo_origem_loc)

    # Pega elemento CSOSN do ICMS ou Planilha correta, depende de qual conta esta trabalhando, e também guarda sua posição na tela
    try:
        csosn = chrome.find_element(By.XPATH,"//button[@aria-label='Seleção de csosn ']//span[@class='andes-form-control__placeholder']")
        if(csosn == None):
            csosn = chrome.find_element(By.XPATH,"//button[@aria-label='Seleção de csosn ']//span[@class='andes-dropdown__display-values']")

        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        csosn_loc_x = csosn.location['x']
        csosn_y = csosn.location['y']
        csosn_loc_y = csosn_y + panel_height
        csosn_loc = csosn_loc_x, csosn_loc_y
        ultima_loc = csosn_loc
        print(ultima_loc)
    except NoSuchElementException:
        print(ultima_loc)

    try:
        planilha = chrome.find_element(By.XPATH,"//button[@aria-label='Seleção de taxRuleId ']//span[@class='andes-form-control__placeholder']")
        if(planilha == None):
            planilha = chrome.find_element(By.XPATH,"//button[@aria-label='Seleção de taxRuleId ']//span[@class='andes-dropdown__display-values']")

        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        planilha_loc_x = planilha.location['x']
        planilha_y = planilha.location['y']
        planilha_loc_y = planilha_y + panel_height
        planilha_loc = planilha_loc_x, planilha_loc_y
        ultima_loc = planilha_loc
        print(ultima_loc)
    except NoSuchElementException:
        print(ultima_loc)

    pyautogui.scroll(100)
    pyautogui.scroll(-100)
    pyautogui.scroll(-100)
    pyautogui.scroll(-100)

    # Pega elemento butão Salvar Dados Fiscais e a sua posição na tela
    try:
        time.sleep(3)
        salvar = chrome.find_element(By.XPATH, "//span[.='Salvar dados fiscais']")
        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        salvar_loc_x = salvar.location['x']
        salvar_y = salvar.location['y']
        salvar_loc_y = salvar_y + panel_height
        salvar_loc = salvar_loc_x, salvar_loc_y
        print(salvar_loc)
    except NoSuchElementException:
        print(salvar_loc)

    # Pega elemento butão Salvar Dados Fiscais e a sua posição na tela
    try:
        name = chrome.find_element(By.XPATH, "//div[@class='sidebar-item__content']//span[@class='name']")
        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        name_loc_x = name.location['x']
        name_y = name.location['y']
        name_loc_y = name_y + panel_height
        name_loc = name_loc_x, name_loc_y
        print(name_loc)
    except NoSuchElementException:
        print(name_loc)

    return sku_loc, ean_loc, nome_produto_loc, ncm_loc, cest_loc, tipo_origem_loc, ultima_loc, salvar_loc, name_loc

def inicio_fiscais_elementos_location(chrome):
    um_produto_loc = 0, 0

    # Pega elemento botão Possui apenas um produto e a sua posição na tela
    try:
        um_produto = chrome.find_element(By.XPATH, "//span[.='Possui apenas um produto']")
        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        um_produto_loc_x = um_produto.location['x']
        um_produto_y = um_produto.location['y']
        um_produto_loc_y = um_produto_y + panel_height
        um_produto_loc = um_produto_loc_x, um_produto_loc_y
        print(um_produto_loc)
    except NoSuchElementException:
        print(um_produto_loc)

    return um_produto_loc

def tray_login_elementos(chrome):
    login_loc = 0, 0

    #Pega elemento botão ENTRAR e a sua posição na tela
    try:
        login = chrome.find_element(By.XPATH, "//button[@id='btn-submit']")
        panel_height = chrome.execute_script('return window.outerHeight - window.innerHeight;')
        login_loc_x = login.location['x']
        login_y = login.location['y']
        login_loc_y = login_y + panel_height
        login_loc = login_loc_x, login_loc_y
        print(login_loc)
    except NoSuchElementException:
        print(login_loc)



