#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from navegador import iniciar_navegador


def coletar_mercadolivre(driver):
    """Coleta dados de teclados no site Mercado Livre."""
    url = "https://lista.mercadolivre.com.br/teclado"
    seletor_produto = "li.ui-search-layout__item, div.ui-search-result__content-wrapper"
    driver.get(url)

    # Aguarda o carregamento dos produtos
    WebDriverWait(driver, 25).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, seletor_produto))
    )

    # Rolagem inicial para estabilizar carregamento dinâmico
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
    time.sleep(0.5)

    produtos = []
    elementos_produto = driver.find_elements(By.CSS_SELECTOR, seletor_produto)
    quantidade = min(20, len(elementos_produto))

    for indice in range(quantidade):
        for _ in range(3):
            try:
                elemento = driver.find_elements(By.CSS_SELECTOR, seletor_produto)[indice]

                nome_produto = ""
                for seletor in ["a.poly-component__title", "h2 a", "h2"]:
                    elementos_nome = elemento.find_elements(By.CSS_SELECTOR, seletor)
                    if elementos_nome:
                        texto = (
                            elementos_nome[0].text
                            or elementos_nome[0].get_attribute("title")
                            or ""
                        ).strip()
                        if texto:
                            nome_produto = texto
                            break
                if not nome_produto:
                    break

                preco_produto = ""
                inteiro = elemento.find_elements(By.CSS_SELECTOR, ".andes-money-amount__fraction")
                if inteiro:
                    preco_produto = "R$ " + inteiro[0].text.strip()
                    centavos = elemento.find_elements(By.CSS_SELECTOR, ".andes-money-amount__cents")
                    if centavos:
                        preco_produto += "," + centavos[0].text.strip()

                produtos.append(
                    {"site": "mercadolivre", "nome": nome_produto, "preco": preco_produto or None}
                )
                break
            except StaleElementReferenceException:
                time.sleep(0.25)

    return produtos


if __name__ == "__main__":
    navegador = iniciar_navegador()
    try:
        resultados = coletar_mercadolivre(navegador)
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    finally:
        navegador.quit()

