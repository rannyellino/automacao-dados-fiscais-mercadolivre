import tkinter
from tkinter import *
import pandas as pd
import openpyxl

import interface


def calc(janela, qtd_1, qtd_2, qtd_3, qtd_4, qtd_5, qtd_6, qtd_7, cod_1, cod_2, cod_3, cod_4, cod_5, cod_6, cod_7, custo_frete):
    #Agrupando as quantidades e codigos dos anuncios
    qtds = [qtd_1, qtd_2, qtd_3, qtd_4, qtd_5, qtd_6, qtd_7]
    cods = [cod_1, cod_2, cod_3, cod_4, cod_5, cod_6, cod_7]
    custo_frete = int(custo_frete)
    print("Custo de frete:", custo_frete)
    custo = 0
    valores_vendas = []
    i_for = 0
    qtd_i = 0
    have_brinde = False
    print(qtds)


    #Verificando os valores que tem na lista, o que não tiver valor é excluido da lista
    if (cods[6] == ''):
        cods.pop(6)
    if (cods[5] == ''):
        cods.pop(5)
    if(cods[4] == ''):
        cods.pop(4)
    if(cods[3] == ''):
        cods.pop(3)
    if(cods[2] == ''):
        cods.pop(2)
    if(cods[1] == ''):
        cods.pop(1)
    if(cods[0] == ''):
        cods.pop(0)

    print(cods)

    #Pegando a planilha com os códigos das peças e preços
    df_base = pd.read_excel('Peças-Preços.xlsx')
    print(df_base)

    while(i_for < cods.__len__()):
        for i in cods:
            if(i != "" or i != None): #Checa se há algum valor no código da peça
                print("Entrou no if dentro do for")
                filtro = df_base.loc[df_base["Cod Peça"] == i.upper().strip()] #Procura a linha com o código da peça
                lista = list(filtro.values.flatten()) #Transforma a linha da planilha em uma lista para termos os valores

                #Caso a lista continue em branco é porque não achou a peça na planilha, um dos motivos pode ser a pesquisa em STR sendo que tem que ser em INT
                if(lista == []):
                    filtro = df_base.loc[df_base["Cod Peça"] == int(i)]  # Procura a linha com o código da peça
                    lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores

                #Verifica se tem valor na lista, se não tiver é porque não encontrou o código na planilha
                print(lista)
                if(lista != []):
                    #0 = Fabricante, 1 = Linha, 2 = Código da Peça, 3 = Preço, 4 = Tipo de Peça(Escap, Fix, Catalisador)
                    fab = lista[0]
                    linha = lista[1]
                    cod = lista[2]
                    preco = lista[3]
                    tipo = lista[4]

                    #Encontrando o indice da fabrica
                    indice = indice_fabricante(fab, linha, tipo)

                    #Calculado quantidade de itens x o preço x o indice para ter assim o valor de custo
                    print(qtd_i)
                    qtd = int(qtds[qtd_i])
                    custo = qtd*preco*indice
                    print("Valor de Preço*Indice {}".format(custo))

                    #Chama função para definir as margens e checar regra de custo
                    custo, margem_scapja, margem_soescap = margem(custo, fab, linha, cods, have_brinde)

                    #Calcula o valor de venda final para cada canal mas sem o MercadoEnvios
                    if(linha == "Leve" or linha == "Pesada"):
                        venda_scapja = custo * margem_scapja
                        valores_vendas.append(venda_scapja)
                        print("Venda Scapjá:", venda_scapja, "Margem:", margem_scapja)
                        venda_soescap = custo * margem_soescap
                        valores_vendas.append(venda_soescap)
                        print("Venda SoEscap:", venda_soescap, "Margem:", margem_soescap)
                    elif(linha == "Fix"):
                        if(custo > 50 and fab == "Fix" and preco > 50):
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
                    i_for = i_for+1
                    qtd_i = qtd_i+1
                else:
                    i_for = i_for + 1
                    break
            else:
                i_for = i_for + 1
                break

    if(i_for == cods.__len__()):
        print(valores_vendas)
        if(valores_vendas.__len__() < 13):
            for i in range(13):
                valores_vendas.append(0)


        #Soma os valores de cada peça pra ter o valor de venda final
        print("Custo frete", custo_frete)
        venda_scapja = int(valores_vendas[0]) + int(valores_vendas[2]) + int(valores_vendas[4]) + int(valores_vendas[6]) + int(valores_vendas[8])
        + int(valores_vendas[10]) + int(valores_vendas[12])
        venda_scapja = venda_scapja + custo_frete

        venda_soescap = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(valores_vendas[7]) + int(valores_vendas[9])
        + int(valores_vendas[11]) + int(valores_vendas[13])
        venda_soescap = venda_soescap + custo_frete

        venda_tray = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(valores_vendas[7]) + int(valores_vendas[9]) \
        + int(valores_vendas[11]) + int(valores_vendas[13]) + 3

        print("Valor de Venda ScapJá: {}".format(venda_scapja))
        print("Valor de Venda SoEscap: {}".format(venda_soescap))
        print("Valor de Venda Tray: {}".format(venda_tray))

        print("Imprimir valores")

        #Colocando os valores de venda na interface
        string_venda = "Valor de venda na ScapJá: {}\n" \
                       "Valor de venda na SoEscap: {}\n" \
                       "Valor de venda na Tray: {}\n" \
                       "\n".format(venda_scapja, venda_soescap, venda_tray)
        valores_venda_label = Label(janela, text=string_venda, font=interface.font_default())
        valores_venda_label.grid(column=0, row=15, columnspan=26)

