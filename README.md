# Aula Plus – Pruebas, integración y calidad (Unidad 5)

![CI](https://github.com/esthergarzac/Aula-Plus3/actions/workflows/ci.yml/badge.svg)

Proyecto de la materia **Componentes de Lógica de Negocio** (FIME, UANL). Aula Plus es una plataforma que conecta estudiantes con tutores particulares y cobra una comisión por cada sesión. Este repositorio contiene un núcleo de lógica de negocio con **3 reglas reales de Aula Plus** y su suite de pruebas automatizadas.

## Equipo 8
- Esther Garza Cano (2143077)
- Luis Ángel David Cavazos Reyes (2142838)
- Emilio Garza Arizpe (2143702)

## Alcance
**Incluye:** dominio (`Sesion`, `Tutor`, `Grabacion`, `Liquidacion`), un servicio de aplicación con pasarela de pago simulada, persistencia con SQLAlchemy, 14 pruebas, cobertura del 100% y un pipeline de CI.

**No incluye:** API web, interfaz gráfica, pruebas de extremo a extremo ni el resto de las reglas del BRD (calificaciones, cancelaciones y reportes). No se usan pagos reales.

## Estructura
```
.github/workflows/ci.yml   Pipeline de GitHub Actions
src/domain.py              Reglas de negocio puras
src/application.py         Servicio de liquidación (usa la pasarela)
src/repository.py          Persistencia con SQLAlchemy
tests/                     Pruebas con pytest
docs/matriz_pruebas.csv    Matriz de casos de prueba
Diagramas/ y *.pdf         Documentación de actividades anteriores
pyproject.toml, requirements.txt
```

## Arquitectura (Ports & Adapters)
| Capa | Archivo | Responsabilidad |
|---|---|---|
| Dominio | `src/domain.py` | Reglas e invariantes. No conoce la base de datos ni la pasarela. |
| Aplicación | `src/application.py` | Orquesta el caso de uso. Recibe la pasarela por inyección, por lo que se sustituye con un mock en las pruebas. |
| Infraestructura | `src/repository.py` | Traduce entre la fila SQL y el objeto de dominio. |

## Reglas implementadas
| Regla | Comportamiento | Mensaje al usuario |
|---|---|---|
| Anticipación | Se reserva con al menos 48 h (48 h exactas se aceptan). La sesión nace `Confirmada`. | "La reserva debe realizarse con al menos 48 horas de anticipación" |
| Duración y liquidación | Si la grabación cubre al menos el 70% de 90 min (63 min exactos, sin reembolso), la sesión se completa y se liquida 200 / 40 / 160. Si no, se rechaza y no se paga al tutor. | "La sesión fue reembolsada: la grabación duró menos del 70% del tiempo contratado" |
| Límite diario | Un tutor puede tener como máximo 5 sesiones por día; el conteo es por día. | "El tutor ya alcanzó el máximo de 5 sesiones por día" |

Los mensajes de las dos últimas reglas son propuesta del equipo, porque los documentos de requerimientos no los definen.

## Casos de prueba
13 casos (5 de éxito, 4 de error y 4 de límite) en 14 pruebas, detallados en `docs/matriz_pruebas.csv`: CP-01 a CP-03 (anticipación), CP-04 a CP-07 (duración), CP-08 y CP-09 (pasarela simulada), CP-10, CP-11 y CP-13 (límite diario) y CP-12 (persistencia con commit y rollback).

## Requisitos e instalación
Python 3.11 o superior.

Windows (PowerShell):
```
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
macOS o Linux:
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Comandos
```
python -m pytest -v
python -m ruff check src tests
python -m pytest --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80
```
El reporte HTML queda en `htmlcov/index.html`.

## Integración continua
El workflow **CI Business Logic** se ejecuta en cada `push` y `pull request`: instala dependencias, corre Ruff, ejecuta pytest con umbral del 80% de cobertura y compila `src/`. El pipeline avisa de los fallos pero no bloquea merges, porque no se configuró branch protection.

## Decisiones de diseño
- **Estado inicial `Confirmada`**, como indican el BRD, Gherkin y el glosario (el diagrama de secuencia decía `PROGRAMADA`).
- **Reembolso total** por duración insuficiente.
- **Umbral del 70% inclusivo.**
- **Fechas explícitas:** `Sesion.crear` recibe `ahora` para que las pruebas no dependan del reloj.
- **Aritmética con `timedelta`** al comparar el 70%, para evitar errores de redondeo con decimales.
- **Fechas en UTC** al persistir, porque SQLite no guarda zona horaria.

## Limitaciones
- SQLite en memoria no sustituye pruebas contra un motor productivo como PostgreSQL.
- La duración contratada (90 min) es constante.
- El conteo diario usa la fecha de cada sesión en su propia zona horaria.
- Las pruebas de repositorio muestran un `ResourceWarning` por conexiones SQLite sin cerrar; no afecta los resultados.

## Uso de IA
Se usó Claude para proponer casos de prueba y estructura. Cada propuesta se verificó contra el BRD, se ejecutó y se corrigió cuando fue necesario. Los casos corregidos están en la bitácora del reporte.