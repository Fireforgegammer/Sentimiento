# ⌨️ `main.py` — Punto de Entrada CLI

🌐 [English](../en/main.md) · [Português](../pt/main.md) · [← Índice](INDEX.md)

---

## Descripción General

Interfaz de línea de comandos (CLI) del sistema. Ofrece dos modos de operación: análisis manual de un texto introducido por el usuario, y análisis por lotes del archivo `textos_a_analizar.txt`.

---

## Diagrama de Flujo General

```
python main.py
      │
      ▼
Menú de opciones
  1. Analizar un texto manualmente
  2. Analizar archivo 'textos_a_analizar.txt'
      │
      ├── opción "1" ──► analizar_texto_manual()
      │
      ├── opción "2" ──► analizar_archivo_lote()
      │
      └── otro ──► "Opción no válida."
```

---

## Función: `analizar_texto_manual`

### Signatura

```python
def analizar_texto_manual() -> None
```

### Descripción

Solicita un texto al usuario por stdin, ejecuta el análisis avanzado, imprime el resultado en consola formateado como JSON y lo guarda en `resultados/analisis_manual.json`.

### Diagrama de Flujo

```
input("Escribe el texto a analizar: ")
      │
      ├── ¿texto vacío? → return
      │
      ▼
analizar_sentimiento_avanzado(texto)
      │
      ▼
print(json.dumps(resultado, indent=2, ensure_ascii=False))
      │
      ▼
guardar_json(resultado, "analisis_manual.json")
```

---

## Función: `analizar_archivo_lote`

### Signatura

```python
def analizar_archivo_lote() -> None
```

### Descripción

Lee el archivo `textos_a_analizar.txt` de la raíz del proyecto (una línea = un texto), lo analiza en lote con `analizar_sentimiento_multitexto`, guarda el resultado en `resultados/resultado_lote.json` e imprime un resumen en consola.

### Diagrama de Flujo

```
base_dir = os.path.dirname(os.path.abspath(__file__))
ruta = base_dir / "textos_a_analizar.txt"
      │
      ├── ¿No existe? → print(error) + return
      │
      ▼
lineas = [líneas no vacías del archivo]
      │
      ├── ¿Vacío? → print("El archivo está vacío.") + return
      │
      ▼
analizar_sentimiento_multitexto(lineas)
      │
      ▼
guardar_json(resultado, "resultado_lote.json")
      │
      ▼
print(f"Positivos: X, Negativos: Y")
```

### Formato del archivo `textos_a_analizar.txt`

```
Me encanta este producto, es fantástico.
El servicio fue terrible y tardaron mucho.
No está mal, cumple lo básico.
```

> Una línea por texto. Las líneas vacías se ignoran automáticamente.

---

## Función: `main`

### Signatura

```python
def main() -> None
```

### Descripción

Punto de entrada del CLI. Muestra el menú, lee la opción del usuario y delega en la función correspondiente.

---

## Dependencias

| Dependencia | Uso |
|-------------|-----|
| `os` | Resolución de rutas |
| `json` | Formateo de salida en consola |
| `sentimiento.niveles` | `analizar_sentimiento_avanzado` |
| `sentimiento.multitexto` | `analizar_sentimiento_multitexto` |
| `almacenamiento.guardar` | `guardar_json` |