from discordbot import get_api, open_link, one_sec, identify_parts, identify_price_shops, calc_parts, close_chrome, difference_price
import time

def check_list(filename):
    file = open(filename, 'r')
    content = file.read()

    content = content.replace("MLB","")
    list_cods = content.split()

    LINES = []

    for cod in list_cods:
        shops = False
        cod_mlb = "MLB"+cod
        account, preco_anuncio, frete_gratis, garantia, status, date_created = get_api(cod_mlb, shops)

        link_mlb = 'https://produto.mercadolivre.com.br/MLB-'+cod

        chrome = open_link(link_mlb)
        one_sec()

        lista_codigos = []

        while (lista_codigos == None or lista_codigos == []):
            lista_codigos = identify_parts(chrome)
            time.sleep(10)
            chrome.refresh()

        preco_anuncio_shops = identify_price_shops(chrome)

        preco_correto, pecas_consulte = calc_parts(lista_codigos, chrome, account)
        close_chrome(chrome)
        diff = difference_price(preco_correto, preco_anuncio)

        if diff > 2 or diff < 2:
            status = 'DIFF >< 2'
        else:
            status = 'OK'

        one_line = f"{cod}  {lista_codigos}  {status}"
        LINES.append(one_line)

    file_send_name = r"CORREÇÃO "+filename

    with open(file_send_name, "w") as txt_file:
        for line in LINES:
            txt_file.write(" ".join(line) + "\n")

    return file_send_name

