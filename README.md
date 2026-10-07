# Pandas frente a PySpark sobre US Accidents (2016–2023)

Proyecto final integrador de **Big Data** — Maestría en Inteligencia Artificial, Universidad de Palermo.

**Grupo 3:** Fernando Romero Etchenique, Aldo Sebastián López, Carlos Johansen.

Cinco consultas analíticas implementadas en Pandas y en PySpark, con medición de tiempo y memoria sobre
dos formatos de almacenamiento (CSV y Parquet), y un clasificador de severidad con Spark MLlib.

## Contenido del repositorio

| Archivo o carpeta | Qué es |
|---|---|
| `proyecto_final_grupo3.ipynb` | Cuaderno único, ya ejecutado: carga, consultas, conversión a Parquet, mediciones y modelo. Las salidas son las de la corrida que se informa en el artículo |
| `resultados/` | Tablas que genera el cuaderno (CSV y JSON): resultados de cada consulta, tiempos, memoria, entorno y métricas del modelo |
| `figuras/` | Gráficos que genera el cuaderno (PNG) |
| `importancia_por_variable.py` | Script que suma la importancia del modelo por variable original (Tabla 9 del artículo). Lee `resultados/consigna6_importancia_variables.csv` y escribe `resultados/consigna6_importancia_por_variable.csv` |
| `README.md` | Este archivo |

El dataset **no está incluido** (pesa 3 GB). Se descarga desde Kaggle; ver más abajo.

## Consultas

| Consulta | Qué responde |
|---|---|
| C1 | Distribución horaria de los siniestros entre 2021 y 2022, y horas pico |
| C4 | Los 5 puntos más peligrosos del país, con un radio de influencia de 2 km |
| C5 | Distancia y duración promedio por nivel de severidad |
| C9 | Las 10 intersecciones con más siniestros, extraídas del texto de la descripción |
| C10 | Tiempo de despeje de día y de noche, en días hábiles y fines de semana |
| Consigna 6 | Clasificación de siniestros de severidad alta (`Severity` ≥ 3) con un bosque aleatorio de Spark MLlib |

## Entorno en el que se probó

| Componente | Versión |
|---|---|
| Sistema operativo | Windows 11 |
| Procesador | Intel Core i9-10980HK, 8 núcleos físicos / 16 lógicos |
| Memoria RAM | 31,7 GB |
| Python | 3.14.4 |
| pandas | 3.0.6 |
| NumPy | 2.5.3 |
| PySpark | 4.2.0 |
| Java | 21.0.9 |

El cuaderno también usa `pyarrow`, `matplotlib`, `psutil` y `kagglehub`. El entorno completo de cada
ejecución queda registrado en `resultados/entorno.json`.

No se probó en Google Colab ni con Java 17. Con menos memoria o menos núcleos, el entrenamiento del modelo
(sección 14) puede tardar mucho más o no completarse.

## Cómo ejecutarlo

### 1. Requisitos

- Python 3 con `pip`.
- **Java 17 o superior** instalado (Spark 4 lo necesita). Para comprobarlo: `java -version`.
- Unos 5 GB libres en disco (3 GB del CSV y 0,8 GB del Parquet que genera el cuaderno).

### 2. Instalar las librerías

```
pip install pyspark pandas numpy pyarrow matplotlib psutil kagglehub jupyter
```

### 3. Descargar el dataset

Descargar `US_Accidents_March23.csv` desde
<https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents> y dejarlo **en la misma carpeta** que el
cuaderno. Si está en otro lugar, indicar la ruta en la variable `RUTA_CSV_MANUAL` de la primera celda de
código.

### 4. Ejecutar

Abrir `proyecto_final_grupo3.ipynb` con Jupyter y ejecutar todas las celdas, en orden.

El cuaderno crea las carpetas `resultados/` y `figuras/`, el archivo `us_accidents.parquet` y
`entregables_grupo3.zip`. Para partir de cero, borrar antes las carpetas `resultados/` y `figuras/`.

Después, para obtener la importancia por variable original:

```
python importancia_por_variable.py
```

### Parámetros principales (primera celda de código)

| Variable | Valor usado | Qué hace |
|---|---|---|
| `REPETICIONES` | 3 | Veces que se ejecuta cada consulta; se informa el mejor tiempo. Con 1 la corrida es más corta |
| `ESCENARIO_PARQUET` | `True` | Convierte el CSV a Parquet y repite las consultas sobre ese formato |
| `C1_DESDE`, `C1_HASTA` | 2021-01-01, 2022-12-31 | Período de la consulta 1 |
| `C4_RADIO_KM`, `C4_CRITERIO` | 2.0, `"graves"` | Radio de influencia y criterio de peligrosidad de la consulta 4 |
| `DURACION_MAX_DIAS` | 7 | Límite de la media acotada de duraciones (consultas 5 y 10) |
| `INTENTAR_CARGA_COMPLETA_PANDAS` | `False` | Experimento opcional de memoria. Dejarlo en `False`: detiene Spark y la sección 14 no se ejecuta |

## Cómo se midió

- Tiempo de reloj de pared, de punta a punta: incluye la lectura del archivo y la consulta, en los dos motores.
- Mejor tiempo de tres ejecuciones; el promedio queda en `resultados/benchmark_detalle.csv`.
- `Speedup = T_Pandas / T_Spark`. Mayor que 1: Spark fue más rápido.
- Después de cada consulta se comprueba que Pandas y Spark devuelvan el mismo resultado, y que el resultado
  sobre Parquet sea igual al obtenido sobre CSV.

## Datos

Moosavi, S. *US Accidents (2016 - 2023)*. Kaggle.
<https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents>
