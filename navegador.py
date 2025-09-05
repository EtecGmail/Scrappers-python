from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def iniciar_navegador():
    """Cria e retorna uma instância configurada do Chrome WebDriver."""
    opcoes_navegador = Options()
    servico_chromedriver = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=servico_chromedriver, options=opcoes_navegador)

