"""Suma la importancia del bosque aleatorio por variable original y por grupo de la hipótesis.

El cuaderno guarda la importancia de cada columna de entrada del modelo en
resultados/consigna6_importancia_variables.csv. Como la codificación one-hot reparte cada variable
categórica en varias columnas (por ejemplo, Crossing_ohe_true y Crossing_ohe_false), este script suma
las columnas de cada variable original. Es la Tabla 9 del artículo.

Uso (desde la carpeta del repositorio):  python importancia_por_variable.py
Solo usa la biblioteca estándar de Python.
"""
import csv
from collections import defaultdict

ENTRADA = "resultados/consigna6_importancia_variables.csv"
SALIDA = "resultados/consigna6_importancia_por_variable.csv"

NUMERICAS = ["Temperature_F", "Humidity_pct", "Pressure_in", "Visibility_mi", "Wind_Speed_mph", "Precipitation_in"]
TIEMPO = ["hora_inicio", "dia_semana", "mes"]
INFRAESTRUCTURA = ["Amenity", "Bump", "Crossing", "Give_Way", "Junction", "No_Exit", "Railway", "Roundabout",
                   "Station", "Stop", "Traffic_Calming", "Traffic_Signal"]

GRUPO = {v: "Meteorología" for v in NUMERICAS + ["Weather_Condition"]}
GRUPO.update({v: "Momento" for v in TIEMPO + ["Sunrise_Sunset"]})
GRUPO.update({v: "Infraestructura vial" for v in INFRAESTRUCTURA})
GRUPO["State"] = "Ubicación"


def variable_original(columna):
    # "Pressure_in_imputada" -> "Pressure_in";  "State_ohe_CA" -> "State"
    for variable in sorted(GRUPO, key=len, reverse=True):
        if columna == variable + "_imputada" or columna.startswith(variable + "_ohe_"):
            return variable
    raise ValueError(f"Columna no reconocida: {columna}")


por_variable, por_grupo = defaultdict(float), defaultdict(float)
with open(ENTRADA, encoding="utf-8", newline="") as f:
    for fila in csv.DictReader(f):
        variable = variable_original(fila["variable"])
        por_variable[variable] += float(fila["importancia"])
        por_grupo[GRUPO[variable]] += float(fila["importancia"])

filas = sorted(por_variable.items(), key=lambda par: -par[1])
with open(SALIDA, "w", encoding="utf-8", newline="") as f:
    salida = csv.writer(f)
    salida.writerow(["grupo", "variable", "importancia", "importancia_del_grupo"])
    for variable, importancia in filas:
        salida.writerow([GRUPO[variable], variable, f"{importancia:.6f}", f"{por_grupo[GRUPO[variable]]:.6f}"])

print("Importancia por grupo")
for grupo, importancia in sorted(por_grupo.items(), key=lambda par: -par[1]):
    print(f"  {grupo:<22}{importancia:.3f}")
print("\nImportancia por variable original")
for variable, importancia in filas:
    print(f"  {variable:<22}{importancia:.3f}   {GRUPO[variable]}")
print(f"\nSuma total: {sum(por_variable.values()):.3f}")
print("Guardado en", SALIDA)
