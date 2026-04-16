---

# 🧩 `tests/unit/test_niveles.py` — Tests Unitarios

---

## Descripción General

Pruebas unitarias del analizador avanzado para casos límite: texto vacío, texto muy positivo y texto con caracteres especiales.

---

## Test: `test_sentimiento_texto_vacio`

### Descripción

Verifica que el sistema maneja texto vacío sin lanzar excepciones y devuelve `"neutral"` como sentimiento global.

```python
res = analizar_sentimiento_avanzado("")
assert res["sentimiento_global"] == "neutral"
```

---

## Test: `test_sentimiento_muy_positivo`

### Descripción

Verifica que texto con carga emocional muy alta produce una polaridad superior a `0.5`.

```python
res = analizar_sentimiento_avanzado("¡Esto es absolutamente increíble y maravilloso!")
assert res["polaridad"] > 0.5
```

---

## Test: `test_sentimiento_caracteres_especiales`

### Descripción

Verifica que el sistema no se rompe ante entrada de caracteres especiales y devuelve un dict con la clave `"sentimiento_global"`.

```python
res = analizar_sentimiento_avanzado("!!! @#$% ^&*")
assert "sentimiento_global" in res
```
