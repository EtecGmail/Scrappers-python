#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager


def configurar_navegador():
    opcoes = Options()
    servico = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=servico, options=opcoes)


def coletar_mercadolivre(driver):
    url = "https://lista.mercadolivre.com.br/teclado"
    seletor_cards = "li.ui-search-layout__item, div.ui-search-result__content-wrapper"
    driver.get(url)

    WebDriverWait(driver, 25).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, seletor_cards))
    )

    # rolar um pouco para estabilizar carregamento dinâmico
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
    time.sleep(0.5)

    itens = []
    cards_iniciais = driver.find_elements(By.CSS_SELECTOR, seletor_cards)
    total = min(20, len(cards_iniciais))

    for i in range(total):
        tentativas = 0
        while tentativas < 3:
            try:
                card = driver.find_elements(By.CSS_SELECTOR, seletor_cards)[i]

                nome = ""
                for seletor in ["a.poly-component__title", "h2 a", "h2"]:
                    els = card.find_elements(By.CSS_SELECTOR, seletor)
                    if els:
                        texto = (els[0].text or els[0].get_attribute("title") or "").strip()
                        if texto:
                            nome = texto
                            break
                if not nome:
                    break

                preco = ""
                inteiro = card.find_elements(By.CSS_SELECTOR, ".andes-money-amount__fraction")
                if inteiro:
                    preco = "R$ " + inteiro[0].text.strip()
                    centavos = card.find_elements(By.CSS_SELECTOR, ".andes-money-amount__cents")
                    if centavos:
                        preco += "," + centavos[0].text.strip()

                itens.append({"site": "mercadolivre", "nome": nome, "preco": preco or None})
                break
            except StaleElementReferenceException:
                tentativas += 1
                time.sleep(0.25)

    return itens


if __name__ == "__main__":
    navegador = configurar_navegador()
    try:
        resultados = coletar_mercadolivre(navegador)
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    finally:
        navegador.quit()
