# 📚 SENTIMIENTO — Documentación / Documentation / Documentação

> Sistema de Análisis de Sentimiento Multimodal con IA · Multimodal Sentiment Analysis System with AI · Sistema de Análise de Sentimento Multimodal com IA

---

## 🌐 Selecciona tu idioma / Select your language / Selecione seu idioma

| Idioma | Language | Língua | Enlace |
|--------|----------|--------|--------|
|  Español | — | — | [**→ Ver documentación en Español**](docs/es/INDEX.md) |
|  — | English | — | [**→ View documentation in English**](docs/en/INDEX.md) |
|  — | — | Português | [**→ Ver documentação em Português**](docs/pt/INDEX.md) |

---

## 🗂️ Estructura del proyecto / Project Structure / Estrutura do Projeto

```
SENTIMIENTO/
├── sentimiento/          # Core de análisis de IA
│   ├── niveles.py        # Analizadores básico, intermedio, avanzado
│   ├── cliente.py        # Cliente Groq API
│   ├── multitexto.py     # Análisis por lotes
│   └── analizador.py     # (Reservado)
├── almacenamiento/       # Persistencia de datos
│   ├── guardar.py        # Escritura JSON
│   └── leer.py           # Lectura JSON
├── interface/            # GUI Tkinter
│   └── app_sentimiento.py
├── tests/                # Suite de pruebas
│   ├── conftest.py       # Fixtures globales
│   ├── e2e/              # Pruebas end-to-end
│   ├── integration/      # Pruebas de integración
│   └── unit/             # Pruebas unitarias
├── .github/workflows/    # CI/CD
│   └── python-tests.yml
├── main.py               # CLI Entry point
└── main_interfaz.py      # GUI Entry point
```