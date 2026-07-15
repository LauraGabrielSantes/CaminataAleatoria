#Implementa la simulacion del Algoritmo de búsqueda por inundación limitada usando como base el algoritmo de PI Segall
import random
from event import Event
from model import Model

class CaminataAleatoria(Model):
    contadorMensajes=0
    encontrado = False
    def init(self):
        print ("\nInicio funciones", self.id)
        print ("Mis vecinos son:", self.neighbors)
        self.visited=False
        self.father = self.id
        self.avalibleNodes = self.neighbors
        self.myResources = self.llenaRecurso()
        self.idFromResourcesFound = []
        print ("[",self.id,"]: Mis recursos son: ", self.mis_recursos,"\n")

    def randomSend( self , avalibleNodes , idRoot , walkingLength , resourcesToFound ) :

        if walkingLength == 0 || len( avalibleNodes ) == 0 :
            return

        # elige el siguiente nodo al que se le envía M
        nextNode = random.choice( avalibleNodes ) 

        # quitamos dicho nodo de la lista de disponibles
        self.avalibleNodes.remove( nextNode )

        # envía mensaje
        newevent = Event("M", self.clock + 1.0, nextNode , self.id)
        newevent.setIdRoot( idRoot )
        newevent.setWalkingLength( walkingLength - 1 )
        newevent.setResourcesToFound( resourcesToFound )
        self.transmit(newevent)

    def iHaveContent( self , resourcesToFound ) :
        for myResource in self.myResources :
            for requiredResource in resourcesToFound :
                if myResources == requiredResource :
                    return True

        return False
        
    def iniciaHandler( self , event ) :
        for i in range( event.getWalkers ) :
            self.randomSend( self.avalibleNodes , event.getIdRoot() , event.getWalkingLength() , event.getResourcesToFound() )

    def mHandler( self , event ) :
        if self.visited == False :
            self.visited = True
            self.father = event.getSource()
            self.avalibleNodes.remove( self.father )

            if self.iHaveContent( event.getResourcesToFound() ) :
                newevent = Event("REGRESA", self.clock + 1.0, event.getIdRoot() , self.id)
                self.transmit(newevent)

            # envíal siguiente si es posible
            self.randomSend( self.avalibleNodes , event.getIdRoot() , event.getWalkingLength() , event.getResourcesToFound() )

        else :
            newevent = Event("RECHAZA", self.clock + 1.0, event.getSource() , self.id)
            self.transmit(newevent)

    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    def receive(self, event):
     if nombre == "INICIA":
         self.iniciaHandler( event )
     elif nombre == "M":
        self.mHandler( event )
     elif nombre == "REGRESA":
     
     elif nombre == "RECHAZA":
        CaminataAleatoria.encontrado = True
        self.nodos_con_recurso.append(origen)
        print ("[", self.id,"]: ¡El nodo ", origen," tiene el recurso!  t = ",self.clock,"\n>>> ACTUALIZO LISTA DE NODOS CON RECURSO: ",self.nodos_con_recurso,"\n")
  
    def llenaRecurso(self):
      listaRecursos =[]
      tam = random.randint(2,10) 
      for _ in range (tam): 
         contenido = random.randint(1,100)
         if contenido not in listaRecursos: 
          listaRecursos.append(contenido)
      return listaRecursos
