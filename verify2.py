import pandas as pd
import openpyxl
import calc
import log
import verify
import googlesheets as gs

def verificar2():
    # Lendo a tabela
    df_base = pd.read_excel('vendas 09-12-24 a 15-12-24.xlsx')
    print(df_base)
    rows = len(df_base.index)  # Pega a quantidade de linhas que tem na base de dados para usar como referencia no while
    i = 0  # Para o while que vai rodar a leitura de cada linha da base de dados

    # Abaixo são apenas variaveis para a criação do LOG no final dando o feedback de cada linha que o sistema verificou
    global contas, mlbs, precos_antigos, precos_corretos, dif, status, codigos_lista, total_pecas, titulos, tipo_peca, linha_peca, fab_peca, montadoras, carros, custos
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
    custos = []

    # Criando um loop para passar por cada linha da planilha de base de dados
    while i < rows:
        dif_ = None
        status_ = None

        # Guardando os valores de uma linha dentro de uma variavel
        linha = df_base.loc[[i]]
        print(linha)
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        print(lista)

        # LISTA
        # 0 = CONTA, 1 = Código do Anúncio, 4 = Descrição, 7 = Preço de Venda, 10 = Frete e 19 = Se está com frete grátis
        conta = str(lista[0])
        cod = str(lista[1])
        desc = str(lista[4])
        preco = int(lista[7])
        frete = int(lista[10])
        frete_gratis = str(lista[16])
        titulo = str(lista[3])

        montadora, carro = verify.indetificar_montadora_carro(titulo)

        codigos = verify.identificar_codigos(desc)  # Chama função que vai identificar quais códigos de peças tem dentro da descrição

        # Continua eliminando caracteres a mais que não sejam códigos
        codigos = codigos.replace(":", "")
        codigos = codigos.replace("1x", "")
        codigos_lista.append(codigos)  # Adiciona na lista de códigos a sequencia de códigos do anuncio que o robo identificou
        codigos = codigos.replace(" ", "")
        codigos = codigos.replace("LinhaPesada", "")
        codigos = codigos.replace("+", ",")
        codigos = codigos.replace("(Novo)", "")
        print("CODIGOS LIMPOS: {}", codigos)

        # Após limpar toda a string e deixar apenas os códigos separados por "," vamos guardar os códigos como uma lista
        lista_codigos = codigos.split(",")
        print(lista_codigos.__len__())

        total_pecas.append(lista_codigos.__len__())

        preco_venda, tipo, linha, fab, custo, message = calc_verify2(lista_codigos, conta, frete, frete_gratis)

        # Calcula diferença
        print("Calcular diferença, PREÇO DE VENDA: {}  | MESSAGE: {}".format(preco_venda, message))
        if (preco_venda != None and message != "BUGOU"):
            dif_ = (preco_venda - preco) / preco * 100
            # Defini o status
            if (dif_ < 2.0 and dif_ > -2.0):
                status_ = "Correto"
            else:
                status_ = "Errado"
        elif(message == "BUGOU"):
            status_ = message
        else:
            status_ = "Não conseguiu calcular todos produtos"

        #print("Preço Venda: {}, Tipo: {}, Linha: {}, Fab: {}".format(preco_venda, tipo, linha, fab))
        contas.append(conta)
        mlbs.append(cod)
        precos_antigos.append(preco)
        precos_corretos.append(preco_venda)
        dif.append(dif_)
        titulos.append(titulo)
        status.append(status_)
        montadoras.append(montadora)
        carros.append(carro)
        custos.append(custo)
        i = i + 1  # Para pular a linha

    print("Contas: {}, MLBS: {}, Preço_Old: {}, Preço Correto: {}, Diff: {}, Status: {}, Codigo_Lista: {}, Total_Peças: {}, Titulos: {}, Montadoras: {}, Carros: {}, Custos: {}".format(
        contas.__len__(), mlbs.__len__(), precos_antigos.__len__(), precos_corretos.__len__(),
          dif.__len__(), status.__len__(), codigos_lista.__len__(), total_pecas.__len__(), titulos.__len__(), montadoras.__len__(), carros.__len__(), custos.__len__()))
    log.log_excel2(contas, mlbs, precos_antigos, precos_corretos, dif, status, codigos_lista, total_pecas, titulos,
                 montadoras, carros, custos)

