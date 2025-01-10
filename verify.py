from tkinter import *
import pandas as pd
import openpyxl
import calc
import log

def verificar():
    #Lendo a tabela
    df_base = pd.read_excel('DESCONTAÇO 2025 JANEIRO.xlsx')
    print(df_base)
    rows = len(df_base.index) #Pega a quantidade de linhas que tem na base de dados para usar como referencia no while
    i = 0 #Para o while que vai rodar a leitura de cada linha da base de dados

    #Abaixo são apenas variaveis para a criação do LOG no final dando o feedback de cada linha que o sistema verificou
    contas = []
    mlbs = []
    precos_antigos = []
    precos_corretos = []
    dif = []
    status = []
    codigos_lista = []
    total_pecas = []
    titulos = []
    tipo_peca = []
    linha_peca = []
    fab_peca = []
    montadoras = []
    carros = []

    #Criando um loop para passar por cada linha da planilha de base de dados
    while i < rows:
        dif_ = None
        status_ = None

        #Guardando os valores de uma linha dentro de uma variavel
        linha = df_base.loc[[i]]
        print(linha)
        lista = list(linha.values.flatten()) #Transforma toda a linha do excel em uma ARRAY
        print(lista)

        #LISTA
        #0 = CONTA, 1 = Código do Anúncio, 4 = Descrição, 7 = Preço de Venda, 10 = Frete e 19 = Se está com frete grátis
        conta = str(lista[0])
        cod = str(lista[1])
        desc = str(lista[4])
        preco = int(lista[7])
        frete = int(lista[10])
        frete_gratis = str(lista[16])
        titulo = str(lista[3])

        montadora, carro = indetificar_montadora_carro(titulo)

        codigos = identificar_codigos(desc) #Chama função que vai identificar quais códigos de peças tem dentro da descrição
        #identificar_acao_zx(desc, zx_cods, px_cods)

        #Continua eliminando caracteres a mais que não sejam códigos
        codigos = codigos.replace(":", "")
        codigos = codigos.replace("1x", "")
        codigos_lista.append(codigos)# Adiciona na lista de códigos a sequencia de códigos do anuncio que o robo identificou
        codigos = codigos.replace(" ", "")
        codigos = codigos.replace("LinhaPesada", "")
        codigos = codigos.replace("+", ",")

        #Após limpar toda a string e deixar apenas os códigos separados por "," vamos guardar os códigos como uma lista
        lista_codigos = codigos.split(",")
        print(lista_codigos.__len__())

        total_pecas.append(lista_codigos.__len__())

        print("Chama a função CALC VERIRIFY")
        preco_venda, tipo, linha, fab = calc_verify(lista_codigos, conta, frete, frete_gratis, titulo)
        tipo_peca.append(tipo)
        linha_peca.append(linha)
        fab_peca.append(fab)
        print("Preço de venda", preco_venda)

        #Calcula diferença
        if(preco_venda != "NÃO"):
            dif_ = (preco_venda-preco)/preco*100
            # Defini o status
            if (dif_ < 2.0 and dif_ > -2.0):
                status_ = "Correto"
            else:
                status_ = "Errado"
        else:
            status_ = "Não conseguiu calcular todos produtos"

        contas.append(conta)
        mlbs.append(cod)
        precos_antigos.append(preco)
        precos_corretos.append(preco_venda)
        dif.append(dif_)
        titulos.append(titulo)
        status.append(status_)
        montadoras.append(montadora)
        carros.append(carro)
        i = i+1 #Para pular a linha

    log.log_excel(contas, mlbs, precos_antigos, precos_corretos, dif, status, codigos_lista, total_pecas, titulos, linha_peca, tipo_peca, fab_peca, montadoras, carros)

