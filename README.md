# CBR Project: Evolución y Mejoras del Sistema

Este documento detalla las últimas actualizaciones (desde el 11 de enero de 2026) realizadas en el proyecto de Razonamiento Basado en Casos (CBR). Las mejoras se han centrado en optimizar el sistema de base de datos (Firestore), robustecer la lógica de nuestro servicio y añadir una capa de presentación gráfica interactiva que categorice y valore cada uno de nuestros casos.

## 💾 Detalle de Actualizaciones en Base de Datos (Firestore)

El servicio principal de conexión y gestión de la base de datos, estructurado dentro de la clase `CasoCRUD` (`service.py`), se ha mejorado considerablemente con los siguientes aspectos técnicos:

1. **Ampliación del Modelo de Datos (Esquema del Documento)**
   Al crear un nuevo caso, el documento JSON que se inserta en la colección `casos` ahora incorpora nuevos campos fundamentales:
   * **`categoria`** (String): Diferencia los casos por su tipo (por defecto, `"General"`).
   * **`valoracion`** (Integer): Guarda un acumulado del nivel de satisfacción o utilidad de una solución. Se inicializa en `0`.
   * **`total_valoraciones`** (Integer): Contabiliza el número total de veces que este caso en particular fue valorado por los usuarios (útil para sacar porcentajes).

2. **Sistema Transaccional y de Prevención de Duplicidad**
   * Se ha añadido el método `leer_caso_repetido(descripcion, solucion, categoria)`.
   * **Operación**: Ejecuta una query (`where`) filtrando la colección por esos tres campos concurrentemente y limita el resultado a `1` (`.limit(1).stream()`).
   * **Propósito**: Si existe coincidencia antes de insertar un nuevo documento, la capa de lógica lo bloquea y avisa al usuario, asegurando una base de conocimiento completamente saneada y sin redundancias.

3. **Sistema de Puntuación Atómica**
   * El nuevo método `valorar_caso(id, valor)` recibe el UID del documento y un valor ponderado (+1 o -1).
   * Mediante una llamada limpia mediante el uso de `doc_ref.update({...})`, recupera los campos `valoracion` y `total_valoraciones`, y los actualiza incrementalmente sin alterar el resto de los metadatos.

---

## 💻 Detalle de Actualizaciones en Código (Frontend / UI Lógica)

La capa de presentación construida con `customtkinter` (`gui.py`) ha visto una gran refactorización para acoplarse y sacar provecho del nuevo diseño de datos.

1. **Filtro Categórico y Dropdowns Interactivos**
   * Se ha integrado un componente `CTkOptionMenu` con la lista predefinida: `["General", "Hardware", "Software", "Redes"]`.
   * La estructura de almacenamiento interactivo (el diccionario `self.casebase`) ahora se rellena filtrando dinámicamente según la categoría de la selección, reduciendo dramáticamente el volumen de comparación en memoria de aquellos casos que no encajan en el entorno seleccionado.

2. **Renderizado de Métricas Mejorado**
   * Al iterar sobre el `top3` de los resultados coincidentes, la UI incluye lógica matemática para calcular en tiempo real y mostrar el éxito de esa solución:
     * Si `total_valoraciones == 0`, se muestra claramente `"Sin valoraciones"`.
     * En caso contario, procesa el cálculo: `((valoracion / total_valoraciones) * 100)` y lo pinta con un formato controlado asintótico y decimal (`%.2f%`).
   * Adicionalmente, se cambió el diseño visual de los resultados empleando una cuadrícula (`grid()`) y alineando a la derecha (`justify="right"`) elementos diferenciadores como la categoría extraída del diccionario final.

3. **Gestión Concurrente (Threading)**
   * Continúa el esfuerzo por mantener la UI principal (Mainloop) reactiva y no bloqueante. Las consultas de búsqueda de patrones o de indexación se despachan y gestionan a través de `threading.Thread(target=self.buscar_casos, args=(problema, categoria)).start()`. 

4. **Experiencia de Funciones Reactivas y Flujos de Cierre**
   * Para añadir inmediatez al botón de proponer soluciones (`proponer_solucion`), se ha rediseñado la entrada y los cierres de ventanas mediante `.pack_forget()`, limpiando los frames.
   * Se ha configurado un estado post-puntuación donde los botones de pulgar arriba y pulgar abajo (`btnLike`, `btnDislike`) se cambian en "disabled" y sus colores de base a rojo o verde visualizando así la respuesta procesada y mitigando el doble envío o rebote.

---

### Mantenimiento Continuo

Todas estas ramas operativas y características aisladas se han revisado bajo la validación y fusión unificada en el commit central contra `main`, solidificando la integridad del aplicativo (`Merge branch 'main' of https://github.com/MarcRoviraP/cbr`).