def calc_verify2(lista_codigos, conta, frete, frete_gratis):
    # Pegando a planilha com os códigos das peças e preços
    i_for = 0
    df_base = pd.read_excel('custos-estoque-2.xlsx')
    #df_base = pd.read_excel('Peças-Preços.xlsx')
    qtds = []
    fabs = []
    fixacoes = []
    valores_vendas = []
    have_pesada = False
    append_one_time = False
    custo = 0
    custos_list = []
    custo_total = 0
    message = ""

    if(qtds.__len__() < lista_codigos.__len__()):
        print(lista_codigos)
        qtds, lista_codigos2, have_brinde = check_cod(lista_codigos)
        print(qtds, lista_codigos2)

    while (i_for < lista_codigos2.__len__()):
        for i in lista_codigos2:
            if(i_for > lista_codigos2.__len__()):
                message = "BUGOU"
                break
            print("I_FOR {} < LISTA CÓDIGOS2 {}".format(i_for,lista_codigos2.__len__()))
            print("I FOR: {}".format(i_for))
            print("Lista Códigos2: {}".format(lista_codigos2))
            print("Código I: {}".format(i))
            print("Lista Códigos2 LEN: {}".format(lista_codigos2.__len__()))
            print("Qtds LEN: {}".format(qtds.__len__()))
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
                    try:
                        preco = int(lista[3])
                    except ValueError:
                        if (lista[3] != "Consulte"):
                            preco = int(float(lista[3]))
                        else:
                            preco = "Consulte"
                    tipo = lista[4]

                    if(append_one_time == False):
                        tipo_peca.append(tipo)
                        linha_peca.append(linha)
                        fab_peca.append(fab)
                        append_one_time = True

                    # Encontrando o indice da fabrica
                    indice = calc.indice_fabricante(fab, linha, tipo)

                    try:
                        qtd = int(qtds[i_for])
                    except IndexError:
                        print("QTDs LEN: {}".format(qtds.__len__()))
                        print("I FOR: {}".format(i_for))
                        qtd = 1

                    print("Quantidade: {}".format(qtd))

                    # Verifica se a peça é sob consulte
                    if (preco == "Consulte"):
                        have_consulte = True

                    if (preco != "Consulte"):
                        # Calculado quantidade de itens x o preço x o indice para ter assim o valor de custo
                        fabs.append(fab)
                        print("Quantidade Peça: ", qtd)
                        custo = qtd * preco * indice
                        print("Valor de Preço*Indice {}".format(custo))
                        print("CUSTO: {}".format(custo))
                        custos_list.append(int(custo))

                        # Chama função para definir as margens e checar regra de custo
                        custo, margem_scapja, margem_soescap = calc.margem(custo, fab, linha, lista_codigos2, have_brinde, tipo, i)


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
                            if (fab == "Fix"):
                                fixacoes.append(int(custo))
                        i_for = i_for + 1
                    else:
                        i_for = i_for + 1
                        break
                else:
                    have_consulte = True
                    i_for = i_for + 1

            print("HAVE PESADA: ", have_pesada)
            print("Valores Venda: {}".format(valores_vendas))

    print("CUSTO LIST: {}".format(custos_list))

    i_custo = 0
    while i_custo < custos_list.__len__():
        print(custos_list[i_custo])
        custo_total = custo_total + custos_list[i_custo]
        i_custo = i_custo+1

    i_for = lista_codigos2.__len__()  # Para resolver o problema de quando não acha a peça na base de dados também, pois ele para de somar o i_for então
    # precisamos igualar ele ao tamanho da lista de códigos para logo abaixo entrar no if que verifica se conseguiu calcular
    # cada peça da lista de códigos

    if (i_for == lista_codigos2.__len__()):
        fix_price = calc.indetify_fix_price(fixacoes)

        venda_scapja = fix_price
        valores_vendas.append(venda_scapja)
        print("Venda Scapjá:", venda_scapja)
        venda_soescap = fix_price
        valores_vendas.append(venda_soescap)
        print("Venda SoEscap:", venda_soescap)

        print(valores_vendas)

        if (valores_vendas.__len__() < 23):
            for i in range(23):
                valores_vendas.append(0)

        # Soma os valores de cada peça pra ter o valor de venda final
        venda_scapja = int(valores_vendas[0]) + int(valores_vendas[2]) + int(valores_vendas[4]) + int(
            valores_vendas[6]) \
                       + int(valores_vendas[8]) + int(valores_vendas[10]) + int(valores_vendas[12]) + int(
            valores_vendas[14]) \
                       + int(valores_vendas[16]) + int(valores_vendas[18]) + int(valores_vendas[20]) + int(valores_vendas[22])

        venda_soescap = int(valores_vendas[1]) + int(valores_vendas[3]) + int(valores_vendas[5]) + int(
            valores_vendas[7]) + int(valores_vendas[9]) \
                        + int(valores_vendas[11]) + int(valores_vendas[13]) + int(valores_vendas[15]) + int(
            valores_vendas[17]) + int(valores_vendas[19]) + int(valores_vendas[21]) + int(valores_vendas[23])

        custo_frete = check_shipping(frete, frete_gratis, venda_scapja, venda_soescap)

        venda_scapja = venda_scapja + custo_frete
        venda_soescap = venda_soescap + custo_frete

        if (have_pesada == True):
            venda_scapja = venda_scapja + (venda_scapja * 0.1)
            venda_soescap = venda_soescap + (venda_soescap * 0.1)

        venda_scapja = round(venda_scapja)
        venda_soescap = round(venda_soescap)

        if(conta == "SCAPJA ESCAPAMENTOS"):
            venda_final = venda_scapja
        else:
            venda_final = venda_soescap

        print("Valor de Venda ScapJá: {}".format(venda_scapja))
        print("Valor de Venda SoEscap: {}".format(venda_soescap))

    return venda_final, tipo_peca, linha_peca, fab_peca, custo_total, message

