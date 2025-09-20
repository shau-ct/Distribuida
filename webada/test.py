from Canales.CanalBroadcast import *
from NodoConvergecast import NodoConvergcast
from NodoGenerador import *
from NodoSort import *
from NodoBusqueda import *
from Auxiliares import *
import random 

# Las unidades de tiempo que les daremos a las pruebas
TIEMPO_DE_EJECUCION = 10

class TestPractica1:
    ''' Clase para las pruebas unitarias de la práctica 1. '''
    # Las aristas de adyacencias de la gráfica.
    adyacencias = [[1, 2], [0, 3], [0, 3, 5], [1, 2, 4], [3, 5], [2, 4]]

    # Aristas de adyacencias del árbol
    adyacencias_arbol_1 = [[1, 2], [3], [5], [4], [], []]
    adyacencias_arbol_2 = [[1, 2], [5], [3], [4], [], [6,7],[],[]]
    adyacencias_arbol_3 = [[1,2,3],[4,5],[6],[7,8,9],[],[],[10],[],[],[],[]]
    
    #Adyacecias Topologia Estrella
    estrella =  [[1,2,3,4,5,6,7],[0],[0],[0],[0],[0],[0],[0]]
    #arr_fijo = [10,9,6,100,50,70,0,1,9]
    arr  = [random.randint(0, 99) for _ in range(11)]
    elem = 100 
    arr.append(elem)
    random.shuffle(arr)
    #############################3
    
    def test_ejercicio_uno(self):
        ''' Prueba para el algoritmo que construye un árbol generador. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)

        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias)):
            grafica.append(NodoGenerador(i, self.adyacencias[i],
                                       bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        for nodo in grafica:
            env.process(nodo.genera_arbol(env))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        # Y probamos que los padres y los hijos sean los correctos.
        padres = [0, 0, 0, 1, 3, 2]
        hijos = [[1, 2], [3], [5], [4], [], []]
        for i in range(0, len(grafica)):
            nodo = grafica[i]
            #print("Nodo padre",nodo.padre," ","padres[i] ",padres[i])
            print("hijos",nodo.hijos," ","set(hijos[i]) ",set(hijos[i]))
            assert nodo.padre == padres[i], ('El nodo %d tiene un padre erróneo' % nodo.id_nodo)
            assert set(nodo.hijos) == set(hijos[i]), ('El nodo %d no tiene a los hijos correctos'
                                                      % nodo.id_nodo)    
    
    def test_dos(self):
        '''Prueba para el algoritmo Convergecast'''
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)
        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias_arbol_1)):
            grafica.append(NodoConvergcast(i, self.adyacencias_arbol_1[i],i,
                                    bc_pipe.crea_canal_de_entrada(), bc_pipe))
        f  =  lambda arr: sum(arr)
        for nodo in grafica:
            env.process( nodo.convergecast(env,f) )
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        #print("Mensaje final ",grafica[0].valor_final)
        for nodo in grafica:
            print("Nodo Valor inicial  ",nodo.id_nodo,"  Valor recopilado", nodo.value)
        
        suma = 0 
        '''EN la implemetacion del convergecast se simulo una suma de los ids donde la suma total de los nodos se recopilaba
            en el nodo central '''
        for i in range(0,len(grafica)):
            suma+=i
        
        assert suma == grafica[0].value

    def test_dos_dos(self):
        '''Prueba para el algoritmo Convergecast'''
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)
        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias_arbol_2)):
            grafica.append(NodoConvergcast(i, self.adyacencias_arbol_2[i],i,
                                    bc_pipe.crea_canal_de_entrada(), bc_pipe))
        f  =  lambda arr: sum(arr)
        for nodo in grafica:
            env.process( nodo.convergecast(env,f) )
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        #print("Mensaje final ",grafica[0].valor_final)
        for nodo in grafica:
            print("Nodo Valor inicial  ",nodo.id_nodo,"  Valor recopilado", nodo.value)
        
        suma = 0 
        '''EN la implemetacion del convergecast se simulo una suma de los ids donde la suma total de los nodos se recopilaba
            en el nodo central '''
        for i in range(0,len(grafica)):
            suma+=i
        
        assert suma == grafica[0].value

    def test_dos_tres(self):
        '''Prueba para el algoritmo Convergecast'''
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)
        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias_arbol_3)):
            grafica.append(NodoConvergcast(i, self.adyacencias_arbol_3[i],i,
                                    bc_pipe.crea_canal_de_entrada(), bc_pipe))
        f  =  lambda arr: sum(arr)
        for nodo in grafica:
            env.process( nodo.convergecast(env,f) )
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        #print("Mensaje final ",grafica[0].valor_final)
        for nodo in grafica:
            print("Nodo Valor inicial  ",nodo.id_nodo,"  Valor recopilado", nodo.value)
        
        suma = 0 
        '''EN la implemetacion del convergecast se simulo una suma de los ids donde la suma total de los nodos se recopilaba
            en el nodo central '''
        for i in range(0,len(grafica)):
            suma+=i
        
        assert suma == grafica[0].value

  
    
    def test_ejercicio_tres(self):
        ''' Prueba para el algoritmo de Ordenamiento. '''
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)

        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.estrella)):
            grafica.append(NodoSort(i, self.estrella[i],len(self.estrella)-1,
                                       bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        for nodo in grafica:
            env.process(nodo.ordernar(env,self.arr))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)
        resultado =  grafica[0].arr

        assert sorted(self.arr) == resultado

    


    def test_ejercicio_cuatro(self):
        ''' Prueba para el algoritmo de Busqueda. '''
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)

        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.estrella)):
            grafica.append(NodoBusqueda(i, self.estrella[i],len(self.estrella)-1,
                                       bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        for nodo in grafica:
            env.process(nodo.busqueda(env,self.arr,self.elem))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)
        resultado =  grafica[0].contenido

        assert True  == resultado

    def test_ejercicio_cuatro_dos(self) :

        ''' Prueba para el algoritmo de Busqueda (dos). '''
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)

        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.estrella)):
            grafica.append(NodoBusqueda(i, self.estrella[i],len(self.estrella)-1,
                                       bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        for nodo in grafica:
            env.process(nodo.busqueda(env,self.arr,-1000))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)
        resultado =  grafica[0].contenido

        assert False   == resultado


        

