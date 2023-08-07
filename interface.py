from tkinter import *
from main import pegando_valores_fiscais
from main import pegando_valores_frete
import main
import resolucao

def main_interface():
    # Criando interface
    janela = Tk() # Criando Janela
    janela.title("Robo Brunão - Automatização E-COMMERCE")  # Alterando o título da Janela

    texto_orientacao = Label(janela,
                             text="Bem-vindo ao robo de automatização para E-commerce, logo abaixo você pode selecionar qual função você quer automatizar\n"
                                  "lembrando que para cada função será pedido valores para poder fazer o processo de automação, importante saber indicar os valores certos")  # Criando um texto
    texto_orientacao.grid(column=0, row=0)  # Indicando posição do texto

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=1)  # Apenas dar espaço na interface

    botao_fiscais = Button(janela, text="Dados Fiscais",command=lambda: interface_fiscais())
    botao_fiscais.grid(column=0, row=2)

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=3)  # Apenas dar espaço na interface

    botao_fiscais = Button(janela, text="Tabela de Frete", command=lambda: interface_frete())
    botao_fiscais.grid(column=0, row=4)

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=5)  # Apenas dar espaço na interface

    botao_calc = Button(janela, text="Calculadora", command=lambda: interface_calc())
    botao_calc.grid(column=0, row=6)

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=7)  # Apenas dar espaço na interface

    botao_margem = Button(janela, text="Calcular Margem", command=lambda: interface_margem())
    botao_margem.grid(column=0, row=8)

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=9)  # Apenas dar espaço na interface

    botao_margem = Button(janela, text="Bianca Dropa AWP", command=lambda: interface_bianca())
    botao_margem.grid(column=0, row=10)

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=11)  # Apenas dar espaço na interface

    janela.mainloop()  # Deixando a janela aberta

def interface_bianca():
    # Criando interface
    janela = Tk()  # Criando Janela
    janela.title("Robo Brunão - Automatização E-COMMERCE")  # Alterando o título da Janela

    texto_orientacao = Label(janela,
                             text="   Preencha todos os valores abaixo para funcionar corretamente   ")  # Criando um texto
    texto_orientacao.grid(column=0, row=0, columnspan=10)  # Indicando posição do texto

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=1)  # Apenas dar espaço na interface

    texto_conta = Label(janela, text="Conta")
    texto_conta.grid(column=0, row=2, columnspan=10)
    entry_conta = Entry(janela, width=20)  # Input para o link da planilha
    entry_conta.grid(column=0, row=3, columnspan=10)

    texto_cod_venda = Label(janela, text="Código da Última Venda")
    texto_cod_venda.grid(column=0, row=4, columnspan=10)
    entry_cod_venda = Entry(janela, width=50)  # Input para o link da planilha
    entry_cod_venda.grid(column=0, row=5, columnspan=10)

    texto_id = Label(janela, text="ID Último Contato")
    texto_id.grid(column=0, row=6, columnspan=10)
    entry_id = Entry(janela, width=20)  # Input para qual célula começa os anuncios
    entry_id.grid(column=0, row=7, columnspan=10)

    texto_user = Label(janela, text="Usuario")
    texto_user.grid(column=0, row=8, columnspan=10)
    entry_user = Entry(janela, width=20)  # Input para qual célula começa os anuncios
    entry_user.grid(column=0, row=9, columnspan=10)

    espaco2 = Label(janela, text="")
    espaco2.grid(column=0, row=10)  # Apenas dar espaço na interface

    botao_start = Button(janela, text="Começar Processo",
                         command=lambda: main.pegando_valores_bianca(entry_conta,
                                                                    entry_cod_venda, entry_id, entry_user,
                                                                    janela))
    botao_start.grid(column=0, row=11, columnspan=10)

    espaco3 = Label(janela, text="")
    espaco3.grid(column=0, row=12)  # Apenas dar espaço na interface

    janela.mainloop()  # Deixando a janela aberta

