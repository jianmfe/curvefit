import pandas as pd
import numpy as np
from src.interpolator import PitchInterpolator
from src.visualizer import plot_pitch_analysis

def main():
    # Cargamos los datos del partido
    df = pd.read_csv('data/pitch_data.csv')
    
    lanzamientos = df['pitch_id'].values
    velocidades = df['velocity'].values
    release_y = df['release_y'].values
    
    # Creamos un rango denso para evaluar la interpolacion de forma continua
    x_dense = np.linspace(lanzamientos[0], lanzamientos[-1], 300)
    
    # Instanciamos nuestro interpolador sabermetrico
    interpolador_vel = PitchInterpolator(lanzamientos, velocidades)
    interpolador_ry = PitchInterpolator(lanzamientos, release_y)
    
    # Calculamos el spline suavizado para ambas metricas
    v_smooth = interpolador_vel.spline_suavizado(x_dense)
    ry_smooth = interpolador_ry.spline_suavizado(x_dense)
    
    # Generamos y guardamos la grafica de fatiga y velocidad 
    # (añadimos opcionalmente una línea de umbral de 95 mph para nivel élite)
    plot_pitch_analysis(
        lanzamientos, velocidades, x_dense, v_smooth,
        title='Curvefit: Analisis de Fatiga y Velocidad de Recta',
        xlabel='Numero de Lanzamiento', ylabel='Velocidad (mph)',
        filename='velocity_fatigue.png',
        threshold=95.0
    )
    
    # Generamos y guardamos la grafica de deriva mecanica del release
    plot_pitch_analysis(
        lanzamientos, release_y, x_dense, ry_smooth,
        title='Curvefit: Deriva Mecanica del Punto de Soltar la Bola',
        xlabel='Numero de Lanzamiento', ylabel='Altura del Release (pies)',
        filename='release_drift.png'
    )
    
    print("Proceso finalizado con exito. Graficas generadas en el directorio.")

if __name__ == '__main__':
    main()