# Risolvere l'equazione differenziale con tutti i parametri configurabili

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, constants

# Funzione che descrive l'equazione differenziale del moto di un corpo sferico
# soggetto ad attrito viscoso

def attrito_eqn (t, r, m, r_s, mu ):

    """
    r : vettore con variabili r(x, y, v_x, v_y)
    t : variabile tempo
    m : massa del corpo
    r_s : raggio del corpo sferico
    mu : coefficiente di viscosità

    """

    g = constants.g

    # componenti del vettore r
    x = r[0]
    y = r[1]
    v_x = r[2]
    v_y = r[3]

    # derivate per equazione differenziale del moto di un corpo sferico soggetto ad attrito viscoso
    dxdt = v_x
    dydt = v_y
    dv_xdt = -(6 * np.pi * mu * r_s/m) * v_x
    dv_ydt = -g - (6 * np.pi * mu * r_s/m) * v_y

    return (dxdt, dydt, dv_xdt, dv_ydt)

# Definizione delle condizioni iniziali e parametri di simulazione

def attrito(m, r_s, mu, v0, theta0):

    # condizioni iniziali
    x0 = 0
    y0 = 0

    theta0 = np.radians(theta0)

    v_x0 = v0 * np.sin(theta0) # m/s
    v_y0 = v0 * np.cos(theta0) # m/s

    rinit = (x0, y0, v_x0, v_y0)

    # arrray con tempi per non avere una traiettoria con y<0
    def caduta_terra(t, r, m, r_s, mu):

        return r[1]
    caduta_terra.terminal = True
    caduta_terra.direction = -1

    sol = integrate.solve_ivp(attrito_eqn, [0, 100], rinit,
          args = (m, r_s, mu), events = caduta_terra, max_step = 0.01, dense_output = True)

    return sol.t, sol.y.T

if __name__ == "__main__":

     # parametri
     m = 0.004 # kg
     r_s = 0.01 # m
     mu = 0.83 # Pa * s
     v0 = 5.00 # m/s
     theta0 = 30 # gradi

     ptimes, soluzione = attrito(m, r_s, mu, v0, theta0)


     # grafico traiettoria
     plt.figure(figsize=(9,7))
     plt.title( 'Traiettoria di un corpo soggetto ad attrito viscoso', fontsize=16)
     plt.plot(soluzione[:,0], soluzione[:,1])

     plt.xlabel('x [m]', fontsize = 14)
     plt.ylabel('y [m]', fontsize = 14)
     plt.grid()
     plt.xticks(fontsize = 14)
     plt.yticks(fontsize = 14)

     plt.show()

