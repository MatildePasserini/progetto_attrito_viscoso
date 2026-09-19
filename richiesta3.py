# Fare uno studio statistico della distribuzione della posizione di caduta per sfere con incertezza
# gaussiana nel raggio (materiale, angolo e massa fissi).

import sys
import numpy as np
import scipy
import matplotlib.pyplot as plt
from matplotlib import transforms
from scipy.stats import norm
from richiesta1 import attrito
from richiesta2 import massa, grandezze

#SCELTE PRELIMINARI
# Coefficienti di viscosità dell'aria e acqua (Pa*s)

fluidi = {
        "aria": 18.6 * 10**-6,
        "acqua": 8.94 * 10**-4
}

v_0 = 5      # m/s
theta0 = 45  # gradi

# Ferro: materiale scelto per lo studio (r0 preso come raggio medio)

rho = 7870  # kg/m^3
r0 = 0.3e-3 # m

# Dispersione della deviazioni standard che verranno variate e numero di sfere simulate per ogni sigma_r

sigma_r_variata = [0.05 * r0, 0.10 * r0, 0.20 * r0]

N = 200


# CAMPIONAMENTO CON CUMULATIVA
# densità di probabilità gaussiana teorica

def dens_prob(r, r0, sigma_r):

    return norm.pdf(r, loc = r0, scale = sigma_r)

# funzione che genera raggi campionati

def r_cum(N, r0, sigma_r):

    r = np.array([])

    while len(r) < N:
        n_mancanti = N -len(r)
        cum = np.random.random(n_mancanti)
        r_nuovi = norm.ppf(cum, loc = r0, scale = sigma_r)

        r_validi = r_nuovi[r_nuovi > 0]
        r = np.concatenate((r, r_validi))

    return r


# SIMULAZIONE: per ciascun raggio campionato calcolo la massa, risolvo equazione del moto.

def simula_gittate(rho, r0, sigma_r, mu, v_0, theta0, N):

    raggi = r_cum(N, r0, sigma_r)
    gittate = []

    for r_s in raggi:

        m = massa(rho, r_s)
        _, soluzione = attrito(m, r_s, mu, v_0, theta0)
        gittata, _, _ = grandezze(soluzione)
        gittate.append(gittata)

    return raggi, np.array(gittate)

# GRAFICI
# istrogramma dei raggi campionati sovrapposto alla curva teoria

def grafico_distr_raggi(nome_fluido,sigma_r):

    raggi = r_cum(N, r0, sigma_r)

    plt.figure(figsize = (9,7))
    plt.hist(raggi, bins = 15, density = True, color = "blue", alpha = 0.6,
             label = " Raggi campionati con cumulativa")

    xx = np.linspace(raggi.min(), raggi.max(), 200)

    plt.plot(xx, dens_prob(xx, r0, sigma_r), color = "red", label = "P(r) teorica")
    plt.title (f"Verifica del campionamento dei raggi - {nome_fluido}\n"
               f"$\\sigma_r$ = {sigma_r:.2e} m", fontsize=16)

    plt.xlabel("raggio [m]", fontsize=14)
    plt.ylabel("densità di probabilità", fontsize=14)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# grafico che simula le gittate al variare di sigma_r e ne disegna l'hist

def grafico_distr_gittate(nome_fluido, mu):

    plt.figure(figsize=(9,7))

    for sigma_r in sigma_r_variata:

        _, gittate = simula_gittate(rho, r0, sigma_r, mu, v_0, theta0, N)

        plt.hist(gittate, bins = 15, density=True, alpha = 0.6,
                 label = f"$\\sigma_r$ = {sigma_r:.2e} m")

    plt.title(f"Distribuzione della gittata al variare di $\\sigma_r$ - {nome_fluido}\n", fontsize=16)

    plt.xlabel("gittata [m]", fontsize=14)
    plt.ylabel("p(gittata)", fontsize=14)
    plt.legend()
    plt.grid(alpha = 0.4)
    plt.tight_layout()
    plt.show()

def grafico_raggi_gittata(nome_fluido, mu, sigma_r):

    raggi, gittate = simula_gittate(rho, r0, sigma_r, mu, v_0, theta0, N)

    plt.figure(figsize=(9,7))
    plt.scatter(raggi, gittate, s=8, alpha=0.4)
    plt.title(f" Gittata vs raggio campionato - {nome_fluido}\n"
              f"$\\sigma_r$ = {sigma_r:.2e} m", fontsize=16)
    plt.xlabel("raggio [m]", fontsize=14)
    plt.ylabel("gittata [m]", fontsize=14)
    plt.grid()
    plt.tight_layout()
    plt.show()

#ESECUZIONE GRAFICI

if __name__ == "__main__":

     for nome_fluido, mu in fluidi.items():

         grafico_distr_raggi(nome_fluido, sigma_r_variata[1])
         grafico_distr_gittate(nome_fluido, mu)
         grafico_raggi_gittata(nome_fluido, mu, sigma_r_variata[1])
