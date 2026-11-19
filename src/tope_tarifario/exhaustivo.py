"""Modulo de solucion exhaustiva para liquidacion de tope tarifario."""

PASAJE: int = 3900
DIARIO: int = 9500
SEMANAL: int = 36000
MENSUAL: int = 135000


def costo_exhaustivo(viajes_por_dia: list[int]) -> int:
    """Calcula el costo minimo probando todas las combinaciones de productos.

    Explora de forma recursiva e ingenua las ramificaciones de compra para
    cada dia con viajes sin memoizacion ni reutilizacion de subproblemas.

    Args:
        viajes_por_dia: Lista de viajes por cada dia del mes.

    Returns:
        El costo minimo total en pesos calculado mediante busqueda exhaustiva.
    """
    n: int = len(viajes_por_dia)

    def _resolver(dia: int) -> int:
        if dia >= n:
            return 0

        if viajes_por_dia[dia] == 0:
            return _resolver(dia + 1)

        viajes_hoy: int = viajes_por_dia[dia]
        costo_dia: int = min(viajes_hoy * PASAJE, DIARIO) + _resolver(dia + 1)
        costo_sem: int = SEMANAL + _resolver(dia + 7)
        costo_mes: int = MENSUAL + _resolver(dia + 30)

        return min(costo_dia, costo_sem, costo_mes)

    return _resolver(0)
