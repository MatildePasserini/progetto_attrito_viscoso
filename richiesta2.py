#Partendo da parametri tipici dell'atmosfera terrestre e dell'acqua studiare alcuni parametri
# al variare di altri

import numpy as np
import matplotlib.pyplot as plt
from richiesta1 import attrito

# SCELTE PRELIMINARI
# Coefficienti di viscosità dei fluidi dati dal problema (Pa*s)

fluidi = {
	"aria": 18.6 * 10**-6,
	"acqua":8.94 * 10**-4
}

v_0 = 5.00 # m/s

# Materiali scelti, rispettive densità (kg/m^3) e raggi di riferimento (m)

materiali = {
	"ferro" : 7870,
	"vetro" : 2500,
	"rame" : 8960
}

raggi = {
	"ferro" : 0.3e-3,
	"vetro" : 0.4e-3,
	"rame" : 0.25e-3
}

# Fattori di scala usati per variare il raggio di riferimento

fattori_raggio = np.linspace(0.3, 2.0, 8)

# Angoli theta rispetto alla verticale

theta_z = [0, 30, 45, 60] # gradi

# Calcolo massa partendo dalla densità

def massa(rho, raggio):

    return 4/3 * np.pi * (raggio**3) * rho


# CALCOLO GRANDEZZE RICHIESTE

def grandezze(soluzione):

    # 1. coordinate e componenti della velocità

    x = soluzione[:, 0]
    y = soluzione[:, 1]

    v_x = soluzione[:, 2]
    v_y = soluzione[:, 3]

    # 2. gittata: l'ultimo punto della simulazione coincide con il momento in cui torna a terra
    gittata = x[-1]

    # 3. altezza massima
    altezza_massima = np.max(y)

    # 4. massima velocità di caduta
    idx_apice = np.argmax(y)
    v_tot_caduta = np.sqrt(v_x[idx_apice:] ** 2 + v_y[idx_apice:] ** 2)
    v_max_caduta = np.max(v_tot_caduta)

    return gittata, altezza_massima, v_max_caduta


# GRAFICI

colori = {
        "ferro" : "blue",
        "vetro" : "green",
        "rame" : "orange",
}

# 1.1 traiettoria VS angolo

def grafico_traiettoria_angolo(nome_fluido, mu):

    for theta0 in theta_z:

         plt.figure(figsize=(9,7))

         for nome_materiale in materiali:

             rho = materiali[nome_materiale]
             r_s = raggi[nome_materiale]
             m = massa(rho, r_s)

             ptimes, soluzione = attrito(m, r_s, mu, v_0, theta0)

             plt.plot(soluzione[:,0], soluzione[:,1],
                      label = nome_materiale, color = colori[nome_materiale] )

         plt.title(f"Traiettoria al variare dell'angolo - {nome_fluido}\n"
                   f" $\\theta_0$ = {theta0}°", fontsize=16)
         plt.xlabel("x [m]", fontsize = 14)
         plt.ylabel("y [m]", fontsize = 14)
         plt.tight_layout()
         plt.legend()
         plt.grid()
         plt.show()

# 1.2 Traiettoria VS massa

def grafico_traiettoria_massa(nome_fluido,mu):

    parametri_massa = [0.5, 1.0, 1.5]

    theta0 = 45

    for parametro in parametri_massa:

        plt.figure(figsize = (9,7))

        for nome_materiale in materiali:

            rho = materiali[nome_materiale]
            r_s = raggi[nome_materiale]
            m_riferimento = massa(rho, r_s)
            m = parametro * m_riferimento

            ptimes, soluzione = attrito(m, r_s, mu, v_0, theta0)

            plt.plot(soluzione [:,0], soluzione[:,1], color = colori[nome_materiale],
                     label = f"{nome_materiale}, m = {m:.2e} kg")

        plt.title(f"Traiettoria al variare della massa - {nome_fluido}\n"
                  f"fattore = {parametro} * massa di riferimento", fontsize = 16)
        plt.xlabel("x[m]", fontsize = 14)
        plt.ylabel("y[m]", fontsize = 14)
        plt.legend()
        plt.grid()
        plt.show()

