#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from navegador import iniciar_navegador


def coletar_kabum(driver):
    """Coleta dados de teclados no site KaBuM!"""
    url = "https://www.kabum.com.br/busca/teclado"
    seletor_produto = "article[class*='product']"
    driver.get(url)

    # Aguarda o carregamento dos produtos
    WebDriverWait(driver, 25).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, seletor_produto))
    )

    # Pequena rolagem para garantir o carregamento dinâmico
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
    time.sleep(0.5)

    produtos = []
    elementos_produto = driver.find_elements(By.CSS_SELECTOR, seletor_produto)
    quantidade = min(20, len(elementos_produto))

    for indice in range(quantidade):
        for _ in range(3):
            try:
                elemento = driver.find_elements(By.CSS_SELECTOR, seletor_produto)[indice]

                elementos_nome = elemento.find_elements(By.CSS_SELECTOR, "span.nameCard")
                if not elementos_nome:
                    break
                nome_produto = elementos_nome[0].text.strip()

                elementos_preco = elemento.find_elements(
                    By.CSS_SELECTOR, "span.priceCard, div[class*='price']"
                )
                preco_produto = (
                    elementos_preco[0].text.strip() if elementos_preco else None
                )

                produtos.append(
                    {"site": "kabum", "nome": nome_produto, "preco": preco_produto}
                )
                break
            except StaleElementReferenceException:
                time.sleep(0.25)

    return produtos


if __name__ == "__main__":
    navegador = iniciar_navegador()
    try:
        resultados = coletar_kabum(navegador)
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    finally:
        navegador.quit()

