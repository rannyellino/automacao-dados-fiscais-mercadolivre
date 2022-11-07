import tkinter
from tkinter import *
import pandas as pd
import openpyxl

def calc(janela, qtd_1, qtd_2, qtd_3, qtd_4, qtd_5, cod_1, cod_2, cod_3, cod_4, cod_5):
    #Agrupando as quantidades e codigos dos anuncios
    qtds = [qtd_1, qtd_2, qtd_3, qtd_4, qtd_5]
    cods = [cod_1, cod_2, cod_3, cod_4, cod_5]
    custo = 0
    valores_vendas = []
    i_for = 0
    qtd_i = 0
    print(qtds)


    #Verificando os valores que tem na lista, o que não tiver valor é excluido da lista
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

    filtro = df_base.loc[df_base["Cod Peça"] == cods[0]]  # Procura a linha com o código da peça
    print(filtro)
    lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
    print(lista)

    while(i_for < cods.__len__()):
        for i in cods:
            if(i != "" or i != None): #Checa se há algum valor no código da peça
                print("Entrou no if dentro do for")
                filtro = df_base.loc[df_base["Cod Peça"] == i.upper()] #Procura a linha com o código da peça
                lista = list(filtro.values.flatten()) #Transforma a linha da planilha em uma lista para termos os valores

                #Caso a lista continue em branco é porque não achou a peça na planilha, um dos motivos pode ser a pesquisa em STR sendo que tem que ser em INT
                if(lista == []):
                    filtro = df_base.loc[df_base["Cod Peça"] == int(i)]  # Procura a linha com o código da peça
                    lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores

                #Verifica se tem valor na lista, se não tiver é porque não encontrou o código na planilha
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

                    #Calcula o valor de venda final para cada canal mas sem o MercadoEnvios
                    if(linha == "Leve"):
                        venda_scapja = custo * 1.75
                        valores_vendas.append(venda_scapja)
                        venda_soescap = custo * 1.65
                        valores_vendas.append(venda_soescap)
                    elif(linha == "Pesada"):
                        venda_scapja = custo * 2.15
                        valores_vendas.append(venda_scapja)
                        venda_soescap = custo * 2.04
                        valores_vendas.append(venda_soescap)
                    elif(linha == "Fix"):
                        if(custo > 50):
                            custo = custo * 0.7
                            venda_scapja = custo
                            valores_vendas.append(venda_scapja)
                            venda_soescap = custo
                            valores_vendas.append(venda_soescap)
                        else:
                            venda_scapja = custo
                            valores_vendas.append(venda_scapja)
                            venda_soescap = custo
                            valores_vendas.append(venda_soescap)
                    i_for = i_for+1
                    qtd_i = qtd_i+1
                else:
                    break
            else:
                break

    if(i_for == cods.__len__()):
        print(valores_vendas)
        if(valores_vendas.__len__() < 7):
            for i in range(7):
                valores_vendas.append(0)


        #Soma os valores de cada peça pra ter o valor de venda final
        venda_scapja = int(valores_vendas[0]) + int(valores_vendas[2]) + int(valores_vendas[4]) + int(valores_vendas[6])
        venda_soescap = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(valores_vendas[7])
        venda_tray = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(valores_vendas[7]) + 3

        #Colocando os valores de venda na interface
        string_venda = "Valor de venda na ScapJá: {}\n" \
                       "Valor de venda na SoEscap: {}\n" \
                       "Valor de venda na Tray: {}\n" \
                       "\n" \
                       "Os valores não tem o custo de frete incluso".format(venda_scapja, venda_soescap, venda_tray)
        valores_venda_label = Label(janela, text=string_venda)
        valores_venda_label.grid(column=0, row=9, columnspan=26)

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

    return indice


