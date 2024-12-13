'''
11/12/2024
Act mantenimiento de software
CRUD aplication Torneo Tenis
Linda Carolina Zambrano Leon
Jose Luis Rodriguez Castillo
Juan Sebastian Hernandez Galindo
'''

import json
from datetime import datetime
from pymongo import MongoClient

# Clase que representa un torneo
class Torneo:
    def __init__(self, nombre, fecha_inicio, fecha_fin):
        self.nombre = nombre  # Nombre del torneo
        self.fecha_inicio = fecha_inicio  # Fecha de inicio del torneo
        self.fecha_fin = fecha_fin  # Fecha de finalización del torneo
        self.participantes = []  # Lista de participantes en el torneo
        self.encuentros = []  # Lista de encuentros en el torneo
        self.resultados = []  # Lista de resultados de los encuentros
        self.ranking = []  # Clasificación de los participantes

    # Método para agregar un participante al torneo
    def agregar_participante(self, participante):
        self.participantes.append(participante)  # Añade el participante a la lista
        participantes.insert_one(vars(participante))  # Inserta el participante en la base de datos

    # Método para agregar un encuentro al torneo
    def agregar_encuentro(self, encuentro):
        self.encuentros.append(encuentro)  # Añade el encuentro a la lista
        encuentros.insert_one(vars(encuentro))  # Inserta el encuentro en la base de datos

    # Método para agregar un resultado al torneo
    def agregar_resultado(self, resultado):
        self.resultados.append(resultado)  # Añade el resultado a la lista
        resultados.insert_one(vars(resultado))  # Inserta el resultado en la base de datos

    # Método para actualizar la clasificación de los participantes
    def actualizar_ranking(self):
        # Actualiza la clasificación de los participantes en el torneo
        pass

    # Método para guardar los datos del torneo en un archivo JSON
    def guardar_datos(self, filename):
        data = {
            "nombre": self.nombre,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "participantes": [vars(p) for p in self.participantes],
            "encuentros": [vars(e) for e in self.encuentros],
            "resultados": [vars(r) for r in self.resultados],
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)  # Guarda los datos en un archivo JSON

    # Método de clase para cargar los datos del torneo desde un archivo JSON
    @classmethod
    def cargar_datos(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)  # Carga los datos desde el archivo JSON
            torneo = cls(data['nombre'], data['fecha_inicio'], data['fecha_fin'])
            for p in data['participantes']:
                torneo.agregar_participante(Participante(p['nombre'], p['país'], p['rol']))
            for e in data['encuentros']:
                torneo.agregar_encuentro(Encuentro(e['id'], e['fecha'], e['hora'], e['participante1'], e['participante2'], e['sets']))
            for r in data['resultados']:
                torneo.agregar_resultado(Resultado(r['id'], r['encuentro'], r['ganador'], r['perdedor'], r['puntos_totales_ganador'], r['puntos_totales_perdedor']))
            return torneo

# Clase que representa un participante en el torneo
class Participante:
    def __init__(self, nombre, país, rol):
        self.nombre = nombre  # Nombre del participante
        self.país = país  # País del participante
        self.rol = rol  # Rol del participante (por ejemplo, jugador, entrenador, etc.)

# Clase que representa un encuentro en el torneo
class Encuentro:
    def __init__(self, id, fecha, hora, participante1, participante2, sets):
        self.id = id  # Identificador del encuentro
        self.fecha = fecha  # Fecha del encuentro
        self.hora = hora  # Hora del encuentro
        self.participante1 = participante1  # Primer participante del encuentro
        self.participante2 = participante2  # Segundo participante del encuentro
        self.sets = sets  # Número de sets del encuentro
        self.resultado = None  # Resultado del encuentro (inicialmente ninguno)

    # Método para agregar un resultado al encuentro
    def agregar_resultado(self, resultado):
        self.resultado = resultado  # Asigna el resultado al encuentro

# Clase que representa un resultado de un encuentro
class Resultado:
    def __init__(self, id, encuentro, ganador, perdedor, puntos_totales_ganador, puntos_totales_perdedor):
        self.id = id  # Identificador del resultado
        self.encuentro = encuentro  # Encuentro al que pertenece el resultado
        self.ganador = ganador  # Ganador del encuentro
        self.perdedor = perdedor  # Perdedor del encuentro
        self.puntos_totales_ganador = puntos_totales_ganador  # Puntos totales del ganador
        self.puntos_totales_perdedor = puntos_totales_perdedor  # Puntos totales del perdedor

