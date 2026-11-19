"""Suite de pruebas unitarias para liquidacion de tope tarifario."""

from estrategia import costo_minimo, liquidar_tope
from exhaustivo import costo_exhaustivo
from regla_actual import costo_regla_actual
from datos import generar_instancia


def probar_casos_limite() -> None:
    """Valida el comportamiento del algoritmo en escenarios frontera."""
    assert costo_minimo([]) == 0
    assert costo_exhaustivo([]) == 0
    assert costo_regla_actual([]) == 0

    assert costo_minimo([0] * 30) == 0
    assert costo_exhaustivo([0] * 30) == 0
    assert costo_regla_actual([0] * 30) == 0

    assert costo_minimo([1]) == 3900
    assert costo_exhaustivo([1]) == 3900
    assert costo_regla_actual([1]) == 3900

    assert costo_minimo([5]) == 9500
    assert costo_exhaustivo([5]) == 9500
    assert costo_regla_actual([5]) == 9500

    mes_intensivo: list[int] = [5] * 30
    assert costo_minimo(mes_intensivo) == 135000
    assert costo_regla_actual(mes_intensivo) == 135000


def probar_ejemplo_a_mano() -> None:
    """Verifica la coincidencia exacta con el calculo teorico manual."""
    ejemplo: list[int] = [2, 1, 3, 0, 0, 3, 2, 1]
    costo_esperado: int = 39900

    assert costo_minimo(ejemplo) == costo_esperado
    assert costo_exhaustivo(ejemplo) == costo_esperado


def probar_instancias_aleatorias_coincidencia() -> None:
    """Compara estrategia dinamica frente a solucion exhaustiva en 25 casos."""
    for i in range(25):
        dias: int = 10 + (i % 6)
        semilla: int = 1000 + i
        instancia: list[int] = generar_instancia(
            dias=dias,
            semilla=semilla,
            probabilidad_viaje=0.75,
            max_viajes_dia=3,
        )

        optimo_dp: int = costo_minimo(instancia)
        optimo_ex: int = costo_exhaustivo(instancia)

        assert optimo_dp == optimo_ex


def probar_restricciones_negocio() -> None:
    """Verifica que la devolucion calculada sea exacta y nunca negativa."""
    instancia: list[int] = [3, 2, 1, 0, 2, 3, 1, 0, 1, 2]
    costo_opt: int = costo_minimo(instancia)

    cobrado_exceso: int = costo_opt + 15000
    assert liquidar_tope(instancia, cobrado_exceso) == 15000

    cobrado_exacto: int = costo_opt
    assert liquidar_tope(instancia, cobrado_exacto) == 0

    cobrado_menor: int = costo_opt - 5000
    assert liquidar_tope(instancia, cobrado_menor) == 0


def probar_contraejemplo_regla_actual() -> None:
    """Valida la ineficiencia economica de la regla actual frente al optimo."""
    contraejemplo: list[int] = [0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0]

    costo_dp: int = costo_minimo(contraejemplo)
    costo_ex: int = costo_exhaustivo(contraejemplo)
    costo_act: int = costo_regla_actual(contraejemplo)

    assert costo_dp == 36000
    assert costo_ex == 36000
    assert costo_act == 64500
    assert costo_act > costo_dp

    sobrecosto: int = costo_act - costo_dp
    assert sobrecosto == 28500
    assert liquidar_tope(contraejemplo, costo_act) == sobrecosto


def ejecutar_pruebas() -> None:
    """Punto de entrada principal para ejecucion integral de la suite."""
    probar_casos_limite()
    probar_ejemplo_a_mano()
    probar_instancias_aleatorias_coincidencia()
    probar_restricciones_negocio()
    probar_contraejemplo_regla_actual()
    print("Todas las pruebas pasaron exitosamente.")


if __name__ == "__main__":
    ejecutar_pruebas()
