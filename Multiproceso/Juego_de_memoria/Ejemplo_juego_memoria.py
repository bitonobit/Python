# Nuestro juego de memoria tiene: 24 cartas = 12 parejas en total
# Las cartas podemos distribuirlas en un tablero imaginario (por ejemplo en una lista de longitud 24)
# En cada turno:
# El jugador uno "Escoge dos cartas" (dos posiciones de la lista)
# El proceso padre “voltea” las cartas
# Si son iguales → suma 1 punto al jugador uno y juega este de nuevo
# Si no son iguales → le pasa el turno al jugador dos
# El juego termina cuando todas las parejas han sido descubiertas y gana el jugador con más puntos
# IMPORTANTE: Hay que tener en cuenta que los jugadores son procesos hijos que se comunican con el proceso padre mediante Pipes y que no pueden ser ellos los que lean el input de las posiciones.
# ----------------------------------------------------------------------------------------------------
# En este ejemplo encontraras la implementación del juego de memoria utilizando procesos y Pipes en Python, para 3 parejas puedes servirte de él para crear tu propia versión con 12 parejas.
import random
from multiprocessing import Process, Pipe

def mostrar_tablero(cartas, estado_cartas):
    print("\nTablero actual:") # Muestra el estado actual del tablero
    for ind, carta in enumerate(cartas): # Recorre las cartas
        display = carta if estado_cartas[ind] else "■" # Muestra la carta si está descubierta, sino un símbolo
        print(f"{display}", end=" ") # Imprime la carta o símbolo
        if (ind + 1) % 6 == 0: # Salto de línea cada 6 cartas
            print("\n  ")         
    print("\n  ")

def proceso_padre():
    # 01. Crea el tablero y las cartas
    cartas = ["AZUL", "AZUL", "BLANCO", "BLANCO", "ROJO", "ROJO"]
    # 02. Desordenamos las cartas
    random.shuffle(cartas)
    # 02. Iniciamos el estado de las cartas (True = descubierta, False = oculta)
    estado_cartas = [False] * 6   # Todas ocultas para empezar
    # 03. Iniciamos los puntos de los jugadores
    puntos = [0, 0]  # En cero para empezar
    # 04. Creamos las tuberías
    conexion1_parent, conexion1_child = Pipe()  #tubería para el jugador 1
    conexion2_parent, conexion2_child = Pipe()  #tubería para el jugador 2
    # 05. Creamos los procesos hijos (jugadores)
    jugador1 = Process(target=proceso_hijo, args=(conexion1_child, 1)) 
    jugador2 = Process(target=proceso_hijo, args=(conexion2_child, 2)) 
    # 06. Iniciamos los procesos hijos
    jugador1.start()
    jugador2.start()
    #07. Establecemos el turno (0 = jugador 1, 1 = jugador 2)
    turno = 0
    # 08. Bucle principal del juego
    while sum(puntos) < 3:
        # 01. Mostramos el tablero 
        mostrar_tablero(cartas, estado_cartas)
        # 02. Mostramos el turno 
        print(f"Turno del Jugador {turno+1}") #Suma uno para mostrar 1 o 2 en lugar de 0 y 1
        while True:
            # 03. Pedimos las posiciones de las cartas a voltear
            try:
                i = int(input("Elige la primera carta (0-5): "))
                j = int(input("Elige la segunda carta (0-5): "))
                # 04. Validamos las posiciones
                if 0 <= i < 7 and 0 <= j < 7 and i != j and not estado_cartas[i] and not estado_cartas[j]:
                    # Si son válidas, salimos del bucle
                    break
                print("Posiciones inválidas o cartas ya encontradas.")
            except ValueError:
                print("Por favor, introduce posiciones válidas.")

        # 05. Enviamos el turno/jugada a los hijos para imprimir info
        if turno == 0:
            conexion = conexion1_parent
            id_jugador = 1
        else:
            conexion = conexion2_parent
            id_jugador = 2

        # Enviamos al hijo el turno y las posiciones elegidas
        conexion.send(("TURNO", id_jugador, i, j))
        acierto = False
        if cartas[i] == cartas[j]:
            acierto = True
            estado_cartas[i] = True
            estado_cartas[j] = True
            puntos[turno] += 1
        else:
            turno = 1 - turno
        # Enviamos el resultado del volteo de las cartas al jugador
        conexion.send({"VOLTEO": (i, j, acierto, cartas[i], cartas[j])})

    # 09. Fin del juego, enviamos resultados a ambos jugadores
    resultado_final = {
        "PUNTUACION": puntos,
        "GANADOR": 1 if puntos[0] > puntos[1] else 2 if puntos[1] > puntos[0] else 0
    }
    # 10. Enviamos el resultado final a ambos jugadores
    conexion1_parent.send(resultado_final)
    conexion2_parent.send(resultado_final)
    # 11. Esperamos a que los procesos hijos terminen
    jugador1.join()
    jugador2.join()


def proceso_hijo(conexion, id_jugador):
    while True:
        mensaje = conexion.recv()
        # Espera turno y muestra jugada, pero NUNCA pide input
        if type(mensaje) is tuple and mensaje[0] == "TURNO":
            _, id_turno, i, j = mensaje # Desempaquetamos el mensaje
            if id_turno == id_jugador:
                print(f"\n Jugador {id_jugador}, es tu turno.")
                print(f"\n Has elegido las posiciones {i} y {j}. Esperando resultado...")
        elif type(mensaje) is dict and "VOLTEO" in mensaje:
            i, j, acierto, carta1, carta2 = mensaje["VOLTEO"]
            if acierto:
                print(f"\n ✅¡Has acertado! Las posiciones {i}-{j} eran ambas {carta1}.")
            else:
                print(f"\n ❌ No has acertado, posiciones {i}: {carta1} y {j}: {carta2} no son pareja.")
        elif type(mensaje) is dict and "PUNTUACION" in mensaje:
            resultado_final = mensaje
            print("\n🏁 El juego ha terminado."
                  f"\n   Jugador 1: {resultado_final['PUNTUACION'][0]} puntos"
                  f"\n   Jugador 2: {resultado_final['PUNTUACION'][1]} puntos"
                  f"\n   Ganador: {'Jugador ' + str(resultado_final['GANADOR']) if resultado_final['GANADOR'] != 0 else 'Empate'}"
                  )
            break

if __name__ == "__main__":
    proceso_padre()
