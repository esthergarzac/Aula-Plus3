from datetime import UTC, datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock

from src.application import LiquidacionService
from src.domain import Grabacion, Sesion

AHORA = datetime(2026, 11, 2, 10, 0, tzinfo=UTC)
INICIO = AHORA + timedelta(hours=72)
TUTOR_ID = 7


def sesion_confirmada():
    return Sesion.crear(1, "Cálculo", "Derivadas", "En línea", INICIO, AHORA)


def grabacion_de(minutos):
    return Grabacion(
        url="grabacion-s1.mp4",
        inicio=INICIO,
        fin=INICIO + timedelta(minutes=minutos),
    )


def test_cp08_sesion_completa_transfiere_160_al_tutor():
    # Arrange: el mock sustituye a la pasarela, no se mueve dinero real
    gateway = Mock()
    servicio = LiquidacionService(gateway)
    sesion = sesion_confirmada()

    # Act
    resultado = servicio.procesar_liquidacion(sesion, grabacion_de(90), TUTOR_ID)

    # Assert
    gateway.transferir.assert_called_once_with(TUTOR_ID, Decimal("160"))
    assert resultado.estado_pago == "Liquidado"
    assert sesion.estado == "Completada"


def test_cp09_sesion_con_reembolso_no_llama_a_la_pasarela():
    # Arrange
    gateway = Mock()
    servicio = LiquidacionService(gateway)
    sesion = sesion_confirmada()

    # Act
    resultado = servicio.procesar_liquidacion(sesion, grabacion_de(45), TUTOR_ID)

    # Assert
    gateway.transferir.assert_not_called()
    assert resultado.estado_pago == "No aplicable – reembolso"
    assert resultado.monto_tutor == Decimal("0")
    assert sesion.estado == "Confirmada"