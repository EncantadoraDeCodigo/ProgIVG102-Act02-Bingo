"""
Script principal de demostración del Sistema de Bingo.
Instancia un juego con 3 jugadores, reparte cartones
(incluyendo un CartónDoble), y ejecuta la partida.
"""
from carton import Carton
from carton_doble import CartonDoble
from jugador import Jugador
from juego import Juego


def main() -> None:
    # Parámetros del juego
    palabra: str = "BINGO"
    numero_maximo: int = 75

    # Los cartones se crean FUERA de los jugadores (agregación)
    carton1: Carton = Carton(palabra, numero_maximo)
    carton2: Carton = Carton(palabra, numero_maximo)
    carton3: Carton = Carton(palabra, numero_maximo)
    carton4: CartonDoble = CartonDoble(palabra, numero_maximo)
    carton5: Carton = Carton(palabra, numero_maximo)

    # Los jugadores se crean FUERA del juego (asociación)
    jugador1: Jugador = Jugador("Ana")
    jugador2: Jugador = Jugador("Carlos")
    jugador3: Jugador = Jugador("María")

    # Repartir cartones a los jugadores (agregación ◇)
    jugador1.agregar_carton(carton1)
    jugador1.agregar_carton(carton2)

    jugador2.agregar_carton(carton3)
    jugador2.agregar_carton(carton4)   # Carlos tiene un cartón doble

    jugador3.agregar_carton(carton5)

    # El juego crea el bombo internamente (composición ◆)
    juego: Juego = Juego(palabra, numero_maximo)

    # Registrar jugadores en el juego (asociación)
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
            tipo: str = "CartónDoble" if isinstance(carton, CartonDoble) else "Cartón"
            print(f"\n  Cartón {idx + 1} ({tipo}):")
            print(carton)

    # Ejecutar la partida
    print("\n" + "=" * 50)
    print("        INICIO DE LA PARTIDA")
    print("=" * 50)

    juego.ejecutar_partida()

    # Reporte final
    juego.generar_reporte()


if __name__ == "__main__":
    main()