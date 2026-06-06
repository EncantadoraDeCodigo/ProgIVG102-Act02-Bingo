"""
Clase Jugador: representa un jugador de bingo que posee cartones.

Relación con ICarton: AGREGACIÓN sobre abstracción.
El jugador TIENE cartones (ICarton), pero los cartones se crean FUERA del jugador
y se le asignan mediante agregar_carton().

Principios SOLID aplicados:
  DIP — Jugador depende de ICarton (abstracción), no de la clase concreta Carton.
        Puede recibir Carton, CartonDoble, o cualquier futura implementación.
  ISP — Jugador usa solo los métodos que ICarton define (marcar, verificar, contar).
"""
from __future__ import annotations
from typing import List
from icarton import ICarton


class Jugador:
    """Modela un jugador de bingo con sus cartones."""

    def __init__(self, nombre: str) -> None:
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser una cadena de texto.")
        if len(nombre.strip()) == 0:
            raise ValueError("El nombre no puede estar vacío.")

        self.nombre: str = nombre.strip()
        self._cartones: List[ICarton] = []
        self._total_marcados: int = 0

    def agregar_carton(self, carton: ICarton) -> None:
        """Agrega un cartón al jugador. El cartón ya existe, se pasa desde fuera."""
        if carton is None:
            raise ValueError("El cartón no puede ser None.")
        if not isinstance(carton, ICarton):
            raise TypeError("El objeto recibido no es un cartón válido (ICarton).")
        self._cartones.append(carton)

    def retirar_carton(self, indice: int) -> ICarton:
        """Retira un cartón por su índice y lo devuelve (el cartón sigue existiendo)."""
        if not isinstance(indice, int):
            raise TypeError("El índice debe ser un entero.")
        if indice < 0 or indice >= len(self._cartones):
            raise IndexError(f"Índice {indice} fuera de rango. El jugador tiene {len(self._cartones)} cartón(es).")
        return self._cartones.pop(indice)

    def marcar_numero(self, numero: int) -> bool:
        """Marca un número en todos los cartones. Retorna True si al menos uno lo tenía."""
        if not isinstance(numero, int):
            raise TypeError("El número a marcar debe ser un entero.")
        encontrado: bool = False
        for carton in self._cartones:
            if carton.marcar_numero(numero):
                self._total_marcados += 1
                encontrado = True
        return encontrado

    def verificar_bingo(self) -> bool:
        """Verifica si alguno de los cartones tiene bingo."""
        return any(carton.verificar_bingo() for carton in self._cartones)

    def get_total_marcados(self) -> int:
        """Retorna el total de números marcados durante la partida."""
        return self._total_marcados

    def get_cartones(self) -> List[ICarton]:
        """Retorna la lista de cartones del jugador."""
        return self._cartones

    def __str__(self) -> str:
        return f"Jugador '{self.nombre}' — Cartones: {len(self._cartones)}"
