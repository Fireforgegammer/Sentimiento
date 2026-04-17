---

# ⚙️ `cicd.md` — GitHub Actions CI/CD

---

## Descripción General

Pipeline de integración continua definido en `.github/workflows/python-tests.yml`. Se ejecuta automáticamente en cada `push` y `pull_request`.

---

## Diagrama del Pipeline

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
  actions/setup-python@v4
    python-version: '3.10'
        │
        ▼
  pip install --upgrade pip
  pip install pytest pytest-cov pytesseract pillow
        │
        ▼
  sudo apt-get install tesseract-ocr tesseract-ocr-spa
        │
        ▼
  pytest --cov=sentimiento tests/
```

