import pandas as pd
import openpyxl
import verify

def bling_parts():
    df_base = pd.read_excel("bling-parts-10-04-24-3.xlsx")
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
    dataframe.to_excel("LOG/" + 'Bling Parts 10-04-24-3.xlsx')


if __name__ == '__main__':
    bling_parts()