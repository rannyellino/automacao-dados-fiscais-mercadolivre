import datetime

import discord
import navegador
import time
import os
import verify
import pandas as pd
import calc
import emoji
import requests
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logado como {self.user}!')

    async def on_message(self, message):
        print(f'Messagem de {message.author}: {message.content}')

        if message.content == '?inutil':
            await message.channel.send(f'{message.author.mention} o inútil do servidor é o Guilherme')

        if '?verify' in message.content:
            #Achando o link e código MLB
            message_str = str(message.content)
            find_link = message_str.find("?verify")
            link_mlb = message_str[0: 0:] + message_str[find_link + 8::]

            #Código MLB
            find_cod_mlb = link_mlb.find("-")
            cod_mlb = link_mlb[0: 0:] + link_mlb[find_cod_mlb + 1::]
            find_cod_mlb = cod_mlb.find("-")
            cod_mlb = cod_mlb[0: find_cod_mlb:] + cod_mlb[len(cod_mlb) + 1::]
            cod_mlb = "MLB"+cod_mlb

            #Recebendo dados da API
            account, preco_anuncio, frete_gratis, garantia, status, date_created = get_api(cod_mlb)

            chrome = open_link(link_mlb)
            one_sec()

            lista_codigos = []

            while (lista_codigos == None or lista_codigos == []):
                lista_codigos = identify_parts(chrome)
                time.sleep(10)
                chrome.refresh()

            print("Lista Códigos {}".format(lista_codigos))
            preco_correto = calc_parts(lista_codigos, chrome, account)
            diff = difference_price(preco_correto, preco_anuncio)
            resume_feedback_emoji = resume_feedback(diff, frete_gratis, garantia)
            close_chrome(chrome)

            await message.channel.send(f'{message.author.mention}{os.linesep}{os.linesep}Link do anúncio: {link_mlb}{os.linesep}Cod do anúncio: {cod_mlb}{os.linesep}{os.linesep}'
                                       f'Conta: {account}{os.linesep}Peças: {lista_codigos}{os.linesep}{garantia}{os.linesep}'
                                       f'Status: {status}{os.linesep}Preço do Anuncio: R${preco_anuncio}{os.linesep}Preço Correto: R${preco_correto}{os.linesep}'
                                       f'Diferença de Preço: {diff}%{os.linesep}{os.linesep}{resume_feedback_emoji}{os.linesep}{os.linesep}Data de Criação: {date_created}')

            # await message.channel.send(f'{message.author.mention} link do anuncio é '+"{}".format(link_mlb)
            #                            +f'{os.linesep}{os.linesep}'+"Anuncio na conta: {}".format(account)+f'{os.linesep}'
            #                            +"Peças: {}".format(lista_codigos)+f'{os.linesep}'+"Preço do Anuncio: R${}".format(preco_anuncio)+f'{os.linesep}'+
            #                            "Preço Correto: R${}".format(preco_correto)+f'{os.linesep}{os.linesep}'+"Diferença de Preço: {}%".format(diff)+f'{os.linesep}{os.linesep}'+
            #                           emoji_price)

