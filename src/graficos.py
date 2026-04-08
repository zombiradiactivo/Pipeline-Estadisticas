# src/graficos.py
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('Agg')


def histograma(datos: list, titulo: str, ruta: str) -> None:
    plt.figure()
    plt.hist(datos, bins=10, color='skyblue', edgecolor='black', alpha=0.7)

    media = float(np.mean(datos))  # Conversión explícita
    plt.axvline(media, color='red',
                linestyle='dashed',
                linewidth=2,
                label=f'Media: {media:.2f}')

    plt.title(titulo)
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.savefig(ruta)
    plt.close()


def boxplot_comparativo(datos_a: list, datos_b: list,
                        etiquetas: list, ruta: str) -> None:
    plt.figure()
    plt.boxplot([datos_a, datos_b], tick_labels=etiquetas)
    plt.title('Comparativa de Distribuciones')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(ruta)
    plt.close()
