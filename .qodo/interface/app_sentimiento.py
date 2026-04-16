import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

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

        self.setup_ui()
        self.ultimo_resultado = None

    def setup_ui(self):
        header = tk.Label(self.root, text="📝 ANÁLISIS DE SENTIMIENTO - LOCAL", font=("Segoe UI", 16, "bold"), bg="#f0f0f0")
        header.pack(anchor="w", padx=20, pady=(15, 10))

        input_label = tk.Label(self.root, text="Texto a analizar", font=("Segoe UI", 10), bg="#f0f0f0")
        input_label.pack(anchor="w", padx=20)
        
        self.text_input = tk.Text(self.root, height=6, font=("Segoe UI", 11), relief="solid", borderwidth=1)
        self.text_input.pack(fill="x", padx=20, pady=(0, 15))
        self.text_input.insert("1.0", "Escribe aquí...")

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

        leyenda_frame = tk.Frame(self.root, bg="#f0f0f0")
        leyenda_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(leyenda_frame, text="¿Qué significa la polaridad?", font=("Segoe UI", 9, "bold"), bg="#f0f0f0").pack(anchor="w")
        tk.Label(leyenda_frame, text="● POSITIVA (+0.00 a +1.00): El texto expresa emociones positivas", fg="green", bg="#f0f0f0").pack(anchor="w")
        tk.Label(leyenda_frame, text="● NEGATIVA (-1.00 a -0.00): El texto expresa emociones negativas", fg="red", bg="#f0f0f0").pack(anchor="w")
        tk.Label(leyenda_frame, text="○ NEUTRAL (0.00): El texto no muestra emociones fuertes", fg="gray", bg="#f0f0f0").pack(anchor="w")

        self.status_var = tk.BooleanVar(value=False)
        self.chk_status = tk.Checkbutton(self.root, text="Análisis completado y guardado automáticamente", 
                                         variable=self.status_var, state="disabled", bg="#f0f0f0")
        self.chk_status.pack(anchor="w", padx=20, pady=10)

    def ejecutar_analisis(self):
        texto = self.text_input.get("1.0", "end-1c").strip()
        if not texto:
            return

        self.btn_analizar.config(text="Procesando...", state="disabled")
        self.root.update()

        try:
            res_b = analizar_sentimiento_basico(texto)
            res_i = analizar_sentimiento_intermedio(texto)
            res_a = analizar_sentimiento_avanzado(texto)

            self.ultimo_resultado = res_a
            self.actualizar_tabla(res_b, res_i, res_a)
            
            guardar_json(res_a, f"auto_{datetime.now().strftime('%H%M%S')}.json")
            self.status_var.set(True)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        self.btn_analizar.config(text="🔍 ANALIZAR SENTIMIENTO", state="normal")

    def actualizar_tabla(self, b, i, a):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        sent_b = str(b.get("sentimiento", "")).upper()
        self.tree.insert("", "end", values=("Básico", sent_b, "-", "-"))

        sent_i = str(i.get("sentimiento", "")).upper()
        pol_i = i.get("polaridad", 0)
        int_i = str(i.get("intensidad", "")).upper()
        self.tree.insert("", "end", values=("Intermedio", sent_i, pol_i, int_i))

        sent_a = str(a.get("sentimiento_global", "")).upper()
        pol_a = a.get("polaridad", 0)
        self.tree.insert("", "end", values=("Avanzado", sent_a, pol_a, "-"))

    def limpiar(self):
        self.text_input.delete("1.0", "end")
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.status_var.set(False)
        self.ultimo_resultado = None

    def guardar_manual(self):
        if not self.ultimo_resultado:
            return
        
        archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if archivo:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(self.ultimo_resultado, f, indent=4, ensure_ascii=False)