from datetime import UTC

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from src.domain import Sesion


class Base(DeclarativeBase):
    pass


class SesionRow(Base):
    __tablename__ = "sesiones"
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, nullable=False)
    materia = Column(String, nullable=False)
    tema = Column(String, nullable=False)
    modalidad = Column(String, nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    estado = Column(String, nullable=False)


class SqlSesionRepository:
    def __init__(self, session: Session):
        self.session = session

    def guardar(self, sesion_id, sesion):
        self.session.add(
            SesionRow(
                id=sesion_id,
                estudiante_id=sesion.estudiante_id,
                materia=sesion.materia,
                tema=sesion.tema,
                modalidad=sesion.modalidad,
                fecha_hora=sesion.fecha_hora.astimezone(UTC).replace(tzinfo=None),
                estado=sesion.estado,
            )
        )

    def obtener_por_id(self, sesion_id):
        fila = self.session.get(SesionRow, sesion_id)
        if fila is None:
            return None
        return Sesion(
            estudiante_id=fila.estudiante_id,
            materia=fila.materia,
            tema=fila.tema,
            modalidad=fila.modalidad,
            fecha_hora=fila.fecha_hora.replace(tzinfo=UTC),
            estado=fila.estado,
        )


def make_engine(url="sqlite+pysqlite:///:memory:"):
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    return engine