# 🧪 `tests/conftest.py` — Global pytest Fixtures

[Español](../../es/tests/tests.md) · 🌐 English · [Português](../../pt/tests/tests.md) · [← Index](../INDEX.md)

---

## Overview

Configuration and shared fixtures file for the entire test suite. Provides reusable test data and environment setup helpers for integration and unit tests.

---

## Fixture: `texto_ejemplo`

### Signature

```python
@pytest.fixture
def texto_ejemplo() -> str
```

### Return

```python
"Este es un mensaje de prueba muy positivo y alegre."
```

---

## Fixture: `mock_resultado_avanzado`

### Signature

```python
@pytest.fixture
def mock_resultado_avanzado() -> dict
```

### Description

Returns a dictionary simulating the response of `analizar_sentimiento_avanzado`. Allows testing logic that consumes analysis results without making real API calls.

### Return

```python
{
    "sentimiento_global": "positivo",
    "polaridad": 0.8,
    "intensidad": 0.9,
    "justificacion": "El texto contiene palabras de alta carga positiva.",
    "recomendacion": "Mantener este tono en la comunicación."
}
```

---

## Fixture: `temp_output`

### Signature

```python
@pytest.fixture
def temp_output(tmp_path) -> str
```

### Description

Generates a temporary file path for write tests. Uses pytest's built-in `tmp_path` fixture to guarantee isolation between tests.

### Return

| Type | Description |
|------|-------------|
| `str` | Full path as string: `<tmp_path>/resultado_test.json` |

---

# 🔬 `tests/e2e/test_app_folw.py` — End-to-End Tests

---

## Overview

Full-flow tests that verify system consistency from text input to analyzer output. **Do not mock the API** — they make real calls to Groq.

---

## Test: `test_flujo_completo_analisis`

### Description

Verifies that clearly negative text is classified as `"negativo"` at the basic level, that the advanced polarity is negative (`< 0`), and that the `justificacion` field exists and has content.

### Test text

```
"No me gusta nada como funciona este servicio, es horrible."
```

### Assertions

```python
assert res_b["sentimiento"] == "negativo"
assert res_a["polaridad"] < 0
assert "justificacion" in res_a
assert len(res_a["justificacion"]) > 0
```

---

## Test: `test_consistencia_entre_niveles`

### Description

Verifies that basic and advanced levels agree on the general sentiment classification for positive text. Guarantees cross-analyzer consistency.

### Test text

```
"Excelente trabajo equipo."
```

### Assertions

```python
assert res_b["sentimiento"].lower() == res_a["sentimiento_global"].lower()
```

---

## Test: `test_analisis_neutral_limpio`

### Description

Verifies system behavior with minimal emotionally-neutral text. Advanced analysis must classify it as `"NEUTRAL"` with zero polarity.

### Test text

```
"hola"
```

### Assertions

```python
assert res_a["sentimiento_global"].upper() == "NEUTRAL"
assert res_a["polaridad"] == 0
```

---

# 🔗 `tests/integration/test_storage.py` — Integration Tests

---

## Overview

Integration tests for the storage module. Verify that `guardar_json` creates the file correctly and that the written content matches the input.

---

## Test: `test_guardar_json_crea_archivo`

### Signature

```python
def test_guardar_json_crea_archivo(tmp_path) -> None
```

### Flow

```
datos = {"test": "ok"}
nombre_archivo = tmp_path / "test_output.json"
guardar_json(datos, str(nombre_archivo))
    │
    ▼
assert os.path.exists(nombre_archivo)
    │
    ▼
contenido = json.load(f)
assert contenido["test"] == "ok"
```

---

# 🧩 `tests/unit/test_niveles.py` — Unit Tests

---

## Overview

Unit tests of the advanced analyzer for edge cases: empty text, very positive text, and text with special characters.

---

## Test: `test_sentimiento_texto_vacio`

Verifies the system handles empty text without raising exceptions and returns `"neutral"` as the global sentiment.

```python
res = analizar_sentimiento_avanzado("")
assert res["sentimiento_global"] == "neutral"
```

---

## Test: `test_sentimiento_muy_positivo`

Verifies that text with very high emotional load produces a polarity above `0.5`.

```python
res = analizar_sentimiento_avanzado("¡Esto es absolutamente increíble y maravilloso!")
assert res["polaridad"] > 0.5
```

---

## Test: `test_sentimiento_caracteres_especiales`

Verifies the system does not crash on special character input and returns a dict with the `"sentimiento_global"` key.

```python
res = analizar_sentimiento_avanzado("!!! @#$% ^&*")
assert "sentimiento_global" in res
```

---

# ⚙️ CI/CD — GitHub Actions Pipeline

---

## Overview

Continuous integration pipeline defined in `.github/workflows/python-tests.yml`. Runs automatically on every `push` and `pull_request`.

---

## Pipeline Diagram

```
push / pull_request
        │
        ▼
  ubuntu-latest
        │
        ▼
  actions/checkout@v3
        │
        ▼
  actions/setup-python@v4  (python 3.10)
        │
        ▼
  pip install pytest pytest-cov pytesseract pillow
        │
        ▼
  sudo apt-get install tesseract-ocr tesseract-ocr-spa
        │
        ▼
  pytest --cov=sentimiento tests/
```

