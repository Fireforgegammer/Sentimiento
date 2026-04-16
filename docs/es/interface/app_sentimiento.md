# 🖥️ `interface/app_sentimiento.py`

🌐 [English](../../en/interface/app_sentimiento.md) · [Português](../../pt/interface/app_sentimiento.md) · [← Índice](../INDEX.md)

---

## Descripción General

Interfaz gráfica principal del sistema. Implementa una aplicación Tkinter **multimodal** que acepta texto por escritura directa, pegado desde portapapeles (incluyendo imágenes via OCR), y arrastrar y soltar archivos de texto o imagen. Muestra los resultados en pestañas organizadas por nivel de análisis.

---

## Diagrama de Arquitectura de la Clase

```
AppSentimiento
├── __init__(root)
│   ├── Configura ventana root
│   ├── setup_ui()
│   └── Bindings globales (teclado, Ctrl+V)
│
├── ENTRADA DE DATOS
│   ├── pegar_desde_portapapeles()   ← Ctrl+V + OCR
│   ├── procesar_drop_general()      ← Drag & Drop
│   ├── capturar_teclado_global()    ← Teclas fuera del widget
│   └── insertar_texto_limpio()      ← Helper común
│
├── GESTIÓN DE PLACEHOLDER
│   ├── limpiar_placeholder()        ← FocusIn
│   └── poner_placeholder()          ← FocusOut
│
├── ANÁLISIS
│   ├── ejecutar_analisis()          ← Botón principal
│   ├── formatear_valor()            ← Helper numérico → texto
│   └── actualizar_vistas()          ← Actualiza todas las pestañas
│
└── UTILIDADES
    └── limpiar()                    ← Reset completo
```

---

## Clase: `AppSentimiento`

### Signatura

```python
class AppSentimiento:
    def __init__(self, root: tk.Tk) -> None
```

### Descripción

Clase principal de la GUI. Recibe la ventana raíz de Tkinter/TkinterDnD2 y construye toda la interfaz, registra los manejadores de eventos y gestiona el ciclo de vida de la aplicación.

### Atributos de instancia

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `root` | `tk.Tk` | Ventana raíz de la aplicación |
| `placeholder` | `str` | Texto de ayuda mostrado en el área de entrada cuando está vacía |
| `ultimo_resultado` | `dict \| None` | Último resultado de análisis (reservado para uso futuro) |
| `text_input` | `tk.Text` | Widget principal de entrada de texto |
| `btn_analizar` | `tk.Button` | Botón de análisis (se deshabilita durante el proceso) |
| `tab_control` | `ttk.Notebook` | Contenedor de pestañas de resultados |
| `tree` | `ttk.Treeview` | Tabla de resultados por nivel |
| `txt_detallado` | `tk.Text` | JSON completo del análisis avanzado |
| `txt_justificacion` | `tk.Text` | Justificación y recomendación legibles |
| `tree_historial` | `ttk.Treeview` | Registro de análisis previos en la sesión |

---

## Método: `setup_ui`

### Signatura

```python
def setup_ui(self) -> None
```

### Descripción

Construye y organiza todos los elementos visuales de la interfaz: cabecera, área de texto con soporte DnD, botones de acción, y sistema de pestañas con sus respectivos widgets.

### Estructura visual

```
┌─────────────────────────────────────────────────────┐
│  📝 ANÁLISIS DE SENTIMIENTO - MULTIMODAL             │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐    │
│  │  [Área de texto — 6 líneas — DnD activo]    │    │
│  └─────────────────────────────────────────────┘    │
│  [🔍 ANALIZAR SENTIMIENTO]  [🧹 LIMPIAR]            │
├─────────────────────────────────────────────────────┤
│  ┌──────────┬────────────┬─────────────┬─────────┐  │
│  │ Niveles  │ Detallado  │ Justific.   │Historial│  │
│  ├──────────┴────────────┴─────────────┴─────────┤  │
│  │                  [Contenido]                   │  │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## Método: `pegar_desde_portapapeles`

### Signatura

```python
def pegar_desde_portapapeles(self, event=None) -> str | None
```

### Descripción

Manejador del evento `Ctrl+V`. Intenta obtener una **imagen** del portapapeles (captura de pantalla, imagen copiada) y extraer texto mediante OCR con Tesseract. Si el portapapeles contiene texto plano, Tkinter lo gestiona de forma nativa.

### Diagrama de Flujo

```
Ctrl+V
  │
  ▼
ImageGrab.grabclipboard()
  │
  ├── isinstance(img, Image.Image)?
  │       │ Sí
  │       ▼
  │   pytesseract.image_to_string(img, lang='spa')
  │       │
  │       ▼
  │   insertar_texto_limpio(texto_extraido)
  │       │
  │       ▼
  │   return "break"  ← evita que Tkinter pegue el raw
  │
  └── No / excepción → pass (Tkinter maneja texto normal)
```

---

## Método: `procesar_drop_general`

### Signatura

```python
def procesar_drop_general(self, event) -> None
```

### Descripción

Manejador de eventos Drag & Drop. Determina si el objeto arrastrado es una **ruta de archivo** (entre llaves `{...}`) o **texto directo**, y actúa en consecuencia: aplica OCR a imágenes, lee el contenido de archivos de texto, o inserta el texto directamente.

### Diagrama de Flujo

```
event.data
    │
    ▼
