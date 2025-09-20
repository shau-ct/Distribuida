import simpy
from Nodo import *
from Canales.CanalBroadcast import *

TICK = 1
GO_MSG = "GO"
BACK_MSG = "BACK"

class NodoGenerador(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de flooding.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        # Atributos propios del algoritmo
        #self.padre = None if id_nodo != 0 else id_nodo # Si es el nodo distinguido, el padre es el mismo 
        self.padre = None
        self.hijos = list()
        self.mensajes_esperados = len(vecinos) # Cantidad de mensajes que esperamo
        self.es_distinguido = False

    def tostring(self):
        return f"ID: {self.id_nodo}, Parent: {self.padre}, Children: {self.hijos}"

    
    def genera_arbol(self, env):
      # Si es el nodo distinguido (nodo 0), inicia el algoritmo
        if self.id_nodo == 0:
            self.es_distinguido = True
            self.padre = self.id_nodo
            self.mensajes_esperados = len(self.vecinos)
            
            # Enviar GO a todos los vecinos
            for vecino in self.vecinos:
                yield self.canal_salida.envia((GO_MSG, self.id_nodo), [vecino])
        
        # Procesar mensajes
        while True:
            mensaje = yield self.canal_entrada.get()
            
            if isinstance(mensaje, tuple) and len(mensaje) == 2:
                tipo_mensaje, sender = mensaje
            else:
                continue  # Ignorar mensajes mal formados
            
            if tipo_mensaje == GO_MSG:
                if self.padre is None:  
                    self.padre = sender
                    self.mensajes_esperados = len(self.vecinos) - 1
                    
                    if self.mensajes_esperados == 0:
                        yield self.canal_salida.envia((BACK_MSG, [self.id_nodo]),[self.padre])
                    else:
                        for vecino in self.vecinos:
                            if vecino != sender:
                                yield self.canal_salida.envia((GO_MSG, self.id_nodo),[vecino])
                else:
                    # Ya tengo padre, enviar BACK
                    yield self.canal_salida.envia((BACK_MSG, None),[sender])
            
            elif tipo_mensaje == BACK_MSG:
                self.mensajes_esperados -= 1
                if sender is not None:
                    self.hijos.append(sender)
                
                if self.mensajes_esperados == 0 and self.padre != self.id_nodo:
                    yield self.canal_salida.envia((BACK_MSG, self.id_nodo), [self.padre])
                    break

        



                    
                    





                    







                


