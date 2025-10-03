import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = None
        self.hijos = []
        self.visitados = set()



    def dfs(self, env):
        ''' Algoritmo DFS. '''
        # Si soy el nodo 0 (nodo distinguido), inicio el algoritmo
        if self.id_nodo == 0:
            start_msg = {'tipo': 'START'}
            yield env.timeout(TICK)
            yield self.canal_entrada.put(start_msg)
            
        while True:
            # Esperar por un mensaje
            mensaje = yield self.canal_entrada.get()
            
            if mensaje['tipo'] == 'START':
                # Solo el nodo distinguido (pa) recibe este mensaje
                # Línea 1: parent_i ← i; children_i ← ∅; visited_i ← ∅;
                self.padre = self.id_nodo  # El nodo raíz es su propio padre
                self.hijos = []
                self.visitados = set()
                
                # Línea 2: let k ∈ neighbors_i; send GO() to p_k
                # Implementamos la modificación: elegir el vecino con menor id
                vecinos_ordenados = sorted(self.vecinos)
                if vecinos_ordenados:
                    vecino_elegido = vecinos_ordenados[0]
                    go_msg = {'tipo': 'GO', 'emisor': self.id_nodo}
                    yield env.timeout(TICK)
                    yield self.canal_salida.envia(go_msg, [vecino_elegido])
                
            elif mensaje['tipo'] == 'GO':
                emisor = mensaje['emisor']
                
                # Líneas 3-4: if (parent_i = ⊥)
                if self.padre is None:  # No tiene padre asignado
                    # then parent_i ← j; children_i ← ∅; visited_i ← {j};
                    self.padre = emisor
                    self.hijos = []
                    self.visitados = {emisor}
                    
                    # Líneas 5-7: if (visited_i = neighbors_i)
                    if self.visitados == set(self.vecinos):
                        # then send BACK(yes) to p_j
                        back_msg = {'tipo': 'BACK', 'respuesta': 'yes', 'emisor': self.id_nodo}
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(back_msg, [emisor])
                    else:
                        # else let k ∈ neighbors_i \ visited_i; send GO() to p_k
                        # Elegir el vecino no visitado con menor id
                        vecinos_no_visitados = sorted([v for v in self.vecinos if v not in self.visitados])
                        if vecinos_no_visitados:
                            vecino_elegido = vecinos_no_visitados[0]
                            go_msg = {'tipo': 'GO', 'emisor': self.id_nodo}
                            yield env.timeout(TICK)
                            yield self.canal_salida.envia(go_msg, [vecino_elegido])
                else:
                    # Línea 9: else send BACK(no) to p_j
                    back_msg = {'tipo': 'BACK', 'respuesta': 'no', 'emisor': self.id_nodo}
                    yield env.timeout(TICK)
                    yield self.canal_salida.envia(back_msg, [emisor])
                    
            elif mensaje['tipo'] == 'BACK':
                emisor = mensaje['emisor']
                resp = mensaje['respuesta']
                
                # Línea 11: if (resp = yes) then children_i ← children_i ∪ {j}
                if resp == 'yes':
                    if emisor not in self.hijos:
                        self.hijos.append(emisor)
                
                # Línea 12: visited_i ← visited_i ∪ {j};
                self.visitados.add(emisor)
                
                # Líneas 13-16: if (visited_i = neighbors_i)
                if self.visitados == set(self.vecinos):
                    # then if (parent_i = i)
                    if self.padre == self.id_nodo:
                        # then the traversal is terminated (global termination)
                        print(f"Nodo {self.id_nodo}: Recorrido DFS completado")
                        return
                    else:
                        # else send BACK(yes) to p_parent_i (local termination)
                        back_msg = {'tipo': 'BACK', 'respuesta': 'yes', 'emisor': self.id_nodo}
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(back_msg, [self.padre])
                else:
                    # Línea 18: else let k ∈ neighbors_i \ visited_i; send GO() to p_k
                    # Elegir el vecino no visitado con menor id
                    vecinos_no_visitados = sorted([v for v in self.vecinos if v not in self.visitados])
                    if vecinos_no_visitados:
                        vecino_elegido = vecinos_no_visitados[0]
                        go_msg = {'tipo': 'GO', 'emisor': self.id_nodo}
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(go_msg, [vecino_elegido])
