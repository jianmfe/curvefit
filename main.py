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