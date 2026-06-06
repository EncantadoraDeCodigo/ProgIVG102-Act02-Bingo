"""
Clase Juego: director de la partida de bingo.

Relación con Bombo: COMPOSICIÓN
El Bombo se crea INTERNAMENTE en el constructor del Juego.

Relación con Jugador: ASOCIACIÓN
El Juego CONOCE a los jugadores pero no los crea ni los destruye.

Principios SOLID aplicados:
  SRP — Juego solo orquesta la partida. La presentación del reporte final fue
        trasladada a ReportePartida (una sola razón para cambiar cada clase).
  OCP — Ya no importa CartonDoble: tipo_nombre() en ICarton elimina el isinstance.
  DIP — No depende de CartonDoble (clase concreta de bajo nivel) para su lógica.
"""
from __future__ import annotations
from typing import List, Optional
from bombo import Bombo
from jugador import Jugador


class Juego:
    """Modela la partida de bingo completa."""

    def __init__(self, palabra: str, numero_maximo: int) -> None:
        if not isinstance(palabra, str) or len(palabra.strip()) == 0:
            raise ValueError("La palabra no puede estar vacía.")
        if not isinstance(numero_maximo, int):
            raise TypeError("El número máximo debe ser un entero.")

        self.palabra: str = palabra.upper()
        self.numero_maximo: int = numero_maximo
        self.turno_actual: int = 0
        self.ganador: Optional[Jugador] = None
        self.finalizado: bool = False

        # ◆ COMPOSICIÓN: el Bombo nace y muere con el Juego
        self.__bombo: Bombo = Bombo(numero_maximo)

        # ASOCIACIÓN: jugadores que se registran desde fuera
        self._jugadores: List[Jugador] = []

    # --- Getters para que ReportePartida acceda al estado sin romper encapsulamiento ---

    def get_historial_bombo(self) -> List[int]:
        """Expone el historial del bombo sin revelar la instancia interna."""
        return self.__bombo.get_historial()

    def get_jugadores(self) -> List[Jugador]:
        """Retorna la lista de jugadores registrados."""
        return self._jugadores

    # --- Gestión de jugadores ---

    def registrar_jugador(self, jugador: Jugador) -> None:
        """Registra un jugador en la partida (no lo crea, solo lo asocia)."""
        if jugador is None:
            raise ValueError("El jugador no puede ser None.")
        if not isinstance(jugador, Jugador):
            raise TypeError("El objeto recibido no es un Jugador válido.")
        if self.finalizado:
            raise RuntimeError("No se pueden registrar jugadores: el juego ya terminó.")
        if len(jugador.get_cartones()) == 0:
            raise ValueError(f"El jugador '{jugador.nombre}' no tiene cartones asignados.")
        self._jugadores.append(jugador)
        print(f"Jugador '{jugador.nombre}' registrado en la partida.")

    def retirar_jugador(self, nombre: str) -> Optional[Jugador]:
        """Retira un jugador por su nombre y lo devuelve (sigue existiendo)."""
        if not isinstance(nombre, str) or len(nombre.strip()) == 0:
            raise ValueError("El nombre del jugador no puede estar vacío.")
        for i in range(len(self._jugadores)):
            if self._jugadores[i].nombre == nombre:
                jugador: Jugador = self._jugadores.pop(i)
                print(f"Jugador '{jugador.nombre}' se retiró de la partida.")
                return jugador
        print(f"No se encontró un jugador con el nombre '{nombre}'.")
        return None

    # --- Lógica de partida ---

    def ejecutar_turno(self) -> Optional[int]:
        """Extrae un número y notifica a todos los jugadores. Retorna el número o None."""
        if self.finalizado:
            print("El juego ya terminó.")
            return None
        if not self.__bombo.quedan_numeros():
            print("No quedan números en el bombo.")
            self.finalizado = True
            return None
        if len(self._jugadores) == 0:
            raise RuntimeError("No hay jugadores registrados para ejecutar un turno.")

        self.turno_actual += 1
        numero: int = self.__bombo.extraer_numero()
        print(f"\n=== TURNO {self.turno_actual} === Número extraído: {numero}")

        for jugador in self._jugadores:
            if jugador.marcar_numero(numero):
                print(f"  -> {jugador.nombre} marcó el número {numero}")

        for jugador in self._jugadores:
            if jugador.verificar_bingo():
                self.ganador = jugador
                self.finalizado = True
                print(f"\n¡¡¡ {jugador.nombre} ha ganado el BINGO !!!")
                return numero

        return numero

    def ejecutar_partida(self) -> None:
        """Ejecuta la partida turno a turno hasta que alguien gane o se agoten los números."""
        if len(self._jugadores) == 0:
            raise RuntimeError("No se puede iniciar la partida sin jugadores registrados.")
        while not self.finalizado and self.__bombo.quedan_numeros():
            self.ejecutar_turno()
        if self.ganador is None:
            print("\nLa partida terminó sin ganador.")

    def __str__(self) -> str:
        estado: str = "Finalizado" if self.finalizado else "En curso"
        return (
            f"Juego [{self.palabra}] — Estado: {estado}, "
            f"Jugadores: {len(self._jugadores)}, Turno: {self.turno_actual}"
        )
