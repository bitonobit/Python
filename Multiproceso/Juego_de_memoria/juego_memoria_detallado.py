"""
JUEGO DE MEMORIA CON MULTIPROCESO EN PYTHON
============================================

Descripción:
- 24 cartas = 12 parejas
- 2 jugadores (2 procesos hijos)
- 1 proceso padre que controla el juego

Funcionamiento:
- Cada jugador es un proceso hijo independiente
- El proceso padre gestiona el tablero, turnos y puntuación
- Comunicación mediante Pipes (tuberías bidireccionales)
- Si un jugador encuentra pareja, juega de nuevo
- Gana quien tenga más puntos al finalizar
"""

import multiprocessing
import random
import time
import os


class JuegoMemoria:
    """Clase que encapsula la lógica del juego de memoria."""

    def __init__(self):
        """Inicializa el juego con 24 cartas (12 parejas)."""
        self.NUM_CARTAS = 24
        self.NUM_PAREJAS = 12

        # Crear tablero: valores del 1 al 12, duplicados y barajados
        self.cartas = list(range(1, self.NUM_PAREJAS + 1)) * 2
        random.shuffle(self.cartas)

        # Estado de cada carta: False = oculta, True = conseguida
        self.cartas_conseguidas = [False] * self.NUM_CARTAS

        # Puntuación de cada jugador
        self.puntos = [0, 0]

        # Turno actual (0 = Jugador 1, 1 = Jugador 2)
        self.turno_actual = 0

    def obtener_tablero_visual(self):
        """
        Retorna una representación visual del tablero.
        'O' = oculta, 'C' = conseguida
        """
        return ['C' if conseguida else 'O' 
                for conseguida in self.cartas_conseguidas]

    def todas_parejas_encontradas(self):
        """Verifica si todas las parejas han sido encontradas."""
        return all(self.cartas_conseguidas)

    def voltear_cartas(self, pos1, pos2):
        """
        Voltea dos cartas y verifica si forman pareja.

        Returns:
            tuple: (son_pareja: bool, valor1: int, valor2: int)
        """
        valor1 = self.cartas[pos1]
        valor2 = self.cartas[pos2]
        son_pareja = valor1 == valor2

        if son_pareja:
            # Marcar cartas como conseguidas
            self.cartas_conseguidas[pos1] = True
            self.cartas_conseguidas[pos2] = True
            # Sumar punto al jugador actual
            self.puntos[self.turno_actual] += 1
        else:
            # Cambiar turno si no son pareja
            self.turno_actual = (self.turno_actual + 1) % 2

        return son_pareja, valor1, valor2

    def cartas_validas(self, pos1, pos2):
        """Verifica si las posiciones son válidas y no están conseguidas."""
        # Verificar rango
        if not (0 <= pos1 < self.NUM_CARTAS and 0 <= pos2 < self.NUM_CARTAS):
            return False

        # Verificar que sean diferentes
        if pos1 == pos2:
            return False

        # Verificar que no estén ya conseguidas
        if self.cartas_conseguidas[pos1] or self.cartas_conseguidas[pos2]:
            return False

        return True

    def obtener_ganador(self):
        """
        Retorna el ganador del juego.

        Returns:
            int: 1 si gana jugador 1, 2 si gana jugador 2, 0 si empate
        """
        if self.puntos[0] > self.puntos[1]:
            return 1
        elif self.puntos[1] > self.puntos[0]:
            return 2
        else:
            return 0


