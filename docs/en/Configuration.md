## Configuration

| Field | Value |
|-------|-------|
| Runner | `ubuntu-latest` |
| Python | `3.10` |
| Trigger | `push`, `pull_request` |
| Coverage | `sentimiento` module |
| Tesseract | Installed in VM with Spanish language pack |

> ⚠️ The `GROQ_API_KEY` variable must be configured as a **GitHub Secret** for E2E tests to work in CI.