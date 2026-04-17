🧪 tests/conftest.py — Fixtures Globais pytest
Español · English · 🇧🇷 Português · ← Índice

Fixture: texto_ejemplo
python@pytest.fixture
def texto_ejemplo() -> str:
    return "Este es un mensaje de prueba muy positivo y alegre."

Fixture: mock_resultado_avanzado
python@pytest.fixture
def mock_resultado_avanzado() -> dict:
    return {
        "sentimiento_global": "positivo",
        "polaridad": 0.8,
        "intensidad": 0.9,
        "justificacion": "El texto contiene palabras de alta carga positiva.",
        "recomendacion": "Mantener este tono en la comunicación."
    }

Fixture: temp_output
python@pytest.fixture
def temp_output(tmp_path) -> str:
    return str(tmp_path / "resultado_test.json")
Gera um caminho de arquivo temporário para testes de escrita. Garante isolamento entre testes via tmp_path do pytest.

🔬 tests/e2e/test_app_folw.py — Testes End-to-End

Teste: test_flujo_completo_analisis
Verifica que texto claramente negativo seja classificado como "negativo" no nível básico, que a polaridade avançada seja negativa (< 0) e que o campo justificacion exista com conteúdo.
pythonassert res_b["sentimiento"] == "negativo"
assert res_a["polaridad"] < 0
assert "justificacion" in res_a
assert len(res_a["justificacion"]) > 0

Teste: test_consistencia_entre_niveles
Verifica que os níveis básico e avançado concordem na classificação geral do sentimento para texto positivo.
pythonassert res_b["sentimiento"].lower() == res_a["sentimiento_global"].lower()

Teste: test_analisis_neutral_limpio
Verifica o comportamento com texto mínimo sem carga emocional.
pythonassert res_a["sentimiento_global"].upper() == "NEUTRAL"
assert res_a["polaridad"] == 0

🔗 tests/integration/test_storage.py — Testes de Integração

Teste: test_guardar_json_crea_archivo
Verifica que guardar_json cria o arquivo corretamente e que o conteúdo escrito é o esperado.
pythonguardar_json({"test": "ok"}, str(nome_arquivo))
assert os.path.exists(nome_arquivo)
assert json.load(f)["test"] == "ok"

🧩 tests/unit/test_niveles.py — Testes Unitários

Teste: test_sentimiento_texto_vacio
pythonres = analizar_sentimiento_avanzado("")
assert res["sentimiento_global"] == "neutral"
Teste: test_sentimiento_muy_positivo
pythonres = analizar_sentimiento_avanzado("¡Esto es absolutamente increíble!")
assert res["polaridad"] > 0.5
Teste: test_sentimiento_caracteres_especiales
pythonres = analizar_sentimiento_avanzado("!!! @#$% ^&*")
assert "sentimiento_global" in res

⚙️ CI/CD — Pipeline GitHub Actions

Diagrama do Pipeline
push / pull_request
        │
        ▼
  ubuntu-latest
        │
        ▼
  actions/checkout@v3
  actions/setup-python@v4  (python 3.10)
        │
        ▼
  pip install pytest pytest-cov pytesseract pillow
  sudo apt-get install tesseract-ocr tesseract-ocr-spa
        │
        ▼
  pytest --cov=sentimiento tests/