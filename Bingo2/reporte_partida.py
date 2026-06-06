"""
Clase ReportePartida: responsable exclusiva de generar el reporte final.

Principio SOLID aplicado:
  SRP — Una sola razón para cambiar: el formato del reporte final.
        Antes, Juego mezclaba lógica de partida con presentación de resultados.
        Ahora, Juego solo orquesta la partida y ReportePartida solo imprime.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from juego import Juego


class ReportePartida:
    """Genera e imprime el reporte final de una partida de bingo.

    Una sola razón para cambiar: el formato o destino del reporte.
    """

    def generar(self, juego: "Juego") -> None:
        """Imprime el reporte final usando el estado del juego."""
        try:
            print("\n" + "=" * 50)
            print("         REPORTE FINAL DE LA PARTIDA")
            print("=" * 50)
            print(f"Palabra: {juego.palabra}")
            print(f"Número máximo: {juego.numero_maximo}")
            print(f"Turnos jugados: {juego.turno_actual}")

            if juego.ganador is not None:
                print(f"Ganador: {juego.ganador.nombre}")
            else:
                print("No hubo ganador.")

            print(f"\nNúmeros extraídos: {juego.get_historial_bombo()}")

            print("\n--- Estadísticas por jugador ---")
            for jugador in juego.get_jugadores():
                print(f"  {jugador.nombre}: {jugador.get_total_marcados()} números marcados")
                for idx, carton in enumerate(jugador.get_cartones()):
                    # OCP: tipo_nombre() evita isinstance(carton, CartonDoble)
                    print(f"    Cartón {idx + 1} ({carton.tipo_nombre()}): {carton.contar_marcados()} marcados")

            print("=" * 50)

        except Exception as error:
            print(f"[ERROR] No se pudo generar el reporte: {error}")
