**MOTO DI UN CORPO SOGGETTO AD ATTRITO VISCOSO**

*OBIETTIVO*

Questo repository contiene i file necessari per la simulazione numerica del moto di un corpo, nel nostro caso sferico, realizzato da diversi materiali (ferro, vetro e rame). 
Lo studio del moto viene svolto andando a considerare attive sull'oggetto la forza di gravità e la resistenza viscosa del mezzo in cui si propaga: acqua e aria.

*STRUTTURA DEL PROGETTO*

Il progetto è articolato in tre script Python, ciascuno corrispondente ad una richiesta:

  - richiesta1.py: la prima richiesta funge anche da libreria comune poiché contiene le funzioni "attrito_eqn" e "attrito" che, poi importate, sono utili al fine di poter eseguire gli altri due script.
    Descrive il modello fisico di base, definendo le equazioni del moto e producendo l'integrazione numerica della traiettoria per un singolo corpo.
    Riporta la sua traiettoria.

  - richiesta2.py: ha il fine ultimo di analizzare in modo sistematico come la resistenza viscosa influenzi il moto di un corpo al variare dei tre parametri         rilevanti: angolo iniziale, massa e raggio. Per ogni parametro si osservano dunque: la traiettoria, la gittata, l'altezza massima e la massima velocità di caduta. Questa è la causa dei diversi grafici che si riportano (3 parametri per 3 grandezze, eseguiti per due fluidi).
Non ci si limita ad un caso solo: l'effetto dell'attrito viscoso dipende in modo non banale dalla densità del fluido, raggio e massa dell'oggetto. Variare i parametri singolarmente permette di isolare l'effetto di ciascuno.
Si sottolinea che massa e raggio vengono considerati come due parametri indipendenti: per ogni materiale si parte dalla massa, calcolata da densità e raggio e da un raggio di riferimento. Negli studi in cui si fa variare la massa, il raggio resta fissato al valore di riferimento e viceversa, dove si varia il raggio la massa è fissata.
Non sono stati fatti variare in modo accoppiato permettendo di isolare l'effetto del peso di un corpo dalla sua grandezza.

- richiesta3.py: è il cuore del progetto che, attraverso il metodo della cumulativa, permette di fare una simulazione statistica: si campionano i raggi da una distribuzione gaussiana e si effettua lo studio della distribuzione della gittata risultante.
  Riporta:
   - grafico_distr_raggi cioè l'istogramma dei raggi campionanti confrontato con la densità di probabilità gaussiana teorica. Ci dice se il campionamento riproduce correttamente la distribuzione attesa;
   - grafico_distr_gittate cioè gli istogrammi della gittata risultante per diverse deviazioni standard;
   - grafico_raggi_gittata cioè la diretta relazione tra il raggio in ogni singola sfera con ogni gittata ottenuta.

*COME ESEGUIRE IL PROGETTO*

Si ricorda che: richiesta2.py importa la funzione attrito da richiesta1.py mentre richiesta3.py importa attrito da richiesta1.py e "massa" e "grandezze" da richiesta2.py. Per passare al grafico successivo va chiusa la finestra del grafico. 
Gli script vanno tenuti nella stessa cartella e vanno eseguiti nel seguente ordine:
- richiesta1.py
- richiesta2.py
- richiesta3.py