¿Empieza con '{' y termina con '}'?
    │
    ├── Sí → ruta = data.strip('{}')
    │         │
    │         ▼
    │    ¿os.path.exists(ruta)?
    │         │
    │         ├── Sí → extensión en [.png, .jpg, .jpeg, .bmp, .tiff]?
    │         │         │
    │         │         ├── Sí → OCR con pytesseract
    │         │         │
    │         │         └── No → leer como texto UTF-8
    │         │
    │         └── No → contenido = data
    │
    └── No → contenido = data (texto arrastrado directamente)
              │
              ▼
    insertar_texto_limpio(contenido)
```

### Formatos de archivo soportados

| Tipo | Extensiones | Procesamiento |
|------|-------------|---------------|
| Imagen | `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff` | OCR via Tesseract (idioma: español) |
| Texto | Cualquier otra extensión | Lectura directa UTF-8 |

---

## Método: `insertar_texto_limpio`

### Signatura

```python
def insertar_texto_limpio(self, texto: str) -> None
```

### Descripción

Helper centralizado para insertar texto en el widget de entrada, reemplazando el placeholder si está presente y reseteando el color a negro.

---

## Método: `capturar_teclado_global`

### Signatura

```python
def capturar_teclado_global(self, event) -> str | None
```

### Descripción

Permite escribir directamente en cualquier parte de la ventana sin necesidad de hacer clic en el área de texto primero. Redirige los caracteres imprimibles al `text_input` automáticamente.

---

## Métodos: `limpiar_placeholder` / `poner_placeholder`

Gestionan la apariencia del placeholder de forma estándar: lo eliminan al enfocar y lo restauran al desenfocar si el campo queda vacío.

---

## Método: `formatear_valor`

### Signatura

```python
def formatear_valor(self, valor, es_intensidad: bool = False) -> str
```

### Descripción

Convierte valores numéricos flotantes a etiquetas de texto legibles para humanos.

### Tabla de conversión

**Polaridad** (`es_intensidad=False`):

| Rango | Etiqueta |
|-------|----------|
| `v ≤ -0.6` | `MUY NEGATIVO` |
| `-0.6 < v < -0.1` | `ALGO NEGATIVO` |
| `-0.1 ≤ v ≤ 0.1` | `NEUTRAL` |
| `0.1 < v < 0.6` | `ALGO POSITIVO` |
| `v ≥ 0.6` | `MUY POSITIVO` |

**Intensidad** (`es_intensidad=True`):

| Rango | Etiqueta |
|-------|----------|
| `v < 0.3` | `BAJA` |
| `0.3 ≤ v < 0.7` | `MEDIA` |
| `v ≥ 0.7` | `ALTA` |

---

## Método: `ejecutar_analisis`

### Signatura

```python
def ejecutar_analisis(self) -> None
```

### Descripción

Orquesta el análisis completo: obtiene el texto del widget, deshabilita el botón mientras procesa, invoca los tres niveles de análisis en secuencia y actualiza la interfaz. Maneja errores con `messagebox`.

### Diagrama de Flujo

```
Clic en "🔍 ANALIZAR SENTIMIENTO"
    │
    ▼
texto = text_input.get("1.0", "end-1c").strip()
    │
    ├── ¿vacío o es placeholder? → return
    │
    ▼
btn_analizar.config(text="Procesando...", state="disabled")
    │
    ▼
res_b = analizar_sentimiento_basico(texto)
res_i = analizar_sentimiento_intermedio(texto)
res_a = analizar_sentimiento_avanzado(texto)
    │
    ├── Exception → messagebox.showerror(...)
    │
    ▼
actualizar_vistas(res_b, res_i, res_a, texto)
    │
    ▼
btn_analizar.config(text="🔍 ANALIZAR...", state="normal")
```

---

## Método: `actualizar_vistas`

### Signatura

```python
def actualizar_vistas(self, b: dict, i: dict, a: dict, texto_original: str) -> None
```

### Descripción

Actualiza simultáneamente las cuatro pestañas de resultados con los datos de los tres niveles de análisis.

### Pestañas actualizadas

| Pestaña | Contenido |
|---------|-----------|
| **Resultados por Nivel** | Tabla con Básico, Intermedio, Avanzado |
| **Análisis Detallado** | JSON completo del nivel avanzado |
| **Justificación & Recomendación** | Texto legible de justificación y recomendación |
| **Historial** | Nueva entrada con hora, texto truncado y sentimiento global |

---

## Método: `limpiar`

### Signatura

```python
def limpiar(self) -> None
```

### Descripción

Resetea completamente la interfaz: vacía el área de texto (restaurando el placeholder), limpia todas las tablas y los campos de texto de las pestañas.

---

## Dependencias

| Dependencia | Uso |
|-------------|-----|
| `tkinter` / `ttk` | Widgets de interfaz gráfica |
| `tkinterdnd2` | Soporte Drag & Drop |
| `PIL.Image`, `PIL.ImageGrab` | Captura y manejo de imágenes |
| `pytesseract` | OCR para extracción de texto de imágenes |
| `sentimiento.niveles` | Los tres analizadores de sentimiento |
| `almacenamiento.guardar` | Persistencia de resultados |
| `json`, `os`, `datetime` | Utilidades estándar |