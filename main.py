from pathlib import Path

import numpy as np
import pandas as pd

from src.interpolator import PitchInterpolator
from src.visualizer import  (
    plot_pitch_analysis, plot_rate_analysis, plot_interpolation_comparison
)


def main():

    # Definimos las rutas del proyecto
    directorio = Path(__file__).resolve().parent
    ruta_datos = directorio / 'data' / 'pitch_data.csv'
    directorio_salida = directorio

    # Comprobamos que el archivo de datos exista
    if not ruta_datos.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo de datos: {ruta_datos}"
        )

    # Cargamos los datos sinteticos del proyecto
    df = pd.read_csv(ruta_datos)

    # Comprobamos que esten presentes todas las columnas necesarias
    columnas = ['pitch_id', 'velocity', 'release_x', 'release_y']

    for columna in columnas:
        if columna not in df.columns:
            raise ValueError(
                f"Falta la columna obligatoria: {columna}"
            )

    # Convertimos las metricas a valores numericos
    for columna in columnas:
        df[columna] = pd.to_numeric(df[columna], errors='raise')

    # Comprobamos que no existan valores vacios o infinitos
    if not np.all(np.isfinite(df[columnas].to_numpy())):
        raise ValueError("El archivo contiene valores vacios o no validos")

    # Ordenamos los registros por identificador de lanzamiento
    df = df.sort_values('pitch_id')

    lanzamientos = df['pitch_id'].to_numpy()
    velocidades = df['velocity'].to_numpy()
    release_x = df['release_x'].to_numpy()
    release_y = df['release_y'].to_numpy()

    # Calculamos algunos indicadores estadisticos de la velocidad
    velocidad_media = np.mean(velocidades)
    velocidad_maxima = np.max(velocidades)
    velocidad_minima = np.min(velocidades)

    # Comparamos la primera y la ultima medicion
    cambio_velocidad = velocidades[-1] - velocidades[0]
    cambio_porcentual = (cambio_velocidad / velocidades[0]) * 100

    # Mostramos el resumen en consola
    print("\n===== RESUMEN DEL ANALISIS =====")
    print(f"Velocidad media: {velocidad_media:.2f} mph")
    print(f"Velocidad maxima: {velocidad_maxima:.2f} mph")
    print(f"Velocidad minima: {velocidad_minima:.2f} mph")
    print(f"Cambio de velocidad: {cambio_velocidad:.2f} mph")
    print(f"Variacion porcentual: {cambio_porcentual:.2f}%")

    # Creamos un rango denso para representar las curvas interpoladas
    x_dense = np.linspace(lanzamientos[0], lanzamientos[-1], 300)

    # Creamos los interpoladores para cada metrica
    interpolador_vel = PitchInterpolator(lanzamientos, velocidades)
    interpolador_rx = PitchInterpolator(lanzamientos, release_x)
    interpolador_ry = PitchInterpolator(lanzamientos, release_y)

    # Calculamos los splines cubicos naturales
    v_spline = interpolador_vel.spline_cubico(x_dense)
    rx_spline = interpolador_rx.spline_cubico(x_dense)
    ry_spline = interpolador_ry.spline_cubico(x_dense)

    # Calculamos el polinomio de Lagrange para comparar los metodos
    v_lagrange = interpolador_vel.polinomio_lagrange(x_dense)

    # Comparamos los valores que producen ambos metodos
    diferencias = np.abs(v_spline - v_lagrange)

    diferencia_maxima = np.max(diferencias)
    diferencia_media = np.mean(diferencias)

    # Buscamos donde ocurre la mayor diferencia
    indice_maximo = np.argmax(diferencias)
    posicion_maxima = x_dense[indice_maximo]

    print("\n===== COMPARACION DE INTERPOLADORES =====")
    print(f"Diferencia maxima: {diferencia_maxima:.6f} mph")
    print(f"Diferencia media: {diferencia_media:.6f} mph")
    print(f"Mayor diferencia en pitch_id: {posicion_maxima:.2f}")

    # Calculamos la tasa de cambio de la velocidad
    tasa_velocidad = interpolador_vel.tasa_cambio(x_dense)

    # Analizamos la velocidad de los lanzamientos
    plot_pitch_analysis(
        lanzamientos,
        velocidades,
        x_dense,
        v_spline,
        title='Curvefit: Evolucion de la Velocidad',
        xlabel='Identificador del Lanzamiento',
        ylabel='Velocidad (mph)',
        filename=str(directorio_salida / 'velocity_analysis.png')
    )

    # Analizamos la posicion horizontal del punto de liberacion
    plot_pitch_analysis(
        lanzamientos,
        release_x,
        x_dense,
        rx_spline,
        title='Curvefit: Posicion Horizontal del Release',
        xlabel='Identificador del Lanzamiento',
        ylabel='Posicion Horizontal (pies)',
        filename=str(directorio_salida / 'release_x_analysis.png')
    )

    # Analizamos la altura del punto de liberacion
    plot_pitch_analysis(
        lanzamientos,
        release_y,
        x_dense,
        ry_spline,
        title='Curvefit: Altura del Release',
        xlabel='Identificador del Lanzamiento',
        ylabel='Altura (pies)',
        filename=str(directorio_salida / 'release_y_analysis.png')
    )

    # Representamos la tasa de cambio de la velocidad
    plot_rate_analysis(
    x_dense,
    tasa_velocidad,
    title='Curvefit: Tasa de Cambio de la Velocidad',
    xlabel='Identificador del Lanzamiento',
    ylabel='Variacion de velocidad (mph por unidad de pitch_id)',
    filename=str(directorio_salida / 'velocity_rate.png')
)

   # Comparamos los dos metodos de interpolacion
    plot_interpolation_comparison(
    lanzamientos,
    velocidades,
    x_dense,
    v_spline,
    v_lagrange,
    title='Curvefit: Comparacion de Metodos de Interpolacion',
    xlabel='Identificador del Lanzamiento',
    ylabel='Velocidad (mph)',
    filename=str(directorio_salida / 'interpolation_comparison.png')
)

    print("Analisis finalizado correctamente")
    print("Se han generado cinco graficas en el directorio del proyecto")


if __name__ == '__main__':
    main()