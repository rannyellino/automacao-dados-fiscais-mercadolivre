from datetime import datetime

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