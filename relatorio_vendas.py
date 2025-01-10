import pandas as pd
import log
from datetime import datetime

sheet_no_costs = '16-12-2024 12-14-29.xlsx'
sheet_with_costs = '16-12-2024 12-43-57.xlsx'
sheet_sells = 'ReportSalesProfitabilityGroupByMLB-Total (58).xlsx'

def create_sheet():
    #Pegando as duas planilhas que servirão para criar uma planilha com todos os dados corretos
    df_no_costs = pd.read_excel(sheet_no_costs)
    df_with_costs = pd.read_excel(sheet_with_costs)

    #Separando a planilha sem custos apenas com o que deu certo de calcular
    df_corrects = df_no_costs[df_no_costs['Status'] == 'Correto']
    df_wrongs = df_no_costs[df_no_costs['Status'] == 'Errado']

    #Concatenando os dois filtros(corretos e errados)
    df_no_costs = pd.concat([df_corrects,df_wrongs])
    df_no_costs = df_no_costs.reset_index(drop=True) #refazendo o index do dataframe
    #print(df_no_costs)

    rows = len(df_no_costs.index)  # Pega a quantidade de linhas que tem na base de dados para usar como referencia no while
    i = 0  # Para o while que vai rodar a leitura de cada linha da base de dados

    mlbs_no_costs = [] #vamos salvar todos os mlbs da planilha filtrada e limpa

    while i < rows:
        # Guardando os valores de uma linha dentro de uma variavel
        linha = df_no_costs.loc[[i]]
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY

        mlb = lista[2] #salvando código mlb

        mlbs_no_costs.append(mlb)
        #print(mlb)
        i = i+1

    #Agora iremos pegar os custos referente a esses mlbs salvos em mlbs_no_costs
    values = df_with_costs['mlbs'].isin(mlbs_no_costs) #Filtrando a planilha com custos para ver se o MLB existe dentro da array
    #print(values)

    #Criando um novo df com os valores filtrados
    df_filtrado = df_with_costs[values]
    df_filtrado = df_filtrado.reset_index(drop=True)
    #print(df_filtrado)

    #Vamos ordenar os dois dataframes por ordem crescente para depois concatenar certos dados
    df_filtrado.sort_values(by="mlbs", ascending=True, inplace=True)
    df_no_costs.sort_values(by="mlbs", ascending=True, inplace=True)

    df_filtrado = df_filtrado.reset_index(drop=True)
    df_no_costs = df_no_costs.reset_index(drop=True)

    #Criando o dataframe que vai servir para pegar os dados para o relatorio de venda
    df_clean = {'mlbs': df_no_costs['mlbs'], 'Peças': df_no_costs['Peças'], 'Linha': df_no_costs['Linha'], 'Tipo': df_no_costs['Tipo'], 'Custos': df_filtrado['Custos']}
    df_clean = pd.DataFrame(df_clean)
    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S')  # Pega a data e hora atual e já formata
    nome_arquivo = "Save 1 " + str(data_hora) + ".xlsx"
    df_clean.to_excel(nome_arquivo)

    print("Salvou o arquivo: ", nome_arquivo)
    return nome_arquivo, mlbs_no_costs

def create_report_sell(nome_arquivo, mlbs):
    df_clean = pd.read_excel(nome_arquivo)
    df_sells = pd.read_excel(sheet_sells)

    print(df_clean)
    print("\n\n\n")
    print(df_sells)

    #Filtrando planilha de vendas pelos mlbs que temos
    values = df_sells['Código do Anúncio'].isin(mlbs)

    df_filtrado = df_sells[values]
    df_filtrado = df_filtrado.reset_index(drop=True)

    # Vamos ordenar os dois dataframes por ordem crescente para depois concatenar certos dados
    df_filtrado2 = df_filtrado.sort_values(by="Código do Anúncio", ascending=True, inplace=False)
    df_clean2 = df_clean.sort_values(by="mlbs", ascending=True, inplace=False)

    df_filtrado2 = df_filtrado2.reset_index(drop=True)
    df_clean2 = df_clean2.reset_index(drop=True)

    # Dividindo Custo de Frete por Quantidade Vendida, Multiplicando Custos por Quantidade Vendida e descobrindo Margem Bruta
    df_filtrado2['Frete Uni'] = df_filtrado2['Frete Total'] / df_filtrado2['Quantidade vendida']
    df_filtrado2['Custo Multi'] = df_clean2['Custos'] * df_filtrado2['Quantidade vendida']
    df_filtrado2['Margem'] = df_filtrado2['Lucro Bruto'] / df_filtrado2['Custo Multi']

    print(df_clean2)
    print("\n\n\n")
    print(df_filtrado2)

    df_sells_clean = {'Conta': df_filtrado2['Nickname'], 'MLBs': df_filtrado2['Código do Anúncio'], 'Título': df_filtrado2['Título'], 'Peças': df_clean2['Peças'], 'Linha': df_clean2['Linha'],
                      'Tipo': df_clean2['Tipo'], 'Qtd Vendidos': df_filtrado2['Quantidade vendida'], 'Total de Vendas': df_filtrado2['Total de Vendas'], 'Comissão': df_filtrado2['Comissão'], 'Frete Total': df_filtrado2['Frete Total'],
                      'Frete Uni': df_filtrado2['Frete Uni'], 'Lucro Bruto': df_filtrado2['Lucro Bruto'], 'Custos': df_clean2['Custos'], 'Custo Multi': df_filtrado2['Custo Multi'], 'Margem': df_filtrado2['Margem']}
    df_sells_clean = pd.DataFrame(df_sells_clean)
    data_hora = datetime.now().strftime('%d-%m-%Y %H-%M-%S')  # Pega a data e hora atual e já formata
    nome_arquivo2 = "Save 2 " + str(data_hora) + ".xlsx"
    df_sells_clean.to_excel(nome_arquivo2)

    print("Salvou o arquivo de Vendas: ", nome_arquivo2)

    return nome_arquivo2

