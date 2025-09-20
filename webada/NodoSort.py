import simpy
from Nodo import *
from Canales.CanalBroadcast import *
from Auxiliares import *



class NodoSort(Nodo):
    def __init__(self, id_nodo,vecinos,cantidad_nodos,canal_entrada, canal_salida,mensaje=None):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.cantidad_nodos =  cantidad_nodos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.arr = []

    def ordernar(self,env,arr):
        # Dividimos el arreglo usando cuadricula
        segmentos = cuadricula(arr, self.cantidad_nodos)
        
        # Asignar y ordenar segmento local
        if self.id_nodo < len(segmentos):
            self.arr = sorted(segmentos[self.id_nodo])
        
        # Enviar segmento ordenado al coordinador
        if self.id_nodo != 0:
            yield self.canal_salida.envia(("SEGMENT", self.arr), [0])
        else:
            # El nodo 0 recolecta y hace k-way merge
            segmentos_ordenados = [self.arr]
            for _ in range(self.cantidad_nodos - 1):
                mensaje = yield self.canal_entrada.get()
                if mensaje[0] == "SEGMENT":
                    segmentos_ordenados.append(mensaje[1])
            
            # Usar k-way merge para obtener resultado final
            resultado_final = k_merge(segmentos_ordenados)
            self.arr = resultado_final
            print(f"Arreglo ordenado: {resultado_final}")


    


        






