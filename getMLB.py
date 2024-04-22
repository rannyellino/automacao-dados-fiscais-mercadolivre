import time
from selenium.webdriver.common.by import By
import navegador

def getMLB():
    user = "Administrator" #Setando usuário
    mlb_id = "sc-list-description__id" #Classe do html que contém o ID
    cods_mlbs = []
    em_processo = True
    numPageActual = 136
    max_pages = 136
    primeiroCiclo = True


    #Abrindo navegador do usuário
    chrome = navegador.abrindo_navegador(user)
    #chrome.maximize_window()

    while(em_processo == True):
        if(numPageActual <= max_pages):
            _url = "https://www.mercadolivre.com.br/anuncios/lista/promos?filters=meli_campaign_offer-p-mlb13947230&page=" + str(numPageActual) + "&task=p-mlb13947230"
            if (primeiroCiclo == True):
                chrome.execute_script("window.open('about:blank','blank');")
                chrome.switch_to.window('blank')

            chrome.execute_script("window.open('about:blank','cods{}');".format(numPageActual))
            pausa_curta()
            chrome.switch_to.window('cods{}'.format(numPageActual))
            chrome.get(_url)
            pausa_longa()

            mlbs = chrome.find_elements(By.CLASS_NAME, mlb_id)
            #print(mlbs)
            for i in range(36):
                try:
                    cods_mlbs.append(mlbs[i].text)
                except IndexError:
                    cods_mlbs.append("ERRO")

            print(cods_mlbs)
            chrome.close()
            chrome.switch_to.window('blank')
            numPageActual = numPageActual + 1
            pausa_curta()
            primeiroCiclo = False
            print("Cods MLBS: {}".format(cods_mlbs.__len__()))
        else:
            with open("CODS MLBS AUTOPARTS 01-04-24 - SoEscap-2.txt",
                      "w") as arquivo:  # Cria o arquivo TXT com o nome certo e começa a escrever em cada linha os códigos que ele finalizou o processo
                for value in cods_mlbs:
                    arquivo.write(str(value) + "\n")
            em_processo = False

def pausa_longa():
    time.sleep(5)

def pausa_curta():
    time.sleep(2.5)

if __name__ == '__main__':
    getMLB()



