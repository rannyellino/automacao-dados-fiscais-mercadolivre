import pandas as pd
import openpyxl
import verify
from verify import calc_verify

def bling_parts():
    df_base = pd.read_excel("produtos_2024-11-27-11-14-53-baterias.xlsx")
    print(df_base)
    rows = len(df_base.index)
    i = 0

    codigos_lista = []
    id_lista = []

    while i < rows:
        linha = df_base.loc[[i]]
        print(linha)
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        print(lista)

        # LISTA
        # 0 = CONTA, 1 = Código do Anúncio, 4 = Descrição, 7 = Preço de Venda, 10 = Frete e 19 = Se está com frete grátis
        cod = str(lista[1])
        desc = str(lista[41])
        desc = desc.replace("<br />"," ")

        if(desc != None or desc != ""):
            codigos = verify.identificar_codigos(desc)

            # Continua eliminando caracteres a mais que não sejam códigos
            codigos = codigos.replace(":", "")
            codigos = codigos.replace("1x", "")
            #codigos = codigos.replace(" ", "")
            codigos = codigos.replace("LinhaPesada", "")
            codigos = codigos.replace("(Novo)", "")
            codigos_lista.append(codigos)  # Adiciona na lista de códigos a sequencia de códigos do anuncio que o robo identificou
            #print("CODIGOS LIMPOS: {}", codigos)

            id_lista.append(cod)
        print("Vai somar I")
        i = i + 1
        print(id_lista)
        print(codigos_lista)

    df_end = {'Cods':id_lista,'Peças':codigos_lista}
    dataframe = pd.DataFrame(df_end)
    dataframe.to_excel("LOG/" + 'Atuais Amazon Parts 24-09-24.xlsx')

def tray_parts():
    df_base = pd.read_excel("tray-parts-28-11-24.xlsx")
    print(df_base)
    rows = len(df_base.index)
    i = 0

    codigos_lista = []
    id_lista = []
    tipo_lista = []
    linha_lista = []
    fabricantes_lista = []
    titulo_lista = []

    while i < rows:
        linha = df_base.loc[[i]]
        print(linha)
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        print(lista)

        # LISTA
        # 0 = CONTA, 1 = Código do Anúncio, 4 = Descrição, 7 = Preço de Venda, 10 = Frete e 19 = Se está com frete grátis
        cod = str(lista[0])
        titulo = str(lista[1])
        desc = str(lista[2])
        desc = desc.replace("<br />", " ")
        desc = desc.replace("<p>", " ")
        desc = desc.replace("</p>", " ")

        if (desc != None or desc != ""):
            conta = 'Tray'
            frete = 0
            frete_gratis = 'no'
            codigos = verify.identificar_codigos(desc)

            # Continua eliminando caracteres a mais que não sejam códigos
            codigos = codigos.replace(":", "")
            codigos = codigos.replace("1x", "")
            # codigos = codigos.replace(" ", "")
            codigos = codigos.replace("LinhaPesada", "")
            codigos = codigos.replace("(Novo)", "")
            codigos_lista.append(
                codigos)  # Adiciona na lista de códigos a sequencia de códigos do anuncio que o robo identificou
            # print("CODIGOS LIMPOS: {}", codigos)

            codigos = codigos.replace("+", ",")
            lista_codigos = codigos.split(",")

            preco_venda, tipo, linha, fab = calc_verify(lista_codigos, conta, frete, frete_gratis, titulo)

            tipo_lista.append(tipo)
            linha_lista.append(linha)
            fabricantes_lista.append(fab)
            id_lista.append(cod)
            titulo_lista.append(titulo)

        print("Vai somar I")
        i = i + 1
        print(id_lista)
        print(codigos_lista)

    df_end = {'Cods': id_lista, 'Titulos': titulo_lista,'Peças': codigos_lista, 'Tipo': tipo_lista, 'Linha': linha_lista, 'Fabricante': fabricantes_lista}
    dataframe = pd.DataFrame(df_end)
    dataframe.to_excel("LOG/" + 'Tray Parts 28-11-24.xlsx')


if __name__ == '__main__':
    tray_parts()