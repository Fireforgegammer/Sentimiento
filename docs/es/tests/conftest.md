# 🧪 `tests/conftest.py` — Fixtures Globales de pytest

🌐 [English](../../en/tests/conftest.md) · [Português](../../pt/tests/conftest.md) · [← Índice](../INDEX.md)

---

## Descripción General

Archivo de configuración y fixtures compartidas para toda la suite de pruebas. Provee datos de prueba reutilizables y helpers de configuración de entorno para tests de integración y unitarios.

---

## Fixture: `texto_ejemplo`

### Signatura

```python
@pytest.fixture
def texto_ejemplo() -> str
```

### Descripción

Retorna un texto de ejemplo con sentimiento claramente positivo, usado como entrada estándar en tests que necesitan un texto con carga emocional definida.

### Retorno

```python
"Este es un mensaje de prueba muy positivo y alegre."
```

---

## Fixture: `mock_resultado_avanzado`

### Signatura

```python
@pytest.fixture
def mock_resultado_avanzado() -> dict
```

### Descripción

Retorna un diccionario que simula la respuesta de `analizar_sentimiento_avanzado`. Permite testear lógica que consume resultados de análisis sin realizar llamadas reales a la API.

### Retorno

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

### Signatura

```python
@pytest.fixture
def temp_output(tmp_path) -> str
```

### Descripción

Genera una ruta de archivo temporal para tests de escritura. Usa el fixture built-in `tmp_path` de pytest para garantizar aislamiento entre tests. La ruta apunta a `resultado_test.json` dentro del directorio temporal único de cada test.

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `tmp_path` | `pathlib.Path` | Directorio temporal único por test (provisto por pytest) |

### Retorno

| Tipo | Descripción |
|------|-------------|
| `str` | Ruta completa como string: `<tmp_path>/resultado_test.json` |

### Uso típico

```python
def test_algo(temp_output):
    guardar_json({"key": "val"}, temp_output)
    assert os.path.exists(temp_output)
```