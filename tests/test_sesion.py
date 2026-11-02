from datetime import UTC, datetime, timedelta

import pytest

from src.domain import AnticipacionInsuficiente, Sesion

AHORA = datetime(2026, 11, 2, 10, 0, tzinfo=UTC)


def crear_sesion(fecha_hora):
    return Sesion.crear(
        estudiante_id=1,
        materia="Cálculo",
        tema="Derivadas",
        modalidad="En línea",
        fecha_hora=fecha_hora,
        ahora=AHORA,
    )


def test_cp01_reserva_con_72_horas_queda_confirmada():
    # Arrange
    fecha = AHORA + timedelta(hours=72)

    # Act
    sesion = crear_sesion(fecha)

    # Assert
    assert sesion.estado == "Confirmada"


def test_cp02_reserva_con_24_horas_es_rechazada():
    # Arrange
    fecha = AHORA + timedelta(hours=24)

    # Act + Assert
    with pytest.raises(
        AnticipacionInsuficiente,
        match="La reserva debe realizarse con al menos 48 horas de anticipación",
    ):
        crear_sesion(fecha)


def test_cp03_reserva_con_exactamente_48_horas_es_aceptada():
    # Arrange: el límite es "al menos 48 h", así que 48 h exactas se aceptan
    fecha = AHORA + timedelta(hours=48)

    # Act
    sesion = crear_sesion(fecha)

    # Assert
    assert sesion.estado == "Confirmada"