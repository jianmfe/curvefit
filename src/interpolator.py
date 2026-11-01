import numpy as np
from scipy.interpolate import CubicSpline, lagrange

class PitchInterpolator:
    def init(self, pitch_ids, metric_values):
        # guardamos los datos de entrada ordenados por numero de lanzamiento
        self.x = np.asarray(pitch_ids)
        self.y = np.asarray(metric_values)
        
    def spline_suavizado(self, x_dense):
        # usamos spline cubico natural porque garantiza continuidad c2
        # esto es clave en cinematica ya que el brazo humano no tiene cambios bruscos de aceleracion
        cs = CubicSpline(self.x, self.y, bc_type='natural')
        return cs(x_dense)
    
    def tasa_fatiga(self, x_dense):
        # la gran ventaja para nosotros como analistas es derivar el spline
        # esto nos da la pendiente instantanea o tasa de cambio de la metrica por cada lanzamiento
        cs = CubicSpline(self.x, self.y, bc_type='natural')
        derivada_primera = cs.derivative(1)
        return derivada_primera(x_dense)

    def polinomio_lagrange(self, x_dense):
        # esto lo usamos puramente para el reporte tecnico y mostrar por que falla
        # un polinomio de grado alto en todo el partido genera oscilaciones locas en los extremos
        poly = lagrange(self.x, self.y)
        return poly(x_dense)