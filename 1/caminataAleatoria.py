#Implementa la simulacion del Algoritmo de búsqueda por inundación limitada usando como base el algoritmo de PI Segall
import random
from event import Event
from model import Model

class CaminataAleatoria(Model):

    # genera los recursos del nodo
    def generateResources( self ) :
        numberOfElements = random.randint( 2 , 10 )

        for element in range( numberOfElements ) :
            self.myResources.append( random.randint( 1 , 10 ) )

    # envía en mensaje M a un nodo aleatorio disponible
    def randomSend( self , event ) :
        if event.getWalkingLength() == 0 :
            print( "[" , self.id , "] El caminante" , event.getWalkerId() , "terminó" )
            return

        if len( self.avalibleNodes ) == 0 :
            print( "[" , self.id , "] no hay más vecinos que visitar. El caminante" , event.getWalkerId() , "terminó" )
            return

        # elige el siguiente nodo al que se le envía M
        nextNode = random.choice( self.avalibleNodes ) 

        # quitamos dicho nodo de la lista de disponibles
        self.avalibleNodes.remove( nextNode )

        # envía mensaje
        print ( "[",self.id,"] envío M a" , nextNode , "del caminante" , event.getWalkerId() , "en" , self.clock )
        newevent = Event("M", self.clock + 1.0, nextNode , self.id)
        newevent.setIdRoot( event.getIdRoot() )
        newevent.setWalkingLength( event.getWalkingLength() - 1 )
        newevent.setResourcesToFound( event.getResourcesToFound() )
        newevent.setWalkerId( event.getWalkerId() )
        self.transmit(newevent)

    # revisa si el nodo tiene el contenido
    def iHaveContent( self , resourcesToFound ) :
        for myResource in self.myResources :
            for requiredResource in resourcesToFound :
                if myResource == requiredResource :
                    return True

        return False
        
    def iniciaHandler( self , event ) :
        print ("[",self.id,"] inicio" , event.getWalkers() , "caminantes que avanzarán" , event.getWalkingLength() ,"pasos")
        print( "[" , self.id , "] busco el siguiente contenido:" , event.getResourcesToFound() )

        # revisa si el contenido lo tiene ya
        if self.iHaveContent( event.getResourcesToFound() ) :
            self.idFromResourcesFound.append( self.id )
            print("[" , self.id , "] nodos con recursos solicitados:" , self.idFromResourcesFound )
            print()

        # raíz donde inicia la búsqueda
        event.setIdRoot( self.id )

        for i in range( event.getWalkers() ) :
            event.setWalkerId( i + 1 )
            self.randomSend( event )

        print()

    def mHandler( self , event ) :
        print ("[",self.id,"] recibo M de" , event.getSource() , "del caminante" , event.getWalkerId() , "en el paso" , event.getWalkingLength() , "en" , self.clock )

        if self.visited == True :
            print ("[",self.id,"] envío RECHAZA a" , event.getSource() , "en" , self.clock )
            print()
            newevent = Event("RECHAZA", self.clock + 1.0, event.getSource() , self.id)
            newevent.setIdRoot( event.getIdRoot() )
            newevent.setWalkingLength( event.getWalkingLength() + 1 )
            newevent.setResourcesToFound( event.getResourcesToFound() )
            newevent.setWalkerId( event.getWalkerId() )
            self.transmit(newevent)
            return

        self.visited = True
        self.father = event.getSource()
        self.avalibleNodes.remove( self.father )

        if self.iHaveContent( event.getResourcesToFound() ) :
            print ("[",self.id,"] envío REGRESA a" , event.getIdRoot() , "en" , self.clock )
            newevent = Event("REGRESA", self.clock + 1.0, event.getIdRoot() , self.id)
            self.transmit(newevent)

        # envíal siguiente si es posible
        self.randomSend( event )
        print()

    def regresaHandler( self , event ) :
        self.idFromResourcesFound.append( event.getSource() )
        print ("[",self.id,"] recibo REGRESA de" , event.getSource() , "del caminante" , event.getWalkerId() , "en" , self.clock )
        print("[" , self.id , "] nodos con recursos solicitados:" , self.idFromResourcesFound )
        print()

    def rechazaHandler( self , event ) :
        print ("[",self.id,"] recibo RECHAZA de" , event.getSource() , "del caminante" , event.getWalkerId() , "en el paso" , event.getWalkingLength() , "en" , self.clock )
        self.randomSend( event )

    def init(self):
        self.visited=False
        self.father = self.id
        self.avalibleNodes = self.neighbors
        self.myResources = [] 
        self.idFromResourcesFound = []
        
        self.generateResources()

        print ("Inicio funciones", self.id)
        print ("Mis vecinos son:", self.neighbors)
        print ("Mis recursos son:", self.myResources ,"\n")

    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    def receive(self, event):
        if event.getName() == "INICIA":
            self.iniciaHandler( event )

        elif event.getName() == "M":
            self.mHandler( event )

        elif event.getName() == "REGRESA":
            self.regresaHandler( event )
     
        elif event.getName() == "RECHAZA":
            self.rechazaHandler( event )
  
