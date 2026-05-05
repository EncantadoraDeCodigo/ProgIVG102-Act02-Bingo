"""
Clase Carton: representa un cartón de bingo con una grilla de 5x5.

Relación: Es la clase base del sistema. CartónDoble hereda de esta clase (HERENCIA).
Adaptada de la Práctica 1 para funcionar como parte del sistema completo.
"""
from __future__ import annotations
import random
from typing import List, Tuple


class Carton:
    """Modela un cartón de bingo con una grilla de 5x5 números."""

    def __init__(self, palabra: str, numero_maximo: int) -> None:
        """
        Constructor del cartón.
        palabra: palabra del bingo (ej: BINGO, PLENO)
        numero_maximo: número máximo del juego (entre 50 y 90, múltiplo de 5)
        """
        # Validaciones de la palabra
        if not isinstance(palabra, str):
            raise ValueError("La palabra debe ser una cadena de texto.")
        if len(palabra) != 5:
            raise ValueError("La palabra debe tener exactamente 5 letras.")
        if not palabra.isalpha():
            raise ValueError("La palabra solo debe contener letras.")
        if len(set(palabra.upper())) != 5:
            raise ValueError("La palabra no debe repetir letras.")

        # Validaciones del número máximo
        if not isinstance(numero_maximo, int):
            raise ValueError("El número máximo debe ser un entero.")
        if not (50 <= numero_maximo <= 90):
            raise ValueError("El número máximo debe estar entre 50 y 90.")
        if numero_maximo % 5 != 0:
            raise ValueError("El número máximo debe ser múltiplo de 5.")

        self.palabra: str = palabra.upper()
        self.numero_maximo: int = numero_maximo
        self.tamanio: int = 5
        self._rangos: List[Tuple[int, int]] = self._calcular_rangos()
        self._grilla: List[List[int]] = self._generar_grilla()
        self._marcados: List[List[bool]] = self._crear_marcados()

    def _calcular_rangos(self) -> List[Tuple[int, int]]:
        """Divide el rango de números en 5 bloques iguales."""
        bloque: int = self.numero_maximo // 5
        rangos: List[Tuple[int, int]] = []
        inicio: int = 1

        for i in range(self.tamanio):
            fin: int = inicio + bloque - 1
            rangos.append((inicio, fin))
            inicio = fin + 1

        return rangos

    def _generar_grilla(self) -> List[List[int]]:
        """Genera una grilla de 5x5 con números aleatorios según los rangos."""
        columnas: List[List[int]] = []

        for inicio, fin in self._rangos:
            numeros: List[int] = random.sample(range(inicio, fin + 1), self.tamanio)
            columnas.append(numeros)

        # Convertir columnas en filas
        grilla: List[List[int]] = []
        for i in range(self.tamanio):
            fila: List[int] = []
            for j in range(self.tamanio):
                fila.append(columnas[j][i])
            grilla.append(fila)

        return grilla

    def _crear_marcados(self) -> List[List[bool]]:
        """Crea una matriz de 5x5 con False (nada marcado al inicio)."""
        marcados: List[List[bool]] = []
        for i in range(self.tamanio):
            fila: List[bool] = []
            for j in range(self.tamanio):
                fila.append(False)
            marcados.append(fila)
        return marcados

    def marcar_numero(self, numero: int) -> bool:
        """
        Busca un número en la grilla y lo marca si lo encuentra.
        Retorna True si encontró y marcó el número, False si no.
        """
        for i in range(self.tamanio):
            for j in range(self.tamanio):
                if self._grilla[i][j] == numero:
                    self._marcados[i][j] = True
                    return True
        return False

    def verificar_bingo(self) -> bool:
        """Verifica si todos los números del cartón están marcados."""
        for i in range(self.tamanio):
            for j in range(self.tamanio):
                if not self._marcados[i][j]:
                    return False
        return True

    def contar_marcados(self) -> int:
        """Cuenta cuántos números han sido marcados en la grilla."""
        contador: int = 0
        for i in range(self.tamanio):
            for j in range(self.tamanio):
                if self._marcados[i][j]:
                    contador += 1
        return contador

    def __str__(self) -> str:
        """Representación en texto del cartón."""
        lineas: List[str] = []
        lineas.append(" | ".join(self.palabra))
        lineas.append("-" * 29)
        for i in range(self.tamanio):
            fila_texto: str = ""
            for j in range(self.tamanio):
                if self._marcados[i][j]:
                    fila_texto += " X  "
                else:
                    fila_texto += f"{self._grilla[i][j]:2}  "
            lineas.append(fila_texto)
        return "\n".join(lineas)