def create_report_segmented(nome_arquivo2):
    df = pd.read_excel(nome_arquivo2)

    df.drop('Unnamed: 0', axis=1, inplace=True)

    #Vamos começar a filtrar e salvar os dataframes com segmentação
    sj = 'SCAPJA ESCAPAMENTOS'
    so = 'SOESCAP'
    catalisador = 'Catalisador'
    fix = 'Fix'
    linha_pesada = 'Pesada'
    linha_leve = 'Leve'

    #Catalisadores
    df_catalisador_total = df[df['Tipo'].str.contains(catalisador, case=False, na=False)]
    df_catalisador_no_fix = df_catalisador_total[~df_catalisador_total['Tipo'].str.contains(fix, case=False, na=False)]
    df_catalisador_fix = df_catalisador_total[df_catalisador_total['Tipo'].str.contains(fix, case=False, na=False)]
    df_sj_catalisador_no_fix = df_catalisador_no_fix[df_catalisador_no_fix['Conta'] == sj]
    df_so_catalisador_no_fix = df_catalisador_no_fix[df_catalisador_no_fix['Conta'] == so]
    df_sj_catalisador_fix = df_catalisador_fix[df_catalisador_fix['Conta'] == sj]
    df_so_catalisador_fix = df_catalisador_fix[df_catalisador_fix['Conta'] == so]

    #Linha Pesada
    df_pesada_total = df[df['Linha'].str.contains(linha_pesada, case=False, na=False)]
    df_pesada_no_fix = df_pesada_total[~df_pesada_total['Tipo'].str.contains(fix, case=False, na=False)]
    df_pesada_fix = df_pesada_total[df_pesada_total['Tipo'].str.contains(fix, case=False, na=False)]
    df_sj_pesada_no_fix = df_pesada_no_fix[df_pesada_no_fix['Conta'] == sj]
    df_so_pesada_no_fix = df_pesada_no_fix[df_pesada_no_fix['Conta'] == so]
    df_sj_pesada_fix = df_pesada_fix[df_pesada_fix['Conta'] == sj]
    df_so_pesada_fix = df_pesada_fix[df_pesada_fix['Conta'] == so]

    # Linha Leve
    df_leve_total = df[df['Linha'].str.contains(linha_leve, case=False, na=False)]
    df_leve_total = df_leve_total[~df_leve_total['Tipo'].str.contains(catalisador, case=False, na=False)]
    df_leve_no_fix = df_leve_total[~df_leve_total['Tipo'].str.contains(fix, case=False, na=False)]
    df_leve_fix = df_leve_total[df_leve_total['Tipo'].str.contains(fix, case=False, na=False)]
    df_sj_leve_no_fix = df_leve_no_fix[df_leve_no_fix['Conta'] == sj]
    df_so_leve_no_fix = df_leve_no_fix[df_leve_no_fix['Conta'] == so]
    df_sj_leve_fix = df_leve_fix[df_leve_fix['Conta'] == sj]
    df_so_leve_fix = df_leve_fix[df_leve_fix['Conta'] == so]

    #Calculando Margem Média, Frete Médio, Total Segmento, Representação em Percentual
    ...

    #Salvando o Relatorio
    with pd.ExcelWriter('Relatorio Vendas.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Total')
        df_sj_catalisador_no_fix.to_excel(writer, sheet_name='ScapJá (Catalisador)')
        df_so_catalisador_no_fix.to_excel(writer, sheet_name='SoEscap (Catalisador)')
        df_sj_catalisador_fix.to_excel(writer, sheet_name='ScapJá (Catalisador + Fix)')
        df_so_catalisador_fix.to_excel(writer, sheet_name='SoEscap (Catalisador + Fix)')
        df_sj_pesada_no_fix.to_excel(writer, sheet_name='ScapJá (Linha Pesada)')
        df_so_pesada_no_fix.to_excel(writer, sheet_name='SoEscap (Linha Pesada)')
        df_sj_pesada_fix.to_excel(writer, sheet_name='ScapJá (Linha Pesada + Fix)')
        df_so_pesada_fix.to_excel(writer, sheet_name='SoEscap (Linha Pesada + Fix)')
        df_sj_leve_no_fix.to_excel(writer, sheet_name='ScapJá (Linha Leve)')
        df_so_leve_no_fix.to_excel(writer, sheet_name='SoEscap (Linha Leve)')
        df_sj_leve_fix.to_excel(writer, sheet_name='ScapJá (Linha Leve + Fix)')
        df_so_leve_fix.to_excel(writer, sheet_name='SoEscap (Linha Leve + Fix)')

    print('Relatorio de vendas criando com sucesso')

if __name__ == '__main__':
    nome_arquivo, mlbs = create_sheet()
    nome_arquivo2 = create_report_sell(nome_arquivo, mlbs)
    create_report_segmented(nome_arquivo2)