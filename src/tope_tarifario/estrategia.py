"""Modulo de estrategia optima para liquidacion de tope tarifario."""

PASAJE: int = 3900
DIARIO: int = 9500
SEMANAL: int = 36000
MENSUAL: int = 135000


def costo_minimo(viajes_por_dia: list[int]) -> int:
    """Calcula el costo de la combinacion mas barata que cubre los viajes.

    Aplica programacion dinamica sobre los dias del periodo evaluado,
    llenando la tabla de subproblemas de atras hacia adelante.

    Args:
        viajes_por_dia: Lista de enteros con el numero de viajes realizados
            en cada dia del mes. El indice 0 corresponde al primer dia.

    Returns:
        El costo minimo total en pesos colombianos para cubrir los viajes.
    """
    n: int = len(viajes_por_dia)
    if n == 0:
        return 0

    costos: list[int] = [0] * (n + 1)

    for i in range(n - 1, -1, -1):
        viajes_hoy: int = viajes_por_dia[i]
        if viajes_hoy == 0:
            costos[i] = costos[i + 1]
            continue

        costo_dia: int = min(viajes_hoy * PASAJE, DIARIO) + costos[i + 1]
        costo_sem: int = SEMANAL + costos[min(i + 7, n)]
        costo_mes: int = MENSUAL + costos[min(i + 30, n)]

        costos[i] = min(costo_dia, costo_sem, costo_mes)

    return costos[0]


def liquidar_tope(viajes_por_dia: list[int], cobrado: int) -> int:
    """Calcula la devolucion que corresponde al usuario al cierre de mes.

    Resta del monto cobrado el costo optimo liquidado por programacion
    dinamica, garantizando que el saldo resultante nunca sea negativo.

    Args:
        viajes_por_dia: Lista de viajes por cada dia del mes.
        cobrado: Valor total en pesos efectivamente cobrado al usuario.

    Returns:
        Monto exacto a devolver al usuario como saldo a favor en tarjeta.
    """
    minimo: int = costo_minimo(viajes_por_dia)
    if cobrado < minimo:
        return 0
    return cobrado - minimo
