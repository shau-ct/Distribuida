import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1


class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = None
        self.hijos = []
        self.distancia = 0
        self.mensajes_esperados = 0

    def bfs(self, env):
        ''' Algoritmo BFS. '''
        # Si soy el nodo 0 (nodo distinguido), inicio el algoritmo
        if self.id_nodo == 0:
            start_msg = {'tipo': 'START'}
            yield env.timeout(TICK)
            yield self.canal_entrada.put(start_msg)
            
        while True:
            # Esperar por un mensaje
            mensaje = yield self.canal_entrada.get()
            
            if mensaje['tipo'] == 'START':
                # Solo el nodo distinguido recibe este mensaje
                # Línea 1: send GO(-1) to itself
                go_msg = {'tipo': 'GO', 'distancia': -1, 'emisor': self.id_nodo}
                yield env.timeout(TICK)
                yield self.canal_entrada.put(go_msg)
                
            elif mensaje['tipo'] == 'GO':
                emisor = mensaje['emisor']
                d = mensaje['distancia']
                
                # Líneas 2-3: if (parent_i = ⊥)
                if self.padre is None:  # No tiene padre asignado
                    # then parent_i ← j; children_i ← ∅; level_i ← d + 1;
                    self.padre = emisor
                    self.hijos = []
                    self.distancia = d + 1
                    
                    # Línea 4: expected_msg_i ← |neighbors_i \ {j}|;
                    vecinos_sin_emisor = [v for v in self.vecinos if v != emisor]
                    self.mensajes_esperados = len(vecinos_sin_emisor)
                    
                    # Líneas 5-7: if (expected_msg_i = 0)
                    if self.mensajes_esperados == 0:
                        # then send BACK(yes, d + 1) to p_parent_i
                        back_msg = {'tipo': 'BACK', 'respuesta': 'yes', 'distancia': d + 1, 'emisor': self.id_nodo}
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(back_msg, [self.padre])
                    else:
                        # else for each k ∈ neighbors_i \ {j} do send GO(d + 1) to p_k
                        go_msg = {'tipo': 'GO', 'distancia': d + 1, 'emisor': self.id_nodo}
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(go_msg, vecinos_sin_emisor)
                        
                # Líneas 9-10: else if (level_i > d + 1)
                elif self.distancia > d + 1:
                    # then parent_i ← j; children_i ← ∅; level_i ← d + 1;
                    self.padre = emisor
                    self.hijos = []
                    self.distancia = d + 1
                    
                    # Línea 11: expected_msg_i ← |neighbors_i \ {j}|;
                    vecinos_sin_emisor = [v for v in self.vecinos if v != emisor]
                    self.mensajes_esperados = len(vecinos_sin_emisor)
                    
                    # Líneas 12-14: if (expected_msg_i = 0)
                    if self.mensajes_esperados == 0:
                        # then send BACK(yes, level_i) to p_parent_i
                        back_msg = {'tipo': 'BACK', 'respuesta': 'yes', 'distancia': self.distancia, 'emisor': self.id_nodo}
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(back_msg, [self.padre])
                    else:
                        # else for each k ∈ neighbors_i \ {j} do send GO(d + 1) to p_k
                        go_msg = {'tipo': 'GO', 'distancia': d + 1, 'emisor': self.id_nodo}
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(go_msg, vecinos_sin_emisor)
                else:
                    # Línea 16: else send BACK(no, d + 1) to p_j
                    back_msg = {'tipo': 'BACK', 'respuesta': 'no', 'distancia': d + 1, 'emisor': self.id_nodo}
                    yield env.timeout(TICK)
                    yield self.canal_salida.envia(back_msg, [emisor])
                    
            elif mensaje['tipo'] == 'BACK':
                emisor = mensaje['emisor']
                resp = mensaje['respuesta']
                d = mensaje['distancia']
                
                # Línea 19: if (d = level_i + 1)
                if d == self.distancia + 1:
                    # Línea 20: then if (resp = yes) then children_i ← children_i ∪ {j}
                    if resp == 'yes':
                        if emisor not in self.hijos:
                            self.hijos.append(emisor)
                    
                    # Línea 21: expected_msg_i ← expected_msg_i - 1;
                    self.mensajes_esperados -= 1
                    
                    # Líneas 22-24: if (expected_msg_i = 0)
                    if self.mensajes_esperados == 0:
                        # then if (parent_i ≠ i) then send BACK(yes, level_i) to p_parent_i
                        if self.padre != self.id_nodo:
                            back_msg = {'tipo': 'BACK', 'respuesta': 'yes', 'distancia': self.distancia, 'emisor': self.id_nodo}
                            yield env.timeout(TICK)
                            yield self.canal_salida.envia(back_msg, [self.padre])
                        else:
                            # else p_i learns that the breadth-first tree is built
                            print(f"Nodo {self.id_nodo}: Árbol BFS completado")
                            return
