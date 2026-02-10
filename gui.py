import customtkinter as ctk
import threading
from cbrkit.retrieval import build, apply_query
from service import CasoCRUD

# Configuración visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Para una función de similitud más simple basada en coincidencias
def similitud_descripcion(caso_desc, query_desc):
    """Calcula similitud básica por palabras en común"""
    caso_words = set(caso_desc.lower().split())
    query_words = set(query_desc.lower().split())
    
    if not query_words:
        return 0.0
    
    # Palabras en común
    comunes = caso_words.intersection(query_words)
    return len(comunes) / len(query_words)

class HW_SW_AI_App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🤖 HW/SW AI - Asistente de Soporte Técnico")
        self.geometry("700x600")
        self.resizable(False, False)

        self.top3 = []
        self.caso_elegido = None

        self.build_ui()

    def build_ui(self):
        self.label_bienvenida = ctk.CTkLabel(self, text="👋 ¡Hola! Cuéntame qué problema tienes con tu PC.", font=("Arial", 16))
        self.label_bienvenida.pack(pady=20)

        self.text_input = ctk.CTkTextbox(self, height=80, width=600)
        self.text_input.pack(pady=10)

        # Frame para contener el botón y el selector
        self.frame_controles = ctk.CTkFrame(self)
        self.frame_controles.pack(pady=10)

        self.dd_categoria = ctk.CTkOptionMenu(self.frame_controles, values=["General", "Hardware", "Software", "Redes"], width=150)
        self.dd_categoria.pack(side="left", padx=10)

        self.btn_enviar = ctk.CTkButton(self.frame_controles, text="Enviar", command=self.iniciar_busqueda)
        self.btn_enviar.pack(side="right", padx=10)

        self.frame_resultados = ctk.CTkScrollableFrame(self, width=650, height=250)
        self.frame_resultados.pack_forget()
        self.frame_resultados.bind("<Enter>", self._bind_mousewheel)
        self.frame_resultados.bind("<Leave>", self._unbind_mousewheel)

        self.frame_solucion = ctk.CTkFrame(self)
        self.frame_solucion.pack_forget()

        self.text_solucion = ctk.CTkTextbox(self.frame_solucion, height=100, width=600)
        self.text_solucion.pack(pady=10)

        self.btn_mejorar = ctk.CTkButton(self.frame_solucion, text="Quiero mejorar la solución", command=self.mostrar_mejora)
        self.btn_mejorar.pack(side="left", padx=10)

        self.btn_aceptar = ctk.CTkButton(self.frame_solucion, text="No valorar", command=self.reiniciar)
        self.btn_aceptar.pack(side="right", padx=10)

        self.frame_mejora = ctk.CTkFrame(self)
        self.frame_mejora.pack_forget()

        self.text_mejora = ctk.CTkTextbox(self.frame_mejora, height=100, width=600)
        self.text_mejora.pack(pady=10)

        self.btn_guardar_mejora = ctk.CTkButton(self.frame_mejora, text="Guardar y aprender", command=self.guardar_con_mejora)
        self.btn_guardar_mejora.pack(pady=10)

        self.label_exito = ctk.CTkLabel(self, text="✅ Caso guardado correctamente. ¿Quieres resolver otro problema?")
        self.btn_nuevo = ctk.CTkButton(self, text="Nuevo caso", command=self.reiniciar)

    def iniciar_busqueda(self):
        problema = self.text_input.get("1.0", "end").strip()
        categoria = self.dd_categoria.get()
        if not problema:
            return
    
        if not categoria:
            categoria = "General"

        self.label_bienvenida.configure(text="🔍 Buscando casos similares...")

        threading.Thread(target=self.buscar_casos, args=(problema, categoria)).start()

    def buscar_casos(self, problema, categoria="General"):
        consulta = {
            "descripcion": problema,
            "categoria": categoria
        }

        if categoria == "General":
            self.casebase = {
                caso['id']: caso for caso in CasoCRUD().leer_todos_casos()
            }
        else:
            self.casebase = {
                caso['id']: caso for caso in CasoCRUD().leer_todos_casos()
                if caso.get("categoria") == categoria
            }

        def sim_func(x, y):
            return similitud_descripcion(x["descripcion"], y["descripcion"])

        retriever = build(sim_func)
        resultado = apply_query(self.casebase, consulta, retriever)
        query_result = resultado.queries["default"]

        self.top3 = []
        for case_id in query_result.ranking:
            caso = query_result.casebase[case_id]
            sim = query_result.similarities[case_id]
            if sim > 0:
                self.top3.append((caso, sim))

        self.after(0, self.mostrar_resultados)

    def mostrar_resultados(self):
        self.label_bienvenida.configure(text="📊 Casos más parecidos encontrados:")
        self.frame_resultados.pack(pady=10, fill="x")

        # Limpiar resultados anteriores
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        for i, (caso, score) in enumerate(self.top3, start=1):
            resultado = ""
            v1 = caso["valoracion"]
            vTotal = caso["total_valoraciones"]
            if vTotal == 0:
                resultado = "Sin valoraciones"
            else:
                resultado = f"{(v1 / vTotal * 100):.2f}%"

            categoria = caso.get("categoria", "General")

            frame = ctk.CTkFrame(self.frame_resultados)
            frame.pack(fill="x", pady=5, padx=10)

            label = ctk.CTkLabel(
                frame,
                text=f"[{i}] {caso['descripcion']}\nSimilitud: {round(score * 100)}%\tValoración: {resultado}\t\tCategoría: {categoria}",
                justify="left",
                anchor="w"
            )
            label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

            btn = ctk.CTkButton(
                frame,
                text="Ver solución",
                command=lambda c=caso: self.mostrar_solucion(c)
            )
            btn.grid(row=0, column=1, sticky="e", padx=10)

            frame.grid_columnconfigure(0, weight=1)

        # Opción adicional
        frame_extra = ctk.CTkFrame(self.frame_resultados)
        frame_extra.pack(fill="x", pady=10, padx=10)

        label_extra = ctk.CTkLabel(
            frame_extra,
            text="Ninguno de estos casos resuelve mi problema",
            anchor="w"
        )
        label_extra.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        btn_extra = ctk.CTkButton(
            frame_extra,
            text="Proponer solución",
            command=self.proponer_solucion
        )
        btn_extra.grid(row=0, column=1, sticky="e", padx=10)

        frame_extra.grid_columnconfigure(0, weight=1)

        
    def proponer_solucion(self):
        self.frame_resultados.pack_forget()
        self.label_bienvenida.configure(text="✏️ Describe la solución que propones para tu problema:")
        self.frame_mejora.pack(pady=10)
        

    def mostrar_solucion(self, caso):
       
        self.caso_elegido = caso
        self.frame_resultados.pack_forget()
        self.label_bienvenida.configure(text="✅ Solución propuesta:")
        self.frame_solucion.pack(pady=10)
        self.text_solucion.insert("1.0", caso["solucion"])
        
        #Sistema de valoracion
        self.label_valoracion = ctk.CTkLabel(self.frame_solucion, text="¿Te ha servido esta solución?", anchor="w")
        self.btnLike = ctk.CTkButton(self.frame_solucion, text="👍", command=lambda: self.valorar_solucion(valoracion=1))
        self.btnDislike = ctk.CTkButton(self.frame_solucion, text="👎", command=lambda: self.valorar_solucion(valoracion=-1))
        
        self.label_valoracion.pack(pady=5)
        self.btnLike.pack(side="left", padx=10)
        self.btnDislike.pack(side="right", padx=10)
        

    def valorar_solucion(self,valoracion):
        crud = CasoCRUD()
        crud.valorar_caso(self.caso_elegido["id"], valoracion)
        self.label_valoracion.configure(text="¡Gracias por tu valoración!")
        self.btnLike.configure(state="disabled")
        self.btnDislike.configure(state="disabled")
        if valoracion == 1:
            self.btnLike.configure(fg_color = "green")
        else:
            self.btnDislike.configure(fg_color = "red")
        
    def mostrar_mejora(self):
        self.frame_solucion.pack_forget()
        self.label_bienvenida.configure(text="✏️ Introduce tu versión mejorada:")
        self.frame_mejora.pack(pady=10)

    def guardar_sin_cambios(self):
        self.guardar_caso(self.caso_elegido["solucion"])

    def guardar_con_mejora(self):
        mejora = self.text_mejora.get("1.0", "end").strip()
        categoria = self.dd_categoria.get()
        self.guardar_caso(mejora, categoria)

    def guardar_caso(self, solucion, categoria="General"):
        crud = CasoCRUD()
        problema = self.text_input.get("1.0", "end").strip()
        nuevo_id = crud.crear_caso(descripcion=problema, solucion=solucion, categoria=categoria)

        self.frame_mejora.pack_forget()
        self.frame_solucion.pack_forget()
        self.label_bienvenida.pack_forget()
        self.text_input.pack_forget()
        self.btn_enviar.pack_forget()
        self.dd_categoria.pack_forget()
        self.frame_controles.pack_forget()

        self.label_exito.pack(pady=20)
        self.btn_nuevo.pack(pady=10)

    def _on_mousewheel(self, event):
        if event.num == 4:      # Linux scroll up
            self.frame_resultados._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5:    # Linux scroll down
            self.frame_resultados._parent_canvas.yview_scroll(1, "units")
        else:                   # Windows / macOS
            self.frame_resultados._parent_canvas.yview_scroll(
                int(-1 * (event.delta / 120)), "units"
            )

    def _bind_mousewheel(self, event):
        self.frame_resultados.bind_all("<MouseWheel>", self._on_mousewheel)
        self.frame_resultados.bind_all("<Button-4>", self._on_mousewheel)
        self.frame_resultados.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.frame_resultados.unbind_all("<MouseWheel>")
        self.frame_resultados.unbind_all("<Button-4>")
        self.frame_resultados.unbind_all("<Button-5>")

    def reiniciar(self):
        self.destroy()
        HW_SW_AI_App().mainloop()

if __name__ == "__main__":
    app = HW_SW_AI_App()
    app.mainloop()