#1.3 Traiettoria VS raggio

def grafico_traiettoria_raggio(nome_fluido, mu):

    theta0 = 45
    fattori_raggio = np.linspace(0.3, 2.0, 8)

    for nome_materiale in materiali:

        rho = materiali[nome_materiale]
        r_riferimento = raggi[nome_materiale]
        m = massa(rho, r_riferimento)

        plt.figure(figsize = (9,7))
        #scala colori ( dal più chiaro (r piccolo) al più scuro (r grande))
        cmap = plt.cm.viridis
        colori_gradiente = cmap(np.linspace(0.15, 0.9, len(fattori_raggio)))

        for fattore, colore in zip(fattori_raggio, colori_gradiente):

            r_s = fattore * r_riferimento
            ptimes, soluzione = attrito(m, r_s, mu, v_0, theta0)

            plt.plot(soluzione[:,0], soluzione[:,1], color = colore,
                     label=f"fattore = {fattore:.2f} (r = {r_s:.2e} m)")

        plt.title(f"Traiettoria del {nome_materiale} al variare del raggio\n"
                  f"{nome_fluido}", fontsize = 16)
        plt.xlabel("x [m]", fontsize = 14)
        plt.ylabel("y [m]", fontsize = 14)
        plt.legend()
        plt.grid()
        plt.show()

# 2.1. Gittata VS massa

def grafico_gittata_m(nome_fluido, mu):

    plt.figure(figsize = (9, 7))

    for nome_materiale in materiali:

        r_s = raggi[nome_materiale]
        rho = materiali[nome_materiale]
        m_riferimento = massa(rho, r_s)
        masse_variate = np.linspace(0.5 * m_riferimento, 1.5 * m_riferimento, 10)

        gittate = []

        for m in masse_variate:

            ptimes, soluzione = attrito( m, r_s, mu, v_0, 45)
            gittata, _, _  = grandezze(soluzione)
            gittate.append(gittata)

        plt.plot( masse_variate, gittate, color = colori[nome_materiale],
                  label = nome_materiale)

    plt.title(f"Gittata in funzione della massa - {nome_fluido}\n"
              f"$\\theta_0$ = 45°", fontsize=16)
    plt.xlabel("massa [kg]", fontsize = 14)
    plt.ylabel("gittata [m]", fontsize = 14)
    plt.legend()
    plt.grid()
    plt.show()

# 2.2 Gittata VS raggio

def grafico_gittata_raggio(nome_fluido, mu):

    plt.figure(figsize = (9,7))

    for nome_materiale in materiali:

        rho = materiali[nome_materiale]
        r_riferimento = raggi[nome_materiale]
        m = massa(rho, r_riferimento)
        raggi_varianti = np.linspace( 0.5 * r_riferimento, 1.5* r_riferimento, 10)

        gittate = []

        for r_s in raggi_varianti:

            ptimes , soluzione = attrito(m, r_s, mu, v_0, 45)
            gittata, _, _ = grandezze(soluzione)
            gittate.append(gittata)

        plt.plot( raggi_varianti, gittate, color = colori[nome_materiale],
                  label = nome_materiale)

    plt.title(f"Gittata in funzione del ragggio - {nome_fluido}\n"
              f"$\\theta_0$ = 45°", fontsize = 16)
    plt.xlabel("raggio [m]", fontsize = 14)
    plt.ylabel("gittata [m]", fontsize = 14)
    plt.legend()
    plt.grid()
    plt.show()

# 2.3 Gittata VS angolo

