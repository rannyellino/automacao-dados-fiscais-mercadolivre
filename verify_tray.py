import pandas as pd
import openpyxl
import calc
import log

def verificar_tray():
    # Lendo a tabela
    df_base = pd.read_excel('tray.xlsx')
    print(df_base)
    rows = len(df_base.index)  # Pega a quantidade de linhas que tem na base de dados para usar como referencia no while
    i = 0  # Para o while que vai rodar a leitura de cada linha da base de dados

    ids = []
    cods = []
    total_pecas = []
    titulos = []
    tipo_peca = []
    linha_peca = []
    fab_peca = []

    while i < rows:
        print("Linha {} de {}".format(i, rows))
        tipos = []
        linhas = []
        fabs = []
        cods_pecas = []

        linha = df_base.loc[[i]]
        lista = list(linha.values.flatten())
        print(lista)

        # LISTA
        # 0 = SKU, 1 = Título, 3 = Códigos das Peças
        id = str(lista[0])
        titulo = str(lista[1])
        codigos = str(lista[3])

        #Continua eliminando caracteres a mais que não sejam códigos
        codigos = codigos.replace("2x", "")
        codigos = codigos.replace("3x", "")
        codigos = codigos.replace("4x", "")
        codigos = codigos.replace("5x", "")
        codigos = codigos.replace(" ", "")
        codigos = codigos.replace("+", ",")

        # Após limpar toda a string e deixar apenas os códigos separados por "," vamos guardar os códigos como uma lista
        lista_codigos = codigos.split(",")

        for cod in lista_codigos:
            # Receber a base de dados dos códigos da peças e seus valores brutos
            df_base2 = pd.read_excel("Peças-Preços.xlsx")

            filtro = df_base2.loc[df_base2["Cod Peça"] == cod.upper().strip()]
            lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores


            # Caso a lista continue em branco é porque não achou a peça na planilha, um dos motivos pode ser a pesquisa em STR sendo que tem que ser em INT
            if (lista == []):
                cod = cod.lower()
                try:
                    filtro = df_base2.loc[df_base2["Cod Peça"] == int(cod)]  # Procura a linha com o código da peça
                    lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
                except ValueError:
                    print("Erro, não conseguiu achar nenhum código equivalente na base de dados", cod)

            # Verifica se tem valor na lista, se não tiver é porque não encontrou o código na planilha
            if (lista != []):
                print(lista)
                # 0 = Fabricante, 1 = Linha, 2 = Código da Peça, 3 = Preço, 4 = Tipo de Peça(Escap, Fix, Catalisador)
                fab = lista[0]
                linha = lista[1]
                cod = lista[2]
                preco = lista[3]
                tipo = lista[4]

                tipos.append(tipo)
                linhas.append(linha)
                fabs.append(fab)
                cods_pecas.append(int(lista_codigos.__len__()))

        total_pecas.append(lista_codigos)
        ids.append(id)
        cods.append(codigos)
        titulos.append(titulo)
        tipo_peca.append(tipos)
        linha_peca.append(linhas)
        fab_peca.append(fabs)
        i = i+1

    log.log_tray(ids, titulos, cods, total_pecas, tipo_peca, linha_peca, fab_peca)

if __name__ == '__main__':
    verificar_tray()
