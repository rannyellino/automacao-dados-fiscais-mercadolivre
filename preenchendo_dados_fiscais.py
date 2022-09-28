import pyautogui
import pyperclip
import time
from tkinter import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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
                else:
                    print("não é catalisador")


            #Indo até o campo nome do produto e colando
            um_segundo()
            pyautogui.click(elementos_loc[8], elementos_loc[9])
            colar_link()

            #Preenchendo Outros Dados
            pyautogui.hotkey("Tab")
            if(checa_catalisador == 0):
                ncm = "87089200"
            else:
                ncm = "84213200"
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

def um_segundo():
    time.sleep(1)

def pausa_longa():
    time.sleep(6.5)

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


