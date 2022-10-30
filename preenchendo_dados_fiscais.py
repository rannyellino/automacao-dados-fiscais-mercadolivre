import pyautogui
import pyperclip
import time
from tkinter import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import elementos
import navegador
import log

def preenchendo(link_planilha_anuncios, link_planilha_EAN, linha_coluna_anuncios, linha_coluna_ean, ncm, cest, qtd_anuncios, conta, janela, user):
    # Aba de Anuncios do MercadoLivre
    anuncios = r"" #É o mesmo link indepedente da conta
    dados_fiscais = r"https://myaccount.mercadolivre.com.br/fiscal-information/item/MLB" #link para entrar na parte fiscal de um anúncio
    primeiroCiclo = True #Checar o primeiro ciclo
    em_processo = True #saber se ainda está dentro do laço para preencher os dados fiscais
    cod_finalizados = [] #Lista para colocar os códigos finalizados
    cod_erros = [] #Lista para colocar os códigos com erro
    qtd_anuncios_number = int(qtd_anuncios)
    locations = []
    print("Puxando a posição dos elementos necessários")
    elementos_loc = elementos.read_elementos()

    chrome = navegador.abrindo_navegador(user) #Chamando a função com Selenium e recebendo o valor do chrome
    chrome.maximize_window() #maximizando a janela
    print(chrome)

    pausa_longa() #Espera segundos por precaução

    # Abrindo cada planilha em uma nova ABA
    abrir_nova_aba()
    pyperclip.copy(link_planilha_anuncios)
    colar_link()
    pyautogui.hotkey("enter") #Entrou no link da planilha de anuncios

    abrir_nova_aba()
    pyperclip.copy(link_planilha_EAN)
    colar_link()
    pyautogui.hotkey("enter") #Entrou no link da planilha de EAN

    abrir_nova_aba()
    pyperclip.copy(anuncios)
    colar_link()
    pyautogui.hotkey("enter") #Entrou no link dos anuncios dentro do ML

    print("Abriu todas as abas que precisa")
    print("Em processo {}".format(em_processo))

    pausa_curta() #Espera segundos por precaução

    # Laço para saber se já preencheu o EAN de todos os anúncios
    while (em_processo):
        checa_catalisador = 0 #Variavel dedicada para o sistema de verificação se contém catalisador no anuncio ou não
                              #Sempre ela vai iniciar com o valor de 0 em cada ciclo
        checa_oleo = 0 #Variavel dedicada para o sistema de verificação se contém oleo no anuncio ou não

        if(primeiroCiclo):
            # Volta para a aba dos anúncios
            mudar_aba_atras()
            mudar_aba_atras()

            pausa_longa() #Espera segundos por precaução

            #Identificando onde começar
            pyautogui.hotkey("ctrl", "j") #Procura celula
            pyautogui.write(linha_coluna_anuncios) #Escreve celula
            pyautogui.hotkey("enter") #Acha a celula

            #Indo para a aba dos EAN
            mudar_aba_frente()

            pausa_longa() #Espera segundos por precaução

            #Identificando onde começar
            pyautogui.hotkey("ctrl", "j")  # Procura celula
            pyautogui.write(linha_coluna_ean)  # Escreve celula
            pyautogui.hotkey("enter")  # Acha a celula

            pausa_curta() #Espera segundos por precaução

            mudar_aba_frente()  # Chegando na aba do MercadoLivre

            pausa_curta()

            # Pesquisando anuncio
            pyautogui.click(x=259, y=55)
            pyperclip.copy(dados_fiscais)
            colar_link()

            #Volta para a aba dos anúncios
            mudar_aba_atras()
            mudar_aba_atras()

            pausa_curta()
        else:
            #Alterando o link da url para o link dos dados fiscais onde só irá faltar colocar o código MLB
            pyautogui.click(x=259, y=55)
            pyperclip.copy(dados_fiscais)
            colar_link()

            # Volta para a aba dos anúncios
            mudar_aba_atras()
            mudar_aba_atras()

        #Pegar código do anuncio do MercadoLivre
        if(primeiroCiclo):
            copiar()
        else:
            pyautogui.hotkey("down")
            um_segundo()
            pyautogui.hotkey("down")
            um_segundo()
            pyautogui.hotkey("down")
            um_segundo()
            copiar()

        mudar_aba_frente()
        mudar_aba_frente() #Chegando na aba do MercadoLivre

        pausa_curta()

        #Colando o código MLB do anuncio e entrando na parte fiscal
        colar_link()
        pyautogui.hotkey("Enter")
        mlb_copiado = janela.clipboard_get()
        print("Trabalhando com o anúncio MLB{}".format(mlb_copiado))

        time.sleep(10)

        #Procura o botão para começar a preencher os dados fiscais pela primeira vez
        pyautogui.click(elementos_loc[0], elementos_loc[1])

        pausa_curta()  # Espera segundos por precaução

        pyautogui.click(elementos_loc[2], elementos_loc[3]) # Clica no SKU que é o primeiro campo
        pyautogui.hotkey("ctrl", "a") # Seleciona todo valor do campo
        pyautogui.hotkey("ctrl", "c")  # Copia o que tiver no campo SKU
        text_copiado = janela.clipboard_get() #Pega o valor copiado e coloca em uma váriavel
        cod_atual = janela.clipboard_get()  # Pega o código MLB que está trabalhando
        if(text_copiado == mlb_copiado): #Sistema de verificação simples que checa se existe algum valor no código SKU dos dados fiscais, caso haja significa que esse anuncio já foi feito os dados fiscais
            #Preenchendo os dados fiscais dos anuncios

            #Volta para a aba dos anúncios
            mudar_aba_atras()
            mudar_aba_atras()

            pausa_curta()  # Espera segundos por precaução

            #Copiando SKU
            if(conta == "1"): #Se for ScapJá
                pyautogui.hotkey("down")
                um_segundo() # Espera segundos por precaução
                pyautogui.hotkey("down") #Chegando até o SKU
                copiar()
                um_segundo()
            elif(conta == "2"): #Se for SoEscap
                pyautogui.hotkey("down")
                um_segundo()  # Espera segundos por precaução
                copiar()
                um_segundo()
            else:
                exit()

            # Ir para a aba do Mercado Livre
            mudar_aba_frente()
            mudar_aba_frente()

            pausa_curta() # Espera segundos por precaução

            #Colando SKU
            colar_link()

            #Voltando para a aba dos EAN
            mudar_aba_atras()

            pausa_curta()  # Espera segundos por precaução

            #Copiando EAN
            if(primeiroCiclo):
                    pyautogui.hotkey("left")  # Chegando até o EAN
                    copiar()
                    pyautogui.hotkey("right") # Voltando para preencher o código do anuncio depois
            else:
                    pyautogui.hotkey("down")
                    pyautogui.hotkey("left")  # Chegando até o EAN
                    copiar()
                    pyautogui.hotkey("right")  # Voltando para preencher o código do anuncio depois

            # Ir para a aba do Mercado Livre
            mudar_aba_frente()

            pausa_curta()  # Espera segundos por precaução

            #Colando EAN
            pyautogui.hotkey("Tab") # Chegou até o campo EAN
            colar_link()

            um_segundo()  # Espera segundos por precaução

            #Copiando nome do produto
            pyautogui.click(elementos_loc[6], elementos_loc[7], clicks=3)
            copiar()

            #Sistema de checagem para saber se é um catalisador ou não, caso seja precisa alterar o valor do NCM
            titulo = janela.clipboard_get()  # coloca a copia do titulo dentro de uma variavel
            titulo_pronto = titulo.casefold()  # transforma toda string em minusculo
            titulo_split = titulo_pronto.rsplit(" ")  # separa a string dentro de uma lista separando cada valor entre um espaço " "

            # Checa se algumas das palavras do título contem a palavra catalisador para saber se precisa trocar os valores fiscais
            for texto in titulo_split:
                if (texto == "catalisador"):
                    checa_catalisador = 1
                    print("É catalisador")
                elif (texto == "oleo" or texto == "óleo"):
                    checa_oleo = 1
                    print("É oleo")
                else:
                    print("não é catalisador nem oleo")


            #Indo até o campo nome do produto e colando
            um_segundo()
            pyautogui.click(elementos_loc[8], elementos_loc[9])
            colar_link()

            #Preenchendo Outros Dados
            pyautogui.hotkey("Tab")
            if(checa_catalisador == 1):
                ncm = "84213200"
                cest = "0107500"
            elif(checa_oleo == 1):
                ncm = "27101932"
                cest = "0600700"
            else:
                ncm = "87089200"
                cest = "0107500"
            pyautogui.write(ncm) #Preenchendo NCM
            pausa_curta()  # Espera segundos por precaução
            pyautogui.hotkey("Tab")
            pyautogui.hotkey("Tab")
            pyautogui.write(cest) #Preenchendo CEST
            um_segundo()  # Espera segundos por precaução
            pyautogui.hotkey("Tab")
            pyautogui.click(elementos_loc[10], elementos_loc[11]) #Abrindo opções de origem
            um_segundo()  # Espera segundos por precaução
            pyautogui.hotkey("Down")
            pyautogui.hotkey("Enter") #Selecionando Nacional
            pausa_curta()  # Espera segundos por precaução
            pyautogui.hotkey("Tab")
            pyautogui.hotkey("Tab")
            pyautogui.hotkey("Enter") #Abrindo CSOSN do ICMS
            time.sleep(1.25)  # Espera segundos por precaução

            if(conta == "1"): # Se for ScapJá
                pyautogui.hotkey("Down")
                pyautogui.hotkey("Down")
                pyautogui.hotkey("Down")
                pyautogui.hotkey("Down") #Chegando na opção certa
                um_segundo()  # Espera segundos por precaução
                pyautogui.hotkey("Enter")  #Selecionando 500
                um_segundo()  # Espera segundos por precaução
            elif(conta == "2"): # Se for SoEscap
                pyautogui.hotkey("Enter")
                um_segundo()

            #Preenchendo nas planilhas de anuncios e de EAN
            #Voltando para a planilha de anúncios
            mudar_aba_atras()
            mudar_aba_atras()

            pausa_curta() # Espera segundos por precaução

            if (conta == "1"):  # Se for ScapJá
                pyautogui.hotkey("up")
                um_segundo()
                pyautogui.hotkey("up") #Volta para o código do anúncio
                copiar()
            elif (conta == "2"):  # Se for SoEscap
                pyautogui.hotkey("up")
                um_segundo()
                copiar()

            #Vai até a aba de EAN
            mudar_aba_frente()
            pausa_curta()  # Espera segundos por precaução

            #Cola o código do anúncio ao EAN referente
            colar_link() #Cola o código do anúncio que editou o EAN
            um_segundo()
            #pyautogui.click(x=710, y=233)
            #um_segundo()
            if(conta == "1"): #Se for ScapJá
               #pyautogui.click(x=801, y=422) #Pinta de verde para indicar que é a conta SCAPJÁ
                um_segundo()
            elif(conta == "2"):
                #pyautogui.click(x=783, y=421)  # Pinta de amarelo para indicar que é a conta SoEscap
                um_segundo()

            #Vai até a aba de ANÚNCIOS
            mudar_aba_atras()
            pausa_curta()

            pyautogui.hotkey("right")
            #pyautogui.click(x=710, y=233)
            um_segundo()
            pyautogui.write("FEITO")
            #pyautogui.click(x=801, y=422)  # Pinta de verde para indicar que finalizou o processo de preencher dados fiscais e EAN
            um_segundo()
            pyautogui.hotkey("left")

            #Indo até a ABA do MercadoLivre
            mudar_aba_frente()
            mudar_aba_frente()

            pausa_curta()

            #Salvando os dados fiscais e voltando para a página de anuncios normal
            if(conta == "1"):
                pyautogui.hotkey("TAB")
                pyautogui.hotkey("Enter")
            else:
                pyautogui.hotkey("TAB")
                pyautogui.hotkey("TAB")
                pyautogui.hotkey("Enter")

            pausa_curta()
            cod_finalizados.append(cod_atual)
            qtd_anuncios_number = qtd_anuncios_number - 1
            print(qtd_anuncios_number)
            #print(qtd_anuncios)
            pausa_curta()

            primeiroCiclo = False;
            #print(primeiroCiclo)
            #print(em_processo)
            if(qtd_anuncios_number == 0):
                finalizado = Label(janela, text="Processo Finalizado!!!")
                finalizado.grid(column=0, row=17)
                log.criando_log(cod_finalizados,cod_erros)
                em_processo = False
                #print("Processo finalizado foi preenchido o EAN de {} anúncios".format(total_anuncios))
        else:
            cod_erros.append(mlb_copiado)
            qtd_anuncios_number = qtd_anuncios_number - 1
            pausa_curta()
            primeiroCiclo = False;
            if (qtd_anuncios_number == 0):
                finalizado = Label(janela, text="Processo Finalizado!!!")
                finalizado.grid(column=0, row=17)
                log.criando_log(cod_finalizados, cod_erros)
                em_processo = False
                # print("Processo finalizado foi preenchido o EAN de {} anúncios".format(total_anuncios))

