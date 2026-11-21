"""Modulo de Programacion Dinamica (Kadane) para deteccion de franjas de congestion (Theta(k))."""

from typing import Tuple


def tramo_maxima_congestion_kadane(saldos: list[int]) -> Tuple[int, int, int]:
    """Calcula la franja de maxima congestion en tiempo lineal Theta(k) y espacio Theta(1).

    Args:
        saldos: Lista de saldos netos por intervalo de tiempo.

    Returns:
        Tupla con (indice_inicio, indice_fin, acumulacion_maxima).
    """
    n: int = len(saldos)
    if n == 0:
        return 0, -1, 0

    maxima_acumulacion: int = saldos[0]
    acumulado_actual: int = saldos[0]

    mejor_inicio: int = 0
    mejor_fin: int = 0
    inicio_candidato: int = 0

    for i in range(1, n):
        if saldos[i] > acumulado_actual + saldos[i]:
            acumulado_actual = saldos[i]
            inicio_candidato = i
        else:
            acumulado_actual += saldos[i]

        if acumulado_actual > maxima_acumulacion:
            maxima_acumulacion = acumulado_actual
            mejor_inicio = inicio_candidato
            mejor_fin = i

    return mejor_inicio, mejor_fin, maxima_acumulacion