def interface_margem():
    # Criando interface
    janela = Tk()  # Criando Janela
    janela.title("Robo Brunão - Automatização E-COMMERCE")  # Alterando o título da Janela

    texto_orientacao = Label(janela,
                             text="   Basta preencher todos os valores abaixo e clicar no botão calcular e terá a margem de lucro bruto   ")  # Criando um texto
    texto_orientacao.grid(column=0, row=0, columnspan=10)  # Indicando posição do texto

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=1)  # Apenas dar espaço na interface

    texto_pecas = Label(janela,
                             text=" Abaixo preencha os códigos das peças ")  # Criando um texto
    texto_pecas.grid(column=0, row=2, columnspan=4)  # Indicando posição do texto

    texto_venda = Label(janela,
                        text=" Abaixo preencha com o valor da venda \nsem as tarifas ")  # Criando um texto
    texto_venda.grid(column=5, row=2, columnspan=5)  # Indicando posição do texto

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=3)  # Apenas dar espaço na interface

    #ABAIXO ESTÁ A INTERFACE REFERENTE AOS CAMPOS QUE IRÃO PREENCHER COM OS CÓDIGOS DAS PEÇAS

    entry_qtd_1 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_1.grid(column=1, row=4, sticky=W)
    entry_qtd_1.insert(0, "1")
    entry_cod_1 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_1.grid(column=2, row=4, sticky=W)
    clear_cod_1 = Button(janela, text="Clear", font=font_default(), command=lambda: clear_calc( entry_cod_1))
    clear_cod_1.grid(column=3, row=4, sticky=W)

    entry_qtd_2 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_2.grid(column=1, row=5, sticky=W)
    entry_qtd_2.insert(0, "1")
    entry_cod_2 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_2.grid(column=2, row=5, sticky=W)
    clear_cod_2 = Button(janela, text="Clear", font=font_default(), command=lambda: clear_calc( entry_cod_2))
    clear_cod_2.grid(column=3, row=5, sticky=W)

    entry_qtd_3 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_3.grid(column=1, row=6, sticky=W)
    entry_qtd_3.insert(0, "1")
    entry_cod_3 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_3.grid(column=2, row=6, sticky=W)
    clear_cod_3 = Button(janela, text="Clear", font=font_default(), command=lambda: clear_calc( entry_cod_3))
    clear_cod_3.grid(column=3, row=6, sticky=W)

    entry_qtd_4 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_4.grid(column=1, row=7, sticky=W)
    entry_qtd_4.insert(0, "1")
    entry_cod_4 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_4.grid(column=2, row=7, sticky=W)
    clear_cod_4 = Button(janela, text="Clear", font=font_default(), command=lambda: clear_calc( entry_cod_4))
    clear_cod_4.grid(column=3, row=7, sticky=W)

    entry_qtd_5 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_5.grid(column=1, row=8, sticky=W)
    entry_qtd_5.insert(0, "1")
    entry_cod_5 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_5.grid(column=2, row=8, sticky=W)
    clear_cod_5 = Button(janela, text="Clear", font=font_default(), command=lambda: clear_calc( entry_cod_5))
    clear_cod_5.grid(column=3, row=8, sticky=W)

    # ABAIXO ESTÁ A INTERFACE REFERENTE AO CAMPO QUE IRÁ SER PREENCHIDO COM O VALOR DA VENDA SEM AS TARIFAS

    entry_cod_01 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_01.grid(column=7, row=4, sticky=W)
    clear_cod_01 = Button(janela, text="Clear", font=font_default(), command=lambda: clear_calc( entry_cod_01))
    clear_cod_01.grid(column=8, row=4, sticky=W)

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=9)  # Apenas dar espaço na interface

    botao_start = Button(janela, text="Calcular", font=font_default(), command=lambda: main.pegando_valores_margem(janela, entry_qtd_1, entry_cod_1, entry_qtd_2,
                                                                                                                   entry_cod_2, entry_qtd_3, entry_cod_3, entry_qtd_4,
                                                                                                                   entry_cod_4, entry_qtd_5, entry_cod_5,entry_cod_01))
    botao_start.grid(column=4, row=10)

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=11)  # Apenas dar espaço na interface

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=14)  # Apenas dar espaço na interface


def interface_fiscais():
    # Criando interface
    janela = Tk()  # Criando Janela
    janela.title("Robo Brunão - Automatização E-COMMERCE")  # Alterando o título da Janela

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

    botao_start = Button(janela, text="Começar processo",command=lambda: main.pegando_valores_fiscais(entry_link_planilha_anuncios, entry_link_planilha_EAN, entry_linha_coluna_anuncios, entry_linha_coluna_ean, entry_qtd_anuncios, entry_conta, janela, entry_user))
    botao_start.grid(column=0, row=15)  # Indicando posição para o botão

    botao_res = Button(janela, text="Pegar Resolução",command=lambda: resolucao.pegando_resolucao_elementos(entry_user))
    botao_res.grid(column=0, row=16)  # Indicando posição para o botão

    janela.mainloop()  # Deixando a janela aberta

