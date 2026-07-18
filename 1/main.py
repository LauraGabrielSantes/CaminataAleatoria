import sys
import time
from event import Event
from simulation import Simulation
from caminataAleatoria import CaminataAleatoria

class main():
 if len(sys.argv) != 2:
  print ("Por favor proporcione el nombre de la grafica de comunicaciones")
  raise SystemExit(1)

 #emisorBusqueda = int(input("Indique el id del nodo iniciador de la búsqueda: "))
 #recursoBuscado = int(input("¿Qué recurso desea buscar? "))
 #ttl = int(input("Indique el TTL de búsqueda: "))  
 #CaminataAleatoria.contadorMensajes = 0
 #inicio = time.time()
 experiment = Simulation(sys.argv[1], 20)  
 #m = ABIL()

 for i in range(1,len(experiment.graph)+1):
  m = CaminataAleatoria()
  experiment.setModel(m, i)

 # inserta un evento semilla en la agenda y arranca
 #mensaje = ("INICIA", [recursoBuscado,emisorBusqueda,ttl])
 seed = Event("INICIA" , 0.0 , 1, 1)
 seed.setWalkingLength( 3 )
 seed.setWalkers(2)
 seed.setResourcesToFound( [2] )
 experiment.init(seed)
 experiment.run()
 #fin = time.time()
 #if not CaminataAleatoria.encontrado: print ("\n EL RECURSO ",recursoBuscado," NO FUE ENCONTRADO \n")
 #print("\nMensajes enviados:", Camina.contadorMensajes) 
