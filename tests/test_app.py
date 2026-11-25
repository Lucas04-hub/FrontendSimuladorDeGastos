from app import app


def test_pagina_inicial():

    cliente = app.test_client()

    resposta = cliente.get("/")

    assert resposta.status_code == 200

def test_pagina_inicial():

    cliente = app.test_client()

    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert resposta.content_type.startswith("text/html")
    assert b"html" in resposta.data.lower()

def test_pagina_inicial_contem_titulo():

    cliente = app.test_client()

    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert b"Simulador de Gastos" in resposta.data