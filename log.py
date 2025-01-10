from datetime import datetime
import pandas as pd

def criando_log(cod_finalizados, cod_erros):
    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S') #Pega a data e hora atual e já formata
    nome_arquivo = 'Log '+str(data_hora)+'.txt' #Salva a data e hora atual formatada em STRING e adiciona a extensão que quero do arquivo TXT

    if(cod_finalizados != []):
        with open(nome_arquivo, "w") as arquivo: #Cria o arquivo TXT com o nome certo e começa a escrever em cada linha os códigos que ele finalizou o processo
            for valor in cod_finalizados:
                arquivo.write(str(valor)+" FINALIZADO" + "\n")

    if (cod_erros != []):
        with open(nome_arquivo, "a") as arquivo:
            for valor in cod_erros:
                arquivo.write(str(valor)+" VERIFICAR" + "\n")

def log_elementos(locations, loc_um_produto, loc_login_tray):
    nome_arquivo = 'Loc Elementos'+'.txt' #Colocando o nome do arquivo
    with open(nome_arquivo, 'w') as arquivo:
        for loc in locations:
            arquivo.write(str(loc))
            arquivo.write('\n')

    with open(nome_arquivo, 'a') as arquivo:
        arquivo.write(str(loc_um_produto))
        arquivo.write('\n')

    with open(nome_arquivo, 'a') as arquivo:
        arquivo.write(str(loc_login_tray))
        arquivo.write('\n')

def log_excel(contas, mlbs, precos_antigos, precos_corretos, dif, status, codigos_lista, total_pecas, titulos, linha_peca, tipo_peca, fab_peca, montadoras, carros):
# def log_excel(contas, mlbs, precos_antigos, precos_corretos, dif, status, codigos_lista, total_pecas, titulos, montadoras, carros, custos):
    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S')  # Pega a data e hora atual e já formata
    nome_arquivo = str(data_hora) + ".xlsx"
    df = {'contas':contas,'mlbs':mlbs,'Título':titulos,'Fabricante':fab_peca,'Peças':codigos_lista,'Qtd Peças':total_pecas,'Linha':linha_peca,'Tipo':tipo_peca,
          'Montadora':montadoras,'Carros':carros,'Preço Antigo':precos_antigos,'Preços Corretos':precos_corretos, 'Diferença':dif, "Status":status}
    # df = {'contas': contas, 'mlbs': mlbs, 'Título': titulos, 'Peças': codigos_lista,
    #       'Qtd Peças': total_pecas,'Montadora': montadoras, 'Carros': carros, 'Preço Antigo': precos_antigos, 'Preços Corretos': precos_corretos,
    #       'Diferença': dif, "Status": status, "Custos": custos}
    dataframe = pd.DataFrame(df)
    print(dataframe)
    dataframe.to_excel("LOG/"+nome_arquivo)
    print("LOG/"+nome_arquivo)

def log_excel2(contas, mlbs, precos_antigos, precos_corretos, dif, status, codigos_lista, total_pecas, titulos, montadoras, carros, custos):
    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S')  # Pega a data e hora atual e já formata
    nome_arquivo = str(data_hora) + ".xlsx"
    df = {'contas': contas, 'mlbs': mlbs, 'Título': titulos, 'Peças': codigos_lista,
          'Qtd Peças': total_pecas,'Montadora': montadoras, 'Carros': carros, 'Preço Antigo': precos_antigos, 'Preços Corretos': precos_corretos,
          'Diferença': dif, "Status": status, "Custos": custos}
    dataframe = pd.DataFrame(df)
    print(dataframe)
    dataframe.to_excel("LOG/"+nome_arquivo)
    print("LOG/"+nome_arquivo)

def log_tray(sku, titulo, cods, total_peca, tipo_peca, linha_peca, fab_peca):
    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S')  # Pega a data e hora atual e já formata
    nome_arquivo = "Tray Linha Leve" + str(data_hora) + ".xlsx"
    df = {'skus':sku,'Títulos':titulo,'Codígos':cods,'Qtd Peças':total_peca,'Linha':linha_peca,'Tipo Peças':tipo_peca,'Fabricante':fab_peca}
    dataframe = pd.DataFrame(df)
    dataframe.to_excel("LOG/"+nome_arquivo)

def log_promo(cods, status):
    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S')  # Pega a data e hora atual e já formata
    nome_arquivo = "Promo-ScapJa " + str(data_hora) + ".xlsx"
    df = {'Cod':cods,'Stats':status}
    dataframe = pd.DataFrame(df)
    dataframe.to_excel("LOG/"+nome_arquivo)

def log_bianca(sells_noted, phone_noted, ids_noted):
    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S')  # Pega a data e hora atual e já formata
    nome_arquivo = "LOG BIANCA " + str(data_hora) + ".xlsx"
    df = {'IDs':ids_noted,'Venda Anotadas':sells_noted,'Telefones':phone_noted}
    dataframe = pd.DataFrame(df)
    dataframe.to_excel("LOG/"+nome_arquivo)

def log_imagens(cods, titles, size1_list, size2_list, size3_list, status_list):
    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S')  # Pega a data e hora atual e já formata
    nome_arquivo = "LOG IMAGENS " + str(data_hora) + ".xlsx"
    df = {'IDs':cods,'Título':titles,'Tamanho 1':size1_list,'Tamanho 2':size2_list,'Tamanho 3':size3_list,'Status':status_list}
    dataframe = pd.DataFrame(df)
    dataframe.to_excel("LOG/"+nome_arquivo)