def proceso_jugador(jugador_id, pipe_hijo, pipe_oponente):
    """
    Proceso hijo que representa a un jugador.

    Args:
        jugador_id (int): ID del jugador (1 o 2)
        pipe_hijo (Connection): Tubería para comunicarse con el padre
        pipe_oponente (Connection): Tubería del oponente (se cierra)
    """
    # Cerrar extremo de tubería que no necesitamos
    pipe_oponente.close()

    print(f"[PROCESO HIJO {jugador_id}] Iniciado (PID: {os.getpid()})")

    while True:
        # Esperar mensaje del padre
        try:
            mensaje = pipe_hijo.recv()
        except EOFError:
            # El padre cerró la conexión
            break

        if mensaje['tipo'] == 'TU_TURNO':
            # Es nuestro turno
            print(f"\n{'='*60}")
            print(f"JUGADOR {jugador_id} - ES TU TURNO")
            print(f"{'='*60}")
            print(f"Tablero: {mensaje['tablero']}")
            print(f"Tus puntos: {mensaje['puntos'][jugador_id-1]} | "
                  f"Rival: {mensaje['puntos'][(jugador_id % 2)]} puntos")
            print(f"{'='*60}")

            # Solicitar elección de cartas
            while True:
                try:
                    entrada = input(f"JUGADOR {jugador_id}: Elige 2 cartas (ej: 5 12): ")
                    partes = entrada.strip().split()

                    if len(partes) != 2:
                        print("Debes ingresar exactamente 2 números.")
                        continue

                    carta1 = int(partes[0])
                    carta2 = int(partes[1])

                    # Validación básica
                    if 0 <= carta1 < 24 and 0 <= carta2 < 24 and carta1 != carta2:
                        break
                    else:
                        print("Las cartas deben ser diferentes y estar entre 0 y 23.")
                except ValueError:
                    print("Por favor, ingresa números válidos.")
                except KeyboardInterrupt:
                    print("\nSaliendo...")
                    pipe_hijo.send({'tipo': 'SALIR'})
                    pipe_hijo.close()
                    return

            # Enviar elección al padre
            pipe_hijo.send({
                'tipo': 'ELECCION',
                'carta1': carta1,
                'carta2': carta2
            })

        elif mensaje['tipo'] == 'FIN_JUEGO':
            # Juego terminado
            print(f"\n{'='*60}")
            print(f"JUGADOR {jugador_id} - JUEGO TERMINADO")
            print(f"{'='*60}")
            print(f"Tu puntuación final: {mensaje['puntos'][jugador_id-1]} puntos")
            print(f"Puntuación rival: {mensaje['puntos'][(jugador_id % 2)]} puntos")

            ganador = mensaje['ganador']
            if ganador == jugador_id:
                print(f"\n🎉 ¡FELICIDADES! ¡HAS GANADO! 🎉")
            elif ganador == 0:
                print(f"\n🤝 ¡EMPATE! 🤝")
            else:
                print(f"\n😔 Has perdido. ¡Mejor suerte la próxima vez!")
            print(f"{'='*60}\n")

            # Cerrar conexión y terminar
            pipe_hijo.close()
            break


