"""Script de benchmarking experimental y generacion de graficas tecnicas."""

import os
import time
from typing import Callable
import matplotlib.pyplot as plt

from estrategia import costo_minimo, PASAJE, DIARIO, SEMANAL, MENSUAL
from exhaustivo import costo_exhaustivo
from regla_actual import costo_regla_actual
from datos import generar_instancia, generar_lote_tarjetas


def contar_operaciones_dp(viajes_por_dia: list[int]) -> int:
    """Calcula las operaciones elementales del enfoque de programacion dinamica.

    Args:
        viajes_por_dia: Lista de viajes diarios.

    Returns:
        Numero total de evaluaciones y comparaciones ejecutadas.
    """
    n: int = len(viajes_por_dia)
    if n == 0:
        return 1

    ops: int = 1
    for i in range(n - 1, -1, -1):
        ops += 1
        if viajes_por_dia[i] == 0:
            continue
        ops += 4

    return ops


def contar_operaciones_ex(viajes_por_dia: list[int]) -> int:
    """Calcula las operaciones elementales de la busqueda exhaustiva.

    Args:
        viajes_por_dia: Lista de viajes diarios.

    Returns:
        Numero total de nodos y comparaciones en el arbol de recursion.
    """
    n: int = len(viajes_por_dia)
    ops: int = 0

    def _rec(dia: int) -> int:
        nonlocal ops
        ops += 1
        if dia >= n:
            return 0
        if viajes_por_dia[dia] == 0:
            return _rec(dia + 1)
        ops += 3
        v: int = viajes_por_dia[dia]
        c1: int = min(v * PASAJE, DIARIO) + _rec(dia + 1)
        c2: int = SEMANAL + _rec(dia + 7)
        c3: int = MENSUAL + _rec(dia + 30)
        return min(c1, c2, c3)

    _rec(0)
    return ops


def contar_operaciones_actual(viajes_por_dia: list[int]) -> int:
    """Calcula las operaciones elementales de la regla simplificada actual.

    Args:
        viajes_por_dia: Lista de viajes diarios.

    Returns:
        Numero total de operaciones aritmeticas y comparaciones.
    """
    n: int = len(viajes_por_dia)
    if n == 0:
        return 1

    ops: int = 1
    for inicio in range(0, n, 7):
        ops += 1
        fin: int = min(inicio + 7, n)
        for dia in range(inicio, fin):
            ops += 1
            if viajes_por_dia[dia] > 0:
                ops += 2
        ops += 2
    ops += 1
    return ops


def medir_tiempo_medio(
    algoritmo: Callable[[list[int]], int],
    instancia: list[int],
    repeticiones: int = 10,
) -> float:
    """Mide el tiempo de ejecucion promedio en microsegundos de un algoritmo.

    Args:
        algoritmo: Funcion a evaluar que recibe la lista de viajes.
        instancia: Datos de entrada a procesar.
        repeticiones: Numero de iteraciones independientes a promediar.

    Returns:
        Tiempo medio medido en microsegundos (µs).
    """
    tiempos: list[float] = []

    for _ in range(repeticiones):
        t0: float = time.perf_counter()
        _ = algoritmo(instancia)
        t1: float = time.perf_counter()
        tiempos.append((t1 - t0) * 1e6)

    return sum(tiempos) / len(tiempos)


