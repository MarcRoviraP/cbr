import cbrkit
from cbrkit.sim import strings, numbers, attribute_value, aggregator
from cbrkit.retrieval import build, apply_query

# --------------------------------------
# 1. BASE DE CASOS
# --------------------------------------
casos = [
    {"id": 1, "descripcion": "guitarra eléctrica roja", "valor": 1200},
    {"id": 2, "descripcion": "guitarra acústica marrón", "valor": 800},
    {"id": 3, "descripcion": "bajo eléctrico negro", "valor": 1100},
    {"id": 4, "descripcion": "guitarra eléctrica azul", "valor": 1300},
]

# Consulta / Query
consulta = {
    "descripcion": "guitarra eléctrica roja brillante",
    "valor": 1250
}

# --------------------------------------
# 2. DEFINIR SIMILITUDES
# --------------------------------------

# Similitud de texto (basada en Levenshtein)
sim_texto = strings.levenshtein()

# Similitud para un valor numérico
sim_valor = numbers.linear(max_distance=500)

# Crear similitud compuesta por atributos
sim_atributos = attribute_value(
    attributes={
        "descripcion": sim_texto,
        "valor": sim_valor,
    },
    aggregator=aggregator(pooling="mean")  # Produce un promedio de similitudes
)

# --------------------------------------
# 3. CONSTRUIR EL RECUPERADOR
# --------------------------------------
retriever = build(sim_atributos)

# --------------------------------------
# 4. APLICAR LA CONSULTA
# --------------------------------------
resultado = apply_query(casos, consulta, retriever)

# --------------------------------------
# 5. MOSTRAR RESULTADOS
# --------------------------------------
print("=== RESULTADOS DE SIMILITUD ===\n")

for caso, sim in zip(resultado.cases, resultado.similarities):
    print(f"ID Caso: {caso['id']}")
    print(f"Similitud: {sim:.3f}")
    print(f"Datos: {caso}")
    print("-------------------------------")
