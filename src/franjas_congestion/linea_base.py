"""Modulo de linea base para deteccion de franjas de congestion (Fuerza Bruta O(k^2))."""

from typing import Tuple


def tramo_maxima_congestion_actual(saldos: list[int]) -> Tuple[int, int, int]:
    """Evalua todos los subintervalos posibles para hallar la maxima acumulacion.

    Args:
        saldos: Lista de saldos netos por intervalo de tiempo.

    Returns:
        Tupla con (indice_inicio, indice_fin, acumulacion_maxima).
    """
    n: int = len(saldos)
    if n == 0:
        return 0, -1, 0

    mejor_inicio: int = 0
    mejor_fin: int = 0
    maxima_acumulacion: int = saldos[0]

    for i in range(n):
        acumulado_actual: int = 0
        for j in range(i, n):
            acumulado_actual += saldos[j]
            if acumulado_actual > maxima_acumulacion:
                maxima_acumulacion = acumulado_actual
                mejor_inicio = i
                mejor_fin = j

    return mejor_inicio, mejor_fin, maxima_acumulacion
