"""
Clase Bombo: mecanismo de extracción de números del bingo.

Relación con Juego: COMPOSICIÓN ◆
El Bombo es creado INTERNAMENTE por el Juego en su constructor.
No puede existir sin el Juego. Si el Juego se destruye, el Bombo
también desaparece. Su ciclo de vida está completamente ligado al Juego.
"""
from __future__ import annotations
import random
from typing import List


class Bombo:
    """Modela el bombo que extrae números aleatorios sin repetición.

    Relación con Juego: COMPOSICIÓN ◆ — el Bombo se crea internamente
    en el constructor de Juego y su ciclo de vida está ligado al de éste.
    """

    def __init__(self, numero_maximo: int) -> None:
        """
        Constructor del bombo.
        numero_maximo: el número más alto que puede salir (ej: 75).
        Debe ser un entero entre 50 y 90, múltiplo de 5.
        """
        if not isinstance(numero_maximo, int):
            raise ValueError("El número máximo debe ser un entero.")
        if numero_maximo < 50 or numero_maximo > 90:
            raise ValueError("El número máximo debe estar entre 50 y 90.")
        if numero_maximo % 5 != 0:
            raise ValueError("El número máximo debe ser múltiplo de 5.")

        self.numero_maximo: int = numero_maximo
        self._disponibles: List[int] = list(range(1, numero_maximo + 1))
        self._historial: List[int] = []

    def extraer_numero(self) -> int:
        """
        Extrae un número aleatorio de los disponibles.
        Lo quita de la lista y lo agrega al historial.
        """
        if len(self._disponibles) == 0:
            raise ValueError("No quedan números en el bombo.")

        numero: int = random.choice(self._disponibles)
        self._disponibles.remove(numero)
        self._historial.append(numero)
        return numero

    def quedan_numeros(self) -> bool:
        """Retorna True si aún quedan números por extraer."""
        return len(self._disponibles) > 0

    def get_historial(self) -> List[int]:
        """Retorna la lista de números extraídos hasta ahora."""
        return self._historial

    def __str__(self) -> str:
        return (
            f"Bombo (máx: {self.numero_maximo}) — "
            f"Extraídos: {len(self._historial)}, "
            f"Disponibles: {len(self._disponibles)}"
        )