---

# 🔬 `tests/e2e/test_app_folw.py` — Tests End-to-End

---

## Descripción General

Pruebas de flujo completo que verifican la coherencia del sistema desde la entrada de texto hasta la salida de los analizadores. No mockean la API: realizan llamadas reales a Groq.

---

## Test: `test_flujo_completo_analisis`

### Descripción

Verifica que un texto con sentimiento claramente negativo sea clasificado como `"negativo"` en el nivel básico, que la polaridad avanzada sea negativa (`< 0`) y que el campo `justificacion` exista y tenga contenido.

### Texto de prueba

```
"No me gusta nada como funciona este servicio, es horrible."
```

### Aserciones

```python
assert res_b["sentimiento"] == "negativo"
assert res_a["polaridad"] < 0
assert "justificacion" in res_a
assert len(res_a["justificacion"]) > 0
```

---

## Test: `test_consistencia_entre_niveles`

### Descripción

Verifica que el nivel básico y el nivel avanzado coincidan en la clasificación general del sentimiento para un texto positivo. Garantiza coherencia entre analizadores.

### Texto de prueba

```
"Excelente trabajo equipo."
```

### Aserciones

```python
assert res_b["sentimiento"].lower() == res_a["sentimiento_global"].lower()
```

---

## Test: `test_analisis_neutral_limpio`

### Descripción

Verifica el comportamiento del sistema ante texto mínimo sin carga emocional. El análisis avanzado debe clasificarlo como `"NEUTRAL"` con polaridad cero.

### Texto de prueba

```
"hola"
```

### Aserciones

```python
assert res_a["sentimiento_global"].upper() == "NEUTRAL"
assert res_a["polaridad"] == 0
```