def calc_verify(lista_codigos, conta, frete, frete_gratis, titulo):
    i_for = 0
    qtd_i = 0
    custo = 0
    valores_vendas = []
    tipo_peca = []
    linha_peca = []
    fab_peca = []
    bool_while = False #Para poder para o WHILE caso não ache a peça na base de dados
    have_brinde = False #Variavel que indica se tem brinde ou não, se tiver essa peça que é brinde não pode ser calculado

    #Receber a base de dados dos códigos da peças e seus valores brutos
    df_base = pd.read_excel('Peças-Preços.xlsx')

    while (i_for < lista_codigos.__len__() and bool_while == False):
        for i in lista_codigos:
            unit_check = 0 #Checar na lista quantas unidades vai de peça caso seja mais de um
            brinde_check = 0 #Checar na lista qual brinde vai no anuncio caso tenha algum
            qtd_str = ""
            have_brinde = False
            qtds = 1
            print(i)
            if (i != "" or i != None):  #Checa se há algum valor no código da peça
                print("Entrou no if dentro do for")

                #Checando quantidade de peças que vai se é apenas um código ou duas vezes o mesmo código
                check_units = str(i).lower()
                print("Check_units,", check_units)
                units = ['2x','3x','4x','5x','6x','7x','8x']

                print("Vai entrar no for que checa quantidade de peças por código")
                for un in units:
                    if(check_units.find(units[unit_check]) != -1):
                        print("Achou as seguintes unidades", units[unit_check])
                        qtd_str2 = units[unit_check]
                        qtd_str = qtd_str2
                        codigo = i.replace(qtd_str2,"")
                        qtd_str2 = qtd_str2.replace("x","")
                        qtd_str2 = qtd_str2.replace("X", "")
                        qtd = int(qtd_str2)
                        #print("Quantidade de peça(s)", qtd)
                        unit_check = units.__len__()
                        break
                    else:
                        #print("Não achou quantidades")
                        codigo = i
                        qtd = 1
                        #print("Quantidade de peça(s)", qtd)
                        if(unit_check < 6):
                            unit_check = unit_check + 1

                print('Saiu do for que checa a quantidade')
                print('Peça', codigo)
                print('Quantidades', qtd)

                #Agora irá checar se existe alguma peça como brinde pois esta não é calculada no preço
                check_brinde = str(codigo).lower()
                brindes = ['(brinde)', '(abraçadeira)', '(coxim)', '(junta)', 'anel']

                print("Vai checar se existe brinde agora")
                for i in brindes:
                    if(check_brinde.find(brindes[brinde_check]) != -1):
                        print("Foi achado o brinde", i)
                        codigo = "X0X"
                        have_brinde = True
                        brinde_check = brindes.__len__()
                        break
                    else:
                        print("Não foi achado brinde")
                        if(brinde_check < 4):
                            brinde_check = brinde_check + 1

                #Já foi checado quantidade de códigos e brindes mas ainda precisa checar se existe código AMAM mascarado
                #Quando o código da AMAM ta mascarado ele fica com um "S" antes do código e é feito uma soma do código real + 13259 e precisa ser checado isso também
                check_mask_amam = str(codigo).lower()
                mask_amam = "s"

                print("Checa se há algum código amam", check_mask_amam, check_mask_amam.find(mask_amam))
                if(check_mask_amam.find(mask_amam) == 0 and check_mask_amam.__len__() < 10):
                    print("O código AMAM está mascarado, index:", check_mask_amam.find(mask_amam))
                    codigo = codigo.replace("s","")
                    codigo = codigo.replace("S", "")
                    try:
                        codigo = int(codigo) - 13259
                        codigo_str = str(codigo)
                        codigo = codigo_str[:2] + '.' + codigo_str[2:]
                        print("Código sem a mascara", codigo)
                    except ValueError:
                        print("Não é um código AMAM")
                        bool_while = True

                #Começa o processo de procurar o código na base de dados pra poder calcular o preço de venda
                print("Começar a procura do código", codigo)
                filtro = df_base.loc[df_base["Cod Peça"] == codigo.upper().strip()]  # Procura a linha com o código da peça
                lista = list(
                    filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
                print(lista)

                # Caso a lista continue em branco é porque não achou a peça na planilha, um dos motivos pode ser a pesquisa em STR sendo que tem que ser em INT
                if (lista == []):
                    codigo = codigo.lower()
                    print(codigo)
                    codigo = codigo.replace(qtd_str,"")
                    print(codigo)
                    print(qtd)
                    try:
                        filtro = df_base.loc[df_base["Cod Peça"] == int(codigo)]  # Procura a linha com o código da peça
                        lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
                        print(lista)
                    except ValueError:
                        print("Erro, não conseguiu achar nenhum código equivalente na base de dados", codigo)
                        bool_while = True


                # Verifica se tem valor na lista, se não tiver é porque não encontrou o código na planilha
                if (lista != []):
                    print("entrou no if lista != []")
                    # 0 = Fabricante, 1 = Linha, 2 = Código da Peça, 3 = Preço, 4 = Tipo de Peça(Escap, Fix, Catalisador)
                    fab = lista[0]
                    linha = lista[1]
                    cod = lista[2]
                    preco = lista[3]
                    tipo = lista[4]

                    tipo_peca.append(tipo)
                    linha_peca.append(linha)
                    fab_peca.append(fab)

                    if(preco != "Consulte"):
                        print("entrou no if preco != Consulte")
                        # Encontrando o indice da fabrica
                        indice = calc.indice_fabricante(fab, linha, tipo)

                        # Calculado quantidade de itens x o preço x o indice para ter assim o valor de custo
                        custo = qtd * preco * indice
                        print("Valor de Preço*Indice {}".format(custo))

                        # Chama função para definir as margens e checar regra de custo
                        custo, margem_scapja, margem_soescap = calc.margem(custo, fab, linha, lista_codigos, have_brinde, tipo, i)

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
                        #qtd_i = qtd_i + 1
                    else:
                        bool_while = True #Apenas para quebrar o WHILE caso o código da peça não tenha sido achado dentro da base de dados
                        #i_for = i_for + 1
                else:
                    bool_while = True

    i_for = lista_codigos.__len__() #Para resolver o problema de quando não acha a peça na base de dados também, pois ele para de somar o i_for então
                                    #precisamos igualar ele ao tamanho da lista de códigos para logo abaixo entrar no if que verifica se conseguiu calcular
                                    #cada peça da lista de códigos
    print("I_for",i_for)
    print("Lista Codigos", lista_codigos.__len__())

    if (i_for == lista_codigos.__len__()):
        print(valores_vendas)
        if (valores_vendas.__len__() < 23):
            for i in range(23):
                valores_vendas.append(0)

        #Soma os valores de cada peça pra ter o valor de venda final
        try:
            valor_venda_scapja = int(valores_vendas[0]) + int(valores_vendas[2]) + int(valores_vendas[4]) + int(valores_vendas[6]) + int(valores_vendas[8]) + int(valores_vendas[10]) + int(valores_vendas[12]) + int(valores_vendas[14]) + int(valores_vendas[16]) + int(valores_vendas[18]) + int(valores_vendas[20]) + int(valores_vendas[22])

            valor_venda_soescap = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(valores_vendas[7]) + int(valores_vendas[9]) + int(valores_vendas[11]) + int(valores_vendas[13]) + int(valores_vendas[15]) + int(valores_vendas[17]) + int(valores_vendas[19]) + int(valores_vendas[21]) + int(valores_vendas[23])

            venda_tray = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(valores_vendas[7]) + int(valores_vendas[9]) + int(valores_vendas[11]) + int(valores_vendas[13]) + 3
        except IndexError:
            valor_venda_scapja = 0
            valor_venda_soescap= 0
            venda_tray= 0
            bool_while = True

        # Ve o custo do frete para somar ao preço de venda
        if (type(frete) == int and frete <= 30 and frete_gratis == "YES"):
            custo_frete = 35
        elif (type(frete) == int and frete > 30 and frete_gratis == "YES"):
            custo_frete = frete + 5
        elif (frete_gratis == "NO" and valor_venda_scapja < 74):
            custo_frete = 5.50
        elif (frete_gratis == "NO" and valor_venda_soescap < 74):
            custo_frete = 5.50
        elif (frete_gratis == "NO"):
            custo_frete = 0
        else:
            #Se chegar até aqui é porque o não foi identificado o código da peça e vai zerar o custo de frete só para não dar erro nas linhas abaixo
            custo_frete = 0

        valor_venda_scapja = valor_venda_scapja + custo_frete
        valor_venda_soescap = valor_venda_soescap + custo_frete

        print("Imprimir valores")

        if(bool_while == False):
            # Colocando os valores de venda na interface
            string_venda = "Valor de venda na ScapJá: {}\n" \
                           "Valor de venda na SoEscap: {}\n" \
                           "Valor de venda na Tray: {}\n".format(valor_venda_scapja, valor_venda_soescap, venda_tray)
        else:
            # Colocando os valores de venda na interface
            string_venda = "Valor de venda na ScapJá: {}\n" \
                           "Valor de venda na SoEscap: {}\n" \
                           "Valor de venda na Tray: {}\n"\
                           "\n"\
                           "Não conseguiu calcular todos os produtos".format(valor_venda_scapja, valor_venda_soescap, venda_tray)
        print(string_venda)

        #Defini qual valor vai retornar de venda de acordo com a conta pois o valor de venda muda de conta para conta
        if(conta == "SCAPJA ESCAPAMENTOS"):
            venda = valor_venda_scapja
        else:
            venda = valor_venda_soescap

        print(bool_while)
        if(bool_while == True):
            venda = "NÃO"

    return venda, tipo_peca, linha_peca, fab_peca

def identificar_codigos(desc):
    # PROCURANDO CÓDIGO DAS PEÇAS
    variation_cod = 0  # 1 = "Código:", 2 = "Códigos:"

    try:
        # Vai tentar achar a posição da palavra "Código:" se não achar vai tentar procurar a palavra "Códigos:", pois são os dois padrões que usamos
        find_cod = desc.find("Código:")
        variation_cod = 1
        if (find_cod == None or find_cod == -1):
            find_cod = desc.find("Códigos:")
            variation_cod = 2

        # Transforma em int para poder funcionar no método de exclusão de string atraves de index
        find_cod = int(find_cod)

        # Aqui adiciona mais index de acordo com a palavra achada se foi no singular ou no plural a palavra Código
        if (find_cod != None and variation_cod == 1):
            find_cod = find_cod + 5
        elif (find_cod != None and variation_cod == 2):
            find_cod = find_cod + 6
        print("Find Cod:", find_cod)

        # Vamos começar a limpar agora a string da descrição do anúncio para ter apenas os códigos das peças
        if len(desc) > find_cod:
            codigos = desc[0: 0:] + desc[find_cod + 1::]
            codigos_len = len(codigos)
            codigos_len = int(codigos_len)

        # Agora precisamos achar onde vai começar novamente a exclusão da string que vai ser pelas duas palavras "Para" ou "Linha" o que sobrar serão os códigos das peças mais alguns caracteres
        find_last_words = ["Para", "Características","Dimensões","Linha", "Esse", "Anúncio", "ANÚNCIO", "ANUNCIO", "Anuncio", "Medidas", "Nossos"]
        i = 0
        while(codigos.find(find_last_words[i]) == None or codigos.find(find_last_words[i]) == -1):
            print("find_last_words[i] ",find_last_words[i])
            print("i = i+1", i)
            if(i == find_last_words.__len__()-1):
                break
            i = i+1

        find_last = codigos.find(find_last_words[i])

        find_last = int(find_last)
        print("Find Last:", find_last)

        # Aqui começa a exclusão de caracteres da string baseado na posição dos caracteres
        if len(codigos) > find_last:
            codigos = codigos[0: find_last:] + codigos[codigos_len + 1::]

        print("Códigos:", codigos)

        return codigos
    except UnboundLocalError:
        codigos = "00000000"
        return codigos

def indetificar_montadora_carro(titulo):
    found = False
    i = 0
    lista = []
    titulo = titulo.replace(" ", ",")
    titulo_array = titulo.split(",")

    df_montadora = pd.read_excel('MONTADORA.xlsx')
    print(df_montadora)

    while i < titulo_array.__len__():
        print("Titulo Array: {}".format(titulo_array[i]))
        linha = df_montadora.loc[lambda df_montadora: df_montadora['Carro'] == titulo_array[i]]
        print(linha)
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        i = i+1
        if(lista != []):
            i = i+100


    if(lista == []):
        linha = df_montadora.loc[lambda df_montadora: df_montadora['Carro'] == 'NAO']
        print(linha)
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY

    montadora = lista[0]
    carro = lista[1]

    print("Montadora: {}, Carro: {}".format(montadora, carro))

    return montadora, carro

if __name__ == '__main__':
    verificar()