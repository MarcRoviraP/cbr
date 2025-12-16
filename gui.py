import customtkinter as ctk
import threading
from main import similitud_descripcion, build, apply_query
from service import CasoCRUD

# ConfiguraciÃ³n visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HW_SW_AI_App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🤖 HW/SW AI - Asistente de Soporte Técnico")
        self.geometry("700x600")
        self.resizable(False, False)

        self.casebase = {caso['id']: caso for caso in CasoCRUD().leer_todos_casos()}
        self.top3 = []
        self.caso_elegido = None

        self.build_ui()

    def build_ui(self):
        self.label_bienvenida = ctk.CTkLabel(self, text="👋 ¡Hola! Cuéntame qué problema tienes con tu PC.", font=("Arial", 16))
        self.label_bienvenida.pack(pady=20)

        self.text_input = ctk.CTkTextbox(self, height=80, width=600)
        self.text_input.pack(pady=10)

        self.btn_enviar = ctk.CTkButton(self, text="Enviar", command=self.iniciar_busqueda)
        self.btn_enviar.pack(pady=10)

        self.frame_resultados = ctk.CTkScrollableFrame(self, width=650, height=250)
        self.frame_resultados.pack_forget()

        self.frame_solucion = ctk.CTkFrame(self)
        self.frame_solucion.pack_forget()

        self.text_solucion = ctk.CTkTextbox(self.frame_solucion, height=100, width=600)
        self.text_solucion.pack(pady=10)

        self.btn_mejorar = ctk.CTkButton(self.frame_solucion, text="Quiero mejorar la solución", command=self.mostrar_mejora)
        self.btn_mejorar.pack(side="left", padx=10)

        self.btn_aceptar = ctk.CTkButton(self.frame_solucion, text="Está bien", command=self.guardar_sin_cambios)
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
        if not problema:
            return

        self.label_bienvenida.configure(text="🔍 Buscando casos similares...")
        self.text_input.configure(state="disabled")
        self.btn_enviar.configure(state="disabled")

        threading.Thread(target=self.buscar_casos, args=(problema,)).start()

    def buscar_casos(self, problema):
        consulta = {"descripcion": problema}
        def sim_func(x, y):
            return similitud_descripcion(x["descripcion"], y["descripcion"])

        retriever = build(sim_func)
        resultado = apply_query(self.casebase, consulta, retriever)
        query_result = resultado.queries["default"]

        self.top3 = []
        for case_id in query_result.ranking[:3]:
            caso = query_result.casebase[case_id]
            sim = query_result.similarities[case_id]
            self.top3.append((caso, sim))

        self.after(0, self.mostrar_resultados)

    def mostrar_resultados(self):
        self.label_bienvenida.configure(text="📊 Casos más parecidos encontrados:")
        self.frame_resultados.pack(pady=10)

        for i, (caso, score) in enumerate(self.top3, start=1):
            frame = ctk.CTkFrame(self.frame_resultados)
            frame.pack(fill="x", pady=5)

            label = ctk.CTkLabel(frame, text=f"[{i}] {caso['descripcion']}\nSimilitud: {round(score*100)}%")
            label.pack(side="left", padx=10)

            btn = ctk.CTkButton(frame, text="Ver solución", command=lambda c=caso: self.mostrar_solucion(c))
            btn.pack(side="right", padx=10)
            
        
        frame = ctk.CTkFrame(self.frame_resultados)
        frame.pack(fill="x", pady=5)
        label = ctk.CTkLabel(frame, text="Ninguno de estos casos resuelve mi problema")
        label.pack(side="left", padx=10)
        btn = ctk.CTkButton(frame, text="Proponer solución", command=lambda c=caso: self.mostrar_cuarta_opcion())
        btn.pack(side="right", padx=10)
        
    def mostrar_cuarta_opcion(self):
        self.frame_resultados.pack_forget()
        self.label_bienvenida.configure(text="✏️ Describe la solución que propones para tu problema:")
        self.frame_mejora.pack(pady=10)
        

    def mostrar_solucion(self, caso):
       
        self.caso_elegido = caso
        self.frame_resultados.pack_forget()
        self.label_bienvenida.configure(text="✅ Solución propuesta:")
        self.frame_solucion.pack(pady=10)
        self.text_solucion.insert("1.0", caso["solucion"])

    def mostrar_mejora(self):
        self.frame_solucion.pack_forget()
        self.label_bienvenida.configure(text="✏️ Introduce tu versión mejorada:")
        self.frame_mejora.pack(pady=10)

    def guardar_sin_cambios(self):
        self.guardar_caso(self.caso_elegido["solucion"])

    def guardar_con_mejora(self):
        mejora = self.text_mejora.get("1.0", "end").strip()
        self.guardar_caso(mejora)

    def guardar_caso(self, solucion):
        crud = CasoCRUD()
        problema = self.text_input.get("1.0", "end").strip()
        nuevo_id = crud.crear_caso(descripcion=problema, solucion=solucion)

        self.frame_mejora.pack_forget()
        self.frame_solucion.pack_forget()
        self.label_bienvenida.pack_forget()
        self.text_input.pack_forget()
        self.btn_enviar.pack_forget()

        self.label_exito.pack(pady=20)
        self.btn_nuevo.pack(pady=10)

    def reiniciar(self):
        self.destroy()
        HW_SW_AI_App().mainloop()

if __name__ == "__main__":
    app = HW_SW_AI_App()
    app.mainloop()