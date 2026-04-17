# 🖥️ `interface/app_sentimiento.py`

[Español](../../es/interface/app_sentimiento.md) · [English](../../en/interface/app_sentimiento.md) · 🇧🇷 Português · [← Índice](../INDEX.md)

---

## Visão Geral

Interface gráfica principal do sistema. Implementa uma aplicação Tkinter **multimodal** que aceita texto por digitação direta, colagem da área de transferência (incluindo imagens via OCR), e arrastar e soltar arquivos de texto ou imagem. Exibe os resultados em abas organizadas por nível de análise.

---

## Diagrama de Arquitetura da Classe

```
AppSentimiento
├── __init__(root)
│   ├── Configurar janela root
│   ├── setup_ui()
│   └── Bindings globais (teclado, Ctrl+V)
│
├── ENTRADA DE DADOS
│   ├── pegar_desde_portapapeles()   ← Ctrl+V + OCR
│   ├── procesar_drop_general()      ← Drag & Drop
│   ├── capturar_teclado_global()    ← Teclas fora do widget
│   └── insertar_texto_limpio()      ← Helper comum
│
├── GESTÃO DE PLACEHOLDER
│   ├── limpiar_placeholder()        ← FocusIn
│   └── poner_placeholder()          ← FocusOut
│
├── ANÁLISE
│   ├── ejecutar_analisis()          ← Botão principal
│   ├── formatear_valor()            ← Numérico → rótulo
│   └── actualizar_vistas()          ← Atualiza todas as abas
│
└── UTILITÁRIOS
    └── limpiar()                    ← Reset completo
```

---

## Classe: `AppSentimiento`

### Atributos de Instância

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `root` | `tk.Tk` | Janela raiz da aplicação |
| `placeholder` | `str` | Texto de ajuda exibido na área de entrada quando vazia |
| `ultimo_resultado` | `dict \| None` | Último resultado de análise (reservado para uso futuro) |
| `text_input` | `tk.Text` | Widget principal de entrada de texto |
| `btn_analizar` | `tk.Button` | Botão de análise (desabilitado durante o processamento) |
| `tab_control` | `ttk.Notebook` | Contêiner de abas de resultados |
| `tree` | `ttk.Treeview` | Tabela de resultados por nível |
| `txt_detallado` | `tk.Text` | JSON completo da análise avançada |
| `txt_justificacion` | `tk.Text` | Justificativa e recomendação legíveis |
| `tree_historial` | `ttk.Treeview` | Registro de análises anteriores na sessão |

---

## Método: `pegar_desde_portapapeles`

### Diagrama de Fluxo

```
Ctrl+V
  │
  ▼
ImageGrab.grabclipboard()
  │
  ├── isinstance(img, Image.Image)?
  │       │ Sim
  │       ▼
  │   pytesseract.image_to_string(img, lang='spa')
  │       │
  │       ▼
  │   insertar_texto_limpio(texto_extraído)
  │       │
  │       ▼
  │   return "break"  ← evita que Tkinter cole o raw
  │
  └── Não / exceção → pass (Tkinter lida com texto normal)
```

---

## Método: `procesar_drop_general`

### Diagrama de Fluxo

```
event.data
    │
    ▼
Começa com '{' e termina com '}'?
    │
    ├── Sim → caminho = data.strip('{}')
    │         ├── Existe? → É imagem? → OCR pytesseract
    │         │           → É texto? → Ler UTF-8
    │         └── Não existe → conteúdo = data
    │
    └── Não → conteúdo = data (texto arrastado diretamente)
              │
              ▼
    insertar_texto_limpio(conteúdo)
```

### Formatos de Arquivo Suportados

| Tipo | Extensões | Processamento |
|------|-----------|---------------|
| Imagem | `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff` | OCR via Tesseract (idioma: espanhol) |
| Texto | Qualquer outra extensão | Leitura direta UTF-8 |

---

## Método: `formatear_valor`

### Tabelas de Conversão

**Polaridade** (`es_intensidad=False`):

| Intervalo | Rótulo |
|-----------|--------|
| `v ≤ -0.6` | `MUY NEGATIVO` |
| `-0.6 < v < -0.1` | `ALGO NEGATIVO` |
| `-0.1 ≤ v ≤ 0.1` | `NEUTRAL` |
| `0.1 < v < 0.6` | `ALGO POSITIVO` |
| `v ≥ 0.6` | `MUY POSITIVO` |

**Intensidade** (`es_intensidad=True`):

| Intervalo | Rótulo |
|-----------|--------|
| `v < 0.3` | `BAJA` |
| `0.3 ≤ v < 0.7` | `MEDIA` |
| `v ≥ 0.7` | `ALTA` |

---

## Método: `ejecutar_analisis`

### Diagrama de Fluxo

```
Clique em "🔍 ANALISAR SENTIMENTO"
    │
    ▼
texto = text_input.get("1.0", "end-1c").strip()
    │
    ├── vazio ou placeholder? → return
    │
    ▼
btn_analizar → desabilitado + "Processando..."
    │
    ▼
res_b = analizar_sentimiento_basico(texto)
res_i = analizar_sentimiento_intermedio(texto)
res_a = analizar_sentimiento_avanzado(texto)
    │
    ├── Exceção → messagebox.showerror(...)
    │
    ▼
actualizar_vistas(res_b, res_i, res_a, texto)
    │
    ▼
btn_analizar → habilitado + rótulo original
```

---

## Método: `actualizar_vistas`

### Abas Atualizadas

| Aba | Conteúdo |
|-----|----------|
| **Resultados por Nível** | Tabela com Básico, Intermediário, Avançado |
| **Análise Detalhada** | JSON completo do nível avançado |
| **Justificativa & Recomendação** | Texto legível de justificativa e recomendação |
| **Histórico** | Nova entrada com hora, texto truncado e sentimento global |

---

## Dependências

| Dependência | Uso |
|-------------|-----|
| `tkinter` / `ttk` | Widgets de interface gráfica |
| `tkinterdnd2` | Suporte Drag & Drop |
| `PIL.Image`, `PIL.ImageGrab` | Captura e manipulação de imagens |
| `pytesseract` | OCR para extração de texto de imagens |
| `sentimiento.niveles` | Os três analisadores de sentimento |
| `almacenamiento.guardar` | Persistência de resultados |
| `json`, `os`, `datetime` | Utilitários padrão |