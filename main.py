#Importando modulos
import interface
import preenchendo_dados_fiscais
import frete
import calc

def main():
    #Criando interface
    interface.main_interface()

def pegando_valores_fiscais(entry_link_planilha_anuncios, entry_link_planilha_EAN, entry_linha_coluna_anuncios, entry_linha_coluna_ean, entry_qtd_anuncios, entry_conta, janela, entry_user):
    #Puxando todos valores do input da interface
    link_planilha_anuncios = entry_link_planilha_anuncios.get()
    link_planilha_EAN = entry_link_planilha_EAN.get()
    linha_coluna_anuncios = entry_linha_coluna_anuncios.get()
    linha_coluna_ean = entry_linha_coluna_ean.get()
    qtd_anuncios = entry_qtd_anuncios.get()
    user = entry_user.get()
    conta = entry_conta.get()
    janela = janela
    print(conta)

    ncm = "87089200"
    cest = "0107500"

    #Começando a preencher os EAN com base nos valores puxados
    if(conta == "1" or conta == "2"):
        preenchendo_dados_fiscais.preenchendo(link_planilha_anuncios, link_planilha_EAN, linha_coluna_anuncios, linha_coluna_ean, ncm, cest, qtd_anuncios, conta, janela, user)
    elif(conta == "3"):
        preenchendo_dados_fiscais.preenchendo_tray(link_planilha_anuncios, link_planilha_EAN, linha_coluna_anuncios, linha_coluna_ean, qtd_anuncios, conta, janela, user)
    else:
        exit()

def pegando_valores_frete(entry_link_planilha_anuncios, entry_linha_coluna_anuncios, entry_user, entry_qtd_anuncios, janela):
    #Puxando todos valores do input da interface
    link_planilha_anuncios = entry_link_planilha_anuncios.get()
    linha_coluna_anuncios = entry_linha_coluna_anuncios.get()
    user = entry_user.get()
    qtd_anuncios = entry_qtd_anuncios.get()
    janela = janela

    if(link_planilha_anuncios != "" and linha_coluna_anuncios != "" and user != "" and qtd_anuncios != ""):
        frete.preechendo_tabela_frete(link_planilha_anuncios, linha_coluna_anuncios, user, qtd_anuncios, janela)
    else:
        print("Não possui todos os valores preenchidos")

def pegando_valores_calc(janela, entry_qtd_1, entry_cod_1, entry_qtd_2, entry_cod_2, entry_qtd_3, entry_cod_3, entry_qtd_4, entry_cod_4, entry_qtd_5, entry_cod_5
                         , entry_qtd_6, entry_cod_6, entry_qtd_7, entry_cod_7, entry_qtd_8, entry_cod_8, entry_qtd_9, entry_cod_9, entry_qtd_10, entry_cod_10, entry_frete):
    #Pegando os valores colocado na interface
    qtd_1 = entry_qtd_1.get()
    qtd_2 = entry_qtd_2.get()
    qtd_3 = entry_qtd_3.get()
    qtd_4 = entry_qtd_4.get()
    qtd_5 = entry_qtd_5.get()
    qtd_6 = entry_qtd_6.get()
    qtd_7 = entry_qtd_7.get()
    qtd_8 = entry_qtd_8.get()
    qtd_9 = entry_qtd_9.get()
    qtd_10 = entry_qtd_10.get()
    cod_1 = entry_cod_1.get()
    cod_2 = entry_cod_2.get()
    cod_3 = entry_cod_3.get()
    cod_4 = entry_cod_4.get()
    cod_5 = entry_cod_5.get()
    cod_6 = entry_cod_6.get()
    cod_7 = entry_cod_7.get()
    cod_8 = entry_cod_8.get()
    cod_9 = entry_cod_9.get()
    cod_10 = entry_cod_10.get()
    custo_frete = entry_frete.get()
    janela = janela #Janela da interface e suas propriedades e elementos

    calc.calc(janela, qtd_1, qtd_2, qtd_3, qtd_4, qtd_5, qtd_6, qtd_7, qtd_8, qtd_9, qtd_10, cod_1, cod_2, cod_3, cod_4, cod_5, cod_6, cod_7, cod_8, cod_9, cod_10, custo_frete)

if __name__ == '__main__':
    main()