def grafico_gittata_angolo(nome_fluido, mu):

    plt.figure(figsize = (9,7))

    for nome_materiale in materiali:

        rho = materiali[nome_materiale]
        r_s = raggi[nome_materiale]
        m = massa(rho, r_s)

        gittate = []

        for theta0 in theta_z:
            ptimes, soluzione = attrito(m, r_s, mu, v_0, theta0)
            gittata, _, _ = grandezze(soluzione)
            gittate.append(gittata)

        plt.plot(theta_z, gittate, color = colori[nome_materiale],
                 label = nome_materiale)

    plt.title(f"Gittata in funzione dell'angolo - {nome_fluido}")
    plt.xlabel("angolo [°]", fontsize = 14)
    plt.ylabel("gittata [m]", fontsize = 14)
    plt.xticks(theta_z)
    plt.legend()
    plt.grid()
    plt.show()

# 3.1 Altezza VS massa

def grafico_altezza_massa(nome_fluido, mu):

    plt.figure(figsize = (9,7))

    for nome_materiale in materiali:

        rho = materiali[nome_materiale]
        r_s = raggi[nome_materiale]
        m_riferimento = massa(rho, r_s)
        masse_variate = np.linspace(0.5* m_riferimento, 1.5 * m_riferimento, 10)

        altezze = []

        for m in masse_variate:
            ptimes, soluzione = attrito(m, r_s, mu, v_0, 45)
            _, altezza_massima, _ = grandezze(soluzione)
            altezze.append(altezza_massima)

        plt.plot(masse_variate, altezze, color = colori[nome_materiale],
                 label = nome_materiale)

    plt.title(f"Altezza massima in funzione della massa - {nome_fluido}", fontsize = 16)
    plt.xlabel("massa [kg]", fontsize = 14)
    plt.ylabel("altezza massima [m]", fontsize = 14)
    plt.legend()
    plt.grid()
    plt.show()

# 3.2 Altezza VS raggio

def grafico_altezza_raggio(nome_fluido, mu):

    plt.figure(figsize = (9,7))

    for nome_materiale in materiali:

        rho = materiali[nome_materiale]
        r_riferimento = raggi[nome_materiale]
        m = massa(rho, r_riferimento)
        raggi_variati = np.linspace( 0.5 * r_riferimento, 1.5 * r_riferimento, 10)

        altezze = []

        for r_s in raggi_variati:

            ptimes, soluzione = attrito( m, r_s, mu, v_0, 45)
            _, altezza_massima, _ = grandezze(soluzione)
            altezze.append(altezza_massima)

        plt.plot(raggi_variati, altezze, color = colori[nome_materiale],
                 label = nome_materiale)

    plt.title(f"Altezza massima in funzione del raggio - {nome_fluido}", fontsize = 16)
    plt.xlabel("raggio [m]", fontsize = 14)
    plt.ylabel("altezza massima [m]", fontsize = 14)
    plt.legend()
    plt.grid()
    plt.show()


# 3.3 Altezza VS angolo

def grafico_altezza_angolo(nome_fluido, mu):

    plt.figure(figsize = (9,7))

    for nome_materiale in materiali:

        rho = materiali[nome_materiale]
        r_s = raggi[nome_materiale]
        m = massa(rho, r_s)

        altezze = []

        for theta0 in theta_z:

            ptimes, soluzione = attrito(m, r_s, mu, v_0, theta0)
            _, altezza_massima, _ = grandezze(soluzione)
            altezze.append(altezza_massima)

        plt.plot(theta_z, altezze, color = colori[nome_materiale],
                 label = nome_materiale)

    plt.title( f"Altezza massima in funzione dell'angolo - {nome_fluido}", fontsize = 16)
    plt.xlabel( "angolo [°]", fontsize = 14)
    plt.ylabel (" altezza massima [m]", fontsize = 14)
    plt.xticks(theta_z)
    plt.grid()
    plt.legend()
    plt.show()

# 4.1 Velocità VS massa

