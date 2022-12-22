from tkinter import *
import pandas as pd
import openpyxl

def verificar():
    #Lendo a tabela
    df_base = pd.read_excel('DESC_TESTE.xlsx')
    print(df_base)

    #Guardando os valores de uma linha dentro de uma variavel
    linha = df_base.loc[[0]]
    print(linha)
    lista = list(linha.values.flatten()) #Transforma toda a linha do excel em uma ARRAY
    print(lista)

    #LISTA
    #0 = CONTA, 1 = Código do Anúncio, 4 = Descrição, 7 = Preço de Venda
    conta = str(lista[0])
    cod = str(lista[1])
    desc = str(lista[4])
    preco = int(lista[7])

    #PROCURANDO CÓDIGO DAS PEÇAS
    variation_cod = 0 # 1 = "Código:", 2 = "Códigos"

    #Vai tentar achar a posição da palavra "Código:" se não achar vai tentar procurar a palavra "Códigos:", pois são os dois padrões que usamos
    find_cod = desc.find("Código:")
    variation_cod = 1
    if(find_cod == None or find_cod == -1):
        find_cod = desc.find("Códigos:")
        variation_cod = 2

    #Transforma em int para poder funcionar no método de exclusão de string atraves de index
    find_cod = int(find_cod)

    #Aqui adiciona mais index de acordo com a palavra achada se foi no singular ou no plural a palavra Código
    if(find_cod != None and variation_cod == 1):
        find_cod = find_cod + 5
    elif(find_cod != None and variation_cod == 2):
        find_cod = find_cod + 6
    print("Find Cod:", find_cod)

    #Vamos começar a limpar agora a string da descrição do anúncio para ter apenas os códigos das peças
    if len(desc) > find_cod:
        codigos = desc[0: 0:] + desc[find_cod + 1::]
        codigos_len = len(codigos)
        codigos_len = int(codigos_len)

    #print("Códigos:", codigos)
    #print("Len Tamanho:", codigos_len)

    #Agora precisamos achar onde vai começar novamente a exclusão da string que vai ser pelas duas palavras "Para" ou "Linha" o que sobrar serão os códigos das peças mais alguns caracteres
    find_last = codigos.find("Para")
    if (find_last == None or find_last == -1):
        find_last = codigos.find("Linha")

    find_last = int(find_last)
    print("Find Last:", find_last)

    #Aqui começa a exclusão de caracteres da string baseado na posição dos caracteres
    if len(codigos) > find_last:
        codigos = codigos[0: find_last:] + codigos[codigos_len + 1::]

    print("Códigos:", codigos)

    #Continua eliminando caracteres a mais que não sejam códigos
    codigos = codigos.replace(":", "")
    codigos = codigos.replace("(Brinde)", "")
    codigos = codigos.replace(" ", "")
    codigos = codigos.replace("LinhaPesada", "")
    codigos = codigos.replace("+", ",")

    #Após limpar toda a string e deixar apenas os códigos separados por "," vamos guardar os códigos como uma lista
    lista_codigos = codigos.split(",")
    print(lista_codigos.__len__())

    print("Chama a função CALC VERIRIFY")
    calc_verify(lista_codigos)

def calc_verify(lista_codigos):
    i_for = 0
    qtd_i = 0
    custo = 0
    valores_vendas = []
    qtds = []
    len_lista_codigos = lista_codigos.__len__()
    len_qtds = qtds.__len__()

    while(len_qtds < len_lista_codigos):
        print(qtds)
        qtds.append(1)
        len_qtds = len_qtds+1

    df_base = pd.read_excel('Peças-Preços.xlsx')
    print(df_base)
    print(lista_codigos)
    print(qtds)

    while (i_for < lista_codigos.__len__()):
        for i in lista_codigos:
            print(i)
            if (i != "" or i != None):  # Checa se há algum valor no código da peça
                print("Entrou no if dentro do for")
                filtro = df_base.loc[df_base["Cod Peça"] == i.upper().strip()]  # Procura a linha com o código da peça
                lista = list(
                    filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
                print(lista)

                # Caso a lista continue em branco é porque não achou a peça na planilha, um dos motivos pode ser a pesquisa em STR sendo que tem que ser em INT
                if (lista == []):
                    filtro = df_base.loc[df_base["Cod Peça"] == int(i)]  # Procura a linha com o código da peça
                    lista = list(
                        filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
                print(lista)


                # Verifica se tem valor na lista, se não tiver é porque não encontrou o código na planilha
                if (lista != []):
                    # 0 = Fabricante, 1 = Linha, 2 = Código da Peça, 3 = Preço, 4 = Tipo de Peça(Escap, Fix, Catalisador)
                    fab = lista[0]
                    linha = lista[1]
                    cod = lista[2]
                    preco = lista[3]
                    tipo = lista[4]

                    # Encontrando o indice da fabrica
                    indice = indice_fabricante(fab, linha, tipo)

                    # Calculado quantidade de itens x o preço x o indice para ter assim o valor de custo
                    print(qtd_i)
                    qtd = int(qtds[qtd_i])
                    custo = qtd * preco * indice
                    print("Valor de Preço*Indice {}".format(custo))

                    # Chama função para definir as margens e checar regra de custo
                    custo, margem_scapja, margem_soescap = margem(custo, fab, linha)

                    # Calcula o valor de venda final para cada canal mas sem o MercadoEnvios
                    if (linha == "Leve" or linha == "Pesada"):
                        venda_scapja = custo * margem_scapja
                        valores_vendas.append(venda_scapja)
                        venda_soescap = custo * margem_soescap
                        valores_vendas.append(venda_soescap)
                    elif (linha == "Fix"):
                        if (custo > 50 and qtd < 2):
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
                    i_for = i_for + 1
                    qtd_i = qtd_i + 1
                else:
                    break
            else:
                break
                exit()

    if (i_for == lista_codigos.__len__()):
        print(valores_vendas)
        if (valores_vendas.__len__() < 9):
            for i in range(9):
                valores_vendas.append(0)

        # Soma os valores de cada peça pra ter o valor de venda final
        venda_scapja = int(valores_vendas[0]) + int(valores_vendas[2]) + int(valores_vendas[4]) + int(
            valores_vendas[6]) + int(valores_vendas[8])
        venda_soescap = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(
            valores_vendas[7]) + int(valores_vendas[9])
        venda_tray = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(
            valores_vendas[7]) + int(valores_vendas[9]) + 3
        print("Valor de Venda ScapJá: {}".format(venda_scapja))
        print("Valor de Venda SoEscap: {}".format(venda_soescap))
        print("Valor de Venda Tray: {}".format(venda_tray))

        print("Imprimir valores")

        # Colocando os valores de venda na interface
        string_venda = "Valor de venda na ScapJá: {}\n" \
                       "Valor de venda na SoEscap: {}\n" \
                       "Valor de venda na Tray: {}\n" \
                       "\n" \
                       "Os valores não tem o custo de frete incluso".format(venda_scapja, venda_soescap, venda_tray)

        print(string_venda)

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

def margem(custo, fab, linha):
    #Função para definir margem e também definir as regras para quando tivermos que usar o custo dele mesmo vezes 2
    #Quando o custo de uma peça é inferior ou igual a R$65,00 ele precisa ser calculado X2 ignorando a margem normal de 175% e 165%

    if(fab == "Mastra" and linha == "Leve" and custo <= 65):
        custo = custo * 2
        margem_scapja = 1
        margem_soescap = 1
    elif(fab == "Pioneiro" and linha == "Leve" and custo <= 65):
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

if __name__ == '__main__':
    verificar()