import tkinter
from tkinter import *
import pandas as pd
import openpyxl
import pyperclip
import googlesheets as gs

import interface

def calc(janela, qtd_1, qtd_2, qtd_3, qtd_4, qtd_5, qtd_6, qtd_7, qtd_8, qtd_9, qtd_10, cod_1, cod_2, cod_3, cod_4, cod_5, cod_6, cod_7, cod_8, cod_9, cod_10, custo_frete):
    #Agrupando as quantidades e codigos dos anuncios
    qtds = [qtd_1, qtd_2, qtd_3, qtd_4, qtd_5, qtd_6, qtd_7, qtd_8, qtd_9, qtd_10]
    cods = [cod_1, cod_2, cod_3, cod_4, cod_5, cod_6, cod_7, cod_8, cod_9, cod_10]
    print("qtds: ",qtds)
    custo_frete = int(custo_frete)
    print("Custo de frete:", custo_frete)
    custo = 0
    valores_vendas = []
    i_for = 0
    qtd_i = 0
    have_brinde = False
    have_pesada = False
    have_consulte = False
    have_nao_fabrica = False
    pecas_consulte = []
    pecas_nao_fabrica = []
    fabs = []
    fixacoes = []
    global sob_consulte
    sob_consulte = Label(janela, text="", font=interface.font_default(), justify="center")
    sob_consulte.grid(column=0, row=17, columnspan=1)
    sob_consulte['text'] = ''

    #Verificando os valores que tem na lista, o que não tiver valor é excluido da lista
    if (cods[9] == ''):
        cods.pop(9)
        qtds.pop(9)
    if (cods[8] == ''):
        cods.pop(8)
        qtds.pop(8)
    if (cods[7] == ''):
        cods.pop(7)
        qtds.pop(7)
    if (cods[6] == ''):
        cods.pop(6)
        qtds.pop(6)
    if (cods[5] == ''):
        cods.pop(5)
        qtds.pop(5)
    if(cods[4] == ''):
        cods.pop(4)
        qtds.pop(4)
    if(cods[3] == ''):
        cods.pop(3)
        qtds.pop(3)
    if(cods[2] == ''):
        cods.pop(2)
        qtds.pop(2)
    if(cods[1] == ''):
        cods.pop(1)
        qtds.pop(1)
    if(cods[0] == ''):
        cods.pop(0)
        qtds.pop(0)

    print("Códigos Limpos: {}".format(cods))
    print("Quantidades Limpas: {}".format(qtds))

    #Pegando a planilha com os códigos das peças e preços
    df_base = gs.main()
    print(df_base)

    while(i_for < cods.__len__()):
        for i in cods:
            print("I FOR: {}".format(i_for))
            if(i != "" or i != None): #Checa se há algum valor no código da peça
                print("Entrou no if dentro do for")
                print("Peça: {}".format(i))
                filtro = df_base.loc[df_base["Cod Peça"] == i.upper().strip()] #Procura a linha com o código da peça
                lista = list(filtro.values.flatten()) #Transforma a linha da planilha em uma lista para termos os valores

                #Caso a lista continue em branco é porque não achou a peça na planilha, um dos motivos pode ser a pesquisa em STR sendo que tem que ser em INT
                if(lista == []):
                    try:
                        filtro = df_base.loc[df_base["Cod Peça"] == int(i)]  # Procura a linha com o código da peça
                        lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
                    except ValueError:
                        print("Peça não existe")

                #Verifica se tem valor na lista, se não tiver é porque não encontrou o código na planilha
                print(lista)
                if(lista != []):
                    #0 = Fabricante, 1 = Linha, 2 = Código da Peça, 3 = Preço, 4 = Tipo de Peça(Escap, Fix, Catalisador)
                    fab = lista[0]
                    linha = lista[1]
                    cod = lista[2]
                    try:
                        preco = int(lista[3])
                    except ValueError:
                        try:
                            if(lista[3] != "Consulte" or lista[3] != "Nao Fabrica"):
                                preco = int(float(lista[3]))
                            else:
                                preco = "Consulte"
                        except ValueError:
                            preco = lista[3]
                    tipo = lista[4]

                    print("Preço: ", preco)
                    #Encontrando o indice da fabrica
                    indice = indice_fabricante(fab, linha, tipo)

                    print("Quantidade I: {}".format(qtd_i))
                    qtd = int(qtds[qtd_i])
                    print()

                    #Verifica se a peça é sob consulte
                    if(preco == "Consulte"):
                        have_consulte = True
                        pecas_consulte.append(cod)

                    # Verifica se a peça é sob consulte
                    if (preco == "Nao Fabrica"):
                        have_nao_fabrica = True
                        pecas_nao_fabrica.append(cod)

                    print("Peças Sob Consulte: {}".format(pecas_consulte))
                    print("Peças Não Fabrica: {}".format(pecas_nao_fabrica))

                    if(preco != "Consulte" and preco != "Nao Fabrica"):
                        #Calculado quantidade de itens x o preço x o indice para ter assim o valor de custo
                        fabs.append(fab)
                        print("Quantidade Peça: ",qtd)
                        custo = qtd*preco*indice
                        print("Valor de Preço*Indice {}".format(custo))

                        #Chama função para definir as margens e checar regra de custo
                        custo, margem_scapja, margem_soescap = margem(custo, fab, linha, cods, have_brinde, tipo, i)

                        #Calcula o valor de venda final para cada canal mas sem o MercadoEnvios
                        if(linha == "Leve" or linha == "Pesada"):
                            venda_scapja = custo * margem_scapja
                            valores_vendas.append(venda_scapja)
                            print("Venda Scapjá:", venda_scapja, "Margem:", margem_scapja)
                            venda_soescap = custo * margem_soescap
                            valores_vendas.append(venda_soescap)
                            print("Venda SoEscap:", venda_soescap, "Margem:", margem_soescap)
                        if(linha == "Pesada"):
                            have_pesada = True
                        elif(linha == "Fix"):
                            if(fab == "Fix"):
                                fixacoes.append(int(custo))
                            #     custo = custo * 0.7
                            #     venda_scapja = custo
                            #     valores_vendas.append(venda_scapja)
                            #     print("Venda Scapjá:", venda_scapja, "Margem:", margem_scapja)
                            #     venda_soescap = custo
                            #     valores_vendas.append(venda_soescap)
                            #     print("Venda SoEscap:", venda_soescap, "Margem:", margem_soescap)
                            # else:
                            #     venda_scapja = custo
                            #     valores_vendas.append(venda_scapja)
                            #     print("Venda Scapjá:", venda_scapja, "Margem:", margem_scapja)
                            #     venda_soescap = custo
                            #     valores_vendas.append(venda_soescap)
                            #     print("Venda SoEscap:", venda_soescap, "Margem:", margem_soescap)
                        i_for = i_for+1
                        qtd_i = qtd_i+1
                    else:
                        i_for = i_for + 1
                        #break
                else:
                    have_consulte = True
                    pecas_consulte.append(i)
                    i_for = i_for + 1
                    qtd_i = qtd_i + 1
            print("HAVE PESADA: ", have_pesada)
            print("HAVE CONSULTE: ", have_consulte)


    if(i_for == cods.__len__()):
        print("HAVE PESADA2: ", have_pesada)
        print("HAVE CONSULTE2: ", have_consulte)

        fix_price = indetify_fix_price(fixacoes)

        venda_scapja = fix_price
        valores_vendas.append(venda_scapja)
        print("Venda Scapjá:", venda_scapja)
        venda_soescap = fix_price
        valores_vendas.append(venda_soescap)
        print("Venda SoEscap:", venda_soescap)

        print(valores_vendas)

        if(valores_vendas.__len__() < 19):
            for i in range(19):
                valores_vendas.append(0)
        if(have_consulte == True or cods == []):
            valores_vendas.append(0)
            #custo_frete = 0

        #Soma os valores de cada peça pra ter o valor de venda final
        print("Custo frete", custo_frete)
        venda_scapja = int(valores_vendas[0]) + int(valores_vendas[2]) + int(valores_vendas[4]) + int(valores_vendas[6]) \
                       + int(valores_vendas[8]) + int(valores_vendas[10]) + int(valores_vendas[12]) + int(valores_vendas[14]) \
                       + int(valores_vendas[16]) + int(valores_vendas[18])
        venda_scapja = venda_scapja + custo_frete

        venda_soescap = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(valores_vendas[7]) + int(valores_vendas[9]) \
                        + int(valores_vendas[11]) + int(valores_vendas[13]) + int(valores_vendas[15]) + int(valores_vendas[17]) + int(valores_vendas[19])
        venda_soescap = venda_soescap + custo_frete

        venda_tray = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(valores_vendas[7]) + int(valores_vendas[9]) \
                    + int(valores_vendas[11]) + int(valores_vendas[13]) + int(valores_vendas[15]) + int(valores_vendas[17]) + int(valores_vendas[19]) + 3
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

        scapja_sem_custo_frete = venda_scapja - custo_frete
        venda_shopee = scapja_sem_custo_frete + (scapja_sem_custo_frete * 0.04) + 4
        venda_shopee = venda_shopee + (venda_shopee * 1)

        venda_scapja = round(venda_scapja)
        venda_soescap = round(venda_soescap)
        venda_tray = round(venda_tray)
        venda_shops = round(venda_shops)
        venda_shopee = round(venda_shopee)

        print("Valor de Venda ScapJá: {}".format(venda_scapja))
        print("Valor de Venda Shops: {}".format(venda_shops))
        print("Valor de Venda SoEscap: {}".format(venda_soescap))
        print("Valor de Venda Tray: {}".format(venda_tray))

        print("Imprimir valores")

        #Criando a area que aparece as peças que estão sob consulte
        sob_consulte.grid(column=0, row=17, columnspan=26)

        if(have_nao_fabrica == True and have_consulte == True):
            sob_consulte['text'] = "                                         Peças Sob Consulte e Não Fabrica: {}, {}                                 ".format(pecas_consulte, pecas_nao_fabrica)
        elif(have_nao_fabrica == True):
            sob_consulte['text'] = "                                         Peças Não Fabrica: {}                                  ".format(pecas_nao_fabrica)
        elif(have_consulte == True):
            sob_consulte['text'] = "                                         Peças Sob Consulte: {}                                  ".format(pecas_consulte)
        else:
            sob_consulte['text'] = "                                         Fabs: {}                                                ".format(fabs)

        #Colocando os valores de venda na interface
        string_venda = "Valor de venda na ScapJá: {}\n" \
                       "Valor de venda na Shops: {}\n" \
                       "Valor de venda na SoEscap: {}\n" \
                       "Valor de venda na Tray: {}\n" \
                       "Valor de venda na Shopee: {}\n" \
                       "\n".format(venda_scapja, venda_shops, venda_soescap, venda_tray, venda_shopee)
        venda_label = Text(janela, height=5, width=35, borderwidth=0, font=interface.font_default())
        venda_label.insert(1.0, string_venda)
        venda_label.tag_configure("tag_name", justify="center")
        venda_label.tag_add("tag_name", "1.0", "end")
        #valores_venda_label = Label(janela, text=string_venda, font=interface.font_default())
        venda_label.configure(state="disabled")
        venda_label.grid(column=0, row=19, columnspan=24, rowspan=3)

        copy_scapja = Button(janela, text="ScapJa", width=10, command=lambda:copy_price("scapja", venda_scapja, venda_shops, venda_soescap, venda_tray))
        copy_scapja.grid(column=17, row=19, columnspan=5, sticky=W)

        copy_scapja = Button(janela, text="SoEscap", width=10,command=lambda:copy_price("soescap", venda_scapja, venda_shops, venda_soescap, venda_tray))
        copy_scapja.grid(column=17, row=20, columnspan=5, sticky=W)

        copy_scapja = Button(janela, text="Tray",width=10, command=lambda:copy_price("tray", venda_scapja, venda_shops, venda_soescap, venda_tray))
        copy_scapja.grid(column=17, row=21, columnspan=5, sticky=W)

