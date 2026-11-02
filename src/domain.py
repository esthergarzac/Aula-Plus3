from dataclasses import dataclass
from datetime import datetime, timedelta

ESTADO_CONFIRMADA = "Confirmada"
ANTICIPACION_MINIMA = timedelta(hours=48)


class AnticipacionInsuficiente(Exception):
    pass


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