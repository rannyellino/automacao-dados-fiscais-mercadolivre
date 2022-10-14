import pyautogui
import pyperclip
import time
from tkinter import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import navegador
import log

def preechendo_tabela_frete(link_planilha_anuncios, linha_coluna_anuncios, user, qtd_anuncios, janela):
    tabela = ["SÃO PAULO", "47,00", "SANTA CATARINA", "56,90", "PARANA", "56,90", "DISTRITO FEDERAL", "67,90", "MINAS GERAIS", "67,90", "RIO DE JANEIRO", "67,90"
              , "ESPIRITO SANTO", "67,90", "RIO GRANDE DO SUL", "67,90", "MATO GROSSO DO SUL", "82,90", "PE - BA - SE", "93,00", "CE - GO - MT - RN - PB - AL", "105,90"
              , "MA - PI", "115,00", "DEMAIS ESTADOS FAZER COTAÇÃO NAS PERGUNTAS", "R$999,99"] #TABELA DE FRETE PARA ADICIONAR NOS ANUNCIOS
    primeiroCiclo = True  # Checar o primeiro ciclo
    em_processo = True  # saber se ainda está dentro do laço para preencher os dados fiscais
    cod_finalizados = []  # Lista para colocar os códigos finalizados
    cod_erros = []  # Lista para colocar os códigos com erro
    qtd_anuncios = int(qtd_anuncios) #Qunatidade de anuncios que serão editados
    anuncio = r"https://www.mercadolivre.com.br/anuncios/MLB" #link para entrar no anuncio para modificar
    plus_anuncio = r"/modificar/" #string para concatenar com o link para ir para a area de edição do anuncio
    estado_xpath = "//*[@id='shipping_task']//div[2]//div[1]//div//div//div[2]//div//div[2]//div[2]//div//ul//li[{}]//div//label[1]//div[1]//input" #Xpath de elemento da tabela de frete que vai o estado
    valor_xpath = "//*[@id='shipping_task']//div[2]//div[1]//div//div//div[2]//div//div[2]//div[2]//div//ul//li[{}]//div//label[2]//div[1]//input" #Xpath de elemento da tabela de frete que vai o valor

    chrome = navegador.abrindo_navegador(user) #abri navegador
    chrome.maximize_window()

    pausa_longa() #Esperar segundos para o navegador carregar

    # Abrindo uma nova aba e entrando na aba de anuncios
    chrome.execute_script("window.open('about:blank','anuncios');")
    chrome.switch_to.window("anuncios")  # Muda a Aba
    chrome.get(link_planilha_anuncios)
    pausa_longa()

    while(em_processo):
        link_acesso = ""
        i = 0  # Esse servira como indice tanto pro nosso laço quanto pra saber qual valor da tabela ele tem que pegar e colocar nos campos do frete
        i_estado = 1  # Será usado para saber qual é o 'li' que estamos usando na lista/tabela de html do frete
        i_valor = 1  # Será usado para saber qual é o 'li' que estamos usando na lista/tabela de html do frete
        cod_anuncio = ""

        if(primeiroCiclo == True):
            #Procura a celula para começar a pegar os anuncios
            chrome.find_element(By.TAG_NAME, "body").click()
            pausa_curta()
            pyautogui.hotkey("ctrl", "j") #Vai para a area de pesquisa de celula
            um_segundo()
            pyautogui.write(linha_coluna_anuncios) #Escreve a celula
            pyautogui.hotkey("Enter") #Acha a celula
            um_segundo()
            print("Achou a celula de onde começa os anuncios")
        else:
            pausa_curta()
            pyautogui.hotkey("down")
            um_segundo()

        copiar() #Copia o codigo do anuncio
        cod_anuncio = janela.clipboard_get() #Coloca a copia em uma variavel
        cod_anuncio = str(cod_anuncio) #transforma essa copia que é o código do anuncio em uma string
        print("Cod anuncio {}".format(cod_anuncio))

        link_acesso = anuncio+cod_anuncio+plus_anuncio #Concatena essas 3 variaveis pra ter o link certo para a modificação do anuncio

        # Abrindo uma nova aba e entrando no link para editar o anuncio
        chrome.execute_script("window.open('about:blank','editar');")
        chrome.switch_to.window("editar")  # Muda a Aba
        chrome.get(link_acesso)
        pausa_longa()

        #Agora iremos começar a preencher de fato a tabela de frete, mas antes precisamos fazer alguns clicks em alguns elementos do HTML para poder ter a tabela
        try:
            chrome.find_element(By.XPATH, "//*[@id='shipping_header_container']//div//div[1]//h2").click() #Faz o primeiro clique em 'Forma de entrega'
            print("Clicou pela 1x")
            um_segundo()
            element2 = chrome.find_element(By.XPATH, "//*[@id='shipping_task']//div[2]//div[1]//div//div//div[1]//label//input") #Apenas acha o elemento para clicar depois
            um_segundo()
            chrome.execute_script("arguments[0].click();", element2) #Faz o segundo clique em 'Faço envio por minha conta'
            print("Clicou pela 2x")
            element3 = chrome.find_element(By.XPATH, "//*[@id='shipping_task']//div[2]//div[1]//div//div//div[2]//div//div[2]//div[1]//label//span") #Apenas acha o elemento para clicar depois
            um_segundo()
            chrome.execute_script("arguments[0].click();", element3) #Faz o terceiro clique em 'Por conta do comprador'
            print("Clicou pela 3x")

            #AGORA FALTA ADICIONAR TODOS OS CAMPOS NECESSARIOS E PREENCHE-LOS

            #Abaixo vai existir um for para adicionar a quantidade de faixas de frete que queremos na tabela
            for x in range(10):
                adicionar = chrome.find_element(By.XPATH, "//*[@id='shipping_task']//div[2]//div[1]//div//div//div[2]//div//div[2]//div[2]//div//a")
                chrome.execute_script("arguments[0].click();", adicionar) #Clica para adicionar mais uma faixa de frete
                um_segundo()
            while i < 26:
                estado = chrome.find_element(By.XPATH, estado_xpath.format(i_estado)) #pega o elemento que será o estado na tabela de frete
                estado.send_keys(tabela[i]) #coloca o valor correto do estado nesse campo
                i = i + 1 #adiciona mais 1 no indice para saber que agora terá que usar o proximo valor da nossa lista 'tabela'
                time.sleep(0.5)#meio segundo de segurança
                valor = chrome.find_element(By.XPATH, valor_xpath.format(i_valor))#pega o elemento que será o valor de custo na tabela de frete
                valor.send_keys(tabela[i])#coloca o valor correto  nesse campo
                i = i + 1#adiciona mais 1 no indice para saber que agora terá que usar o proximo valor da nossa lista 'tabela'
                i_estado = i_estado+1 #Faz soma pra ir pro proximo 'li' do html
                i_valor = i_valor+1 #Faz soma pra ir pro proximo 'li' do html

            #Precisamos clicar no botão CONFIRMAR para salvar a tabela de frete
            salvar = chrome.find_element(By.XPATH, "//*[@id='shipping_task']//div[2]//div[2]//button[1]")
            chrome.execute_script("arguments[0].click();", salvar) #Clica no botão salvar

            pausa_longa()
            chrome.close() #Fecha a aba do anuncio que tava editando

            # Volta pra aba de anuncios e indica que finalizou o processo daquele anuncio
            chrome.switch_to.window("anuncios")
            um_segundo()
            pyautogui.hotkey("right")
            pyautogui.write("FEITO")
            pyautogui.hotkey("left")

            # Agora depois de finalizado o processo diminui a contagem de anuncios e atribui a codigo finalizados
            qtd_anuncios = qtd_anuncios - 1
            print("Qtd Anuncios {}".format(qtd_anuncios))
            primeiroCiclo = False
            cod_finalizados.append(cod_anuncio)
            um_segundo()

        except NoSuchElementException:
            print("Não achou o ELEMENTO")
            cod_erros.append(cod_anuncio)
            qtd_anuncios = qtd_anuncios - 1
            primeiroCiclo = False
            um_segundo()

        if(qtd_anuncios ==0):
            finalizado = Label(janela, text="Processo Finalizado!!!")
            finalizado.grid(column=0, row=10)
            log.criando_log(cod_finalizados, cod_erros)
            em_processo = False


def pausa_longa():
    time.sleep(6.5)

def pausa_curta():
    time.sleep(3.5)

def um_segundo():
    time.sleep(1)

def colar():
    pyautogui.hotkey("ctrl", "v")

def copiar():
    pyautogui.hotkey("ctrl", "c")