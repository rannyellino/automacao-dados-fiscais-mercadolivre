import pyautogui
import pyperclip
import time
import webbrowser
from tkinter import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def main():
    #Criando interface
    janela = Tk() #Criando Janela
    janela.title("Automatização de Dados Fiscais e EAN - MercadoLivre") #Alterando o título da Janela

    texto_orientacao = Label(janela, text="Preencha todos os campos abaixo e após isso clique no botão para começar o processo!!!\n\nEste programa foi feito"
                                          " com o intuito de ajudar quem precisa preencher varios dados fiscais de varios anuncios e em vez de fazer tudo isso "
                                          "a mão\n eu @rannyellino decidi fazer um robo que fizesse isso tudo de forma automatizada onde você apenas precisaria "
                                          "indicar atraves de planilhas quais\n lista de anuncios ele vai trabalhar e quais EANs ele tem que usar\n") #Criando um texto
    texto_orientacao.grid(column=0, row=0) #Indicando posição do texto


    texto_link_planilha_anuncios = Label(janela, text="Coloque o link da planilha de anuncios")
    texto_link_planilha_anuncios.grid(column=0, row=1)
    entry_link_planilha_anuncios = Entry(janela, width=110) #Input para o link da planilha
    entry_link_planilha_anuncios.grid(column=0, row=2)

    texto_link_planilha_EAN = Label(janela, text="Coloque o link da planilha de EAN")
    texto_link_planilha_EAN.grid(column=0, row=3)
    entry_link_planilha_EAN = Entry(janela, width=110) #Input para o link da planilha
    entry_link_planilha_EAN.grid(column=0, row=4)

    texto_linha_coluna_anuncios = Label(janela, text="Em qual célula começa os Anúncios")
    texto_linha_coluna_anuncios.grid(column=0, row=5)
    entry_linha_coluna_anuncios = Entry(janela, width=20) #Input para qual célula começa os anuncios
    entry_linha_coluna_anuncios.grid(column=0, row=6)

    texto_linha_coluna_ean = Label(janela, text="Em qual célula começa os EAN disponiveis")
    texto_linha_coluna_ean.grid(column=0, row=7)
    entry_linha_coluna_ean = Entry(janela, width=20) #Input para qual célula começa os EAN
    entry_linha_coluna_ean.grid(column=0, row=8)

    texto_linha_qtd_anuncios = Label(janela, text="Quantidade de anuncios que você quer alterar")
    texto_linha_qtd_anuncios.grid(column=0, row=9)
    entry_qtd_anuncios = Entry(janela, width=20) #Input para saber quantos anuncios editar
    entry_qtd_anuncios.grid(column=0, row=10)

    #Selecionar Conta, 1 = ScapJá, 2 = SoEscap
    texto_conta = Label(janela, text="Qual conta será usada ? 1 = ScapJá, 2 = SoEscap")
    texto_conta.grid(column=0, row=11)
    entry_conta = Entry(janela, width=20)  # Input para saber quantos anuncios editar
    entry_conta.grid(column=0, row=12)

    botao = Button(janela, text="Começar processo", command=lambda: pegando_valores(entry_link_planilha_anuncios, entry_link_planilha_EAN, entry_linha_coluna_anuncios, entry_linha_coluna_ean, entry_qtd_anuncios, entry_conta, janela))
    botao.grid(column=0, row=13) #Indicando posição para o botão

    janela.mainloop() #Deixando a janela aberta

def pegando_valores(entry_link_planilha_anuncios, entry_link_planilha_EAN, entry_linha_coluna_anuncios, entry_linha_coluna_ean, entry_qtd_anuncios, entry_conta, janela):
    #Puxando todos valores do input da interface
    link_planilha_anuncios = entry_link_planilha_anuncios.get()
    link_planilha_EAN = entry_link_planilha_EAN.get()
    linha_coluna_anuncios = entry_linha_coluna_anuncios.get()
    linha_coluna_ean = entry_linha_coluna_ean.get()
    qtd_anuncios = entry_qtd_anuncios.get()
    conta = entry_conta.get()
    janela = janela
    print(conta)

    ncm = "87089200"
    cest = "0107500"

    #Começando a preencher os EAN com base nos valores puxados
    preenchendo_EAN(link_planilha_anuncios, link_planilha_EAN, linha_coluna_anuncios, linha_coluna_ean, ncm, cest, qtd_anuncios, conta, janela)

