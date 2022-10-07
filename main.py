#Importando modulos
import interface
import preenchendo_dados_fiscais

def main():
    #Criando interface
    interface.criando_interface()

def pegando_valores(entry_link_planilha_anuncios, entry_link_planilha_EAN, entry_linha_coluna_anuncios, entry_linha_coluna_ean, entry_qtd_anuncios, entry_conta, janela, entry_user):
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

if __name__ == '__main__':
    main()