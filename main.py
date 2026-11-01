import pandas as pd
import numpy as np
from src.interpolator import PitchInterpolator
from src.visualizer import plot_pitch_analysis

def main():
    # cargamos los datos del partido
    df = pd.read_csv('data/pitch_data.csv')
    
    lanzamientos = df['pitch_id'].values
    velocidades = df['velocity'].values
    release_y = df['release_y'].values
    
    # creamos un rango denso para evaluar la interpolacion de forma continua
    x_dense = np.linspace(lanzamientos[0], lanzamientos[-1], 300)
    
    # instanciamos nuestro interpolador sabermetrico
    interpolador_vel = PitchInterpolator(lanzamientos, velocidades)
    interpolador_ry = PitchInterpolator(lanzamientos, release_y)
    
    # calculamos el spline suavizado para ambas metricas
    v_smooth = interpolador_vel.spline_suavizado(x_dense)
    ry_smooth = interpolador_ry.spline_suavizado(x_dense)
    
    # generamos y guardamos la grafica de fatiga y velocidad
    plot_pitch_analysis(
        lanzamientos, velocidades, v_smooth,
        title='Curvefit: Analisis de Fatiga y Velocidad de Recta',
        xlabel='Numero de Lanzamiento', ylabel='Velocidad (mph)',
        filename='velocity_fatigue.png'
    )
    
    # generamos y guardamos la grafica de deriva mecanica del release
    plot_pitch_analysis(
        lanzamientos, release_y, ry_smooth,
        title='Curvefit: Deriva Mecanica del Punto de Soltar la Bola',
        xlabel='Numero de Lanzamiento', ylabel='Altura del Release (pies)',
        filename='release_drift.png'
    )
    
    print("Proceso finalizado con exito. Graficas generadas en el directorio.")

if name == 'main':
    main()