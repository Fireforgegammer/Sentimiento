# 🚀 `main_interfaz.py` — Punto de Entrada GUI

🌐 [English](../en/main_interfaz.md) · [Português](../pt/main_interfaz.md) · [← Índice](INDEX.md)

---

## Descripción General

Lanzador de la interfaz gráfica. Inicializa el bucle de eventos TkinterDnD (necesario para soporte Drag & Drop), gestiona la visibilidad inicial de la ventana y arranca la aplicación `AppSentimiento`.

---

## Diagrama de Flujo

```
python main_interfaz.py
        │
        ▼
    main()
        │
        ▼
root = TkinterDnD.Tk()          ← ventana DnD-compatible
        │
        ▼
root.withdraw()                 ← ocultar mientras carga
        │
        ▼
root.after(0, root.deiconify)   ← mostrar tras primer ciclo
        │
        ▼
app = AppSentimiento(root)      ← construir la UI
        │
        ▼
root.mainloop()                 ← bucle de eventos
```

---

## Función: `main`

### Signatura

```python
def main() -> None
```

### Descripción

Crea la ventana raíz con soporte DnD, oculta la ventana momentáneamente (evita el parpadeo inicial en algunos sistemas operativos), programa su aparición en el siguiente ciclo de eventos, instancia la aplicación y arranca el bucle principal.

### Por qué `withdraw` + `deiconify`

Algunos sistemas operativos muestran la ventana en su tamaño por defecto antes de que Tkinter aplique la geometría configurada en `AppSentimiento`, produciendo un parpadeo visual. Esta técnica elimina ese artefacto.

---

## Dependencias

| Dependencia | Uso |
|-------------|-----|
| `os`, `sys` | Importados (disponibles para futuras extensiones) |
| `tkinterdnd2.TkinterDnD` | Ventana raíz con soporte Drag & Drop |
| `interface.app_sentimiento.AppSentimiento` | Clase principal de la GUI |