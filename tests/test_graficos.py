# tests/test_graficos.py
import os
from src.graficos import histograma, boxplot_comparativo


def test_histograma_genera_archivo(tmp_path):
    ruta = os.path.join(tmp_path, "test_hist.png")
    datos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    histograma(datos, "Test Hist", ruta)

    assert os.path.exists(ruta)
    assert os.path.getsize(ruta) > 0


def test_boxplot_comparativo_genera_archivo(tmp_path):
    ruta = os.path.join(tmp_path, "test_box.png")
    datos_a = [1, 2, 3]
    datos_b = [4, 5, 6]
    etiquetas = ["Grupo A", "Grupo B"]

    boxplot_comparativo(datos_a, datos_b, etiquetas, ruta)

    assert os.path.exists(ruta)
    assert os.path.getsize(ruta) > 0
