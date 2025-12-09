from cbrkit.sim import generic, strings
from cbrkit.retrieval import build, apply_query
from service import *

# ======================================================
# 1. CREAR BASE DE CASOS
# ======================================================

# La base de casos debe ser un diccionario
casos_lista = CasoCRUD().leer_todos_casos()
# Convertir lista a diccionario usando el ID como clave
casebase = {caso['id']: caso for caso in casos_lista}

# ======================================================
# 2. DEFINIR SIMILITUD DE TEXTO
# ======================================================

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

# Agregar el nuevo caso a la base de casos en Firestore
crud = CasoCRUD()
nuevo_id = crud.crear_caso(descripcion=nuevo_caso_texto, solucion=nueva_sol)

nuevo_caso = {
    "id": nuevo_id,
    "descripcion": nuevo_caso_texto,
    "solucion": nueva_sol,
    "basado_en": caso_elegido["descripcion"]
}

print("\nCaso guardado correctamente:\n")
print("Descripción:", nuevo_caso["descripcion"])
print("Solución:", nuevo_caso["solucion"])
print("Basado en:", nuevo_caso["basado_en"])
