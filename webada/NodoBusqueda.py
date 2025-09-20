import simpy
from Nodo import *
from Canales.CanalBroadcast import *
from Auxiliares import *

TICK = 1
class NodoBusqueda(Nodo):
    def __init__(self, id_nodo,vecinos,cantidad_nodos ,canal_entrada, canal_salida,mensaje=None):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.cantidad_nodos =  cantidad_nodos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.arr = []
        self.contenido = False 
    

    def toString(self):
        return f"Id_nodo = {self.id_nodo},Vecinos: {self.vecinos},array: {self.arr},estado: {self.contenido}"

    def busqueda(self,env,arr,elemento):
        # Dividir el arreglo usando la función cuadricula
        segmentos = cuadricula(arr, self.cantidad_nodos)
        
        # Asignar segmento a este nodo
        if self.id_nodo < len(segmentos):
            self.arr = segmentos[self.id_nodo]
        
        # Buscar elemento en el segmento asignado
        if elemento in self.arr:
            self.contenido = True
        
        # Enviar resultado al nodo coordinador (nodo 0)
        if self.id_nodo != 0:
            yield self.canal_salida.envia(("RESULT", self.contenido), [0])
        else:
            # El nodo 0 recolecta resultados
            resultados = [self.contenido]
            for _ in range(self.cantidad_nodos - 1):
                mensaje = yield self.canal_entrada.get()
                if mensaje[0] == "RESULT":
                    resultados.append(mensaje[1])
            
            # El elemento se encontró si algún nodo lo tiene
            encontrado = any(resultados)
            self.contenido = encontrado
            print(f"Elemento {elemento} encontrado: {encontrado}")
 



                    
                     







    
        

    
