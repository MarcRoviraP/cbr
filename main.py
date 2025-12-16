from cbrkit.sim import generic, strings
from cbrkit.retrieval import build, apply_query
from service import *

# ======================================================
# 1. CREAR BASE DE CASOS
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


def sim_func(x, y):
    """Función de similitud personalizada"""
    return similitud_descripcion(x["descripcion"], y["descripcion"])


