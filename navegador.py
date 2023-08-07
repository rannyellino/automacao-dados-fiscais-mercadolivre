from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def abrindo_navegador(user):
    # Abrindo Chrome(NAVEGADOR PADRÃO DO WINDOWS)
    #s = Service(ChromeDriverManager().install())
    options = Options() #Para poder pegar o perfil do chrome
    options.add_argument(r"user-data-dir=C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(user)) #Indicado diretorio do perfil do chrome
    chrome = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    chrome.maximize_window()
    chrome.get("https://google.com.br") #abri o chrome com o endereço indicado
    print(chrome)
    return chrome

def open_chrome_dc():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    chrome = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    chrome.get("https://google.com.br")  # abri o chrome com o endereço indicado
    print(chrome)
    return chrome