def preenchendo_EAN(link_planilha_anuncios, link_planilha_EAN, linha_coluna_anuncios, linha_coluna_ean, ncm, cest, qtd_anuncios, conta, janela):
    # Aba de Anuncios do MercadoLivre
    anuncios = r"https://www.mercadolivre.com.br/anuncios/lista?filters=CHANNEL_ONLY_MARKETPLACE|CHANNEL_MARKETPLACE_MSHOPS&page=1&sort=DEFAULT" #É o mesmo link indepedente da conta
    dados_fiscais = r"https://myaccount.mercadolivre.com.br/fiscal-information/item/MLB" #link para entrar na parte fiscal de um anúncio
    primeiroCiclo = True
    em_processo = True
    qtd_anuncios_number = int(qtd_anuncios)
    print(conta)
    print(type(conta))
    print(qtd_anuncios_number)
    print(type(qtd_anuncios_number))

    chrome = abrindo_navegador() #Chamando a função com Selenium e recebendo o valor do chrome
    chrome.maximize_window() #maximizando a janela
    print(chrome)

    pausa_curta() #Espera segundos por precaução

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

    pausa_curta() #Espera segundos por precaução

    # Laço para saber se já preencheu o EAN de todos os anúncios
    while (em_processo):
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

        pausa_longa()

        pyautogui.click(x=502, y=321)
        pausa_curta()  # Espera segundos por precaução x=409, y=370
        pyautogui.click(x=409, y=370) # Clica no SKU que é o primeiro campo
        pyautogui.hotkey("ctrl", "a") # Seleciona todo valor do campo
        pyautogui.hotkey("ctrl", "c")  # Copia o que tiver no campo SKU
        text_copiado = janela.clipboard_get() #Pega o valor copiado e coloca em uma váriavel
        if(text_copiado == ""):
            pyautogui.hotkey("Tab")
            pyautogui.hotkey("Tab")
            pyautogui.hotkey("Tab")
            pyautogui.hotkey("Tab")
            pyautogui.hotkey("Tab")

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
            pyautogui.hotkey("Tab")
            pyautogui.hotkey("Tab") # Chegou até o campo EAN
            colar_link()

            um_segundo()  # Espera segundos por precaução

            #Copiando nome do produto
            pyautogui.click(x=1271, y=278, clicks=3)
            copiar()

            #Indo até o campo nome do produto e colando
            pyautogui.click(x=411, y=671)
            colar_link()

            #Preenchendo Outros Dados
            pyautogui.hotkey("Tab")
            pyautogui.write(ncm) #Preenchendo NCM
            um_segundo()  # Espera segundos por precaução
            pyautogui.hotkey("Tab")
            pyautogui.hotkey("Tab")
            pyautogui.write(cest) #Preenchendo CEST
            um_segundo()  # Espera segundos por precaução
            pyautogui.hotkey("Tab")
            pyautogui.click(x=548, y=912) #Abrindo opções de origem
            um_segundo()  # Espera segundos por precaução
            pyautogui.hotkey("Down")
            pyautogui.hotkey("Enter") #Selecionando Nacional
            um_segundo()  # Espera segundos por precaução
            pyautogui.hotkey("Tab")
            pyautogui.hotkey("Tab")
            pyautogui.hotkey("Enter") #Abrindo CSOSN do ICMS
            um_segundo()  # Espera segundos por precaução

            if(conta == "1"): # Se for ScapJá
                pyautogui.hotkey("Down")
                pyautogui.hotkey("Down")
                pyautogui.hotkey("Down")
                pyautogui.hotkey("Down") #Chegando na opção certa
                um_segundo()  # Espera segundos por precaução
                pyautogui.hotkey("Enter")  #Selecionando 500
                um_segundo()  # Espera segundos por precaução
            elif(conta == "2"): # Se for SoEscap
                pyautogui.hotkey("Down") #Chegando na opção certa
                um_segundo()
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
            pyautogui.click(x=710, y=186)
            um_segundo()
            if(conta == "1"): #Se for ScapJá
                pyautogui.click(x=807, y=373) #Pinta de verde para indicar que é a conta SCAPJÁ
                um_segundo()
            elif(conta == "2"):
                pyautogui.click(x=783, y=378)  # Pinta de amarelo para indicar que é a conta SoEscap
                um_segundo()

            #Vai até a aba de ANÚNCIOS
            mudar_aba_atras()
            pausa_curta()

            pyautogui.hotkey("right")
            pyautogui.click(x=710, y=186)
            um_segundo()
            pyautogui.click(x=807, y=373)  # Pinta de verde para indicar que finalizou o processo de preencher dados fiscais e EAN
            um_segundo()
            pyautogui.hotkey("left")

            #Indo até a ABA do MercadoLivre
            mudar_aba_frente()
            mudar_aba_frente()

            pausa_curta()

            #Salvando os dados fiscais e voltando para a página de anuncios normal
            pyautogui.click(x = 461, y = 816)
            qtd_anuncios_number = qtd_anuncios_number - 1
            print(qtd_anuncios_number)
            #print(qtd_anuncios)
            pausa_curta()
            pyautogui.click(x=748, y=570) #Voltando para a lista de anuncios
            pausa_longa()

            primeiroCiclo = False;
            #print(primeiroCiclo)
            #print(em_processo)
            if(qtd_anuncios_number == 0):
                finalizado = Label(janela, text="Processo Finalizado!!!")
                finalizado.grid(column=0, row=14)
                em_processo = False
                #print("Processo finalizado foi preenchido o EAN de {} anúncios".format(total_anuncios))
        else:
            qtd_anuncios_number = qtd_anuncios_number - 1
            pausa_curta()
            primeiroCiclo = False;
            if (qtd_anuncios_number == 0):
                finalizado = Label(janela, text="Processo Finalizado!!!")
                finalizado.grid(column=0, row=14)
                em_processo = False
                # print("Processo finalizado foi preenchido o EAN de {} anúncios".format(total_anuncios))

def abrindo_navegador():
    # Abrindo Chrome(NAVEGADOR PADRÃO DO WINDOWS)
    s = Service(ChromeDriverManager().install())
    options = Options() #Para poder pegar o perfil do chrome
    options.add_argument(r"user-data-dir=C:\Users\Rannyel\AppData\Local\Google\Chrome\User Data") #Indicado diretorio do perfil do chrome
    chrome = webdriver.Chrome(service=s, options=options) #Passando parametros do chrome
    chrome.maximize_window()
    chrome.get("https://google.com.br") #abri o chrome com o endereço indicado
    print(chrome)
    return chrome

def um_segundo():
    time.sleep(1)

def pausa_longa():
    time.sleep(6)

def pausa_curta():
    time.sleep(2.5)

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

if __name__ == '__main__':
    main()