def preenchendo_tray(link_planilha_anuncios, link_planilha_EAN, linha_coluna_anuncios, linha_coluna_ean, qtd_anuncios, conta, janela, user):
    link_tray = r"https://www.scapja.com.br/mvc/adm/panel" #Link para fazer login na TRAY
    link_produto_tray = r"https://www.scapja.com.br/admin/#/mvc/adm/products/edit/" #Link para entrar na parte de edição da tray
    iframe = "//html//body//div[1]//div//div[3]//div[1]//div//div//div//iframe[@id='centro']" #Caminho XPATH do iframe que existe dentro da página de produto da TRAY
    em_processo = True #Variavel para manter o loop
    primeiro_ciclo = True #Variavel para saber está no primeiro loop
    cod_finalizados = [] #Lista para colocar os códigos que finalizou o processo
    cod_erros = [] #Lista para colocar os códigos que deram erro no processo
    qtd_anuncios = int(qtd_anuncios) #Quantidade de anuncios que serão editados

    #Abrindo navegador CHROME
    chrome = navegador.abrindo_navegador(user)
    chrome.maximize_window()

    pausa_longa()

    #Abrindo uma nova aba e entrando na aba de anuncios
    chrome.execute_script("window.open('about:blank','anuncios');")
    chrome.switch_to.window("anuncios") #Muda a Aba
    chrome.get(link_planilha_anuncios)
    pausa_curta()

    #Abrindo uma nova aba e entrando na aba de EAN
    chrome.execute_script("window.open('about:blank','eans');")
    chrome.switch_to.window("eans") #Muda a Aba
    chrome.get(link_planilha_EAN)
    pausa_curta()

    # Abrindo uma nova aba e entrando na aba TRAY
    chrome.execute_script("window.open('about:blank','login_tray');")
    chrome.switch_to.window("login_tray") #Muda a Aba
    chrome.get(link_tray)
    pausa_curta()
    login_tray(chrome)
    chrome.close()

    while(em_processo):
        sku = "" #Codigo sku que será concatenado ao link de produto da tray
        ean_preenchido = "" #Para fazer a verificação posteriomente para saber se já existe um ean preenchido
        cod_anuncio_scapja = "" #Para armazenar o código do mesmo anuncios porém na ScapJá dentro do MercadoLivre para no futuro poder pegar o mesmo ean utilizado
                                #dentro do MercadoLivre
        link_produto_tray = r"https://www.scapja.com.br/admin/#/mvc/adm/products/edit/"  # Link para entrar na parte de edição da tray

        if(primeiro_ciclo == True):
            #Procurando a celula certa na planilha de anuncios
            chrome.switch_to.window("anuncios")
            pausa_curta()
            chrome.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + 'J') #Procurar Celula no Google Sheets
            pyautogui.hotkey('ctrl', 'j')
            um_segundo()
            pyautogui.write(linha_coluna_anuncios) #Escreve a Celula
            pyautogui.hotkey("Enter") #Acha a celula
            print("Achou a celula de onde começa os anuncios")
        else:
            chrome.switch_to.window("anuncios")
            pausa_curta()
            pyautogui.hotkey("down")
            um_segundo()
            pyautogui.hotkey("down")
            um_segundo()
            pyautogui.hotkey("down")

        #Pega o SKU(Código interno do anuncio) para poder preencher os dados fiscais desse anuncio mais pra frente
        um_segundo()
        copiar()
        sku = janela.clipboard_get()
        sku = str(sku) #Transforma o que foi copiado em uma STRING
        print(sku)
        link_produto_tray = link_produto_tray+sku #Deixa o link pronto pra entrar no anuncio e edita-lo dentro da TRAY
        print(link_produto_tray)

        # Abrindo uma nova aba e entrando na aba TRAY
        chrome.execute_script("window.open('about:blank','produto_tray');")
        chrome.switch_to.window("produto_tray")  # Muda a Aba
        chrome.get(link_produto_tray)
        pausa_longa()

        #Antes de checar os valores para editar é preciso entrar dentro do iframe do HTML da página
        chrome.switch_to.frame(chrome.find_element(By.XPATH, iframe))
        pausa_curta()

        #Checando se existe valor no campo EAN
        ean_element = chrome.find_element(By.XPATH, "//input[@id='ProductEan']")
        ean_preenchido = ean_element.get_attribute('value')
        ean_preenchido = str(ean_preenchido)
        um_segundo()
        print("Ean Preenchido: {}".format(ean_preenchido))
        #Checa se o campo tem algum valor, se não tiver vai começar a preencher
        if(ean_preenchido == ""):
            chrome.switch_to.window("anuncios")
            um_segundo()
            pyautogui.hotkey("up")
            um_segundo()
            pyautogui.hotkey("up")
            copiar()
            cod_anuncio_scapja = janela.clipboard_get() #Guarda o código do anuncio da scapja referente a este SKU
            um_segundo()
            pyautogui.hotkey("down")
            um_segundo()
            pyautogui.hotkey("down")

            #Vai ate a aba de EANS e procura o código da ScapJá para saber qual código de EAN usar dentro da TRAY
            chrome.switch_to.window("eans")
            pausa_curta()
            chrome.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + 'f')  # Procurar Celula no Google Sheets
            pyautogui.hotkey('ctrl', 'f') #Abri a janela de procura
            um_segundo()
            pyautogui.write(cod_anuncio_scapja) #Escreve o código da ScapJá
            um_segundo()
            pyautogui.hotkey('enter') #Acha o código na planilha
            pyautogui.hotkey('esc') #Fecha a janela de procura

            #Agora basta copiar o ean que foi utilizado também na scapjá e usar o mesmo dentro da TRAY
            pyautogui.hotkey('left')
            copiar() #Copia o codigo EAN
            pyautogui.hotkey('right')
            ean = janela.clipboard_get()
            ean = str(ean) #Guarda o ean em uma variavel e o transforma em STRING
            um_segundo()

            #Novamanete tem que entrar na aba do produto da tray e depois de entrar precisa ir dentro do iframe e localizar
            #O elemento novamente para poder edita-lo
            chrome.switch_to.window("produto_tray")
            pausa_curta()
            chrome.switch_to.frame(chrome.find_element(By.XPATH, iframe))
            um_segundo()
            ean_element = chrome.find_element(By.XPATH, "//input[@id='ProductEan']")
            ean_element.send_keys(ean) #Cola o código EAN que copiou no campo de ean da TRAY
            um_segundo()
            pyautogui.scroll(-1000) #Faz um scroll para baixo

            #Apos ter colado o EAN no campo certo basta clicar no botão SALVAR
            chrome.find_element(By.XPATH, "//input[@id='addSaveAndListBtn']").click()
            pausa_curta()
            chrome.close() #Fecha a aba do produto_tray para poder abri-la novamente no proximo ciclo

            #Agora iremos indicar na planilha de anuncios e de ean que fizemos o processo
            chrome.switch_to.window("anuncios")
            pausa_curta()
            pyautogui.hotkey("right")
            pyautogui.write("FEITO")
            um_segundo()
            pyautogui.hotkey("left")

            chrome.switch_to.window("eans")
            pausa_curta()
            pyautogui.hotkey("right")
            pyautogui.write(sku)
            pyautogui.hotkey("enter") #Para confirmar o que escreveu no Google Sheets
            um_segundo()

            qtd_anuncios = qtd_anuncios - 1
            print("Qtd Anuncios {}".format(qtd_anuncios))
            primeiro_ciclo = False
            cod_finalizados.append(sku)
        else:
            primeiro_ciclo = False
            qtd_anuncios = qtd_anuncios - 1
            print("Qtd Anuncios {}".format(qtd_anuncios))
            cod_erros.append(sku)

        if(qtd_anuncios == 0):
            finalizado = Label(janela, text="Processo Finalizado!!!")
            finalizado.grid(column=0, row=17)
            log.criando_log(cod_finalizados, cod_erros)
            em_processo = False

def um_segundo():
    time.sleep(1)

def pausa_longa():
    time.sleep(6.5)

def pausa_10():
    time.sleep(10)

def pausa_curta():
    time.sleep(3)

def mudar_aba_frente():
    pyautogui.hotkey("ctrl", "tab")

def mudar_aba_atras():
    pyautogui.hotkey("ctrl", "shift", "tab")

def abrir_nova_aba():
    pyautogui.hotkey("ctrl", "t")

def colar_link():
    pyautogui.hotkey("ctrl", "v")

def copiar():
    pyautogui.hotkey("ctrl", "c")

def login_tray(chrome):
    #Acha o botão de login e clica nele
    try:
        login = chrome.find_element(By.XPATH, "//button[@id='btn-submit']").click()  # Acha elemento
    except NoSuchElementException:
        print("Não tem botão de login")