def grafico_v_massa(nome_fluido, mu):

    plt.figure(figsize = (9,7))

    for nome_materiale in materiali:

        rho = materiali[nome_materiale]
        r_s = raggi[nome_materiale]
        m_riferimento = massa(rho, r_s)
        masse_variate = np.linspace( 0.5 * m_riferimento, 1.5 * m_riferimento, 10)

        vel = []

        for m in masse_variate:

            ptimes, soluzione = attrito(m, r_s, mu, v_0, 45)
            _, _, v_max_caduta = grandezze(soluzione)
            vel.append(v_max_caduta)

        plt.plot(masse_variate, vel, color = colori[nome_materiale],
                 label= nome_materiale)

    plt.title(f"Massima velocità di caduta in funzione della massa - {nome_fluido}", fontsize = 16)
    plt.xlabel( "massa [kg]", fontsize = 14)
    plt.ylabel( "massima velocità di caduta [m/s]", fontsize = 14)
    plt.grid()
    plt.legend()
    plt.show()

# 4.2 Velocità VS raggio

def grafico_v_raggio(nome_fluido, mu):

    plt.figure(figsize = (9,7))

    for nome_materiale in materiali:

        rho = materiali[nome_materiale]
        r_riferimento = raggi[nome_materiale]
        m = massa(rho, r_riferimento)
        raggi_variati = np.linspace(0.5 * r_riferimento, 1.5 * r_riferimento, 10)

        vel = []

        for r_s in raggi_variati:

            ptimes, soluzione = attrito(m, r_s, mu, v_0, 45)
            _, _, v_max_caduta = grandezze(soluzione)
            vel.append(v_max_caduta)

        plt.plot(raggi_variati, vel,color = colori[nome_materiale],
                 label = nome_materiale)

    plt.title( f"Massima velocità di caduta in funzione del raggio - {nome_fluido}", fontsize = 16)
    plt.xlabel( "raggio [m]", fontsize = 14)
    plt.ylabel( "massima velocità di caduta [m/s]", fontsize = 14)
    plt.grid()
    plt.legend()
    plt.show()

# 4.3 Velocità VS angolo

def grafico_v_angolo(nome_fluido, mu):

    plt.figure(figsize = (9,7))

    for nome_materiale in materiali:

        rho = materiali[nome_materiale]
        r_s = raggi[nome_materiale]
        m = massa(rho, r_s)


        vel = []

        for theta0 in theta_z:

            ptimes, soluzione = attrito(m, r_s, mu, v_0, theta0)
            _, _, v_max_caduta = grandezze(soluzione)
            vel.append(v_max_caduta)

        plt.plot(theta_z, vel, color = colori[nome_materiale],
                 label = nome_materiale)

    plt.title( f"Massima velocità di caduta in funzione dell'angolo - {nome_fluido}", fontsize = 16)
    plt.ylabel( "massima velocità di caduta [m/s]", fontsize = 14)
    plt.xlabel( "angolo [°]", fontsize = 14)
    plt.xticks(theta_z)
    plt.legend()
    plt.grid()
    plt.show()



#ESECUZIONE GRAFICI

if __name__ == "__main__":

     for nome_fluido, mu in fluidi.items():

         grafico_traiettoria_angolo(nome_fluido, mu)
         grafico_traiettoria_massa(nome_fluido,mu)
         grafico_traiettoria_raggio(nome_fluido, mu)

         grafico_gittata_m(nome_fluido,mu)
         grafico_gittata_raggio(nome_fluido, mu)
         grafico_gittata_angolo(nome_fluido, mu)

         grafico_altezza_massa(nome_fluido, mu)
         grafico_altezza_raggio(nome_fluido, mu)
         grafico_altezza_angolo(nome_fluido, mu)

         grafico_v_massa(nome_fluido, mu)
         grafico_v_raggio(nome_fluido, mu)
         grafico_v_angolo(nome_fluido, mu)