def indice_fabricante(fab, linha, tipo):
    fabricantes = ["Mastra", "Pioneiro", "Alpha", "Amam", "Fix"]

    #Atribuindo cada indice para cada fabricante

    #Mastra
    if(fab == fabricantes[0] and linha == "Leve" and tipo == "Escap"):
        indice = 0.449
    elif(fab == fabricantes[0] and linha == "Pesada" and tipo == "Escap"):
        indice = 0.5466
    elif(fab == fabricantes[0] and linha == "Leve" and tipo == "Catalisador"):
        indice = 0.4413

    #Pioneiro
    if (fab == fabricantes[1]):
        indice = 0.19

    #Fixações
    if(fab == fabricantes[4]):
        indice = 1

    #Alpha
    if(fab == fabricantes[2]):
        indice = 0.4505

    #Amam
    if(fab == fabricantes[3]):
        indice = 0.21

    return indice

def margem(custo, fab, linha, cods, have_brinde):
    #Função para definir margem e também definir as regras para quando tivermos que usar o custo dele mesmo vezes 2
    #Quando o custo de uma peça é inferior ou igual a R$65,00 ele precisa ser calculado X2 ignorando a margem normal de 175% e 165%

    qtd_cods = cods.__len__() #Checa a quantidade de códigos, pois se for acima de 1 não pode fazer o custo x2
    print("Qtds Cods:", qtd_cods)

    if(fab == "Mastra" and linha == "Leve" and custo <= 65 and qtd_cods < 2 and have_brinde == False):
        custo = custo * 2
        margem_scapja = 1
        margem_soescap = 1
    elif(fab == "Pioneiro" and linha == "Leve" and custo <= 65 and qtd_cods < 2 and have_brinde == False):
        custo = custo * 2
        margem_scapja = 1
        margem_soescap = 1
    elif(fab == "Alpha" and linha == "Leve" and custo <= 65 and qtd_cods < 2 and have_brinde == False):
        custo = custo * 2
        margem_scapja = 1
        margem_soescap = 1
    elif(fab == "Amam" and linha == "Leve" and custo <= 65 and qtd_cods < 2 and have_brinde == False):
        custo = custo * 2
        margem_scapja = 1
        margem_soescap = 1
    elif(fab == "Mastra" and linha == "Pesada"):
        margem_scapja = 2.15
        margem_soescap = 2.04
    else:
        margem_scapja = 1.75
        margem_soescap = 1.65

    return custo, margem_scapja, margem_soescap