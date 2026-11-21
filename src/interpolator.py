import numpy as np
from scipy.interpolate import CubicSpline, lagrange


class PitchInterpolator:
    """
    Clase para aplicar métodos de interpolación numérica
    a métricas de lanzamientos de béisbol
    """

    def __init__(self, pitch_ids, metric_values):

        self.x = np.asarray(pitch_ids, dtype=float)
        self.y = np.asarray(metric_values, dtype=float)

        if self.x.ndim != 1 or self.y.ndim != 1:
            raise ValueError("Los datos deben ser vectores unidimensionales")

        if len(self.x) != len(self.y):
            raise ValueError(
                "Los identificadores y las métricas deben tener "
                "la misma longitud"
            )

        if len(self.x) < 2:
            raise ValueError("Se necesitan al menos dos puntos de datos")

        if not np.all(np.isfinite(self.x)) or not np.all(np.isfinite(self.y)):
            raise ValueError(
                "Los datos no pueden contener valores NaN o infinitos"
            )

        if not np.all(np.diff(self.x) > 0):
            raise ValueError(
                "Los identificadores deben estar ordenados de forma "
                "creciente y no pueden repetirse."
            )

    def spline_cubico(self, x_dense):
        """
        Calcula la interpolación mediante spline cúbico natural.
        La función y sus dos primeras derivadas son continuas (C2).
        La segunda derivada es cero en ambos extremos.
        """

        cs = CubicSpline(self.x, self.y, bc_type='natural')

        return cs(x_dense)

    def tasa_cambio(self, x_dense):
        """
        Calcula la primera derivada del spline cúbico.
        Representa la tasa de variación de la métrica
        respecto al identificador del lanzamiento.
        """

        cs = CubicSpline(self.x, self.y, bc_type='natural')

        return cs.derivative(1)(x_dense)

    def polinomio_lagrange(self, x_dense):
        """
        Calcula el polinomio interpolador global de Lagrange.
        Se utiliza para comparar su comportamiento con el spline.
        """

        poly = lagrange(self.x, self.y)

        return poly(x_dense)