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
    root =1
    seed = Event("INICIA" , 0.0 , root, root)
    seed.setWalkingLength( 20 )
    seed.setWalkers(3)
    seed.setResourcesToFound( [200] )
    experiment.init(seed)
    experiment.run()

    # Imprimir resultados de idFromResourcesFound de todos los nodos

    print("RESULTADOS DE BÚSQUEDA DE RECURSOS:")
    process = experiment.table[root]
    model = process.model

    if model.idFromResourcesFound:
        print(f"Nodo {root}: {model.idFromResourcesFound}")
    else:
        print ("No se encontró el recurso :( ")

