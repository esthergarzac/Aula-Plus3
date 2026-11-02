from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal

ESTADO_CONFIRMADA = "Confirmada"
ESTADO_COMPLETADA = "Completada"
ANTICIPACION_MINIMA = timedelta(hours=48)
DURACION_CONTRATADA = timedelta(minutes=90)
PORCENTAJE_MINIMO_GRABADO = 70


class AnticipacionInsuficiente(Exception):
    pass


class DuracionInsuficiente(Exception):
    pass


@dataclass(frozen=True)
class Liquidacion:
    precio: Decimal = Decimal("200")
    comision: Decimal = Decimal("40")
    monto_tutor: Decimal = Decimal("160")


@dataclass(frozen=True)
class Grabacion:
    url: str
    inicio: datetime
    fin: datetime

    @property
    def duracion(self):
        return self.fin - self.inicio

    def cubre_porcentaje_minimo(self):
        return self.duracion * 100 >= DURACION_CONTRATADA * PORCENTAJE_MINIMO_GRABADO


@dataclass
class Sesion:
    estudiante_id: int
    materia: str
    tema: str
    modalidad: str
    fecha_hora: datetime
    estado: str = ESTADO_CONFIRMADA

    @staticmethod
    def _validar_anticipacion(fecha_hora, ahora):
        if fecha_hora - ahora < ANTICIPACION_MINIMA:
            raise AnticipacionInsuficiente(
                "La reserva debe realizarse con al menos 48 horas de anticipación"
            )

    @classmethod
    def crear(cls, estudiante_id, materia, tema, modalidad, fecha_hora, ahora):
        cls._validar_anticipacion(fecha_hora, ahora)
        return cls(estudiante_id, materia, tema, modalidad, fecha_hora)

    def completar_con_grabacion(self, grabacion):
        if not grabacion.cubre_porcentaje_minimo():
            raise DuracionInsuficiente(
                "La sesión fue reembolsada: "
                "la grabación duró menos del 70% del tiempo contratado"
            )
        self.estado = ESTADO_COMPLETADA
        return Liquidacion()