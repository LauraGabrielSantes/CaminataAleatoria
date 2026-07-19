import sys
import time
from event import Event
from simulation import Simulation
from caminataAleatoria import CaminataAleatoria

class main:

    if len(sys.argv) != 3:
        print ("Por favor proporcione el nombre de la grafica de comunicaciones")
        raise SystemExit(1)


    # crea los nodos, los inicializa y puebla
    experiment = Simulation(sys.argv[1], 20 , sys.argv[2] )    

    for i in range(1,len(experiment.graph)+1):
        m = CaminataAleatoria()
        experiment.setModel(m, i)

 # inserta un evento semilla en la agenda y arranca
    seed = Event("INICIA" , 0.0 , 1, 1)
    seed.setWalkingLength( 3 )
    seed.setWalkers(2)
    seed.setResourcesToFound( [2] )
    experiment.init(seed)
    experiment.run()
