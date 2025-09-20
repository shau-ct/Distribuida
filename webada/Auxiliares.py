def k_merge(arrays):
    """Merge k arrays ordenados en uno solo ordenado"""
    import heapq
    
    # Lista para el heap con (valor, índice_array, índice_elemento)
    heap = []
    result = []
    
    # Inicializar heap con el primer elemento de cada array
    for i, arr in enumerate(arrays):
        if arr:  # Solo si el array no está vacío
            heapq.heappush(heap, (arr[0], i, 0))
    
    # Procesar heap hasta que esté vacío
    while heap:
        val, array_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        # Agregar siguiente elemento del mismo array si existe
        if elem_idx + 1 < len(arrays[array_idx]):
            next_val = arrays[array_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, array_idx, elem_idx + 1))
    
    return result

def cuadricula(arr,cantidad_nodos):
    #cuadricula = [[]] * cantidad_nodos NO es correcto
    cuadricula =  [[] for _ in range(cantidad_nodos)]
    if not arr:
        return cuadricula
    
    # Calcular tamaño base de cada segmento
    tamaño_base = len(arr) // cantidad_nodos
    elementos_extra = len(arr) % cantidad_nodos
    
    idx = 0
    for i in range(cantidad_nodos):
        # Algunos nodos tendrán un elemento extra
        tamaño_segmento = tamaño_base + (1 if i < elementos_extra else 0)
        
        if tamaño_segmento > 0:
            cuadricula[i] = arr[idx:idx + tamaño_segmento]
            idx += tamaño_segmento

    return cuadricula









'''Pruebas locales 
ar1 = [1,2,3,4,5] 
n_c_1 = 5
c1 =  cuadricula(ar1,n_c_1)


ar2= [1,2,3,4]
n_c_2 = 5
c2 =  cuadricula(ar2,n_c_2)

ar3= [1,2,3,4]
n_c_3 = 8
c3 = cuadricula(ar3,n_c_3)


ar4= [1,2,3,4,5,6,7,8]
n_c4 = 4
c4 =  cuadricula(ar4,n_c4)



ar5= [1,2,3,4,5,6,7,8,9,10,11,12,13]
n_c5 = 5
c5 =  cuadricula(ar5,n_c5)

'''
