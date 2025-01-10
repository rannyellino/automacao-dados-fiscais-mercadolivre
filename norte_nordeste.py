import pandas as pd
import openpyxl
from datetime import datetime

def check_sells(filename):
    estados = ['Acre', 'Amapá', 'Amazonas', 'Pará', 'Rondônia', 'Roraima', 'Tocatins', 'Alagoas', 'Bahia', 'Ceará', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Rio Grande do Norte', 'Sergipe']
    count = 0
    contas = []
    pedidos = []
    compradores = []
    cidades = []
    ufs = []
    ceps = []
    mlbs = []
    fretes = []

    df_base = pd.read_excel(filename)
    print(df_base)

    rows = len(df_base.index)  # Pega a quantidade de linhas que tem na base de dados para usar como referencia no while
    i = 0  # Para o while que vai rodar a leitura de cada linha da base de dados

    while i < rows:
        norte_nordeste = False

        # Guardando os valores de uma linha dentro de uma variavel
        linha = df_base.loc[[i]]
        print(linha)
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        print(lista)

        # LISTA
        # 0 = CONTA, 1 = Código do Anúncio, 4 = Descrição, 7 = Preço de Venda, 10 = Frete e 19 = Se está com frete grátis
        conta = str(lista[1])
        pedido = str(lista[4])
        comprador = str(lista[9])
        cidade = str(lista[10])
        uf = str(lista[11])
        cep = str(lista[12])
        mlb = str(lista[13])
        frete = str(lista[21])

        for estado in estados:
            if(uf == estado):
                norte_nordeste = True

        if(norte_nordeste == True):
            contas.append(conta)
            pedidos.append(pedido)
            compradores.append(comprador)
            cidades.append(cidade)
            ufs.append(uf)
            ceps.append(cep)
            mlbs.append(mlb)
            fretes.append(frete)
            count = count+1

        i = i+1

    df = {'Contas': contas, "Pedidos": pedidos, "Compradores": compradores, "Estados": ufs, "Cidades": cidades, "CEPs": ceps, "Fretes": fretes, "MLBs": mlbs}
    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S')  # Pega a data e hora atual e já formata
    nome_arquivo = str(data_hora) + ".xlsx"
    dataframe = pd.DataFrame(df)
    dataframe.to_excel(nome_arquivo)
    return nome_arquivo, count