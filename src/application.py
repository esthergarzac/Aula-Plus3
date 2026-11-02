from dataclasses import dataclass
from decimal import Decimal

from src.domain import DuracionInsuficiente

PAGO_LIQUIDADO = "Liquidado"
PAGO_NO_APLICABLE = "No aplicable – reembolso"


@dataclass(frozen=True)
class ResultadoLiquidacion:
    estado_pago: str
    monto_tutor: Decimal
    mensaje: str = ""


class LiquidacionService:
    def __init__(self, gateway):
        self.gateway = gateway

    def procesar_liquidacion(self, sesion, grabacion, tutor_id):
        try:
            liquidacion = sesion.completar_con_grabacion(grabacion)
        except DuracionInsuficiente as error:
            return ResultadoLiquidacion(PAGO_NO_APLICABLE, Decimal(0), str(error))
        self.gateway.transferir(tutor_id, liquidacion.monto_tutor)
        return ResultadoLiquidacion(PAGO_LIQUIDADO, liquidacion.monto_tutor)