def interface_frete():
    # Criando interface
    janela = Tk()  # Criando Janela
    janela.title("Robo Brunão - Automatização E-COMMERCE")  # Alterando o título da Janela

    texto_orientacao = Label(janela,
                             text="Para adicionar a tabela de frete personalizado em anuncios é muito simples, indique a planilha na qual estão os códigos dos anuncios\n"
                                  "após isso também coloque em que celula começa os anuncios, quantos anuncios você quer que preencha com a tabela de frete e por último\n"
                                  "o seu usuario do windows para poder pegar as configurações do seu Google Chrome")  # Criando um texto
    texto_orientacao.grid(column=0, row=0)  # Indicando posição do texto

    texto_link_planilha_anuncios = Label(janela, text="Coloque o link da planilha de anuncios")
    texto_link_planilha_anuncios.grid(column=0, row=1)
    entry_link_planilha_anuncios = Entry(janela, width=110)  # Input para o link da planilha
    entry_link_planilha_anuncios.grid(column=0, row=2)

    texto_linha_coluna_anuncios = Label(janela, text="Em qual célula começa os Anúncios")
    texto_linha_coluna_anuncios.grid(column=0, row=3)
    entry_linha_coluna_anuncios = Entry(janela, width=20)  # Input para qual célula começa os anuncios
    entry_linha_coluna_anuncios.grid(column=0, row=4)

    texto_linha_qtd_anuncios = Label(janela, text="Quantidade de anuncios que você quer alterar")
    texto_linha_qtd_anuncios.grid(column=0, row=5)
    entry_qtd_anuncios = Entry(janela, width=20)  # Input para saber quantos anuncios editar
    entry_qtd_anuncios.grid(column=0, row=6)

    # Usuario do chrome
    texto_user = Label(janela, text="Qual usuário do Windows")
    texto_user.grid(column=0, row=7)
    entry_user = Entry(janela, width=20)  # Input para saber qual usuario vai puxar as configurações
    entry_user.grid(column=0, row=8)

    botao_start = Button(janela, text="Começar Processo", command=lambda: main.pegando_valores_frete(entry_link_planilha_anuncios, entry_linha_coluna_anuncios, entry_user, entry_qtd_anuncios, janela))
    botao_start.grid(column=0, row=9)
    janela.mainloop()  # Deixando a janela aberta