def copy_price(account,venda_scapja, venda_shops, venda_soescap, venda_tray):
    if(account == "scapja"):
        pyperclip.copy(str(venda_scapja))
    if (account == "soescap"):
        pyperclip.copy(str(venda_soescap))
    if (account == "tray"):
        pyperclip.copy(str(venda_tray))

def margemBruta(janela, qtd_1, qtd_2, qtd_3, qtd_4, qtd_5, cod_1, cod_2, cod_3, cod_4, cod_5, cod_01):
    #Agrupando quantidades e os códigos das peças
    qtds = [qtd_1, qtd_2, qtd_3, qtd_4, qtd_5]
    cods = [cod_1, cod_2, cod_3, cod_4, cod_5]
    valor_venda = cod_01 #Lembrando que o cod_01 é o preço de venda sem tarifas do ML
    have_brinde = False
    valores_custo = []

    #Variaveis importantes para loops
    i_for = 0
    qtd_i = 0

    if (cods[4] == ''):
        cods.pop(4)
        qtds.pop(4)
    if (cods[3] == ''):
        cods.pop(3)
        qtds.pop(3)
    if (cods[2] == ''):
        cods.pop(2)
        qtds.pop(2)
    if (cods[1] == ''):
        cods.pop(1)
        qtds.pop(1)
    if (cods[0] == ''):
        cods.pop(0)
        qtds.pop(0)

    print(cods)

    # Pegando a planilha com os códigos das peças e preços
    df_base = gs.main()
    print(df_base)

    while (i_for < cods.__len__()):
        for i in cods:
            if (i != "" or i != None):  # Checa se há algum valor no código da peça
                print("Entrou no if dentro do for")

                filtro = df_base.loc[df_base["Cod Peça"] == i.upper().strip()]  # Procura a linha com o código da peça
                lista = list(
                    filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores

                # Caso a lista continue em branco é porque não achou a peça na planilha, um dos motivos pode ser a pesquisa em STR sendo que tem que ser em INT
                if (lista == []):
                    filtro = df_base.loc[df_base["Cod Peça"] == int(i)]  # Procura a linha com o código da peça
                    lista = list(
                        filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores

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
                    indice = indice_fabricante(fab, linha, tipo)

                    # Chama função para definir as margens e checar regra de custo
                    custo = preco * indice
                    valores_custo.append(custo)
                    print("Custo da {} é: {}".format(cod, custo))

                    i_for = i_for + 1
                    qtd_i = qtd_i + 1
                else:
                    i_for = i_for + 1
                    break
            else:
                i_for = i_for + 1
                break

    if (i_for == cods.__len__()):
        print(valores_custo)
        if (valores_custo.__len__() < 4):
            for i in range(4):
                valores_custo.append(0)

    custo_total = 0
    i_custo = 0

    if(i_custo < valores_custo.__len__()):
        for i in range(4):
            custo_total = custo_total + int(valores_custo[i_custo])
            i_custo = i_custo+1

    #Calcularando margem
    print("Custo total: {}   Valor de Venda: {}".format(custo_total, valor_venda))
    margem_bruta = (int(valor_venda) / int(custo_total) * 100) - 100
    print(margem_bruta)

    string_print = "Custo total das peças: {}\n" \
                    "Valor de venda sem tarifa: {}\n" \
                    "Margem de Lucro Bruto: {}%\n".format(custo_total, valor_venda, int(margem_bruta))

    venda_label = Text(janela, height=3, width=40, borderwidth=0, font=interface.font_default())
    venda_label.insert(1.0, string_print)
    venda_label.tag_configure("tag_name", justify="center")
    venda_label.tag_add("tag_name", "1.0", "end")
    venda_label.configure(state="disabled")
    venda_label.grid(column=0, row=13, columnspan=26)

def indice_fabricante(fab, linha, tipo):
    fabricantes = ["Mastra", "Pioneiro", "Alpha", "Amam", "Fix", "Nalu", "J.L.F"]
    indice = 0

    #Atribuindo cada indice para cada fabricante

    #Mastra
    if(fab == fabricantes[0] and linha == "Leve" and tipo == "Escap"):
        indice = 0.4959
    elif(fab == fabricantes[0] and linha == "Pesada" and tipo == "Escap"):
        indice = 0.6038
    elif(fab == fabricantes[0] and linha == "Leve" and tipo == "Catalisador"):
        # ATUAL = indice = 0.3989 + 12% = 0.4467
        indice = 0.3989
    elif (fab == fabricantes[0] and linha == "Leve" and tipo == "Flexivel"):
        indice = 1

    #Pioneiro
    if (fab == fabricantes[1]):
        #ATUAL = indice = 0.1722 + 12% = 0.1928
        indice = 0.1722
    elif(fab == fabricantes[1] and tipo == "Flexivel"):
        indice = 1

    if (fab == fabricantes[1] and tipo == "Catalisador"):
        indice = 2

    #Fixações
    if(fab == fabricantes[4]):
        indice = 1

    # Fixações
    if(fab == fabricantes[4]):
            indice = 1

    #Alpha
    if(fab == fabricantes[2]):
        indice = 0.4976

    #Amam
    if(fab == fabricantes[3]):
        indice = 0.2212

    #Nalu
    if(fab == fabricantes[5] and tipo == "Catalisador"):
        indice = 2

    # J.L.F
    if (fab == fabricantes[6]):
        indice = 1

    if(indice == None or indice == 0):
        indice = 1

    # PREÇO DE CUSTO
    if (fab == "ZZ"):
            indice = 1

    return indice

def margem(custo, fab, linha, cods, have_brinde, tipo, i):
    #Função para definir margem e também definir as regras para quando tivermos que usar o custo dele mesmo vezes 2
    #Quando o custo de uma peça é inferior ou igual a R$65,00 ele precisa ser calculado X2 ignorando a margem normal de 175% e 165%
    effa = ['7800-0', '7801-0', '7802-0']

    print("Cods Margem: {}".format(cods))
    print(i)
    qtd_cods = cods.__len__() #Checa a quantidade de códigos, pois se for acima de 1 não pode fazer o custo x2
    print("Qtds Cods:", qtd_cods)

    double = check_fix(cods, linha)

    if(fab == "Mastra" and linha == "Leve" and custo <= 65 and double == True and have_brinde == False):
        custo = custo * 2
        margem_scapja = 1
        margem_soescap = 1
    elif(fab == "Pioneiro" and linha == "Leve" and custo <= 65 and double == True and have_brinde == False):
        custo = custo * 2
        margem_scapja = 1
        margem_soescap = 1
    elif(fab == "Alpha" and linha == "Leve" and custo <= 65 and double == True and have_brinde == False):
        custo = custo * 2
        margem_scapja = 1
        margem_soescap = 1
    elif(fab == "Amam" and linha == "Leve" and custo <= 65 and double == True and have_brinde == False):
        custo = custo * 2
        margem_scapja = 1
        margem_soescap = 1
    elif(fab == "Mastra" and tipo == "Tubo"):
        custo = custo * 2
        margem_scapja = 1
        margem_soescap = 1
    elif(fab == "Pioneiro" and tipo == "Tubo"):
        custo = custo * 2
        margem_scapja = 1
        margem_soescap = 1
    elif(fab == "Mastra" and linha == "Pesada"):
        margem_scapja = 2.21
        margem_soescap = 2.10
    elif(tipo == "Catalisador"):
        margem_scapja = 1.75
        margem_soescap = 1.65
    else:
        margem_scapja = 1.87
        margem_soescap = 1.73

    if str(i) in effa:
        margem_scapja = 2.75
        margem_soescap = 2.5

    return custo, margem_scapja, margem_soescap

def check_fix(cods, linha):
    #Essa função é para checar se só uma das peças é escapamento mesmo e o resto tudo fixação, isso é para poder multiplicar o custo da peça x2
    double = False
    parts = 0
    z = 0
    linhas = []

    # Pegando a planilha com os códigos das peças e preços
    #df_base = pd.read_excel('Peças-Preços.xlsx')
    df_base = gs.main()

    for i in cods:
        print("Código Check Fix: {}".format(i))
        if(type(i) == str and "Brinde" in i):
            cods.remove(i)
            print("Removeu Código")
        else:
            filtro = df_base.loc[df_base["Cod Peça"] == i.upper().strip()]  # Procura a linha com o código da peça
            lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores

            # Caso a lista continue em branco é porque não achou a peça na planilha, um dos motivos pode ser a pesquisa em STR sendo que tem que ser em INT
            try:
                if (lista == []):
                    filtro = df_base.loc[df_base["Cod Peça"] == int(i)]  # Procura a linha com o código da peça
                    lista = list(
                        filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
                    print("Lista = [] 1 ", lista, " I: ", i)
                    linha = lista[1]
                    linhas.append(linha)
                elif (lista == []):
                    filtro = df_base.loc[df_base["Cod Peça"] == str(i)]  # Procura a linha com o código da peça
                    lista = list(
                        filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
                    print("Lista = [] 2 ", lista, " I: ", i)
                    linha = lista[1]
                    linhas.append(linha)
                elif (lista == []):
                    print("Não achou a peça na base de dados")
                    continue
                else:
                    print("ELSE LINHA LISTA")
                    linha = lista[1]
                    linhas.append(linha)
            except (ValueError, IndexError) as e:
                print("Não achou a peça na base de dados")
                continue

    print(linhas)

    for x in cods:
        print(x, " in ", cods)
        try:
            print(cods)
            print("Z: {}, Parts: {}".format(z, parts))
            print("LINHA: ", linha)
            print("LINHAS: ", linhas)
            print("LINHAS Z:", linhas[z])
            if(linhas[z] == "Leve"):
                parts = parts+1
            z = z+1
            print("PARTS: ", parts, "Z: ", z)
        except IndexError:
            print("Except IndexError")

    if(parts == 1):
        double = True

    print("Double: {}".format(double))
    return double

def indetify_fix_price(fixacoes):
    print("LISTA DE FIXAÇÕES: {}".format(fixacoes))
    fix_price = 0

    for x in fixacoes:
        fix_price = fix_price + x

    print("Fix Price: {}".format(fix_price))

    if (fix_price > 90):
        fix_price = fix_price - (fix_price * 0.3)

    return fix_price