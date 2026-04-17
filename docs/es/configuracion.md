## Configuración

| Campo | Valor |
|-------|-------|
| Runner | `ubuntu-latest` |
| Python | `3.10` |
| Trigger | `push`, `pull_request` |
| Cobertura | Módulo `sentimiento` |
| Tesseract | Instalado en la VM con idioma español |

> ⚠️ La variable `GROQ_API_KEY` debe configurarse como **GitHub Secret** para que los tests E2E funcionen en CI.