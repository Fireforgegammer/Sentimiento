import pytest
from sentimiento.niveles import analizar_sentimiento_basico, analizar_sentimiento_avanzado

def test_flujo_completo_analisis():
    texto = "No me gusta nada como funciona este servicio, es horrible."
    
    res_b = analizar_sentimiento_basico(texto)
    res_a = analizar_sentimiento_avanzado(texto)
    
    assert res_b["sentimiento"] == "negativo"
    assert res_a["polaridad"] < 0
    assert "justificacion" in res_a
    assert len(res_a["justificacion"]) > 0

def test_consistencia_entre_niveles():
    texto = "Excelente trabajo equipo."
    
    res_b = analizar_sentimiento_basico(texto)
    res_a = analizar_sentimiento_avanzado(texto)
    
    assert res_b["sentimiento"].lower() == res_a["sentimiento_global"].lower()

def test_analisis_neutral_limpio():
    texto = "hola"
    res_a = analizar_sentimiento_avanzado(texto)
    
    assert res_a["sentimiento_global"].upper() == "NEUTRAL"
    assert res_a["polaridad"] == 0