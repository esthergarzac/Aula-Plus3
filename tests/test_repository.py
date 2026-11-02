from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from src.domain import Sesion
from src.repository import SqlSesionRepository, make_engine

AHORA = datetime(2026, 11, 2, 10, 0, tzinfo=UTC)
INICIO = AHORA + timedelta(hours=72)


def sesion_confirmada():
    return Sesion.crear(1, "Cálculo", "Derivadas", "En línea", INICIO, AHORA)


def test_cp12_commit_persiste_la_sesion():
    # Arrange
    engine = make_engine()
    with Session(engine) as session:
        SqlSesionRepository(session).guardar(1, sesion_confirmada())

        # Act
        session.commit()

    # Assert: una sesión nueva demuestra que el dato quedó guardado
    with Session(engine) as nueva:
        recuperada = SqlSesionRepository(nueva).obtener_por_id(1)
        assert recuperada == sesion_confirmada()
        assert recuperada.estado == "Confirmada"


def test_cp12_rollback_descarta_la_sesion():
    # Arrange
    engine = make_engine()
    with Session(engine) as session:
        SqlSesionRepository(session).guardar(1, sesion_confirmada())

        # Act
        session.rollback()

    # Assert
    with Session(engine) as nueva:
        assert SqlSesionRepository(nueva).obtener_por_id(1) is None