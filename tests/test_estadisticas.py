import pytest
import numpy as np
import pandas as pd
from src.estadisticas import (
    resumen_estadistico,
    detectar_outliers_iqr,
    analizar_dataframe,
    correlacion_columnas
)


@pytest.fixture
def datos_simples():
    """Fixture con una lista de control para cálculos manuales."""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def datos_con_outliers():
    """Fixture con un valor claramente fuera del rango IQR."""
    return [10, 12, 11, 13, 100]


@pytest.fixture
def df_ejemplo():
    """Fixture de DataFrame para pruebas de pandas."""
    return pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [5, 4, 3, 2, 1],  # Correlación perfecta negativa
        "C": ["no", "soy", "un", "numero", "!"]
    })


def test_resumen_estadistico(datos_simples):
    res = resumen_estadistico(datos_simples)
    np.testing.assert_almost_equal(res["media"], 3.0)
    np.testing.assert_almost_equal(res["percentil_25"], 2.0)
    assert res["minimo"] == 1
    assert res["maximo"] == 5


def test_resumen_vacio():
    with pytest.raises(ValueError, match="no puede estar vacía"):
        resumen_estadistico([])


def test_detectar_outliers(datos_con_outliers):
    outliers = detectar_outliers_iqr(datos_con_outliers)
    assert 100 in outliers
    assert len(outliers) == 1


def test_analizar_dataframe(df_ejemplo):
    res = analizar_dataframe(df_ejemplo, "A")
    assert res["media"] == 3.0

    with pytest.raises(TypeError):
        analizar_dataframe(df_ejemplo, "C")


def test_correlacion(df_ejemplo):
    corr = correlacion_columnas(df_ejemplo, "A", "B")
    np.testing.assert_almost_equal(corr, -1.0)


def test_resumen_estadistico_con_string_lanza_error():
    """Verifica que una lista con tipos no numéricos dispare ValueError."""
    datos_mixtos = [1, 2, "error", 4]
    with pytest.raises(ValueError, match="contiene valores no numéricos"):
        resumen_estadistico(datos_mixtos)


def test_detectar_outliers_iqr_vacio_si_no_hay():
    """Verifica que el método IQR no invente
    outliers en distribuciones uniformes."""
    datos_homogeneos = [10, 10, 10, 10, 10]
    outliers = detectar_outliers_iqr(datos_homogeneos)
    assert outliers == []
    assert isinstance(outliers, list)


def test_analizar_dataframe_columna_inexistente_lanza_error():
    """Verifica el manejo de KeyErrors
    en el acceso a columnas del DataFrame."""
    df = pd.DataFrame({"A": [1, 2, 3]})
    with pytest.raises(KeyError, match="no existe"):
        analizar_dataframe(df, "columna_fantasma")


def test_resumen_error_conversion():
    # Forzamos la línea que lanza ValueError por contenido no convertible
    with pytest.raises(ValueError):
        resumen_estadistico([1, "texto_imposible"])