def proceso_padre():
    """
    Proceso padre que gestiona el juego completo.
    """
    print(f"[PROCESO PADRE] Iniciado (PID: {os.getpid()})")

    # Crear instancia del juego
    juego = JuegoMemoria()

    # Crear tuberías (Pipes) para comunicación bidireccional
    pipe_padre1, pipe_hijo1 = multiprocessing.Pipe()
    pipe_padre2, pipe_hijo2 = multiprocessing.Pipe()

    # Crear procesos hijos (jugadores)
    print("[PROCESO PADRE] Creando jugadores...")
    jugador1 = multiprocessing.Process(
        target=proceso_jugador,
        args=(1, pipe_hijo1, pipe_hijo2),
        name="Jugador-1"
    )
    jugador2 = multiprocessing.Process(
        target=proceso_jugador,
        args=(2, pipe_hijo2, pipe_hijo1),
        name="Jugador-2"
    )

    # Iniciar procesos hijos
    jugador1.start()
    jugador2.start()

    # Cerrar extremos que no usa el padre
    pipe_hijo1.close()
    pipe_hijo2.close()

    # Lista de pipes para acceso fácil
    pipes = [pipe_padre1, pipe_padre2]

    # Mostrar introducción
    print("\n" + "="*60)
    print("🎮 JUEGO DE MEMORIA - MULTIPROCESO 🎮")
    print("="*60)
    print(f"Cartas: {juego.NUM_CARTAS} (12 parejas)")
    print(f"Jugadores: 2")
    print("\nReglas:")
    print("  • Cada turno, elige 2 cartas por su posición (0-23)")
    print("  • Si coinciden: +1 punto y vuelves a jugar")
    print("  • Si no coinciden: pasa el turno al otro jugador")
    print("  • Gana quien tenga más puntos al final")
    print("="*60 + "\n")

    time.sleep(2)

    # Bucle principal del juego
    while not juego.todas_parejas_encontradas():
        # Preparar mensaje para el jugador actual
        mensaje = {
            'tipo': 'TU_TURNO',
            'tablero': juego.obtener_tablero_visual(),
            'puntos': juego.puntos.copy()
        }

        # Enviar turno al jugador actual
        pipes[juego.turno_actual].send(mensaje)

        # Recibir elección del jugador
        try:
            respuesta = pipes[juego.turno_actual].recv()
        except EOFError:
            print("[PROCESO PADRE] Error: jugador desconectado")
            break

        if respuesta['tipo'] == 'SALIR':
            print("[PROCESO PADRE] Juego interrumpido por el usuario")
            break

        carta1 = respuesta['carta1']
        carta2 = respuesta['carta2']

        # Validar elección
        if not juego.cartas_validas(carta1, carta2):
            print(f"\n[PADRE] ⚠️ Cartas inválidas o ya conseguidas. "
                  f"Jugador {juego.turno_actual + 1} pierde el turno.")
            juego.turno_actual = (juego.turno_actual + 1) % 2
            time.sleep(1)
            continue

        # Voltear cartas
        print(f"\n[PADRE] 🔄 Volteando cartas {carta1} y {carta2}...")
        son_pareja, valor1, valor2 = juego.voltear_cartas(carta1, carta2)

        print(f"[PADRE] Carta {carta1} = {valor1}")
        print(f"[PADRE] Carta {carta2} = {valor2}")

        if son_pareja:
            print(f"[PADRE] ✅ ¡PAREJA! Jugador {juego.turno_actual + 1} "
                  f"suma 1 punto (total: {juego.puntos[juego.turno_actual]})")
        else:
            print(f"[PADRE] ❌ No coinciden. "
                  f"Turno para Jugador {juego.turno_actual + 1}")

        time.sleep(1.5)

    # Juego terminado
    ganador = juego.obtener_ganador()

    print("\n" + "="*60)
    print("🏁 TODAS LAS PAREJAS ENCONTRADAS 🏁")
    print("="*60)
    print(f"Puntuación final:")
    print(f"  Jugador 1: {juego.puntos[0]} puntos")
    print(f"  Jugador 2: {juego.puntos[1]} puntos")

    if ganador == 1:
        print(f"\n👑 ¡GANADOR: JUGADOR 1! 👑")
    elif ganador == 2:
        print(f"\n👑 ¡GANADOR: JUGADOR 2! 👑")
    else:
        print(f"\n🤝 ¡EMPATE! 🤝")
    print("="*60 + "\n")

    # Notificar fin a ambos jugadores
    for pipe in pipes:
        try:
            pipe.send({
                'tipo': 'FIN_JUEGO',
                'puntos': juego.puntos,
                'ganador': ganador
            })
        except:
            pass

    # Esperar a que terminen los procesos hijos
    print("[PROCESO PADRE] Esperando a que terminen los jugadores...")
    jugador1.join(timeout=5)
    jugador2.join(timeout=5)

    # Cerrar tuberías
    pipe_padre1.close()
    pipe_padre2.close()

    print("[PROCESO PADRE] Juego finalizado correctamente.\n")


if __name__ == '__main__':
    # Configurar método de inicio (importante en Windows)
    multiprocessing.set_start_method('spawn', force=True)

    try:
        proceso_padre()
    except KeyboardInterrupt:
        print("\n\nJuego interrumpido por el usuario.")
    except Exception as e:
        print(f"\nError inesperado: {e}")
