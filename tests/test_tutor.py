from datetime import UTC, datetime, timedelta

import pytest

from src.domain import LimiteDiarioExcedido, Sesion, Tutor

DIA = datetime(2026, 11, 10, 8, 0, tzinfo=UTC)
MENSAJE_LIMITE = "El tutor ya alcanzó el máximo de 5 sesiones por día"


def sesion_a_las(hora, dia=DIA):
    return Sesion(1, "Cálculo", "Derivadas", "En línea", dia.replace(hour=hora))


def tutor_con(cantidad):
    tutor = Tutor(id=7, nombre="Ana")
    for i in range(cantidad):
        tutor.asignar(sesion_a_las(8 + 2 * i))
    return tutor


def test_cp10_tutor_con_4_sesiones_acepta_la_quinta():
    # Arrange
    tutor = tutor_con(4)

    # Act
    tutor.asignar(sesion_a_las(18))

    # Assert
    assert tutor.sesiones_del_dia(DIA.date()) == 5


def test_cp11_tutor_con_5_sesiones_rechaza_la_sexta():
    # Arrange
    tutor = tutor_con(5)

    # Act + Assert
    with pytest.raises(LimiteDiarioExcedido, match=MENSAJE_LIMITE):
        tutor.asignar(sesion_a_las(20))
    assert tutor.sesiones_del_dia(DIA.date()) == 5


def test_cp13_el_limite_se_cuenta_por_dia():
    # Arrange: 5 sesiones el martes, la nueva cae al día siguiente
    tutor = tutor_con(5)
    dia_siguiente = DIA + timedelta(days=1)

    # Act
    tutor.asignar(sesion_a_las(8, dia_siguiente))

    # Assert
    assert tutor.sesiones_del_dia(DIA.date()) == 5
    assert tutor.sesiones_del_dia(dia_siguiente.date()) == 1