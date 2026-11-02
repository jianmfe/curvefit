import numpy as np
import matplotlib.pyplot as plt

def plot_pitch_analysis(lanzamientos, metric_real, x_dense, metric_smooth, title, xlabel, ylabel, filename, threshold=None):
    """
    Genera una gráfica de alta calidad técnica comparando los datos discretos
    del partido frente a la curva continua modelada por el spline cúbico.
    Incluye soporte para líneas de umbral crítico sabermétrico.
    """
    # Configuramos un estilo oscuro profesional de analítica
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
    
    # Ploteamos los puntos discretos reales registrados en el juego
    ax.scatter(
        lanzamientos, metric_real, 
        color='#ff5555', s=90, zorder=5, 
        label='Datos Registrados (CSV)', edgecolor='#ffffff', linewidth=0.8
    )
    
    # Trazamos la curva continua del spline cúbico con el dominio denso recibido
    ax.plot(
        x_dense, metric_smooth, 
        color='#50fa7b', linewidth=2.5, linestyle='-',
        label='Interpolación Spline Cúbico ($C^2$)'
    )
    
    # Si se pasa un umbral crítico (ej. línea de alerta de fatiga), lo dibujamos
    if threshold is not None:
        ax.axhline(
            threshold, color='#ffb86c', linestyle='--', linewidth=1.5, alpha=0.8,
            label=f'Umbral Crítico ({threshold})'
        )
    
    # Margen estético en el eje X para que los puntos extremos no toquen el borde
    margin = (lanzamientos[-1] - lanzamientos[0]) * 0.05
    ax.set_xlim(lanzamientos[0] - margin, lanzamientos[-1] + margin)
    
    # Detalles estéticos orientados a reporte académico/técnico
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15, color='#f8f8f2')
    ax.set_xlabel(xlabel, fontsize=11, labelpad=10, color='#f8f8f2')
    ax.set_ylabel(ylabel, fontsize=11, labelpad=10, color='#f8f8f2')
    
    # Cuadrícula técnica sutil
    ax.grid(True, linestyle=':', alpha=0.4, color='#6272a4')
    
    # Leyenda estilizada acorde al tema oscuro
    ax.legend(frameon=True, facecolor='#21222c', edgecolor='#6272a4', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()