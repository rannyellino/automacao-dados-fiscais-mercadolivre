import pandas as pd
import requests
import log

def get_api(mlbs):
    cods = []
    titles = []
    size1_list = []
    size2_list = []
    size3_list = []
    status_list = []

    _url = r"https://api.mercadolibre.com/items/"
    i = 0

    while i < mlbs.__len__():
        response = requests.get(_url+mlbs[i])
        data = response.json()
        code = response.status_code

        print(response)
        print(data)
        print("STATUS CODE {}".format(code))

        # Caso a resposta da API seja um sucesso vamos começar a guardar as informações que queremos
        if (response.status_code == 200):
            pictures = data["pictures"]
            title = data["title"]
            cod = data["id"]
            status = data["status"]

        try:
            size1 = pictures[0]['max_size']
            size2 = pictures[1]['max_size']
            size3 = pictures[2]['max_size']
        except IndexError:
            print("Tem menos de três fotos")
            if(size3 == '' or size3 == None):
                size3 = 'Sem Foto'
            if(size2 == '' or size2 == None):
                size2 = 'Sem Foto'
            if(size1 == '' or size1 == None):
                size1 = 'Sem Foto'

        cods.append(cod)
        titles.append(title)
        size1_list.append(size1)
        size2_list.append(size2)
        size3_list.append(size3)
        status_list.append(status)

        i = i+1

    log.log_imagens(cods, titles, size1_list, size2_list, size3_list, status_list)

def mlbs():
    mlbs = []
    df_base = pd.read_excel('mlbs2.xlsx')
    print(df_base)
    rows = len(df_base.index)
    i = 0

    while i < rows:
        linha = df_base.loc[[i]]  # Localiza a linha referente ao indice 'i'
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        mlb = str(lista[0])
        mlbs.append(mlb)
        i = i+1

    print(mlbs)

    get_api(mlbs)

if __name__ == '__main__':
    mlbs()