def interface_calc():
    # Criando interface
    janela = Tk()  # Criando Janela
    janela.title("Robo Brunão - Automatização E-COMMERCE")  # Alterando o título da Janela

    texto_orientacao = Label(janela,
                             text="Atualmente a calculadora está apenas com a base de dados da Mastra, Pioneiro, AMAM e Alpha,\n"
                                  "para calcular basta inserir o código das peças nos campos a baixo e a quantidade de cada peça", font=font_default())  # Criando um texto
    texto_orientacao.grid(column=0, row=0, columnspan=26)  # Indicando posição do texto

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=1)  # Apenas dar espaço na interface

    entry_qtd_1 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_1.grid(column=13, row=2, sticky=W)
    entry_qtd_1.insert(0, "1")
    entry_cod_1 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_1.grid(column=14, row=2, sticky=W)
    clear_cod_1 = Button(janela, text="Clear", font=font_default(),
                         command=lambda: clear_calc( entry_cod_1))
    clear_cod_1.grid(column=15, row=2, sticky=W)

    entry_qtd_2 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_2.grid(column=13, row=3, sticky=W)
    entry_qtd_2.insert(0, "1")
    entry_cod_2 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_2.grid(column=14, row=3, sticky=W)
    clear_cod_2 = Button(janela, text="Clear", font=font_default(),
                         command=lambda: clear_calc( entry_cod_2))
    clear_cod_2.grid(column=15, row=3, sticky=W)

    entry_qtd_3 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_3.grid(column=13, row=4, sticky=W)
    entry_qtd_3.insert(0, "1")
    entry_cod_3 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_3.grid(column=14, row=4, sticky=W)
    clear_cod_3 = Button(janela, text="Clear", font=font_default(),
                         command=lambda: clear_calc( entry_cod_3))
    clear_cod_3.grid(column=15, row=4, sticky=W)

    entry_qtd_4 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_4.grid(column=13, row=5, sticky=W)
    entry_qtd_4.insert(0, "1")
    entry_cod_4 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_4.grid(column=14, row=5, sticky=W)
    clear_cod_4 = Button(janela, text="Clear", font=font_default(),
                         command=lambda: clear_calc( entry_cod_4))
    clear_cod_4.grid(column=15, row=5, sticky=W)

    entry_qtd_5 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_5.grid(column=13, row=6, sticky=W)
    entry_qtd_5.insert(0, "1")
    entry_cod_5 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_5.grid(column=14, row=6, sticky=W)
    clear_cod_5 = Button(janela, text="Clear", font=font_default(),
                         command=lambda: clear_calc( entry_cod_5))
    clear_cod_5.grid(column=15, row=6, sticky=W)

    entry_qtd_6 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_6.grid(column=13, row=7, sticky=W)
    entry_qtd_6.insert(0, "1")
    entry_cod_6 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_6.grid(column=14, row=7, sticky=W)
    clear_cod_6 = Button(janela, text="Clear", font=font_default(),
                         command=lambda: clear_calc( entry_cod_6))
    clear_cod_6.grid(column=15, row=7, sticky=W)

    entry_qtd_7 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_7.grid(column=13, row=8, sticky=W)
    entry_qtd_7.insert(0, "1")
    entry_cod_7 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_7.grid(column=14, row=8, sticky=W)
    clear_cod_7 = Button(janela, text="Clear", font=font_default(),
                         command=lambda: clear_calc( entry_cod_7))
    clear_cod_7.grid(column=15, row=8, sticky=W)

    entry_qtd_8 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_8.grid(column=13, row=9, sticky=W)
    entry_qtd_8.insert(0, "1")
    entry_cod_8 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_8.grid(column=14, row=9, sticky=W)
    clear_cod_8 = Button(janela, text="Clear", font=font_default(),
                         command=lambda: clear_calc( entry_cod_8))
    clear_cod_8.grid(column=15, row=9, sticky=W)

    entry_qtd_9 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_9.grid(column=13, row=10, sticky=W)
    entry_qtd_9.insert(0, "1")
    entry_cod_9 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_9.grid(column=14, row=10, sticky=W)
    clear_cod_9 = Button(janela, text="Clear", font=font_default(),
                         command=lambda: clear_calc( entry_cod_9))
    clear_cod_9.grid(column=15, row=10, sticky=W)

    entry_qtd_10 = Entry(janela, width=2, font=font_default())  # Input para quantidade de peças
    entry_qtd_10.grid(column=13, row=11, sticky=W)
    entry_qtd_10.insert(0, "1")
    entry_cod_10 = Entry(janela, width=10, font=font_default())  # Input para código da peça
    entry_cod_10.grid(column=14, row=11, sticky=W)
    clear_cod_10 = Button(janela, text="Clear", font=font_default(),
                         command=lambda: clear_calc( entry_cod_10))
    clear_cod_10.grid(column=15, row=11, sticky=W)

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=12)  # Apenas dar espaço na interface

    custo_frete_label = Label(janela, text="Custo do Frete", font=font_default()) #Label para indicar onde colocar o custo do frete
    custo_frete_label.grid(column=13, row=13, columnspan=2)

    entry_frete = Entry(janela, width=5, font=font_default())#Espaço para por o valor do frete
    entry_frete.grid(column=13, row=14, columnspan=2)
    entry_frete.insert(0,"35")

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=15)  # Apenas dar espaço na interface

    botao_start = Button(janela, text="Calcular",command=lambda: main.pegando_valores_calc(janela, entry_qtd_1, entry_cod_1, entry_qtd_2,
                                                                                           entry_cod_2, entry_qtd_3, entry_cod_3, entry_qtd_4, entry_cod_4,
                                                                                           entry_qtd_5, entry_cod_5, entry_qtd_6, entry_cod_6, entry_qtd_7,
                                                                                           entry_cod_7, entry_qtd_8, entry_cod_8, entry_qtd_9, entry_cod_9,
                                                                                           entry_qtd_10, entry_cod_10, entry_frete), font=("Segoe UI", 17))
    botao_start.grid(column=13, row=16, columnspan=2)

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=17)  # Apenas dar espaço na interface

    espaco = Label(janela, text="")
    espaco.grid(column=0, row=22)  # Apenas dar espaço na interface

def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and  ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode==86 and  ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")


def clear_calc(entry_cod):

    entry_cod.delete(0, END)

def font_default():
    font = ("Segoe UI", 12)
    return font



