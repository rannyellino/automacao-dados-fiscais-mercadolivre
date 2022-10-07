from tkinter import *
from main import pegando_valores
import main
import resolucao

def criando_interface():
    # Criando interface
    janela = Tk()  # Criando Janela
    janela.title("Automatização de Dados Fiscais e EAN - MercadoLivre")  # Alterando o título da Janela

    texto_orientacao = Label(janela,
                             text="Preencha todos os campos abaixo e após isso clique no botão para começar o processo!!!\n\nEste programa foi feito"
                                  " com o intuito de ajudar quem precisa preencher varios dados fiscais de varios anuncios e em vez de fazer tudo isso "
                                  "a mão\n eu @rannyellino decidi fazer um robo que fizesse isso tudo de forma automatizada onde você apenas precisaria "
                                  "indicar atraves de planilhas quais\n lista de anuncios ele vai trabalhar e quais EANs ele tem que usar\n")  # Criando um texto
    texto_orientacao.grid(column=0, row=0)  # Indicando posição do texto

    texto_link_planilha_anuncios = Label(janela, text="Coloque o link da planilha de anuncios")
    texto_link_planilha_anuncios.grid(column=0, row=1)
    entry_link_planilha_anuncios = Entry(janela, width=110)  # Input para o link da planilha
    entry_link_planilha_anuncios.grid(column=0, row=2)

    texto_link_planilha_EAN = Label(janela, text="Coloque o link da planilha de EAN")
    texto_link_planilha_EAN.grid(column=0, row=3)
    entry_link_planilha_EAN = Entry(janela, width=110)  # Input para o link da planilha
    entry_link_planilha_EAN.grid(column=0, row=4)

    texto_linha_coluna_anuncios = Label(janela, text="Em qual célula começa os Anúncios")
    texto_linha_coluna_anuncios.grid(column=0, row=5)
    entry_linha_coluna_anuncios = Entry(janela, width=20)  # Input para qual célula começa os anuncios
    entry_linha_coluna_anuncios.grid(column=0, row=6)

    texto_linha_coluna_ean = Label(janela, text="Em qual célula começa os EAN disponiveis")
    texto_linha_coluna_ean.grid(column=0, row=7)
    entry_linha_coluna_ean = Entry(janela, width=20)  # Input para qual célula começa os EAN
    entry_linha_coluna_ean.grid(column=0, row=8)

    texto_linha_qtd_anuncios = Label(janela, text="Quantidade de anuncios que você quer alterar")
    texto_linha_qtd_anuncios.grid(column=0, row=9)
    entry_qtd_anuncios = Entry(janela, width=20)  # Input para saber quantos anuncios editar
    entry_qtd_anuncios.grid(column=0, row=10)

    # Selecionar Conta, 1 = ScapJá, 2 = SoEscap
    texto_conta = Label(janela, text="Qual conta será usada ? 1 = ScapJá, 2 = SoEscap e 3 = Tray")
    texto_conta.grid(column=0, row=11)
    entry_conta = Entry(janela, width=20)  # Input para saber quantos anuncios editar
    entry_conta.grid(column=0, row=12)

    # Usuario do chrome
    texto_user = Label(janela, text="Qual usuário do Chrome")
    texto_user.grid(column=0, row=13)
    entry_user = Entry(janela, width=20)  # Input para saber qual usuario vai puxar as configurações
    entry_user.grid(column=0, row=14)

    botao = Button(janela, text="Começar processo",command=lambda: main.pegando_valores(entry_link_planilha_anuncios, entry_link_planilha_EAN, entry_linha_coluna_anuncios, entry_linha_coluna_ean, entry_qtd_anuncios, entry_conta, janela, entry_user))
    botao.grid(column=0, row=15)  # Indicando posição para o botão

    botao = Button(janela, text="Pegar Resolução",command=lambda: resolucao.pegando_resolucao_elementos(entry_user))
    botao.grid(column=0, row=16)  # Indicando posição para o botão

    janela.mainloop()  # Deixando a janela aberta