def check_cod(lista_codigos):
    print("Chamou CHECK COD")
    i_for = 0
    i_for2 = 0
    units = ['2x', '3x', '4x', '5x', '6x', '7x', '8x']
    brinde_check = 0  # Checar na lista qual brinde vai no anuncio caso tenha algum
    qtds = []
    have_brinde = False
    lista_editada = 0

    while (lista_editada != -1):
        print("PRINT I_FOR 2 ", i_for2)
        print("PRINT LISTA CODIGOS", lista_codigos)
        print("PRINT LISTA EDITADA", lista_editada)
        if(lista_codigos.__len__() == 0):
            break
        if(i_for2 == lista_codigos.__len__() and lista_editada == 0):
            lista_editada = -1
        elif(i_for2 == lista_codigos.__len__() and lista_editada > 0):
            lista_editada = lista_editada-1
            i_for2 = 0
        for i in lista_codigos:
            unit_check = 0  # Checar na lista quantas unidades vai de peça caso seja mais de um
            check_units = str(i).lower()
            print("Check Unit: {}".format(check_units))
            print("Vai entrar no for que checa quantidade de peças por código")
            for un in units:
                print("Un :",un)
                print("Units[unit_check] :", units[unit_check])
                print(check_units.find(units[unit_check]))
                if (check_units.find(units[unit_check]) != -1):
                    print("Achou as seguintes unidades", units[unit_check])
                    print("VAI EXCLUIR LISTA CÓDIGOS NA POSIÇÃO: {}".format(i_for2))
                    print(lista_codigos)
                    qtd_str2 = units[unit_check]
                    qtd_str = qtd_str2
                    codigo = check_units.replace(qtd_str2, "")
                    qtd_str2 = qtd_str2.replace("x", "")
                    qtd_str2 = qtd_str2.replace("X", "")
                    qtd = int(qtd_str2)
                    # print("Quantidade de peça(s)", qtd)
                    unit_check = units.__len__()
                    #lista_codigos.append(codigo)
                    lista_codigos.insert(i_for2, codigo)
                    lista_codigos.pop(i_for2+1)
                    lista_editada = lista_editada+1
                    break
                else:
                    # print("Não achou quantidades")
                    print("LISTA CÓDIGOS ELSE: {}".format(lista_codigos))
                    codigo = i
                    qtd = 1
                    # print("Quantidade de peça(s)", qtd)
                    if (unit_check < 6):
                        unit_check = unit_check + 1

            print('Saiu do for que checa a quantidade')
            print('Peça', codigo)
            print('Quantidades', qtd)

            # Agora irá checar se existe alguma peça como brinde pois esta não é calculada no preço
            check_brinde = str(codigo).lower()
            brindes = ['(brinde)', '(abraçadeira)', '(coxim)', '(junta)', 'anel']

            print("Vai checar se existe brinde agora")
            for i in brindes:
                try:
                    if (check_brinde.find(brindes[brinde_check]) != -1):
                        print("Foi achado o brinde", i)
                        have_brinde = True
                        print(lista_codigos)
                        print(i_for)
                        lista_codigos.pop(i_for)
                        brinde_check = brindes.__len__()
                        break
                    else:
                        print("Não foi achado brinde")
                        if (brinde_check < 4):
                            brinde_check = brinde_check + 1
                except IndexError:
                    print("BRINDE except IndexError")

            qtds.append(qtd)
            i_for = i_for+1
            i_for2 = i_for2+1

            if(i_for2 > 20):
                lista_editada = -1



    return qtds, lista_codigos, have_brinde

def check_shipping(custo_frete, frete_gratis, venda_scapja, venda_soescap):
    if(frete_gratis == "YES"):
        # Ve o custo do frete para somar ao preço de venda
        if (type(custo_frete) == int and custo_frete <= 30):
            custo_frete = 35
        elif (type(custo_frete) == int and custo_frete > 30):
            custo_frete = custo_frete + 5
    else:
        if(venda_scapja < 74 or venda_soescap < 74):
            custo_frete = 5.50
        else:
            custo_frete = 35

    return custo_frete

if __name__ == '__main__':
    verificar2()