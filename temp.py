import service

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



for caso in casebase.values():
    service_instance = service.CasoCRUD()
    service_instance.crear_caso(caso['descripcion'], caso['solucion'])