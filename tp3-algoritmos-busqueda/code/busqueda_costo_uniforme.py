import heapq
import time

def busqueda_costo_uniforme(env): #PLAN BU
    
    estados_explorados = 0
    desc = env.unwrapped.desc
    rows, cols = desc.shape

    for i in range(0,rows):
        for j in range(0,cols):
            if desc[i,j] ==b"S":
                startpos = (i,j)

    global start
    start = time.time()

    visitados = {}
    cola = [(startpos,[],0)]                            
    while cola:

        cost, (pos,path) = heapq.heappop(cola)
        if pos in visitados:
            continue

        visitados[(pos[0],pos[1])] = True
        if desc[pos[0],pos[1]] != b"H" and desc[pos[0],pos[1]]!=b"G":
            estados_explorados +=1

            if pos[0]-1>0 and (pos[0]-1,pos[1]) not in visitados.keys(): # me movi hacia arriba en fila
                heapq.heappush(cola,(cost+10,((pos[0]-1,pos[1]),path + [3])))

            if pos[0]+1<rows and (pos[0]+1,pos[1]) not in visitados.keys(): #me movi hacia abajo en fila
                heapq.heappush(cola,(cost+10,((pos[0]+1,pos[1]),path + [1])))

            if pos[1]-1>0 and (pos[0],pos[1]-1) not in visitados.keys(): #me movi hacia la izquierda en columna
                heapq.heappush(cola,(cost +1,((pos[0],pos[1]-1),path + [0])))

            if pos[1]+1<cols and (pos[0],pos[1]+1) not in visitados.keys(): #me movi hacia derecha en columna
                heapq.heappush(cola,(cost+1,((pos[0],pos[1]+1),path + [2])))

        if desc[pos[0],pos[1]]==b"G":
            return (startpos,path,estados_explorados)
    
    return (startpos,path,estados_explorados)