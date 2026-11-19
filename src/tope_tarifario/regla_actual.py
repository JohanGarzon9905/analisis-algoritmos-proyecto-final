"""Modulo que reproduce la regla simplificada del sistema actual."""

PASAJE: int = 3900
DIARIO: int = 9500
SEMANAL: int = 36000
MENSUAL: int = 135000


def costo_regla_actual(viajes_por_dia: list[int]) -> int:
    """Calcula lo que cobra hoy la regla simplificada del sistema.

    Aplica el cobro diario entre pasajes sencillos y pase diario en bloques
    semanales fijos de siete dias, acotando cada bloque al costo del pase
    semanal y acotando el acumulado mensual al costo del pase mensual.

    Args:
        viajes_por_dia: Lista de viajes por cada dia del mes.

    Returns:
        El monto total cobrado en pesos segun la regla simplificada actual.
    """
    n: int = len(viajes_por_dia)
    if n == 0:
        return 0

    total_acumulado: int = 0

    for inicio_bloque in range(0, n, 7):
        fin_bloque: int = min(inicio_bloque + 7, n)
        suma_bloque: int = 0

        for dia in range(inicio_bloque, fin_bloque):
            viajes: int = viajes_por_dia[dia]
            if viajes > 0:
                costo_dia: int = min(viajes * PASAJE, DIARIO)
                suma_bloque += costo_dia

        total_acumulado += min(suma_bloque, SEMANAL)

    return min(total_acumulado, MENSUAL)
