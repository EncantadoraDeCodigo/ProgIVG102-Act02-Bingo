"""
Script principal de demostración del Sistema de Bingo.
Instancia un juego con 3 jugadores, reparte cartones
(incluyendo un CartónDoble), y ejecuta la partida.

Manejo de excepciones: todos los errores de configuración y ejecución
son capturados y reportados sin detener abruptamente el programa.
"""
from carton import Carton
from carton_doble import CartonDoble
from jugador import Jugador
from juego import Juego
from reporte_partida import ReportePartida


def main() -> None:
    try:
        palabra: str = "BINGO"
        numero_maximo: int = 75

        # Crear cartones (existen independientemente de los jugadores — agregación)
        carton1: Carton = Carton(palabra, numero_maximo)
        carton2: Carton = Carton(palabra, numero_maximo)
        carton3: Carton = Carton(palabra, numero_maximo)
        carton4: CartonDoble = CartonDoble(palabra, numero_maximo)
        carton5: Carton = Carton(palabra, numero_maximo)

        # Crear jugadores (existen independientemente del juego — asociación)
        jugador1: Jugador = Jugador("Luisa")
        jugador2: Jugador = Jugador("Victoria")
        jugador3: Jugador = Jugador("Daniel")

        # Repartir cartones (agregación: el jugador usa el cartón, no lo crea)
        jugador1.agregar_carton(carton1)
        jugador1.agregar_carton(carton2)

        jugador2.agregar_carton(carton3)
        jugador2.agregar_carton(carton4)

        jugador3.agregar_carton(carton5)

        # El juego crea el bombo internamente (composición)
        juego: Juego = Juego(palabra, numero_maximo)

        juego.registrar_jugador(jugador1)
        juego.registrar_jugador(jugador2)
        juego.registrar_jugador(jugador3)

        # Mostrar cartones antes de empezar
        print("\n" + "=" * 50)
        print("        CARTONES DE CADA JUGADOR")
        print("=" * 50)

        for jugador in [jugador1, jugador2, jugador3]:
            print(f"\n--- {jugador.nombre} ---")
            for idx, carton in enumerate(jugador.get_cartones()):
                # OCP: tipo_nombre() en lugar de isinstance(carton, CartonDoble)
                print(f"\n  Cartón {idx + 1} ({carton.tipo_nombre()}):")
                print(carton)

        # Ejecutar la partida
        print("\n" + "=" * 50)
        print("        INICIO DE LA PARTIDA")
        print("=" * 50)

        juego.ejecutar_partida()

        # SRP: el reporte lo genera ReportePartida, no Juego
        reporte: ReportePartida = ReportePartida()
        reporte.generar(juego)

    except (ValueError, TypeError) as error:
        print(f"\n[ERROR DE CONFIGURACIÓN] {error}")
    except RuntimeError as error:
        print(f"\n[ERROR DE PARTIDA] {error}")
    except Exception as error:
        print(f"\n[ERROR INESPERADO] {error}")


if __name__ == "__main__":
    main()
