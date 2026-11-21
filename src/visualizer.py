import matplotlib.pyplot as plt


def _configurar_grafica(ax, title, xlabel, ylabel):
    """
    Aplica el formato comun a todas las graficas
    """

    # Configuramos los titulos y las etiquetas
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=11, labelpad=10)

    # Añadimos la cuadrícula y la leyenda
    ax.grid(True, linestyle=':', alpha=0.4, color='#6272a4')
    ax.legend(
        frameon=True,
        facecolor='#21222c',
        edgecolor='#6272a4',
        fontsize=10
    )


def plot_pitch_analysis(
    lanzamientos,
    metric_real,
    x_dense,
    metric_smooth,
    title,
    xlabel,
    ylabel,
    filename,
    threshold=None
):
    """
    Representa los datos originales junto con el spline cubico
    """

    # Aplicamos el estilo oscuro solo a esta figura
    with plt.style.context('dark_background'):

        fig, ax = plt.subplots(figsize=(10, 6), dpi=120)

        # Mostramos los datos originales
        ax.scatter(
            lanzamientos,
            metric_real,
            color='#ff5555',
            s=90,
            zorder=5,
            label='Datos originales',
            edgecolor='#ffffff',
            linewidth=0.8
        )

        # Dibujamos la curva del spline cubico
        ax.plot(
            x_dense,
            metric_smooth,
            color='#50fa7b',
            linewidth=2.5,
            label='Spline cubico natural'
        )

        # Añadimos un umbral si se proporciona
        if threshold is not None:
            ax.axhline(
                threshold,
                color='#ffb86c',
                linestyle='--',
                linewidth=1.5,
                alpha=0.8,
                label=f'Umbral de referencia ({threshold})'
            )

        # Dejamos un pequeño margen a los lados
        margen = (lanzamientos[-1] - lanzamientos[0]) * 0.05
        ax.set_xlim(
            lanzamientos[0] - margen,
            lanzamientos[-1] + margen
        )

        _configurar_grafica(ax, title, xlabel, ylabel)

        plt.tight_layout()
        fig.savefig(filename, dpi=300)
        plt.close(fig)


def plot_rate_analysis(
    x_dense,
    rate_values,
    title,
    xlabel,
    ylabel,
    filename
):
    """
    Representa la primera derivada del spline cubico
    """

    # Aplicamos el estilo oscuro
    with plt.style.context('dark_background'):

        fig, ax = plt.subplots(figsize=(10, 6), dpi=120)

        # Dibujamos la tasa de cambio
        ax.plot(
            x_dense,
            rate_values,
            color='#50fa7b',
            linewidth=2.5,
            label='Primera derivada del spline'
        )

        # Añadimos la referencia de tasa de cambio nula
        ax.axhline(
            0,
            color='#ffb86c',
            linestyle='--',
            linewidth=1.2,
            label='Tasa de cambio nula'
        )

        _configurar_grafica(ax, title, xlabel, ylabel)

        plt.tight_layout()
        fig.savefig(filename, dpi=300)
        plt.close(fig)


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

    # Aplicamos el estilo oscuro
    with plt.style.context('dark_background'):

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

        # Dibujamos el spline cubico natural
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

        _configurar_grafica(ax, title, xlabel, ylabel)

        plt.tight_layout()
        fig.savefig(filename, dpi=300)
        plt.close(fig)