# Crear una instancia de la clase Torneo
torneo = Torneo("Torneo de Tenis", "2024-12-01", "2024-12-31")

# Conectar a la base de datos
cliente = MongoClient("mongodb://localhost:27017/")
base_de_datos = cliente["TorneoTenisexe"]

# Seleccionar las colecciones
participantes = base_de_datos["participantes"]
encuentros = base_de_datos["encuentros"]
resultados = base_de_datos["resultados"]
ranking = base_de_datos["ranking"]

# Funciones CRUD para participantes

# Función para insertar un participante
def insertar_participante():
    nombre = input("Ingrese el nombre del participante: ")
    país = input("Ingrese el país del participante: ")
    rol = input("Ingrese el rol del participante: ")
    
    participante = Participante(nombre, país, rol)
    torneo.agregar_participante(participante)
    print("Participante insertado con éxito.\n")

# Función para leer todos los participantes
def leer_participantes():
    participantes_lista = list(participantes.find())
    if participantes_lista:
        for participante in participantes_lista:
            print(participante)
    else:
        print("No hay participantes en la base de datos.\n")

# Función para actualizar un participante
def actualizar_participante():
    nombre = input("Ingrese el nombre del participante a actualizar: ")
    nuevo_nombre = input("Ingrese el nuevo nombre: ")
    nuevo_país = input("Ingrese el nuevo país: ")
    nuevo_rol = input("Ingrese el nuevo rol: ")
    
    participantes.update_one(
        {"nombre": nombre},
        {"$set": {"nombre": nuevo_nombre, "país": nuevo_país, "rol": nuevo_rol}}
    )
    print("Participante actualizado con éxito.\n")

# Función para validar si un participante existe por nombre
def validar_nombre_participante(nombre):
    participante = participantes.find_one({"nombre": nombre})
    if participante:
        return True
    else:
        return False

# Función para eliminar un participante
def eliminar_participante():
    nombre = input("Ingrese el nombre del participante a eliminar: ")
    if validar_nombre_participante(nombre):
        participantes.delete_one({"nombre": nombre})
        print(f"Participante '{nombre}' eliminado con éxito.\n")
    else:
        print(f"El participante '{nombre}' no existe en la base de datos.\n")

# Funciones CRUD para encuentros

# Función para insertar un encuentro
def insertar_encuentro():
    id = int(input("Ingrese el ID del encuentro: "))
    fecha = input("Ingrese la fecha del encuentro (YYYY-MM-DD): ")
    hora = input("Ingrese la hora del encuentro (HH:MM): ")
    participante1 = input("Ingrese el nombre del primer participante: ")
    participante2 = input("Ingrese el nombre del segundo participante: ")
    sets = []
    num_sets = int(input("Ingrese el número de sets: "))
    for i in range(num_sets):
        set_num = i + 1
        puntaje1 = int(input(f"Ingrese el puntaje del participante 1 en el set {set_num}: "))
        puntaje2 = int(input(f"Ingrese el puntaje del participante 2 en el set {set_num}: "))
        sets.append({f"Set{set_num}": {f"{participante1}S{set_num}": puntaje1, f"{participante2}S{set_num}": puntaje2}})
    
    encuentro = Encuentro(id, fecha, hora, participante1, participante2, sets)
    torneo.agregar_encuentro(encuentro)
    print("Encuentro insertado con éxito.\n")

# Función para leer todos los encuentros
def leer_encuentros():
    for encuentro in encuentros.find():
        print(encuentro)

# Función para actualizar un encuentro
def actualizar_encuentro():
    id = int(input("Ingrese el ID del encuentro a actualizar: "))
    nueva_fecha = input("Ingrese la nueva fecha (YYYY-MM-DD): ")
    nueva_hora = input("Ingrese la nueva hora (HH:MM): ")
    nuevo_participante1 = input("Ingrese el nuevo nombre del primer participante: ")
    nuevo_participante2 = input("Ingrese el nuevo nombre del segundo participante: ")
    sets = []
    num_sets = int(input("Ingrese el número de sets: "))
    for i in range(num_sets):
        set_num = i + 1
        puntaje1 = int(input(f"Ingrese el nuevo puntaje del participante 1 en el set {set_num}: "))
        puntaje2 = int(input(f"Ingrese el nuevo puntaje del participante 2 en el set {set_num}: "))
        sets.append({f"Set{set_num}": {f"{nuevo_participante1}S{set_num}": puntaje1, f"{nuevo_participante2}S{set_num}": puntaje2}})
    
    encuentros.update_one(
        {"id": id},
        {"$set": {"fecha": nueva_fecha, "hora": nueva_hora, "participante1": nuevo_participante1, "participante2": nuevo_participante2, "sets": sets}}
    )
    print("Encuentro actualizado con éxito.\n")

