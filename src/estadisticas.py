# src/estadisticas.py
import numpy as np
import pandas as pd


def resumen_estadistico(datos: list) -> dict:
    if not datos:
        raise ValueError("La lista de datos no puede estar vacía.")

    try:
        arr = np.array(datos, dtype=float)
    except (ValueError, TypeError):
        raise ValueError("La lista contiene valores no numéricos.")

    return {
        "media": float(np.mean(arr)),
        "mediana": float(np.median(arr)),
        "desv_tipica": float(np.std(arr)),
        "minimo": float(np.min(arr)),
        "maximo": float(np.max(arr)),
        "percentil_25": float(np.percentile(arr, 25)),
        "percentil_75": float(np.percentile(arr, 75))
    }


def detectar_outliers_iqr(datos: list) -> list:
    if not datos:
        return []

    arr = np.array(datos, dtype=float)
    q1 = np.percentile(arr, 25)
    q3 = np.percentile(arr, 75)
    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    outliers = arr[(arr < limite_inferior) | (arr > limite_superior)]
    return outliers.tolist()


def analizar_dataframe(df: pd.DataFrame, columna: str) -> dict:
    if columna not in df.columns:
        raise KeyError(f"La columna '{columna}' no existe en el DataFrame.")

    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise TypeError(f"La columna '{columna}' debe ser de tipo numérico.")

    return resumen_estadistico(df[columna].dropna().tolist())


def correlacion_columnas(df: pd.DataFrame, col1: str, col2: str) -> float:
    return float(df[col1].corr(df[col2], method='pearson'))
