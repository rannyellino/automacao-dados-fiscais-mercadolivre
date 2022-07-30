import pyautogui
import pyperclip
import time
import webbrowser
from tkinter import *

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

    texto_linha_coluna_anuncios = Label(janela, text="Em qual célula começa os Anúcnios")
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

    botao = Button(janela, text="Começar processo", command=lambda: pegando_valores(entry_link_planilha_anuncios, entry_link_planilha_EAN, entry_linha_coluna_anuncios, entry_linha_coluna_ean, entry_qtd_anuncios))
    botao.grid(column=0, row=11) #Indicando posição para o botão
    janela.mainloop() #Deixando a janela aberta

def pegando_valores(entry_link_planilha_anuncios, entry_link_planilha_EAN, entry_linha_coluna_anuncios, entry_linha_coluna_ean, entry_qtd_anuncios):
    #Puxando todos valores do input da interface
    link_planilha_anuncios = entry_link_planilha_anuncios.get()
    link_planilha_EAN = entry_link_planilha_EAN.get()
    linha_coluna_anuncios = entry_linha_coluna_anuncios.get()
    linha_coluna_ean = entry_linha_coluna_ean.get()
    qtd_anuncios = entry_qtd_anuncios.get()

    ncm = "87089200"
    cest = "0107500"

    #Começando a preencher os EAN com base nos valores puxados
    preenchendo_EAN(link_planilha_anuncios, link_planilha_EAN, linha_coluna_anuncios, linha_coluna_ean, ncm, cest, qtd_anuncios)

def preenchendo_EAN(link_planilha_anuncios, link_planilha_EAN, linha_coluna_anuncios, linha_coluna_ean, ncm, cest, qtd_anuncios):
    # Aba de Anuncios do MercadoLivre
    anuncios = r"https://www.mercadolivre.com.br/anuncios/lista?filters=CHANNEL_ONLY_MARKETPLACE|CHANNEL_MARKETPLACE_MSHOPS&page=1&sort=DEFAULT"
    primeiroCiclo = True
    em_processo = True
    total_anuncios = int(qtd_anuncios)

    abrindo_navegador()

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
        #Volta para a aba dos anúncios
        mudar_aba_atras()
        mudar_aba_atras()

        if(primeiroCiclo):
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

            #Volta para a aba dos anúncios
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

        #Pesquisando anuncio
        pyautogui.click(x=469, y=620) #Clicka para pesquisar
        colar_link() #Cola codigo do anuncio
        pyautogui.hotkey("enter") #Pesquisa

        pausa_curta()  # Espera segundos por precaução

        #Abrindo os dados fiscais do anúncios
        pyautogui.click(x=1537, y=616)
        um_segundo() # Espera segundos por precaução
        pyautogui.click(x=1377, y=748)
        pausa_curta() # Espera segundos por precaução
        pyautogui.click(x=502, y=321)
        pausa_curta() # Espera segundos por precaução
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
        pyautogui.hotkey("down")
        um_segundo() # Espera segundos por precaução
        pyautogui.hotkey("down") #Chegando até o SKU
        copiar()

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
        pyautogui.hotkey("Down")
        pyautogui.hotkey("Down")
        pyautogui.hotkey("Down")
        pyautogui.hotkey("Down") #Chegando na opção certa
        um_segundo()  # Espera segundos por precaução
        pyautogui.hotkey("Enter")  #Selecionando 500
        um_segundo()  # Espera segundos por precaução

        #Preenchendo nas planilhas de anuncios e de EAN

        #Voltando para a planilha de anúncios
        mudar_aba_atras()
        mudar_aba_atras()

        pausa_curta() # Espera segundos por precaução

        pyautogui.hotkey("up")
        um_segundo()
        pyautogui.hotkey("up") #Volta para o código do anúncio
        copiar()

        #Vai até a aba de EAN
        mudar_aba_frente()
        pausa_curta()  # Espera segundos por precaução

        #Cola o código do anúncio ao EAN referente
        colar_link() #Cola o código do anúncio que editou o EAN
        um_segundo()
        pyautogui.click(x=710, y=186)
        um_segundo()
        pyautogui.click(x=807, y=373) #Pinta de verde para indicar que é a conta SCAPJÁ
        um_segundo()

        #Vai até a aba de ANÚNCIOS
        mudar_aba_atras()
        pausa_curta()

        pyautogui.hotkey("right")
        pyautogui.click(x=710, y=186)
        um_segundo()
        pyautogui.click(x=807, y=373)  # Pinta de verde para indicar que preencheu o EAN
        um_segundo()
        pyautogui.hotkey("left")

        #Indo até a ABA do MercadoLivre
        mudar_aba_frente()
        mudar_aba_frente()

        pausa_curta()

        #Salvando os dados fiscais e voltando para a página de anuncios normal
        pyautogui.click(x = 461, y = 816)
        qtd_anuncios = qtd_anuncios - 1
        #print(qtd_anuncios)
        pausa_curta()
        pyautogui.click(x=748, y=570) #Voltando para a lista de anuncios
        pausa_longa()

        primeiroCiclo = False;
        #print(primeiroCiclo)
        #print(em_processo)
        if(qtd_anuncios == 0):
            em_processo = False
            print("Processo finalizado foi preenchido o EAN de {} anúncios".format(total_anuncios))

def abrindo_navegador():
    # Abrindo Chrome(NAVEGADOR PADRÃO DO WINDOWS)
    webbrowser.get().open(r'https://www.google.com.br/')

def um_segundo():
    time.sleep(1)

def pausa_longa():
    time.sleep(5.5)

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