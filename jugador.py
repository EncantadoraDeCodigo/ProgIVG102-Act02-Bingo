"""
Clase Jugador: representa un jugador de bingo que posee cartones.

Relación con Cartón: AGREGACIÓN ◇
El jugador TIENE cartones, pero los cartones se crean FUERA del jugador
y se le asignan mediante agregar_carton(). Si el jugador desaparece,
los cartones siguen existiendo y pueden ser reasignados.
"""
from __future__ import annotations
from typing import List
from carton import Carton


class Jugador:
    """Modela un jugador de bingo con sus cartones."""

    def __init__(self, nombre: str) -> None:
        """
        Constructor del jugador.
        nombre: nombre del jugador
        """
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser una cadena de texto.")
        if len(nombre) == 0:
            raise ValueError("El nombre no puede estar vacío.")

        self.nombre: str = nombre
        # ◇ Lista vacía: el Jugador no crea Cartones, los recibe
        self._cartones: List[Carton] = []
        self._total_marcados: int = 0

    def agregar_carton(self, carton: Carton) -> None:
        """Agrega un cartón al jugador (el cartón ya existe, se pasa desde fuera)."""
        self._cartones.append(carton)

    def retirar_carton(self, indice: int) -> Carton:
        """
        Retira un cartón por su índice y lo DEVUELVE.
        El cartón sigue existiendo (agregación).
        """
        if indice < 0 or indice >= len(self._cartones):
            raise ValueError("Índice de cartón no válido.")
        return self._cartones.pop(indice)

    def marcar_numero(self, numero: int) -> bool:
        """
        Marca un número en todos los cartones del jugador.
        Retorna True si al menos un cartón tenía ese número.
        """
        encontrado: bool = False
        for carton in self._cartones:
            if carton.marcar_numero(numero):
                self._total_marcados += 1
                encontrado = True
        return encontrado

    def verificar_bingo(self) -> bool:
        """Verifica si alguno de los cartones tiene bingo."""
        for carton in self._cartones:
            if carton.verificar_bingo():
                return True
        return False

    def get_total_marcados(self) -> int:
        """Retorna el total de números marcados durante la partida."""
        return self._total_marcados

    def get_cartones(self) -> List[Carton]:
        """Retorna la lista de cartones del jugador."""
        return self._cartones

    def __str__(self) -> str:
        return f"Jugador '{self.nombre}' — Cartones: {len(self._cartones)}"