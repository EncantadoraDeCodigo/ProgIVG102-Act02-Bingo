"""
Interfaz ICarton: contrato que todo cartón de bingo debe cumplir.

Principios SOLID aplicados:
  ISP — Define una interfaz cohesiva y mínima para cartones.
  DIP — Jugador y Juego dependen de esta abstracción, no de la clase concreta Carton.
"""
from abc import ABC, abstractmethod


class ICarton(ABC):
    """Contrato que todo cartón de bingo debe cumplir."""

    @abstractmethod
    def marcar_numero(self, numero: int) -> bool:
        """Marca un número en el cartón. Retorna True si lo encontró."""

    @abstractmethod
    def verificar_bingo(self) -> bool:
        """Retorna True si el cartón tiene bingo."""

    @abstractmethod
    def contar_marcados(self) -> int:
        """Retorna cuántos números han sido marcados."""

    @abstractmethod
    def tipo_nombre(self) -> str:
        """Retorna el nombre del tipo de cartón.
        OCP: evita isinstance() en código externo al agregar nuevos tipos."""

    @abstractmethod
    def __str__(self) -> str:
        """Representación en texto del cartón."""
