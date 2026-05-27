Este programa permite gestionar una red de transporte compuesta por estaciones y conexiones entre ellas. El sistema calcula la ruta más rápida y verifica si existe conexión entre diferentes puntos de la red.

Estructura de Datos Que utiliza 
El programa organiza la información de la siguiente manera:
Diccionario de diccionarios: Se utiliza para representar la red. Cada estación es una clave que contiene otro diccionario con sus estaciones vecinas y el tiempo necesario para llegar a ellas, permitiendo buscar conexiones de forma inmediata.
 Cola de prioridad (Heap): Se emplea en el cálculo de la ruta más rápida para procesar siempre primero los caminos con menor tiempo acumulado, mejorando la eficiencia.
 Conjunto (Set): Sirve para registrar las estaciones ya visitadas, evitando procesar la misma información dos veces y previniendo bucles.
 Cola (Deque): Se utiliza para la comprobación de conectividad, procesando las estaciones en el orden en que son descubiertas.

Análisis de Rendimiento y complejidad 
 Añadir conexión: La operación es muy rápida y constante, sin importar el tamaño de la red.
 Ruta más rápida (Dijkstra): El tiempo aumenta según el número de estaciones y conexiones, pero se mantiene eficiente gracias a la cola de prioridad, que descarta rutas innecesarias.
 Comprobación de conectividad (BFS): Es muy veloz. Realiza un recorrido lógico marcando lo ya visto hasta encontrar el destino o agotar las rutas posibles.
 Espacio: El uso de memoria es proporcional a la cantidad de estaciones y conexiones añadidas.

 Posibles Mejoras
Para ampliar las capacidades del programa , se podrían implementar:
1. Autocompletado: Sugerir nombres de estaciones al escribir para evitar errores.
2. mini mapa de la red : Crear un gráfico interactivo que muestre el mapa de la red.
3. Guardado automático: Asegurar que los cambios se guarden al instante tras cada modificación.
4. Estado de las estaciones: Marcar estaciones como "cerradas" o "con retraso" para recalcular rutas según el estado real.
5. Factor horario : Añadir una opcion de poner el horario de salida para calcular las aglomeraciones y los posibles retrasos que pued haber debido a ellas 

 Cómo usar el programa
1. Ejecuta el archivo desde la terminal: `python red_estaciones.py`.
2. Utiliza el menú numérico para seleccionar las opciones deseadas.
3. El programa cargará por defecto el archivo `red_estaciones.json` si está en la misma carpeta.
4. Al finalizar, elige la opción de guardar para conservar tus cambios en el archivo.