# Función para eliminar un encuentro
def eliminar_encuentro():
    id = int(input("Ingrese el ID del encuentro a eliminar: "))
    encuentros.delete_one({"id": id})
    print("Encuentro eliminado con éxito.\n")

# Funciones CRUD para resultados

# Función para insertar un resultado
def insertar_resultado():
    id = int(input("Ingrese el ID del resultado: "))
    encuentro = int(input("Ingrese el ID del encuentro: "))
    ganador = input("Ingrese el nombre del ganador: ")
    perdedor = input("Ingrese el nombre del perdedor: ")
    puntos_totales_ganador = int(input("Ingrese los puntos totales del ganador: "))
    puntos_totales_perdedor = int(input("Ingrese los puntos totales del perdedor: "))
    
    resultado = Resultado(id, encuentro, ganador, perdedor, puntos_totales_ganador, puntos_totales_perdedor)
    torneo.agregar_resultado(resultado)  # Agrega el resultado al torneo y a la base de datos
    print("Resultado insertado con éxito.\n")

# Función para leer todos los resultados
def leer_resultados():
    for resultado in resultados.find():
        print(resultado)

# Función para actualizar un resultado
def actualizar_resultado():
    id = int(input("Ingrese el ID del resultado a actualizar: "))
    nuevo_encuentro = int(input("Ingrese el nuevo ID del encuentro: "))
    nuevo_ganador = input("Ingrese el nuevo nombre del ganador: ")
    nuevo_perdedor = input("Ingrese el nuevo nombre del perdedor: ")
    nuevos_puntos_totales_ganador = int(input("Ingrese los nuevos puntos totales del ganador: "))
    nuevos_puntos_totales_perdedor = int(input("Ingrese los nuevos puntos totales del perdedor: "))
    
    resultados.update_one(
        {"id": id},
        {"$set": {"encuentro": nuevo_encuentro, "ganador": nuevo_ganador, "perdedor": nuevo_perdedor, "puntos_totales_ganador": nuevos_puntos_totales_ganador, "puntos_totales_perdedor": nuevos_puntos_totales_perdedor}}
    )
    print("Resultado actualizado con éxito.\n")

# Función para eliminar un resultado
def eliminar_resultado():
    id = int(input("Ingrese el ID del resultado a eliminar: "))
    resultados.delete_one({"id": id})
    print("Resultado eliminado con éxito.\n")

# Ejecución del programa
if __name__ == "__main__":
    while True:
        print("1. Insertar participante")
        print("2. Leer participantes")
        print("3. Actualizar participante")
        print("4. Eliminar participante")
        print("5. Insertar encuentro")
        print("6. Leer encuentros")
        print("7. Actualizar encuentro")
        print("8. Eliminar encuentro")
        print("9. Insertar resultado")
        print("10. Leer resultados")
        print("11. Actualizar resultado")
        print("12. Eliminar resultado")
        print("13. Salir")
        
        opcion = int(input("Seleccione una opción: "))
        
        if opcion == 1:
            insertar_participante()
        elif opcion == 2:
            leer_participantes()
        elif opcion == 3:
            actualizar_participante()
        elif opcion == 4:
            eliminar_participante()
        elif opcion == 5:
            insertar_encuentro()
        elif opcion == 6:
            leer_encuentros()
        elif opcion == 7:
            actualizar_encuentro()
        elif opcion == 8:
            eliminar_encuentro()
        elif opcion == 9:
            insertar_resultado()
        elif opcion == 10:
            leer_resultados()
        elif opcion == 11:
            actualizar_resultado()
        elif opcion == 12:
            eliminar_resultado()
        elif opcion == 13:
            break
        else:
            print("Opción no válida. Intente de nuevo.")