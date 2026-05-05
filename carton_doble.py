"""
Clase CartonDoble: representa un cartón con dos grillas de bingo.

Relación con Carton: HERENCIA.
CartonDoble ES UN tipo de Carton. Extiende su comportamiento
agregando una segunda grilla. Sobrescribe verificar_bingo()
y marcar_numero() para considerar ambas grillas.
"""
from __future__ import annotations
from typing import List
from carton import Carton


class CartonDoble(Carton):
    """Cartón de bingo con dos grillas independientes."""

    def __init__(self, palabra: str, numero_maximo: int) -> None:
        """
        Constructor del cartón doble.
        Llama al constructor padre para crear la primera grilla,
        y luego genera una segunda grilla con los mismos parámetros.
        """
        # Llama al constructor de Carton → crea grilla 1, marcados 1
        super().__init__(palabra, numero_maximo)

        # Genera la segunda grilla y sus marcados reutilizando métodos del padre
        self._grilla2: List[List[int]] = self._generar_grilla()
        self._marcados2: List[List[bool]] = self._crear_marcados()

    def marcar_numero(self, numero: int) -> bool:
        """
        Sobrescribe marcar_numero del padre.
        Marca el número en AMBAS grillas.
        Retorna True si se encontró en al menos una.
        """
        # Marcar en grilla 1 usando el método del padre
        encontrado1: bool = super().marcar_numero(numero)

        # Marcar en grilla 2 manualmente
        encontrado2: bool = False
        for i in range(self.tamanio):
            for j in range(self.tamanio):
                if self._grilla2[i][j] == numero:
                    self._marcados2[i][j] = True
                    encontrado2 = True

        return encontrado1 or encontrado2

    def verificar_bingo(self) -> bool:
        """
        Sobrescribe verificar_bingo del padre (POLIMORFISMO).
        Gana si ALGUNA de las dos grillas está completa.
        """
        # Verificar grilla 1 con el método del padre
        bingo_grilla1: bool = super().verificar_bingo()

        # Verificar grilla 2
        bingo_grilla2: bool = True
        for i in range(self.tamanio):
            for j in range(self.tamanio):
                if not self._marcados2[i][j]:
                    bingo_grilla2 = False
                    break
            if not bingo_grilla2:
                break

        return bingo_grilla1 or bingo_grilla2

    def contar_marcados(self) -> int:
        """Cuenta los marcados en ambas grillas sumados."""
        total: int = super().contar_marcados()
        for i in range(self.tamanio):
            for j in range(self.tamanio):
                if self._marcados2[i][j]:
                    total += 1
        return total

    def grilla_mas_cercana(self) -> int:
        """
        Indica cuál grilla está más cerca de completarse.
        Retorna 1 o 2 según cuál tenga más números marcados.
        """
        marcados_g1: int = super().contar_marcados()

        marcados_g2: int = 0
        for i in range(self.tamanio):
            for j in range(self.tamanio):
                if self._marcados2[i][j]:
                    marcados_g2 += 1

        if marcados_g1 >= marcados_g2:
            return 1
        else:
            return 2

    def __str__(self) -> str:
        """Representación en texto mostrando ambas grillas."""
        lineas: List[str] = []
        lineas.append("--- Grilla 1 ---")
        lineas.append(super().__str__())
        lineas.append("\n--- Grilla 2 ---")
        lineas.append(" | ".join(self.palabra))
        lineas.append("-" * 29)
        for i in range(self.tamanio):
            fila_texto: str = ""
            for j in range(self.tamanio):
                if self._marcados2[i][j]:
                    fila_texto += " X  "
                else:
                    fila_texto += f"{self._grilla2[i][j]:2}  "
            lineas.append(fila_texto)
        return "\n".join(lineas)