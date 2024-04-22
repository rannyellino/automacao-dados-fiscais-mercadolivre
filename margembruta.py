from __future__ import print_function

import os.path

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import calc

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1WFRZtxFrgiKTLB5BXEzPQ-j2EpSXPeUBFW2O-MNYeGs'
SAMPLE_RANGE_NAME = 'Vendas - Margem Bruta!A2:G20000'

def main():
    codigos_pecas = []
    subtotais = []
    custos = []
    df = getSheets()
    print(df)

    rows = len(df.index)
    i = 0

    while i < rows:
        linha = df.loc[[i]]  # Localiza a linha referente ao indice 'i'
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        cod_pecas = lista[2]
        subtotal = lista[3]
        custo = lista[4]

        codigos_pecas.append(cod_pecas)  #Adiciona na array em questão o valor
        subtotais.append(subtotal)  # Adiciona na array em questão o valor
        custos.append(custo)  # Adiciona na array em questão o valor
        i = i + 1

    d = {'Códigos Peças': codigos_pecas, 'Subtotais:': subtotais, 'Custos':custos}
    df = pd.DataFrame(d)
    #print(df)
    rows = len(df.index)
    i = 0

    while i < rows:
        linha = df.loc[[i]]  # Localiza a linha referente ao indice 'i'
        lista = list(linha.values.flatten())  # Transforma toda a linha do excel em uma ARRAY
        custo = lista[2]
        subtotal = int(lista[1])
        print(lista)

        if(custo == 'n/a'):
            #CHAMAR FUNÇÃO PARA CALCULAR
            qtds, codigos = discovery_parts(lista)
            print("Qtds ", qtds, "Codigos ", codigos)
            custo, linha = calc_custo(qtds, codigos)
            print("Custo: {}".format(custo))
            print("Subtotal: {}".format(subtotal))
            margem_bruta = calc_margem(custo, subtotal)
            print("Margem Bruta: {}".format(margem_bruta))
            range_sheet = 'E'+str(i+2)+':''G'+str(i+2)
            sheet_range = "Vendas - Margem Bruta!"+range_sheet
            print("Range Sheet: {}".format(sheet_range))
            _values = [custo, margem_bruta, linha]
            print("_VALUES: {}".format(_values))
            update_values(SAMPLE_SPREADSHEET_ID, sheet_range, "USER_ENTERED",  _values)

        i = i+1

def calc_margem(custo, subtotal):
    try:
        margem_bruta = int(subtotal) / int(custo)
        print("MARGEM BRUTA1: ", margem_bruta)
        margem_bruta = round(margem_bruta, 2)
        print("MARGEM BRUTA2: ", margem_bruta)
        smargem = str(margem_bruta)
        print("SMARGEM: ", smargem)

        margemcomzero = ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9",]
        i_for = 0

        for m in margemcomzero:
            if (smargem.__len__() == 3 and smargem.find(margemcomzero[i_for]) != -1):
                print("smargem.find(0.9)")
                smargem = smargem.replace("0.", "")
                smargem = smargem+"0"
                try:
                    margem_bruta = 100 - int(smargem)
                    margem_bruta = str("-" + str(margem_bruta))
                    i_for = i_for+1
                except ValueError:
                    margem_bruta = 'n/a'
                    i_for = i_for + 1

        if (smargem.find("0.") != -1):
            print("smargem.find(0.)")
            smargem = smargem.replace("0.", "")
            try:
                margem_bruta = 100 - int(smargem)
                margem_bruta = str("-"+str(margem_bruta))
            except ValueError:
                margem_bruta = 'n/a'

        if(smargem.find("1.") != -1):
            print("smargem.find(1.)")
            if(smargem.__len__() == 3):
                smargem = smargem.replace("1.", "")
                smargem = smargem+"0"
            else:
                smargem = smargem.replace("1.", "")
            margem_bruta = smargem

        if(smargem.find("2.") != -1):
            print("smargem.find(2.)")
            smargem = smargem.replace("2.", "1")
            margem_bruta = smargem
    except ZeroDivisionError:
        margem_bruta = 'n/a'

    return margem_bruta

