import pytest
from sentimiento.niveles import analizar_sentimiento_avanzado

def test_sentimiento_texto_vacio():
    res = analizar_sentimiento_avanzado("")
    assert res["sentimiento_global"] == "neutral"

def test_sentimiento_muy_positivo():
    res = analizar_sentimiento_avanzado("¡Esto es absolutamente increíble y maravilloso!")
    assert res["polaridad"] > 0.5

def test_sentimiento_caracteres_especiales():
    res = analizar_sentimiento_avanzado("!!! @#$% ^&*")
    assert "sentimiento_global" in res