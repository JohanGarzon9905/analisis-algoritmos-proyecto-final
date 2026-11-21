"""Modulo de Dividir y Vencer para deteccion de franjas de congestion (Theta(k log k))."""

from typing import Tuple


def _cruzar_medio(
    saldos: list[int], bajo: int, medio: int, alto: int
) -> Tuple[int, int, int]:
    suma_izquierda: int = saldos[medio]
    suma_actual: int = 0
    max_izq: int = medio
    for i in range(medio, bajo - 1, -1):
        suma_actual += saldos[i]
        if suma_actual > suma_izquierda:
            suma_izquierda = suma_actual
            max_izq = i

    suma_derecha: int = saldos[medio + 1]
    suma_actual = 0
    max_der: int = medio + 1
    for j in range(medio + 1, alto + 1):
        suma_actual += saldos[j]
        if suma_actual > suma_derecha:
            suma_derecha = suma_actual
            max_der = j

    return max_izq, max_der, suma_izquierda + suma_derecha


def _subarreglo_maximo_rec(
    saldos: list[int], bajo: int, alto: int
) -> Tuple[int, int, int]:
    if bajo == alto:
        return bajo, alto, saldos[bajo]

    medio: int = (bajo + alto) // 2

    izq_inicio, izq_fin, suma_izq = _subarreglo_maximo_rec(saldos, bajo, medio)
    der_inicio, der_fin, suma_der = _subarreglo_maximo_rec(saldos, medio + 1, alto)
    cruz_inicio, cruz_fin, suma_cruz = _cruzar_medio(saldos, bajo, medio, alto)

    if suma_izq >= suma_der and suma_izq >= suma_cruz:
        return izq_inicio, izq_fin, suma_izq
    elif suma_der >= suma_izq and suma_der >= suma_cruz:
        return der_inicio, der_fin, suma_der
    else:
        return cruz_inicio, cruz_fin, suma_cruz


def tramo_maxima_congestion_dyv(saldos: list[int]) -> Tuple[int, int, int]:
    """Calcula la franja de maxima congestion mediante Dividir y Vencer.

    Args:
        saldos: Lista de saldos netos por intervalo de tiempo.

    Returns:
        Tupla con (indice_inicio, indice_fin, acumulacion_maxima).
    """
    n: int = len(saldos)
    if n == 0:
        return 0, -1, 0

    return _subarreglo_maximo_rec(saldos, 0, n - 1)
