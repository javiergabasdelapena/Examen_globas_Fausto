import heapq
import json
from collections import deque


class RedEstaciones:
    """Clase que representa una red de estaciones como grafo ponderado."""
    
    def __init__(self):
        # Diccionario de listas de adyacencia: {estacion: {vecino: tiempo, ...}, ...}
        self.grafo = {}
    
    def cargar_desde_archivo(self, nombre_archivo):
        """Carga la red de estaciones desde un archivo JSON."""
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            self.grafo = {}
            for estacion, conexiones in datos.items():
                self.grafo[estacion] = dict(conexiones)
            
            print(f"✓ Red cargada: {len(self.grafo)} estaciones desde '{nombre_archivo}'")
            return True
            
        except FileNotFoundError:
            print(f"⚠ Archivo '{nombre_archivo}' no encontrado. Se inicia red vacía.")
            return False
        except json.JSONDecodeError:
            print(f"✗ Error: El archivo '{nombre_archivo}' no tiene formato JSON válido.")
            return False
        except Exception as e:
            print(f"✗ Error al cargar archivo: {e}")
            return False
    
    def guardar_en_archivo(self, nombre_archivo):
        """Guarda la red de estaciones en un archivo JSON."""
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.grafo, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Red guardada en '{nombre_archivo}'")
            return True
            
        except PermissionError:
            print(f"✗ Error: Sin permisos para escribir en '{nombre_archivo}'.")
            return False
        except Exception as e:
            print(f"✗ Error al guardar archivo: {e}")
            return False
    
    def añadir_estacion(self, nombre):
        """Añade una nueva estación a la red."""
        nombre = nombre.strip()
        
        if not nombre:
            print("✗ Error: El nombre de la estación no puede estar vacío.")
            return False
        
        if nombre in self.grafo:
            print(f"✗ Error: La estación '{nombre}' ya existe.")
            return False
        
        self.grafo[nombre] = {}
        print(f"✓ Estación '{nombre}' añadida.")
        return True
    
    def añadir_conexion(self, origen, destino, tiempo):
        """Añade una conexión bidireccional entre dos estaciones."""
        # Validar que las estaciones existan
        if origen not in self.grafo:
            print(f"✗ Error: La estación origen '{origen}' no existe.")
            return False
        
        if destino not in self.grafo:
            print(f"✗ Error: La estación destino '{destino}' no existe.")
            return False
        
        # Validar que no sea la misma estación
        if origen == destino:
            print("✗ Error: No se puede conectar una estación consigo misma.")
            return False
        
        # Validar tiempo positivo
        try:
            tiempo = float(tiempo)
            if tiempo <= 0:
                print("✗ Error: El tiempo debe ser un número positivo.")
                return False
        except ValueError:
            print("✗ Error: El tiempo debe ser un número válido.")
            return False
        
        # Validar conexión duplicada
        if destino in self.grafo[origen]:
            print(f"✗ Error: Ya existe conexión entre '{origen}' y '{destino}'.")
            return False
        
        # Añadir conexión bidireccional
        self.grafo[origen][destino] = tiempo
        self.grafo[destino][origen] = tiempo
        
        print(f"✓ Conexión añadida: {origen} ↔ {destino} ({tiempo} min)")
        return True
    
    def mostrar_estaciones(self):
        """Muestra todas las estaciones y sus conexiones."""
        if not self.grafo:
            print("La red está vacía. No hay estaciones registradas.")
            return
        
        print(f"\n{'═' * 50}")
        print(f"  RED DE ESTACIONES ({len(self.grafo)} estaciones)")
        print(f"{'═' * 50}\n")
        
        for estacion in sorted(self.grafo.keys()):
            conexiones = self.grafo[estacion]
            print(f"🚉 {estacion}")
            
            if conexiones:
                for vecino, tiempo in sorted(conexiones.items()):
                    print(f"   └─→ {vecino}: {tiempo} min")
            else:
                print("   └─→ (sin conexiones)")
            print()
    
    def mostrar_conexiones_estacion(self, estacion):
        """Muestra las conexiones directas de una estación específica."""
        if estacion not in self.grafo:
            print(f"✗ Error: La estación '{estacion}' no existe.")
            return False
        
        conexiones = self.grafo[estacion]
        
        print(f"\n🚉 Estación: {estacion}")
        print(f"{'─' * 40}")
        
        if conexiones:
            print(f"Conexiones directas ({len(conexiones)}):")
            for vecino, tiempo in sorted(conexiones.items()):
                print(f"  → {vecino}: {tiempo} min")
        else:
            print("  (sin conexiones directas)")
        
        return True
    
    def dijkstra(self, origen, destino):
        """
        Calcula la ruta más rápida entre dos estaciones usando Dijkstra.
        Retorna (ruta, tiempo_total) o (None, None) si no hay camino.
        """
        # Validar estaciones
        if origen not in self.grafo:
            print(f"✗ Error: La estación origen '{origen}' no existe.")
            return None, None
        
        if destino not in self.grafo:
            print(f"✗ Error: La estación destino '{destino}' no existe.")
            return None, None
        
        if origen == destino:
            return [origen], 0
        
        # Inicialización
        distancias = {estacion: float('inf') for estacion in self.grafo}
        distancias[origen] = 0
        predecesores = {estacion: None for estacion in self.grafo}
        visitados = set()  # Conjunto para nodos visitados
        
        # Cola de prioridad: (distancia, estacion)
        heap = [(0, origen)]
        
        while heap:
            dist_actual, actual = heapq.heappop(heap)
            
            # Si ya visitamos este nodo, ignorar
            if actual in visitados:
                continue
            
            visitados.add(actual)
            
            # Si llegamos al destino, reconstruir camino
            if actual == destino:
                ruta = []
                nodo = destino
                while nodo is not None:
                    ruta.append(nodo)
                    nodo = predecesores[nodo]
                ruta.reverse()
                return ruta, distancias[destino]
            
            # Explorar vecinos
            for vecino, tiempo in self.grafo[actual].items():
                if vecino not in visitados:
                    nueva_dist = dist_actual + tiempo
                    if nueva_dist < distancias[vecino]:
                        distancias[vecino] = nueva_dist
                        predecesores[vecino] = actual
                        heapq.heappush(heap, (nueva_dist, vecino))
        
        # No se encontró camino
        return None, None
    
    def ruta_mas_rapida(self, origen, destino):
        """Muestra la ruta más rápida entre dos estaciones."""
        ruta, tiempo_total = self.dijkstra(origen, destino)
        
        if ruta is None:
            print(f"\n✗ No existe ruta entre '{origen}' y '{destino}'.")
            return False
        
        if len(ruta) == 1:
            print(f"\n✓ Origen y destino son la misma estación.")
            return True
        
        print(f"\n{'═' * 50}")
        print(f"  RUTA MÁS RÁPIDA")
        print(f"{'═' * 50}")
        print(f"  De: {origen}")
        print(f"  A:  {destino}")
        print(f"{'─' * 50}")
        print(f"  Recorrido:")
        
        for i, estacion in enumerate(ruta):
            if i == 0:
                print(f"    🚉 {estacion} (inicio)")
            elif i == len(ruta) - 1:
                tiempo_tramo = self.grafo[ruta[i-1]][estacion]
                print(f"    🏁 {estacion} (destino) ← {tiempo_tramo} min")
            else:
                tiempo_tramo = self.grafo[ruta[i-1]][estacion]
                print(f"    ↓  {estacion} ← {tiempo_tramo} min")
        
        print(f"{'─' * 50}")
        print(f"  ⏱  TIEMPO TOTAL: {tiempo_total} minutos")
        print(f"  📍 Estaciones: {len(ruta)}")
        print(f"{'═' * 50}\n")
        
        return True
    
    def estan_conectadas_bfs(self, origen, destino):
        """Comprueba si dos estaciones están conectadas usando BFS."""
        if origen not in self.grafo:
            print(f"✗ Error: La estación '{origen}' no existe.")
            return None
        
        if destino not in self.grafo:
            print(f"✗ Error: La estación '{destino}' no existe.")
            return None
        
        if origen == destino:
            return True
        
        visitados = set()  # Conjunto para nodos visitados
        cola = deque([origen])
        visitados.add(origen)
        
        while cola:
            actual = cola.popleft()
            
            if actual == destino:
                return True
            
            for vecino in self.grafo[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
        
        return False
    
    def estan_conectadas_dfs(self, origen, destino):
        """Comprueba si dos estaciones están conectadas usando DFS."""
        if origen not in self.grafo:
            print(f"✗ Error: La estación '{origen}' no existe.")
            return None
        
        if destino not in self.grafo:
            print(f"✗ Error: La estación '{destino}' no existe.")
            return None
        
        if origen == destino:
            return True
        
        visitados = set()  # Conjunto para nodos visitados
        pila = [origen]
        
        while pila:
            actual = pila.pop()
            
            if actual == destino:
                return True
            
            if actual not in visitados:
                visitados.add(actual)
                for vecino in self.grafo[actual]:
                    if vecino not in visitados:
                        pila.append(vecino)
        
        return False
    
    def verificar_conexion(self, origen, destino):
        """Verifica y muestra si dos estaciones están conectadas."""
        # Usar BFS por defecto (también podría usar DFS)
        resultado = self.estan_conectadas_bfs(origen, destino)
        
        if resultado is None:
            return False
        
        print(f"\n{'─' * 40}")
        if resultado:
            print(f"✓ SÍ están conectadas: '{origen}' y '{destino}'")
            # Mostrar también la ruta más corta
            ruta, tiempo = self.dijkstra(origen, destino)
            if ruta and len(ruta) > 1:
                print(f"  Ruta: {' → '.join(ruta)}")
                print(f"  Tiempo: {tiempo} min")
        else:
            print(f"✗ NO están conectadas: '{origen}' y '{destino}'")
        print(f"{'─' * 40}\n")
        
        return resultado
    
    def listar_estaciones(self):
        """Retorna lista ordenada de estaciones."""
        return sorted(self.grafo.keys())


def mostrar_menu():
    """Muestra el menú principal."""
    print(f"""
╔══════════════════════════════════════════╗
║     PLANIFICADOR DE RUTAS - METRO        ║
╠══════════════════════════════════════════╣
║  1. Cargar red desde archivo             ║
║  2. Añadir estación                      ║
║  3. Añadir conexión                      ║
║  4. Ver estaciones y conexiones          ║
║  5. Ruta más rápida entre estaciones     ║
║  6. ¿Están conectadas dos estaciones?    ║
║  7. Guardar y salir                      ║
╚══════════════════════════════════════════╝""")


def obtener_opcion():
    """Obtiene la opción del usuario con validación."""
    try:
        opcion = input("\nSelecciona opción (1-7): ").strip()
        if opcion in ['1', '2', '3', '4', '5', '6', '7']:
            return opcion
        print("✗ Opción no válida. Introduce un número del 1 al 7.")
        return None
    except (EOFError, KeyboardInterrupt):
        return '7'


def main():
    """Función principal del programa."""
    red = RedEstaciones()
    archivo_red = "red_estaciones.json"
    
    print("\n" + "═" * 45)
    print("  INICIANDO PLANIFICADOR DE RUTAS")
    print("═" * 45)
    
    # Intentar cargar red existente al iniciar
    red.cargar_desde_archivo(archivo_red)
    
    while True:
        mostrar_menu()
        opcion = obtener_opcion()
        
        if opcion is None:
            continue
        
        if opcion == '1':
            nombre = input("Nombre del archivo (Enter para 'red_estaciones.json'): ").strip()
            if not nombre:
                nombre = archivo_red
            red.cargar_desde_archivo(nombre)
        
        elif opcion == '2':
            nombre = input("Nombre de la nueva estación: ").strip()
            red.añadir_estacion(nombre)
        elif opcion == '3':
            if not red.grafo:
                print("✗ No hay estaciones. Añade estaciones primero.")
                continue
            
            print("\nEstaciones disponibles:", ", ".join(red.listar_estaciones()))
            origen = input("Estación origen: ").strip()
            destino = input("Estación destino: ").strip()
            tiempo = input("Tiempo de viaje (minutos): ").strip()
            
            red.añadir_conexion(origen, destino, tiempo)
        
        elif opcion == '4':
            red.mostrar_estaciones()
            
            if red.grafo:
                ver_detalle = input("¿Ver conexiones de una estación específica? (s/n): ").strip().lower()
                if ver_detalle == 's':
                    estacion = input("Nombre de la estación: ").strip()
                    red.mostrar_conexiones_estacion(estacion)
        
        elif opcion == '5':
            if not red.grafo:
                print("✗ No hay estaciones en la red.")
                continue
            
            print("\nEstaciones disponibles:", ", ".join(red.listar_estaciones()))
            origen = input("Estación origen: ").strip()
            destino = input("Estación destino: ").strip()
            
            red.ruta_mas_rapida(origen, destino)
        
        elif opcion == '6':
            if not red.grafo:
                print("✗ No hay estaciones en la red.")
                continue
            
            print("\nEstaciones disponibles:", ", ".join(red.listar_estaciones()))
            origen = input("Primera estación: ").strip()
            destino = input("Segunda estación: ").strip()
            
            red.verificar_conexion(origen, destino)
        

        elif opcion == '7':
            if red.grafo:
                guardar = input("¿Guardar cambios antes de salir? (s/n): ").strip().lower()
                if guardar == 's':
                    nombre = input(f"Archivo (Enter para '{archivo_red}'): ").strip()
                    if not nombre:
                        nombre = archivo_red
                    red.guardar_en_archivo(nombre)
            
            print("\n¡Hasta pronto! \n")
            break


if __name__ == "__main__":
    main()
