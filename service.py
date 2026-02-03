import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate("./cbr-8041f-firebase-adminsdk-fbsvc-460010673c.json")
firebase_admin.initialize_app(cred)

# Obtener referencia a Firestore
db = firestore.client()

class CasoCRUD:
    def __init__(self):
        self.collection = db.collection('casos')
    
    # CREATE - Crear un nuevo caso
    def crear_caso(self, descripcion, solucion="", categoria="General"):
        """Crea un nuevo caso en Firestore"""
        nuevo_caso = {
            'descripcion': descripcion,
            'solucion': solucion,
            'fecha_creacion': datetime.now(),
            'fecha_actualizacion': datetime.now(),
            'valoracion': 0,
            'categoria': categoria
        }
        
        doc_ref = self.collection.add(nuevo_caso)
        caso_id = doc_ref[1].id
        # print(f"âœ“ Caso creado con ID: {caso_id}")
        return caso_id
    
    # READ - Leer un caso especÃ­fico
    def leer_caso(self, caso_id):
        """Lee un caso por su ID"""
        doc = self.collection.document(caso_id).get()
        
        if doc.exists:
            caso = doc.to_dict()
            caso['id'] = doc.id
            # print(f"\n--- Caso {doc.id} ---")
            # print(f"Descripción: {caso['descripcion']}")
            # print(f"Solución: {caso['solucion']}")
            return caso
        else:
            # print(f"âœ— No existe un caso con ID: {caso_id}")
            return None
    
    # READ ALL - Leer todos los casos
    def leer_todos_casos(self):
        """Lee todos los casos de la colecciÃ³n"""
        docs = self.collection.stream()
        casos = []
        
        # print("\n=== TODOS LOS CASOS ===")
        for doc in docs:
            caso = doc.to_dict()
            caso['id'] = doc.id
            casos.append(caso)
            # print(f"\nID: {doc.id}")
            # print(f"DescripciÃ³n: {caso['descripcion']}")
            # print(f"SoluciÃ³n: {caso['solucion']}")
        
        if not casos:
            print("No hay casos registrados")
        
        return casos
    
    # UPDATE - Actualizar un caso
    def actualizar_caso(self, caso_id, descripcion=None, solucion=None):
        """Actualiza un caso existente"""
        doc_ref = self.collection.document(caso_id)
        
        if not doc_ref.get().exists:
            # print(f"âœ— No existe un caso con ID: {caso_id}")
            return False
        
        datos_actualizados = {'fecha_actualizacion': datetime.now()}
        
        if descripcion is not None:
            datos_actualizados['descripcion'] = descripcion
        if solucion is not None:
            datos_actualizados['solucion'] = solucion
        
        doc_ref.update(datos_actualizados)
        # print(f"âœ“ Caso {caso_id} actualizado correctamente")
        return True
    
    # DELETE - Eliminar un caso
    def eliminar_caso(self, caso_id):
        """Elimina un caso por su ID"""
        doc_ref = self.collection.document(caso_id)
        
        if not doc_ref.get().exists:
            # print(f"âœ— No existe un caso con ID: {caso_id}")
            return False
        
        doc_ref.delete()
        # print(f"âœ“ Caso {caso_id} eliminado correctamente")
        return True


# ============ EJEMPLO DE USO ============

if __name__ == "__main__":
    crud = CasoCRUD()
    
    # CREATE - Crear casos
    print("\n1. CREANDO CASOS...")
    caso1_id = crud.crear_caso(
        descripcion="Error en login de usuarios",
        solucion="Revisar configuraciÃ³n de autenticaciÃ³n"
    )
    
    caso2_id = crud.crear_caso(
        descripcion="Base de datos lenta",
        solucion=""
    )
    
    # READ - Leer caso especÃ­fico
    print("\n2. LEYENDO CASO ESPECÃFICO...")
    crud.leer_caso(caso1_id)
    
    # READ ALL - Leer todos los casos
    print("\n3. LEYENDO TODOS LOS CASOS...")
    crud.leer_todos_casos()
    
    # UPDATE - Actualizar caso
    print("\n4. ACTUALIZANDO CASO...")
    crud.actualizar_caso(
        caso2_id,
        solucion="Optimizar Ã­ndices de Firestore"
    )
    
    # READ - Verificar actualizaciÃ³n
    print("\n5. VERIFICANDO ACTUALIZACIÃ“N...")
    crud.leer_caso(caso2_id)
    
    # DELETE - Eliminar caso
    print("\n6. ELIMINANDO CASO...")
    crud.eliminar_caso(caso1_id)
    
    # READ ALL - Ver casos restantes
    print("\n7. CASOS FINALES...")
    crud.leer_todos_casos()