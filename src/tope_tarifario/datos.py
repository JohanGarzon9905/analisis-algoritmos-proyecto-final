"""Generador de datos sinteticos para medicion de liquidacion tarifaria."""

import random


def generar_instancia(
    dias: int,
    semilla: int = 42,
    probabilidad_viaje: float = 0.85,
    max_viajes_dia: int = 4,
) -> list[int]:
    """Genera una serie temporal de viajes diarios con semilla deterministica.

    Args:
        dias: Numero total de dias del periodo a simular.
        semilla: Entero que fija el estado del generador pseudoaleatorio.
        probabilidad_viaje: Probabilidad entre 0 y 1 de que un dia tenga viajes.
        max_viajes_dia: Maximo numero de viajes posibles en un dia activo.

    Returns:
        Lista de enteros donde cada elemento representa los viajes de un dia.
    """
    rng = random.Random(semilla)
    resultado: list[int] = []

    for _ in range(dias):
        if rng.random() < probabilidad_viaje:
            resultado.append(rng.randint(1, max_viajes_dia))
        else:
            resultado.append(0)

    return resultado


def generar_lote_tarjetas(
    cantidad_tarjetas: int,
    dias: int = 30,
    semilla: int = 42,
) -> list[list[int]]:
    """Genera un lote de historiales de viajes para un conjunto de tarjetas.

    Args:
        cantidad_tarjetas: Numero de tarjetas o usuarios a generar.
        dias: Duracion del periodo mensual en dias para cada tarjeta.
        semilla: Semilla base para reproducibilidad de todo el lote.

    Returns:
        Lista de historiales diarios, uno por cada tarjeta simulada.
    """
    rng = random.Random(semilla)
    lote: list[list[int]] = []

    for i in range(cantidad_tarjetas):
        semilla_tarjeta: int = rng.randint(1, 1000000)
        lote.append(
            generar_instancia(
                dias=dias,
                semilla=semilla_tarjeta,
                probabilidad_viaje=0.8,
                max_viajes_dia=4,
            )
        )

    return lote