def calc_parts(lista_codigos, chrome, account):
    print("Lista Códigos: {}\n Conta: {}\n\n".format(lista_codigos, account))
    valores_vendas = []
    custo_frete = 35
    have_consulte = False
    have_pesada = False

    #Calcular o valor das peças mas antes de tudo precisamos checar se tem frete grátis

    free_shipping = ''
    free_shipping_xpath = '//*[@id="shipping_summary"]/div/div/p[1]'

    try:
        free_shipping_element = chrome.find_element(By.XPATH, free_shipping_xpath)
        free_shipping = 'yes'
        print("Tem frete grátis")
    except NoSuchElementException:
        free_shipping = 'no'
        print("Não tem frete grátis")

    #Agora precisamos verificar a quantidade de cada peça e também se existe brindes
    check_units = ['2x', '3x', '4x', '5x', '6x', '7x', '8x', '9x', '10x']
    qtds = []
    codigos = []

    for i in lista_codigos:
        for u in check_units:
            if u in i:
                print("Tem {} unidades da peça {}".format(u, i))
                qtd_i = u
                qtd_i = qtd_i.replace("x", "")
                qtds.append(qtd_i)
                codigo = i.replace("{}".format(u),"")
                codigos.append(codigo)
                break
            elif(u == '10x'):
                qtd_i = 1
                codigos.append(i)
                print("Tem {} unidades da peça {}".format(qtd_i, i))
                qtds.append(qtd_i)

    print("Peças: {}".format(codigos))
    print("Quantidades: {}".format(qtds))

    #Vamos verificar se há a existencia de algum brinde
    brindes = ['(brinde)', '(abraçadeira)', '(coxim)', '(junta)', '(anel)']
    count = 0

    for i in codigos:
        cod = str(i).lower()
        count = count + 1
        for b in brindes:
            if b in i:
                print("Tem brinde")
                codigos.pop(count-1)
                qtds.pop(count-1)
                print("Peças2: {}".format(codigos))
                print("Quantidades2: {}".format(qtds))

    # Pegando a planilha com os códigos das peças e preços
    df_base = pd.read_excel('Peças-Preços.xlsx')
    print(df_base)

    i_for = 0
    qtd_i = 0

    while (i_for < codigos.__len__()):
        for i in codigos:
            if (i != "" or i != None):  # Checa se há algum valor no código da peça
                print("Entrou no if dentro do for")
                print("Peça: {}".format(i))
                filtro = df_base.loc[df_base["Cod Peça"] == i.upper().strip()]  # Procura a linha com o código da peça
                lista = list(
                    filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores

                # Caso a lista continue em branco é porque não achou a peça na planilha, um dos motivos pode ser a pesquisa em STR sendo que tem que ser em INT
                if (lista == []):
                    try:
                        filtro = df_base.loc[df_base["Cod Peça"] == int(i)]  # Procura a linha com o código da peça
                        lista = list(
                            filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
                    except ValueError:
                        print("Peça não existe")

                # Verifica se tem valor na lista, se não tiver é porque não encontrou o código na planilha
                print(lista)
                if (lista != []):
                    # 0 = Fabricante, 1 = Linha, 2 = Código da Peça, 3 = Preço, 4 = Tipo de Peça(Escap, Fix, Catalisador)
                    fab = lista[0]
                    linha = lista[1]
                    cod = lista[2]
                    preco = lista[3]
                    tipo = lista[4]

                    # Encontrando o indice da fabrica
                    indice = calc.indice_fabricante(fab, linha, tipo)

                    print("Quantidade I: {}".format(qtd_i))
                    qtd = int(qtds[qtd_i])

                    # Verifica se a peça é sob consulte
                    if (preco == "Consulte"):
                        have_consulte = True
                        #pecas_consulte.append(cod)

                    if (preco != "Consulte"):
                        have_brinde = False

                        # Calculado quantidade de itens x o preço x o indice para ter assim o valor de custo
                        print("Quantidade Peça: ", qtd)
                        custo = qtd * preco * indice
                        print("Valor de Preço*Indice {}".format(custo))

                        # Chama função para definir as margens e checar regra de custo
                        custo, margem_scapja, margem_soescap = calc.margem(custo, fab, linha, codigos, have_brinde)

                        # Calcula o valor de venda final para cada canal mas sem o MercadoEnvios
                        if (linha == "Leve" or linha == "Pesada"):
                            venda_scapja = custo * margem_scapja
                            valores_vendas.append(venda_scapja)
                            print("Venda Scapjá:", venda_scapja, "Margem:", margem_scapja)
                            venda_soescap = custo * margem_soescap
                            valores_vendas.append(venda_soescap)
                            print("Venda SoEscap:", venda_soescap, "Margem:", margem_soescap)
                        if (linha == "Pesada"):
                            have_pesada = True
                        elif (linha == "Fix"):
                            if (custo > 50 and fab == "Fix" and preco > 50):
                                custo = custo * 0.7
                                venda_scapja = custo
                                valores_vendas.append(venda_scapja)
                                print("Venda Scapjá:", venda_scapja, "Margem:", margem_scapja)
                                venda_soescap = custo
                                valores_vendas.append(venda_soescap)
                                print("Venda SoEscap:", venda_soescap, "Margem:", margem_soescap)
                            else:
                                venda_scapja = custo
                                valores_vendas.append(venda_scapja)
                                print("Venda Scapjá:", venda_scapja, "Margem:", margem_scapja)
                                venda_soescap = custo
                                valores_vendas.append(venda_soescap)
                                print("Venda SoEscap:", venda_soescap, "Margem:", margem_soescap)
                        i_for = i_for + 1
                        qtd_i = qtd_i + 1
                    else:
                        i_for = i_for + 1
                        break
                else:
                    have_consulte = True
                    #pecas_consulte.append(i)
                    i_for = i_for + 1
                    qtd_i = qtd_i + 1

    if (i_for == codigos.__len__()):
        print(valores_vendas)
        if (valores_vendas.__len__() < 19):
            for i in range(19):
                valores_vendas.append(0)
        if (have_consulte == True or codigos == []):
            valores_vendas.append(0)
            custo_frete = 0

        if(free_shipping == 'no'):
            custo_frete = 0

        # Soma os valores de cada peça pra ter o valor de venda final
        print("Custo frete", custo_frete)
        venda_scapja = int(valores_vendas[0]) + int(valores_vendas[2]) + int(valores_vendas[4]) + int(valores_vendas[6]) \
                       + int(valores_vendas[8]) + int(valores_vendas[10]) + int(valores_vendas[12]) + int(
            valores_vendas[14]) \
                       + int(valores_vendas[16]) + int(valores_vendas[18])
        venda_scapja = venda_scapja + custo_frete

        venda_soescap = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(
            valores_vendas[7]) + int(valores_vendas[9]) \
                        + int(valores_vendas[11]) + int(valores_vendas[13]) + int(valores_vendas[15]) + int(
            valores_vendas[17]) + int(valores_vendas[19])
        venda_soescap = venda_soescap + custo_frete

        venda_tray = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(
            valores_vendas[7]) + int(valores_vendas[9]) \
                     + int(valores_vendas[11]) + int(valores_vendas[13]) + int(valores_vendas[15]) + int(
            valores_vendas[17]) + int(valores_vendas[19]) + 3
        if (have_pesada == True):
            venda_scapja = venda_scapja + (venda_scapja * 0.1)
            venda_soescap = venda_soescap + (venda_soescap * 0.1)
            venda_tray = venda_tray + (venda_tray * 0.1)

        venda_shops = venda_scapja - custo_frete
        print(venda_shops)
        venda_shops = venda_shops - (venda_shops * 0.1)
        print(venda_shops)
        venda_shops = venda_shops + custo_frete
        print(venda_shops)

        print("Valor de Venda ScapJá: {}".format(venda_scapja))
        print("Valor de Venda Shops: {}".format(venda_shops))
        print("Valor de Venda SoEscap: {}".format(venda_soescap))
        print("Valor de Venda Tray: {}".format(venda_tray))

        print("A conta é: {}".format(account))

        if(account == "ScapJá"):
            print("Conta: {} Valor de Venda: {}".format(account, venda_scapja))
            return venda_scapja
        if(account == "SoEscap"):
            print("Conta: {} Valor de Venda: {}".format(account, venda_soescap))
            return venda_soescap


def close_chrome(chrome):
    one_sec()
    chrome.close()

def resume_feedback(diff, frete_gratis, garantia):
    emojis_resume_list = []

    if (diff < 2.0 and diff > -2.0):
        emoji_price = emoji.emojize("PREÇO: :check_mark_button:", language='en')
    else:
        emoji_price = emoji.emojize("PREÇO: :quadrado_vermelho:", language='pt')

    emojis_resume_list.append(emoji_price)

    if (garantia == "Garantia de fábrica: 1 anos" or garantia == "Garantia de fábrica: 12 meses"):
        emoji_garantia = emoji.emojize("GARANTIA: :check_mark_button:", language='en')
    else:
        emoji_garantia = emoji.emojize("GARANTIA: :quadrado_vermelho:", language='pt')

    emojis_resume_list.append(emoji_garantia)

    if(frete_gratis == "yes"):
        emoji_frete = emoji.emojize("FRETE: :check_mark_button:", language='en')
    else:
        emoji_frete = emoji.emojize("FRETE: :quadrado_vermelho:", language='pt')

    emojis_resume_list.append(emoji_frete)

    emojis_resume_str = f"{emojis_resume_list[0]}{os.linesep}{emojis_resume_list[1]}{os.linesep}{emojis_resume_list[2]}{os.linesep}"

    return emojis_resume_str
def difference_price(preco_correto, preco_anuncio):
    print("Preço Correto: {}\nPreço Anuncio: {}".format(preco_correto, preco_anuncio))
    diff = (preco_correto - preco_anuncio) / preco_anuncio * 100
    diff = round(diff, 2)

    return diff

def get_api(cod_mlb):
    #variaveis
    account = ""
    preco_anuncio = 0
    frete_gratis = ""
    garantia = ""
    status = ""

    #Configurando requisição GET para a API
    url = r"https://api.mercadolibre.com/items/{}".format(cod_mlb)
    print(url)

    response = requests.get(url)
    data = response.json()
    code = response.status_code

    print(response)
    print(data)
    print("STATUS CODE {}".format(code))

    #Caso a resposta da API seja um sucesso vamos começar a guardar as informações que queremos
    if (response.status_code == 200):
        #Salvando Conta
        if data["seller_id"] == 84058800:
            account = "ScapJá"
        elif data["seller_id"] == 142839488:
            account = "SoEscap"

        #Salvando Preço
        preco_anuncio = data["price"]

        #Salvando Frete Grátis
        if data["shipping"]["free_shipping"] == True:
            frete_gratis = 'yes'
        else:
            frete_gratis = 'no'

        #Salvando Garantia
        garantia = data["warranty"]

        #Salvando Status
        if data["status"] == "active":
            status = "Ativo"
        else:
            status = "Inativo"

        #Salvando a data de criação do anuncio
        date_created_str = data["date_created"]

        find_time = date_created_str.find("T")
        print(find_time)
        date_created_str = date_created_str[0: find_time:] + date_created_str[40::]
        print(date_created_str)

        date_created = datetime.strptime(date_created_str, '%Y-%m-%d')
        date_created = date_created.strftime("%d-%m-%Y")

    print("P" + str(account) + str(preco_anuncio) + str(frete_gratis) + str(garantia) + str(status))

    return account, preco_anuncio, frete_gratis, garantia, status, date_created

def open_link(link_mlb):
    # Função para abrir o link que foi identificado atraves da messagem do usuário

    # Abrindo navegador do usuário
    chrome = navegador.open_chrome_dc()
    pausa_curta()
    chrome.execute_script("window.open('{}','mlb');".format(link_mlb))
    pausa_curta()
    chrome.switch_to.window('mlb')
    pausa_curta()
    print("Abriu navegador com sucesso")

    return chrome

def identify_price(chrome):
    price_xpath = '//*[@id="price"]/div/div[1]/div[1]/span/span[3]'

    try:
        price_element = chrome.find_element(By.XPATH, price_xpath)
        price = int(price_element.text)
    except NoSuchElementException:
        print("Não achou informações de preço")

    return price,

def identify_account(chrome):
    #Função focada em identificar em qual conta foi feito o anuncio

    scapja_xpath = '//*[@id="price"]/div/div[1]/div[2]/p'
    account = ''

    try:
        scapja_element = chrome.find_element(By.XPATH, scapja_xpath)
        juros = scapja_element.text
        if 'sem juros' in juros:
            account = r'ScapJá'
        else:
            account = r'SoEscap'
    except NoSuchElementException:
        print("Não achou informações de juros")

    return account

def identify_parts(chrome):
    #Função para verificar quais são os códigos das peças
    global lista_codigos
    print("Chamou a função indetify_parts")
    desc_xpath = '//*[@id="description"]/div/p'

    try:
        desc_element = chrome.find_element(By.XPATH, desc_xpath)
        desc = desc_element.text
        codigos = verify.identificar_codigos(desc)

        # Continua eliminando caracteres a mais que não sejam códigos
        codigos = codigos.replace(":", "")
        #codigos_lista.append(codigos)  # Adiciona na lista de códigos a sequencia de códigos do anuncio que o robo identificou
        codigos = codigos.replace(" ", "")
        codigos = codigos.replace("\n", "")
        codigos = codigos.replace("LinhaPesada", "")
        codigos = codigos.replace("+", ",")
        print("432 - Codigos: {}".format(codigos))

        # Após limpar toda a string e deixar apenas os códigos separados por "," vamos guardar os códigos como uma lista
        lista_codigos = codigos.split(",")
        print(lista_codigos.__len__())
        print(lista_codigos)
        return lista_codigos
    except NoSuchElementException:
        print("Não conseguiu achar descrição")



def pausa_longa():
    time.sleep(4.5)

def pausa_curta():
    time.sleep(2)

def one_sec():
    time.sleep(1)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTEzMDg3NTkyNTExOTEwNzEzMw.GrnDDg.PnYj49II4Sf_Ik19rHtxwrIkE6YOS14-m06q_0')