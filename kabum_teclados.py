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


def coletar_kabum(driver):
    url = "https://www.kabum.com.br/busca/teclado"
    seletor_cards = "article[class*='product']"
    driver.get(url)

    WebDriverWait(driver, 25).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, seletor_cards))
    )

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

                nome_el = card.find_elements(By.CSS_SELECTOR, "span.nameCard")
                if not nome_el:
                    break
                nome = nome_el[0].text.strip()

                preco = ""
                preco_el = card.find_elements(By.CSS_SELECTOR, "span.priceCard, div[class*='price']")
                if preco_el:
                    preco = preco_el[0].text.strip()

                itens.append({"site": "kabum", "nome": nome, "preco": preco or None})
                break
            except StaleElementReferenceException:
                tentativas += 1
                time.sleep(0.25)

    return itens


if __name__ == "__main__":
    navegador = configurar_navegador()
    try:
        resultados = coletar_kabum(navegador)
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    finally:
        navegador.quit()
