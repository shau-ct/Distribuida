import simpy
from Canales.Canal import Canal


class CanalBroadcast(Canal):
    '''
    Clase que modela un canal, permite enviar mensajes one-to-many.
    '''

    def __init__(self, env, capacidad=simpy.core.Infinity):
        self.env = env
        self.capacidad = capacidad
        self.canales = []



    '''
    Metodo que regresa la lista de canales 
    '''
    def get_canales(self):
        return self.canales 
    

    def envia(self, mensaje, vecinos):
        '''
        Envia un mensaje a los canales de salida de los vecinos.
        '''
        if not self.canales:
            raise RuntimeError( "No hay canales disponibles ")
        eventos = [] 
        
        for vecino in vecinos:
            if vecino in range(len(self.canales)):
                eventos.append(self.canales[vecino].put(mensaje))
                
        return self.env.all_of(eventos) if eventos else self.env.timeout(0)



    def crea_canal_de_entrada(self):
        '''
        Creamos un canal de entrada
        '''
        canal_entrada = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal_entrada)
        return canal_entrada
