import simpy
from Nodo import *
from Canales.CanalBroadcast import *
from Auxiliares import *
# from NodoGenerador import NodoGenerador

TICK = 1

class NodoConvergcast(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de convergecast.'''
    def __init__(self, id_nodo, vecinos, valor, canal_entrada, canal_salida, mensaje=None):
        # Inicializa el nodo con su id, vecinos, valor propio, canales y mensaje opcional
        self.id_nodo = id_nodo
        self.padre = None
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje
        self.value = valor  # Valor propio del nodo (ejemplo: su id)
        self.val_set = {self.value}  # Conjunto de valores recolectados
        self.funcion = None  # Función a aplicar en el convergecast
        self.valor_final = None  # Resultado final tras convergecast

    def toString(self):
        # Devuelve una representación en texto del nodo y sus valores
        return f"Nodo : {self.id_nodo},valor: {self.value}, valores: {self.val_set}"
    
    def convergecast(self, env, f):
        # Proceso principal del algoritmo convergecast
        if self.id_nodo == 0:
            # Nodo raíz inicia el proceso
            self.padre = self.id_nodo
            self.funcion = f
            yield env.timeout(TICK)
            self.canal_salida.envia(("INIT", self.id_nodo, set()), self.vecinos)
        
        while True:
            # Espera mensajes en el canal de entrada
            msg = yield self.canal_entrada.get()
            
            if msg[0] == "INIT":
                # Mensaje de inicialización: establece el padre
                self.padre = msg[1]
                
                if self.vecinos:  # Si tiene hijos, propaga INIT
                    msg_ = ("INIT", self.id_nodo, set())
                    self.canal_salida.envia(msg_, self.vecinos)
                else:
                    # Si es hoja, inicia el convergecast enviando BACK al padre
                    msg_back = ("BACK", self.id_nodo, self.val_set)
                    self.canal_salida.envia(msg_back, [self.padre])
            else:
                # Mensaje BACK: actualiza el conjunto de valores
                self.val_set.update(msg[2])
                if self.padre != self.id_nodo:
                    # Si no es raíz, envía BACK al padre
                    msg_back = ("BACK", self.id_nodo, self.val_set)
                    self.canal_salida.envia(msg_back, [self.padre])
                else:
                    # Si es raíz, aplica la función f al conjunto de valores
                    self.value = f(self.val_set)

# Estructura de adyacencias para el árbol de ejemplo
adyacencias_arbol_1 = [[1,2],[3,4,5],[6],[],[7],[],[],[8,9],[],[]]
TIEMPO_DE_EJECUCION = 10 
env = simpy.Environment()
bc_pipe = CanalBroadcast(env)
grafica = []

# Crea los nodos y los agrega a la lista grafica
for i in range(0, len(adyacencias_arbol_1)):
    grafica.append(NodoConvergcast(i, adyacencias_arbol_1[i], i, bc_pipe.crea_canal_de_entrada(), bc_pipe))

# Función a aplicar en el convergecast (ejemplo: suma de valores)
f = lambda escructura: sum(escructura)

# Inicia el proceso convergecast en cada nodo
for nodo in grafica:
    env.process(nodo.convergecast(env, f))

# Ejecuta la simulación
env.run(until=TIEMPO_DE_EJECUCION)

# Imprime el estado final de cada nodo
for nodo in grafica:
    print(nodo.toString())
