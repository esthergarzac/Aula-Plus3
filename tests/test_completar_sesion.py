from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from src.domain import DuracionInsuficiente, Grabacion, Sesion

AHORA = datetime(2026, 11, 2, 10, 0, tzinfo=UTC)
INICIO = AHORA + timedelta(hours=72)
MENSAJE_REEMBOLSO = (
    "La sesión fue reembolsada: "
    "la grabación duró menos del 70% del tiempo contratado"
)


def sesion_confirmada():
    return Sesion.crear(1, "Cálculo", "Derivadas", "En línea", INICIO, AHORA)


def grabacion_de(minutos):
    return Grabacion(
        url="grabacion-s1.mp4",
        inicio=INICIO,
        fin=INICIO + timedelta(minutes=minutos),
    )


def test_cp04_sesion_de_90_minutos_se_completa_y_liquida():
    # Arrange
    sesion = sesion_confirmada()

    # Act
    liquidacion = sesion.completar_con_grabacion(grabacion_de(90))

    # Assert
    assert sesion.estado == "Completada"
    assert liquidacion.precio == Decimal(200)
    assert liquidacion.comision == Decimal(40)
    assert liquidacion.monto_tutor == Decimal(160)


def test_cp05_sesion_de_45_minutos_es_rechazada_por_duracion():
    # Arrange
    sesion = sesion_confirmada()

    # Act + Assert
    with pytest.raises(DuracionInsuficiente, match=MENSAJE_REEMBOLSO):
        sesion.completar_con_grabacion(grabacion_de(45))
    assert sesion.estado == "Confirmada"


def test_cp06_sesion_de_63_minutos_exactos_se_completa():
    # Arrange: 70% de 90 min = 63 min, el límite exacto no se reembolsa
    sesion = sesion_confirmada()

    # Act
    sesion.completar_con_grabacion(grabacion_de(63))

    # Assert
    assert sesion.estado == "Completada"


def test_cp07_sesion_de_62_minutos_es_rechazada():
    # Arrange: un minuto por debajo del 70%
    sesion = sesion_confirmada()

    # Act + Assert
    with pytest.raises(DuracionInsuficiente, match=MENSAJE_REEMBOLSO):
        sesion.completar_con_grabacion(grabacion_de(62))