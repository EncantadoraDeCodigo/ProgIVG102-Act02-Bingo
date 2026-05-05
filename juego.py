"""
Clase Juego: director de la partida de bingo.

Relación con Bombo: COMPOSICIÓN ◆
El Bombo se crea INTERNAMENTE en el constructor del Juego.
El código externo nunca crea un Bombo directamente.
Si el Juego se destruye, el Bombo también desaparece.

Relación con Jugador: ASOCIACIÓN
El Juego CONOCE a los jugadores pero no los crea ni los destruye.
Los jugadores se registran voluntariamente y pueden retirarse.
Son entidades completamente independientes.
"""
from __future__ import annotations
from typing import List, Optional
from bombo import Bombo
from jugador import Jugador
from carton_doble import CartonDoble


class Juego:
    """Modela la partida de bingo completa."""

    def __init__(self, palabra: str, numero_maximo: int) -> None:
        """
        Constructor del juego.
        palabra: la palabra del bingo (ej: BINGO)
        numero_maximo: número máximo del juego (ej: 75)
        """
        self.palabra: str = palabra.upper()
        self.numero_maximo: int = numero_maximo
        self.turno_actual: int = 0
        self.ganador: Optional[Jugador] = None
        self.finalizado: bool = False

        # ◆ COMPOSICIÓN: el Bombo nace aquí dentro del Juego
        self.__bombo: Bombo = Bombo(numero_maximo)

        # ASOCIACIÓN: lista de jugadores que se registran desde fuera
        self._jugadores: List[Jugador] = []

    def registrar_jugador(self, jugador: Jugador) -> None:
        """Registra un jugador en la partida (asociación, no lo crea)."""
        if self.finalizado:
            raise ValueError("No se pueden registrar jugadores, el juego terminó.")
        self._jugadores.append(jugador)
        print(f"Jugador '{jugador.nombre}' registrado en la partida.")

    def retirar_jugador(self, nombre: str) -> Optional[Jugador]:
        """
        Retira un jugador por su nombre y lo DEVUELVE.
        El jugador sigue existiendo (asociación).
        """
        for i in range(len(self._jugadores)):
            if self._jugadores[i].nombre == nombre:
                jugador: Jugador = self._jugadores.pop(i)
                print(f"Jugador '{jugador.nombre}' se retiró de la partida.")
                return jugador
        print(f"No se encontró un jugador con el nombre '{nombre}'.")
        return None

    def ejecutar_turno(self) -> Optional[int]:
        """
        Ejecuta un turno: extrae un número del bombo y notifica a todos.
        Retorna el número extraído, o None si el juego ya terminó.
        """
        if self.finalizado:
            print("El juego ya terminó.")
            return None

        if not self.__bombo.quedan_numeros():
            print("No quedan números en el bombo.")
            self.finalizado = True
            return None

        if len(self._jugadores) == 0:
            print("No hay jugadores registrados.")
            return None

        # Extraer número del bombo
        self.turno_actual += 1
        numero: int = self.__bombo.extraer_numero()
        print(f"\n=== TURNO {self.turno_actual} === Número extraído: {numero}")

        # Notificar a cada jugador
        for jugador in self._jugadores:
            if jugador.marcar_numero(numero):
                print(f"  -> {jugador.nombre} marcó el número {numero}")

        # Verificar si alguien ganó
        for jugador in self._jugadores:
            if jugador.verificar_bingo():
                self.ganador = jugador
                self.finalizado = True
                print(f"\n¡¡¡ {jugador.nombre} ha ganado el BINGO !!!")
                return numero

        return numero

    def ejecutar_partida(self) -> None:
        """Ejecuta la partida turno a turno hasta que alguien gane."""
        while not self.finalizado and self.__bombo.quedan_numeros():
            self.ejecutar_turno()

        if self.ganador is None:
            print("\nLa partida terminó sin ganador.")

    def generar_reporte(self) -> None:
        """Genera un reporte final de la partida."""
        print("\n" + "=" * 50)
        print("         REPORTE FINAL DE LA PARTIDA")
        print("=" * 50)
        print(f"Palabra: {self.palabra}")
        print(f"Número máximo: {self.numero_maximo}")
        print(f"Turnos jugados: {self.turno_actual}")

        if self.ganador is not None:
            print(f"Ganador: {self.ganador.nombre}")
        else:
            print("No hubo ganador.")

        print(f"\nNúmeros extraídos: {self.__bombo.get_historial()}")

        print("\n--- Estadísticas por jugador ---")
        for jugador in self._jugadores:
            print(f"  {jugador.nombre}: {jugador.get_total_marcados()} números marcados")
            for idx, carton in enumerate(jugador.get_cartones()):
                tipo: str = "CartónDoble" if isinstance(carton, CartonDoble) else "Cartón"
                print(f"    Cartón {idx + 1} ({tipo}): {carton.contar_marcados()} marcados")

        print("=" * 50)

    def __str__(self) -> str:
        estado: str = "Finalizado" if self.finalizado else "En curso"
        return (
            f"Juego [{self.palabra}] — Estado: {estado}, "
            f"Jugadores: {len(self._jugadores)}, Turno: {self.turno_actual}"
        )