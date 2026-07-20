# Este archivo contiene la implementacion de la clase Simulator (11.11.10)
""" Un objeto de la clase Simulator representa el motor de simulacion que 
coordina la comunicacion entre los procesos del sistema """

# ----------------------------------------------------------------------------------------
class Simulator:                   # Descendiente de la clase "object" (default)
    """ Atributos: "clock", "agenda", contiene tambien un constructor
    y los metodos "insertEvent()", "returnEvent()", "isOn()" """
	
    def __init__(self, lastmoment):
        """ define el valor inicial del reloj de simulacion y fija los 
        valores extremos de la agenda """
        self.clock = 0.0
        self.agenda = [[-1.0],[lastmoment+0.1]]
        self.messageCounter = 0
        self.elapsedTime = 0.0
		
    def insertEvent(self, event):
        """ inserta un evento en una lista ordenada por tiempo (agenda), 
        con valores extremos fijos (asi evita casos especiales) """
        key=event.getTime()
        newitem = [key, event]
        for i,item in enumerate(self.agenda):
            if key < item[0]: 
                self.agenda.insert(i,newitem)

                # cuenta los mensajes relevantes
                if event.getName() != "INICIA" :
                    self.messageCounter += 1

                # cuenta el tiempo transcurrido
                if event.getTime() > self.elapsedTime :
                    self.elapsedTime = event.getTime()
                break
    
    def returnEvent(self):
        """ devuelve el segundo evento de la agenda (el primero esta fijo) """
        item = self.agenda.pop(1) 
        return item[1] 

    def isOn(self):
        """ Verdadero si aun hay eventos que procesar """
        return len(self.agenda)>2 

    def returnMessagesCounter( self ) :
        return self.messageCounter

    def returnElapsedTime( self ) :
        return self.elapsedTime
