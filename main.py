from cbrkit.sim import generic, strings
from cbrkit.retrieval import build, apply_query

# ======================================================
# 1. CREAR BASE DE CASOS
# ======================================================

# La base de casos debe ser un diccionario
casebase = {
    1: {"id": 1, "descripcion": "El pc va muy lento al iniciar", "solucion": "Desactivar programas de inicio"},
    2: {"id": 2, "descripcion": "No hay conexion a internet por wifi", "solucion": "Reiniciar router y revisar configuración WiFi"},
    3: {"id": 3, "descripcion": "La pantalla queda en negro al encender", "solucion": "Comprobar cables y GPU"},
    4: {"id": 4, "descripcion": "Hace ruido extraño", "solucion": "Limpiar ventiladores"},
    5: {"id": 5, "descripcion": "Se reinicia al abrir juegos pesados", "solucion": "Comprobar temperatura CPU"},
    6: {"id": 6, "descripcion": "El teclado no funciona", "solucion": "Revisar drivers"},
    7: {"id": 7, "descripcion": "Falta espacio en disco", "solucion": "Eliminar archivos"},
    8: {"id": 8, "descripcion": "Programas tardan en abrir", "solucion": "Ampliar RAM"},
    9: {"id": 9, "descripcion": "No detecta disco duro", "solucion": "Comprobar cables SATA"},
    10: {"id": 10, "descripcion": "Se apaga de repente", "solucion": "Revisar fuente alimentación"},
    11: {"id": 11, "descripcion": "Ratón se congela", "solucion": "Actualizar drivers"},
    12: {"id": 12, "descripcion": "Problemas sonido en Windows", "solucion": "Revisar configuración"},
    13: {"id": 13, "descripcion": "FPS bajos en juegos", "solucion": "Actualizar drivers GPU"},
    14: {"id": 14, "descripcion": "No enciende", "solucion": "Comprobar fuente"},
    15: {"id": 15, "descripcion": "Ventilador siempre rápido", "solucion": "Cambiar pasta térmica"},
    16: {"id": 16, "descripcion": "Batería dura poco", "solucion": "Ajustar energía"},
    17: {"id": 17, "descripcion": "No detecta USB", "solucion": "Reinstalar drivers USB"},
    18: {"id": 18, "descripcion": "Errores al ejecutar programas", "solucion": "Reinstalar software"},
    19: {"id": 19, "descripcion": "Internet va lento", "solucion": "Comprobar ancho banda"},
    20: {"id": 20, "descripcion": "Pantalla parpadea", "solucion": "Actualizar drivers vídeo"},
    21: {"id": 21, "descripcion": "No se conecta a red WiFi", "solucion": "Olvidar red y reconectar"},
    22: {"id": 22, "descripcion": "Monitor no se enciende", "solucion": "Comprobar cable HDMI y fuente"},
    23: {"id": 23, "descripcion": "Tarjeta gráfica con artefactos visuales", "solucion": "Limpiar GPU y revisar ventilación"},
    24: {"id": 24, "descripcion": "Sistema operativo no inicia", "solucion": "Ejecutar reparación de inicio"},
    25: {"id": 25, "descripcion": "Azules de pantalla aleatorios", "solucion": "Actualizar BIOS y drivers"},
    26: {"id": 26, "descripcion": "Sobrecalentamiento constante", "solucion": "Limpiar disipadores y cambiar pasta"},
    27: {"id": 27, "descripcion": "Aplicaciones se cierran inesperadamente", "solucion": "Verificar integridad del sistema"},
    28: {"id": 28, "descripcion": "Webcam no funciona", "solucion": "Reinstalar drivers de cámara"},
    29: {"id": 29, "descripcion": "Micrófono sin sonido", "solucion": "Ajustar niveles de grabación"},
    30: {"id": 30, "descripcion": "Navegador va muy lento", "solucion": "Limpiar caché y extensiones"},
}

# ======================================================
# 2. DEFINIR SIMILITUD DE TEXTO
# ======================================================

# Opción 1: Usando tabla de similitudes personalizadas para palabras clave
palabras_clave = [
    ("lento", "lento", 1.0),
    ("lento", "tardan", 0.7),
    ("internet", "wifi", 0.8),
    ("internet", "conexion", 0.8),
    ("pantalla", "pantalla", 1.0),
    ("pantalla", "negro", 0.6),
    ("ruido", "ventilador", 0.7),
    ("reinicia", "apaga", 0.6),
    ("teclado", "ratón", 0.5),
    ("drivers", "drivers", 1.0),
    ("disco", "espacio", 0.7),
    ("juegos", "fps", 0.8),
]

sim_texto = strings.table(palabras_clave, symmetric=True, default=0.0, case_sensitive=False)

# Opción 2: Para una función de similitud más simple basada en coincidencias
def similitud_descripcion(caso_desc, query_desc):
    """Calcula similitud básica por palabras en común"""
    caso_words = set(caso_desc.lower().split())
    query_words = set(query_desc.lower().split())
    
    if not query_words:
        return 0.0
    
    # Palabras en común
    comunes = caso_words.intersection(query_words)
    return len(comunes) / len(query_words)

# ======================================================
# 3. FLUJO PRINCIPAL
# ======================================================

print("=== SISTEMA EXPERTO CBR CON CBRkit ===\n")

# Entrada
nuevo_caso_texto = input("Describe tu problema: ")

# Crear una consulta simple con solo la descripción
consulta = {"descripcion": nuevo_caso_texto}

# Construir retriever usando la similitud de texto personalizada
# Usamos una función que compare solo las descripciones
def sim_func(x, y):
    """Función de similitud personalizada"""
    return similitud_descripcion(x["descripcion"], y["descripcion"])

retriever = build(sim_func)

# Aplicar la consulta
resultado = apply_query(casebase, consulta, retriever)

# Obtener los resultados
query_result = resultado.queries["default"]

# Obtener top 3 casos ordenados por similitud
top3 = []
for case_id in query_result.ranking[:3]:
    caso = query_result.casebase[case_id]
    sim = query_result.similarities[case_id]
    top3.append((caso, sim))

print("\nCasos más parecidos:\n")
for i, (caso, score) in enumerate(top3, start=1):
    print(f"[{i}] {caso['descripcion']}")
    print(f"     Similitud: {round(score*100)}%")
    print()

opcion = int(input("Elige el caso más parecido (1-3): "))
caso_elegido, score = top3[opcion - 1]

print("\n--- SOLUCIÓN PROPUESTA ---")
print(caso_elegido["solucion"])
print("--------------------------\n")

mod = input("¿Quieres modificar la solución? (s/n): ")

if mod.lower() == "s":
    nueva_sol = input("Introduce la solución corregida: ")
else:
    nueva_sol = caso_elegido["solucion"]

# ======================================================
# 4. RETENER (APRENDER)
# ======================================================

# Agregar el nuevo caso a la base de casos
nuevo_id = max(casebase.keys()) + 1
nuevo_caso = {
    "id": nuevo_id,
    "descripcion": nuevo_caso_texto,
    "solucion": nueva_sol,
    "basado_en": caso_elegido["descripcion"]
}

casebase[nuevo_id] = nuevo_caso

print("\nCaso guardado correctamente:\n")
print("Descripción:", nuevo_caso["descripcion"])
print("Solución:", nuevo_caso["solucion"])
print("Basado en:", nuevo_caso["basado_en"])