def ejecutar_experimento() -> None:
    """Ejecuta los benchmarks sistematicos y exporta las graficas comparativas."""
    tamanos: list[int] = [4, 8, 12, 16, 20, 24]
    semilla_fija: int = 42
    repeticiones: int = 15

    tiempos_dp: list[float] = []
    tiempos_ex: list[float] = []
    tiempos_act: list[float] = []

    ops_dp: list[int] = []
    ops_ex: list[int] = []
    ops_act: list[int] = []

    for tam in tamanos:
        instancia: list[int] = generar_instancia(
            dias=tam,
            semilla=semilla_fija + tam,
            probabilidad_viaje=0.85,
            max_viajes_dia=3,
        )

        res_dp: int = costo_minimo(instancia)
        res_ex: int = costo_exhaustivo(instancia)
        assert res_dp == res_ex

        t_dp: float = medir_tiempo_medio(costo_minimo, instancia, repeticiones)
        t_ex: float = medir_tiempo_medio(costo_exhaustivo, instancia, repeticiones)
        t_act: float = medir_tiempo_medio(costo_regla_actual, instancia, repeticiones)

        tiempos_dp.append(t_dp)
        tiempos_ex.append(t_ex)
        tiempos_act.append(t_act)

        ops_dp.append(contar_operaciones_dp(instancia))
        ops_ex.append(contar_operaciones_ex(instancia))
        ops_act.append(contar_operaciones_actual(instancia))

    carpeta_graficas: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "graficas",
        "tope_tarifario",
    )
    os.makedirs(carpeta_graficas, exist_ok=True)

    plt.figure(figsize=(9, 5))
    plt.plot(tamanos, tiempos_dp, marker="o", color="#1f77b4", label="Programación Dinámica Θ(d)")
    plt.plot(tamanos, tiempos_act, marker="s", color="#2ca02c", linestyle="--", label="Regla Actual Θ(d)")
    plt.plot(tamanos, tiempos_ex, marker="^", color="#d62728", label="Búsqueda Exhaustiva O(3ᵈ)")
    plt.title("Liquidación de Tope Tarifario: Tiempo de Ejecución vs. Tamaño de Entrada (d)")
    plt.xlabel("Tamaño de entrada d (Días evaluados)")
    plt.ylabel("Tiempo medio de ejecución (µs)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    ruta_tiempo: str = os.path.join(carpeta_graficas, "tiempo_vs_n.png")
    plt.savefig(ruta_tiempo, dpi=300)
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.plot(tamanos, ops_dp, marker="o", color="#1f77b4", label="Programación Dinámica Θ(d)")
    plt.plot(tamanos, ops_act, marker="s", color="#2ca02c", linestyle="--", label="Regla Actual Θ(d)")
    plt.plot(tamanos, ops_ex, marker="^", color="#d62728", label="Búsqueda Exhaustiva O(3ᵈ)")
    plt.title("Liquidación de Tope Tarifario: Operaciones Elementales vs. Tamaño de Entrada (d)")
    plt.xlabel("Tamaño de entrada d (Días evaluados)")
    plt.ylabel("Número de operaciones elementales")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    ruta_ops: str = os.path.join(carpeta_graficas, "operaciones_vs_n.png")
    plt.savefig(ruta_ops, dpi=300)
    plt.close()

    print("Tabla 1: Comparacion de tiempos de ejecucion (µs)")
    print("| Tamano d | Prog. Dinamica (µs) | Regla Actual (µs) | Busqueda Exhaustiva (µs) |")
    print("|---|---|---|---|")
    for i, tam in enumerate(tamanos):
        print(f"| {tam:2d} | {tiempos_dp[i]:.2f} | {tiempos_act[i]:.2f} | {tiempos_ex[i]:.2f} |")

    print("\nTabla 2: Comparacion de operaciones elementales")
    print("| Tamano d | Ops Prog. Dinamica | Ops Regla Actual | Ops Busqueda Exhaustiva |")
    print("|---|---|---|---|")
    for i, tam in enumerate(tamanos):
        print(f"| {tam:2d} | {ops_dp[i]} | {ops_act[i]} | {ops_ex[i]} |")

    tamanos_grandes: list[int] = [30, 60, 120, 240, 480, 960]
    tiempos_extrap: list[float] = []
    for tam in tamanos_grandes:
        inst_g: list[int] = generar_instancia(dias=tam, semilla=999, probabilidad_viaje=0.85)
        t_g: float = medir_tiempo_medio(costo_minimo, inst_g, 20)
        tiempos_extrap.append(t_g)

    print("\nTabla 3: Escalabilidad de Programacion Dinamica en horizontes amplios")
    print("| Dias (d) | Tiempo PD (µs) |")
    print("|---|---|")
    for i, tam in enumerate(tamanos_grandes):
        print(f"| {tam:4d} | {tiempos_extrap[i]:.2f} |")

    lote_10k: list[list[int]] = generar_lote_tarjetas(10000, dias=30, semilla=42)
    t_inicio_lote: float = time.perf_counter()
    for tarjeta in lote_10k:
        _ = costo_minimo(tarjeta)
    t_fin_lote: float = time.perf_counter()
    duracion_10k: float = t_fin_lote - t_inicio_lote
    t_por_tarjeta_us: float = (duracion_10k / 10000) * 1e6

    print(f"\nBenchmark lote 10,000 tarjetas (mes de 30 dias):")
    print(f"  Duracion total lote: {duracion_10k:.4f} segundos")
    print(f"  Tiempo unitario medio por tarjeta: {t_por_tarjeta_us:.2f} µs")
    print(f"  Tarjetas procesadas por segundo: {10000 / duracion_10k:.1f} tarjetas/s")


if __name__ == "__main__":
    ejecutar_experimento()