def calc_custo(qtds, codigos):
    df_preços = pd.read_excel('Produtos-Online.xlsx')
    i_for = 0
    custos = []
    global custo
    custo = 0
    linha_return = ''

    while (i_for < codigos.__len__()):
        print("I FOR", i_for, "LEN", codigos.__len__())
        for i in codigos:
            filtro = df_preços.loc[df_preços["Cod Peça"] == i.upper().strip()]  # Procura a linha com o código da peça
            lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores

            # Caso a lista continue em branco é porque não achou a peça na planilha, um dos motivos pode ser a pesquisa em STR sendo que tem que ser em INT
            if (lista == []):
                try:
                    filtro = df_preços.loc[df_preços["Cod Peça"] == int(i)]  # Procura a linha com o código da peça
                    lista = list(filtro.values.flatten())  # Transforma a linha da planilha em uma lista para termos os valores
                except ValueError:
                    print("Peça não existe")

            # Verifica se tem valor na lista, se não tiver é porque não encontrou o código na planilha
            print("LISTA: ", lista)
            if (lista != []):
                # 0 = Fabricante, 1 = Linha, 2 = Código da Peça, 3 = Preço, 4 = Tipo de Peça(Escap, Fix, Catalisador)
                fab = lista[0]
                linha = lista[1]
                cod = lista[2]
                try:
                    preco = int(lista[3])
                except ValueError:
                    if (lista[3] != "Consulte"):
                        preco = int(float(lista[3]))
                    else:
                        preco = "Consulte"
                tipo = lista[4]

                if(linha_return == ''):
                    linha_return = linha

                # Encontrando o indice da fabrica
                indice = calc.indice_fabricante(fab, linha, tipo)

                if (preco != "Consulte"):
                    qtd = int(qtds[i_for])
                    # Calculado quantidade de itens x o preço x o indice para ter assim o valor de custo
                    print("Quantidade Peça: ", qtd)
                    custo = qtd * preco * indice
                    print("Custo: {}".format(custo))
                    custos.append(custo)
                    i_for = i_for + 1
                    continue
                else:
                    print("Peça é CONSULTE")
                    custos = [0]
                    i_for = i_for + 100
                    break
            else:
                #A PEÇA NÃO FOI ACHADA NA BASE DE DADOS
                print("Não achou a peça")
                have_consulte = True
                i_for = i_for + 1
                linha = 'n/a'

    i_for = 0

    print("Custos antes do While ", custos)
    print("CUSTOS LEN {}".format(custos.__len__()))
    custo = 0
    while(i_for < custos.__len__()):
        print(custos[i_for])
        custo = custo + custos[i_for]
        i_for = i_for+1

    if(linha_return == None or linha_return == ''):
        linha_return = 'n/a'

    return custo, linha_return


def discovery_parts(lista):
    codigos = lista[0]
    codigos_str = str(codigos)
    print(type(codigos_str))
    primeiro_processo = True
    qtds = []
    i_for2 = 0
    global unit_check

    while(codigos_str.find("X") != -1 or codigos_str.find("x") != -1 or i_for2 < codigos.__len__()):
        print("CODIGO STR", codigos_str)
        if(primeiro_processo == True):
            codigos = lista[0]
            codigos = codigos.replace(" ", "")
            codigos = codigos.split("+")
        i_for = 0
        brinde_check = 0
        pop_append = False

        units = ['2x', '3x', '4x', '5x', '6x', '7x', '8x', '9x', '10x', '11x', '12x']

        for i in codigos:
            unit_check = 0  # Checar na lista quantas unidades vai de peça caso seja mais de um
            check_units = str(i).lower()
            print("Check Unit: {}".format(check_units))
            print("Vai entrar no for que checa quantidade de peças por código")
            for un in units:
                print("unit check", unit_check)
                print("Un :",un)
                print("Units[unit_check] :", units[unit_check])
                print(check_units.find(units[unit_check]))
                if (check_units.find(units[unit_check]) != -1):
                    print("Achou as seguintes unidades", units[unit_check])
                    qtd_str2 = units[unit_check]
                    qtd_str = qtd_str2
                    codigo = check_units.replace(qtd_str2, "")
                    qtd_str2 = qtd_str2.replace("x", "")
                    qtd_str2 = qtd_str2.replace("X", "")
                    qtd = int(qtd_str2)
                    # print("Quantidade de peça(s)", qtd)
                    unit_check = units.__len__()
                    codigos.append(codigo)
                    codigos.pop(i_for)
                    pop_append = True
                    break
                else:
                    # print("Não achou quantidades")
                    codigo = i
                    qtd = 1
                    # print("Quantidade de peça(s)", qtd)
                    if (unit_check < 9):
                        unit_check = unit_check + 1

            print('Saiu do for que checa a quantidade')
            print('Peça', codigo)
            print('Quantidades', qtd)

            # Agora irá checar se existe alguma peça como brinde pois esta não é calculada no preço
            check_brinde = str(codigo).lower()
            print("CHECK BRINDE: ", check_brinde)
            brindes = ['(brinde)', '(abraçadeira)', '(coxim)', '(junta)', 'anel']

            print("Vai checar se existe brinde agora")
            for i in brindes:
                print(i)
                print("brindes[brinde_check] ",brindes[brinde_check])
                if (check_brinde.find(brindes[brinde_check]) != -1):
                    print("Foi achado o brinde", i)
                    print("I FOR:", i_for)
                    print("Codigos.POP ".format(codigos[i_for]))
                    codigos.pop(i_for)
                    brinde_check = brindes.__len__()
                    break
                else:
                    print("Não foi achado brinde")
                    if (brinde_check < 4):
                        brinde_check = brinde_check + 1
                    else:
                        qtds.append(qtd)

            print("COOOODIGOS ", codigos)
            print("Pop Append", pop_append)
            print(codigos)
            if(pop_append == False):
                i_for = i_for + 1
            brinde_check = 0
            codigos_str = str(codigos)
            primeiro_processo = False
            i_for2 = i_for2 + 1

    return qtds, codigos

def getSheets():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        df = pd.DataFrame(values, columns=['Conta', 'Código Venda', 'Cod Peça', 'Subtotal', 'Custo', 'Margem Bruta', 'Status'])
        return df

    except HttpError as err:
        print(err)

def update_values(spreadsheet_id, range_name, value_input_option,_values):
    print(spreadsheet_id)
    print(range_name)
    print(_values)
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:

        service = build('sheets', 'v4', credentials=creds)
        values = [
            [
                _values[0],
                _values[1],
                _values[2]
            ],
            # Additional rows ...
        ]
        body = {
            'values': values
        }
        print(spreadsheet_id)
        print(range_name)
        print(value_input_option)
        print(body)
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

if __name__ == '__main__':
    main()