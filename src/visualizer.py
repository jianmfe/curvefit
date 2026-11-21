import numpy as np
import matplotlib.pyplot as plt

def plot_pitch_analysis(lanzamientos, metric_real, x_dense, metric_smooth, title, xlabel, ylabel, filename, threshold=None):
    """
    Genera una gráfica comparando los datos discretos
    del partido frente a la curva continua modelada por el spline cúbico.
    Incluye soporte para líneas de umbral crítico sabermétrico
    """
    # Configuramos un estilo oscuro 
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
    
    # Ploteo de los puntos discretos reales registrados en el juego
    ax.scatter(
        lanzamientos, metric_real, 
        color='#ff5555', s=90, zorder=5, 
        label='Datos Registrados (CSV)', edgecolor='#ffffff', linewidth=0.8
    )
    
    # Trazado de la curva continua del spline cúbico con el dominio denso recibido
    ax.plot(
        x_dense, metric_smooth, 
        color='#50fa7b', linewidth=2.5, linestyle='-',
        label='Interpolación Spline Cúbico ($C^2$)'
    )
    
    # Si se pasa un umbral crítico (ej. línea de alerta de fatiga), se dibuja
    if threshold is not None:
        ax.axhline(
            threshold, color='#ffb86c', linestyle='--', linewidth=1.5, alpha=0.8,
            label=f'Umbral Crítico ({threshold})'
        )
    
    # Margen estético en el eje X para que los puntos extremos no toquen el borde
    margin = (lanzamientos[-1] - lanzamientos[0]) * 0.05
    ax.set_xlim(lanzamientos[0] - margin, lanzamientos[-1] + margin)
    
    # Detalles estéticos
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15, color='#f8f8f2')
    ax.set_xlabel(xlabel, fontsize=11, labelpad=10, color='#f8f8f2')
    ax.set_ylabel(ylabel, fontsize=11, labelpad=10, color='#f8f8f2')
    
    # Cuadrícula técnica
    ax.grid(True, linestyle=':', alpha=0.4, color='#6272a4')
    
    # Leyenda
    ax.legend(frameon=True, facecolor='#21222c', edgecolor='#6272a4', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


def plot_rate_analysis(x_dense, rate_values, title, xlabel, ylabel, filename):
    """
    Representa la tasa de cambio calculada mediante la derivada
    del spline cubico
    """

    # Creamos la figura
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)

    # Dibujamos la tasa de cambio
    ax.plot(
        x_dense,
        rate_values,
        color='#50fa7b',
        linewidth=2.5,
        label='Primera derivada del spline'
    )

    # Añadimos una referencia donde la tasa de cambio es cero
    ax.axhline(
        0,
        color='#ffb86c',
        linestyle='--',
        linewidth=1.2,
        label='Tasa de cambio nula'
    )

    # Configuramos los detalles de la grafica
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=11, labelpad=10)

    ax.grid(True, linestyle=':', alpha=0.4)
    ax.legend()

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

def plot_interpolation_comparison(
    lanzamientos,
    metric_real,
    x_dense,
    spline_values,
    lagrange_values,
    title,
    xlabel,
    ylabel,
    filename
):
    """
    Compara la interpolacion mediante spline cubico y Lagrange
    """

    # Creamos la figura
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)

    # Mostramos los datos originales
    ax.scatter(
        lanzamientos,
        metric_real,
        color='#ff5555',
        s=70,
        zorder=5,
        label='Datos originales',
        edgecolor='#ffffff',
        linewidth=0.8
    )

    # Dibujamos el spline cubico
    ax.plot(
        x_dense,
        spline_values,
        color='#50fa7b',
        linewidth=2.5,
        label='Spline cubico natural'
    )

    # Dibujamos el polinomio de Lagrange
    ax.plot(
        x_dense,
        lagrange_values,
        color='#8be9fd',
        linewidth=2,
        linestyle='--',
        label='Polinomio de Lagrange'
    )

    # Configuramos los detalles de la grafica
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=11, labelpad=10)

    ax.grid(True, linestyle=':', alpha=0.4, color='#6272a4')
    ax.legend()

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()