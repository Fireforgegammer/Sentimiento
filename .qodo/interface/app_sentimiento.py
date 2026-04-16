import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from tkinterdnd2 import DND_FILES, DND_TEXT

from sentimiento.niveles import (
    analizar_sentimiento_basico,
    analizar_sentimiento_intermedio,
    analizar_sentimiento_avanzado
)
from almacenamiento.guardar import guardar_json

class AppSentimiento:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Sentimiento - Local")
        self.root.geometry("950x750")
        self.root.configure(bg="#f0f0f0")

        self.placeholder = "Escribe, pega o arrastra texto o un archivo aquí..."
        self.setup_ui()
        self.ultimo_resultado = None
        
        self.root.bind("<Key>", self.capturar_teclado_global)

    def setup_ui(self):
        header = tk.Label(self.root, text="📝 ANÁLISIS DE SENTIMIENTO - LOCAL", font=("Segoe UI", 16, "bold"), bg="#f0f0f0")
        header.pack(anchor="w", padx=20, pady=(15, 10))

        self.text_input = tk.Text(self.root, height=6, font=("Segoe UI", 11), relief="solid", borderwidth=1, fg="grey")
        self.text_input.pack(fill="x", padx=20, pady=(0, 15))
        
        self.text_input.drop_target_register(DND_FILES, DND_TEXT)
        self.text_input.dnd_bind('<<Drop>>', self.procesar_drop_general)
        
        self.text_input.insert("1.0", self.placeholder)
        self.text_input.bind("<FocusIn>", self.limpiar_placeholder)
        self.text_input.bind("<FocusOut>", self.poner_placeholder)

        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(anchor="w", padx=20, pady=(0, 15))

        self.btn_analizar = tk.Button(btn_frame, text="🔍 ANALIZAR SENTIMIENTO", command=self.ejecutar_analisis, bg="#e1e1e1", padx=10)
        self.btn_analizar.pack(side="left", padx=(0, 10))

        btn_limpiar = tk.Button(btn_frame, text="🧹 LIMPIAR", command=self.limpiar, bg="#e1e1e1", padx=10)
        btn_limpiar.pack(side="left", padx=10)

        btn_guardar = tk.Button(btn_frame, text="💾 GUARDAR", command=self.guardar_manual, bg="#e1e1e1", padx=10)
        btn_guardar.pack(side="left", padx=10)

        self.tab_control = ttk.Notebook(self.root)
        self.tab_niveles = tk.Frame(self.tab_control, bg="white")
        self.tab_detallado = tk.Frame(self.tab_control, bg="white")
        self.tab_justificacion = tk.Frame(self.tab_control, bg="white")
        self.tab_historial = tk.Frame(self.tab_control, bg="white")

        self.tab_control.add(self.tab_niveles, text="Resultados por Nivel")
        self.tab_control.add(self.tab_detallado, text="Análisis Detallado")
        self.tab_control.add(self.tab_justificacion, text="Justificación & Recomendación")
        self.tab_control.add(self.tab_historial, text="Historial")
        self.tab_control.pack(expand=1, fill="both", padx=20, pady=5)

        cols = ("Nivel", "Sentimiento", "Polaridad", "Intensidad")
        self.tree = ttk.Treeview(self.tab_niveles, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(expand=1, fill="both", padx=10, pady=10)

        self.txt_detallado = tk.Text(self.tab_detallado, font=("Consolas", 10), padx=10, pady=10)
        self.txt_detallado.pack(expand=1, fill="both")

        self.txt_justificacion = tk.Text(self.tab_justificacion, font=("Segoe UI", 11), padx=10, pady=10)
        self.txt_justificacion.pack(expand=1, fill="both")

        self.tree_historial = ttk.Treeview(self.tab_historial, columns=("Hora", "Texto", "Global"), show="headings")
        for col in ("Hora", "Texto", "Global"):
            self.tree_historial.heading(col, text=col)
        self.tree_historial.pack(expand=1, fill="both", padx=10, pady=10)

        self.status_var = tk.BooleanVar(value=False)
        self.chk_status = tk.Checkbutton(self.root, text="Auto-guardado OK", variable=self.status_var, state="disabled", bg="#f0f0f0")
        self.chk_status.pack(anchor="w", padx=20, pady=10)

    def procesar_drop_general(self, event):
        data = event.data
        if data.startswith('{') and data.endswith('}'):
            archivo = data.strip('{}')
            if os.path.exists(archivo):
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                except:
                    contenido = data
            else:
                contenido = data
        else:
            contenido = data

        self.text_input.delete("1.0", "end")
        self.text_input.config(fg="black")
        self.text_input.insert("1.0", contenido)

    def capturar_teclado_global(self, event):
        if self.root.focus_get() != self.text_input:
            if event.char and event.char.isprintable():
                self.text_input.focus_set()
                if self.text_input.get("1.0", "end-1c") == self.placeholder:
                    self.text_input.delete("1.0", "end")
                    self.text_input.config(fg="black")
                self.text_input.insert("end", event.char)
                return "break"

    def limpiar_placeholder(self, event):
        if self.text_input.get("1.0", "end-1c") == self.placeholder:
            self.text_input.delete("1.0", "end")
            self.text_input.config(fg="black")

    def poner_placeholder(self, event):
        if not self.text_input.get("1.0", "end-1c").strip():
            self.text_input.delete("1.0", "end")
            self.text_input.insert("1.0", self.placeholder)
            self.text_input.config(fg="grey")

    def formatear_valor(self, valor, es_intensidad=False):
        try:
            v = float(valor)
            if es_intensidad:
                if v < 0.3: return "BAJA"
                if v < 0.7: return "MEDIA"
                return "ALTA"
            else:
                if v <= -0.6: return "MUY NEGATIVO"
                if v < -0.1: return "ALGO NEGATIVO"
                if -0.1 <= v <= 0.1: return "NEUTRAL"
                if v < 0.6: return "ALGO POSITIVO"
                return "MUY POSITIVO"
        except:
            return "NEUTRAL" if not es_intensidad else "BAJA"

    def ejecutar_analisis(self):
        texto = self.text_input.get("1.0", "end-1c").strip()
        if not texto or texto == self.placeholder: return

        self.btn_analizar.config(text="Procesando...", state="disabled")
        self.root.update()

        try:
            res_b = analizar_sentimiento_basico(texto)
            res_i = analizar_sentimiento_intermedio(texto)
            res_a = analizar_sentimiento_avanzado(texto)

            self.ultimo_resultado = res_a
            self.actualizar_vistas(res_b, res_i, res_a, texto)
            
            guardar_json(res_a, f"auto_{datetime.now().strftime('%H%M%S')}.json")
            self.status_var.set(True)
        except Exception as e:
            messagebox.showerror("Error", f"Fallo en el análisis: {e}")
        
        self.btn_analizar.config(text="🔍 ANALIZAR SENTIMIENTO", state="normal")

    def actualizar_vistas(self, b, i, a, texto_original):
        for row in self.tree.get_children(): self.tree.delete(row)
        
        def to_up(val): 
            return str(val).upper() if val is not None and str(val).strip() != "" else "NEUTRAL"

        self.tree.insert("", "end", values=("Básico", to_up(b.get("sentimiento")), self.formatear_valor(b.get("polaridad")), self.formatear_valor(b.get("intensidad"), True)))
        self.tree.insert("", "end", values=("Intermedio", to_up(i.get("sentimiento")), self.formatear_valor(i.get("polaridad")), self.formatear_valor(i.get("intensidad"), True)))
        self.tree.insert("", "end", values=("Avanzado", to_up(a.get("sentimiento_global")), self.formatear_valor(a.get("polaridad")), self.formatear_valor(a.get("intensidad"), True)))

        self.txt_detallado.delete("1.0", "end")
        self.txt_detallado.insert("1.0", json.dumps(a, indent=4, ensure_ascii=False))

        self.txt_justificacion.delete("1.0", "end")
        contenido = f"JUSTIFICACIÓN:\n{a.get('justificacion', 'No disponible')}\n\nRECOMENDACIÓN:\n{a.get('recomendacion', 'No disponible')}"
        self.txt_justificacion.insert("1.0", contenido)

        self.tree_historial.insert("", 0, values=(datetime.now().strftime("%H:%M:%S"), texto_original[:45]+"...", to_up(a.get("sentimiento_global"))))

    def limpiar(self):
        self.text_input.delete("1.0", "end")
        self.text_input.config(fg="grey")
        self.text_input.insert("1.0", self.placeholder)
        self.root.focus_set()
        for row in self.tree.get_children(): self.tree.delete(row)
        self.txt_detallado.delete("1.0", "end")
        self.txt_justificacion.delete("1.0", "end")
        self.status_var.set(False)
        self.ultimo_resultado = None

    def guardar_manual(self):
        if not self.ultimo_resultado: return
        archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if archivo:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(self.ultimo_resultado, f, indent=4, ensure_ascii=False)