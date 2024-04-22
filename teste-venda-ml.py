import pandas as pd
import openpyxl
import calc
import log
from datetime import datetime

global mlbs, subtotais, custos
mlbs = []
subtotais = []
custos = []

def venda_ml():
    # Lendo a tabela
    df_base = pd.read_excel('teste-venda-ml-soescap.xlsx')
    #print(df_base)
    rows = len(df_base.index)  # Pega a quantidade de linhas que tem na base de dados para usar como referencia no while
    i = 0  # Para o while que vai rodar a leitura de cada linha da base de dados

    while(i < rows):
        # Guardando os valores de uma linha dentro de uma variavel
        linha = df_base.loc[[i]]
        #print(linha)
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        #print(lista)

        # LISTA
        mlb = str(lista[0])
        subtotal = int(lista[1])

        df_custos = pd.read_excel("custo-unitario-scapja.xlsx")
        #print(df_custos) #Código do Anúncio

        filtro = df_custos.loc[df_custos["Código do Anúncio"] == mlb.upper().strip()]  # Procura a linha com o código da peça
        lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores

        if(lista != []):
            custo = lista[1]
            print("MLB: {}, SUBTOTAL: {}, CUSTO: {}".format(mlb, subtotal, custo))

            mlbs.append(mlb)
            subtotais.append(subtotal)
            custos.append(custo)
            i = i+1
        else:
            i = i+1

    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S')  # Pega a data e hora atual e já formata
    nome_arquivo = str(data_hora) + ".xlsx"

    df = {'MLBs': mlbs, 'Subtotais': subtotais, 'Custos': custos}
    dataframe = pd.DataFrame(df)
    print(dataframe)
    dataframe.to_excel("LOG/" + nome_arquivo)
    print("LOG/" + nome_arquivo)

if __name__ == '__main__':
    venda_ml()