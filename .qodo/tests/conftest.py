import pytest
import os

@pytest.fixture
def texto_ejemplo():
    return "Este es un mensaje de prueba muy positivo y alegre."

@pytest.fixture
def mock_resultado_avanzado():
    return {
        "sentimiento_global": "positivo",
        "polaridad": 0.8,
        "intensidad": 0.9,
        "justificacion": "El texto contiene palabras de alta carga positiva.",
        "recomendacion": "Mantener este tono en la comunicación."
    }

@pytest.fixture
def temp_output(tmp_path):
    f = tmp_path / "resultado_test.json"
    return str(f)
