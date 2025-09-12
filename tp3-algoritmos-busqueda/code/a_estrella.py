import math
import heapq
import time


def calcular_hipotenusa(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def a_estrella(env):
    estados_explorados = 0
    desc = env.unwrapped.desc
    rows, cols = desc.shape

    for i in range(0,rows):
        for j in range(0,cols):
            if desc[i,j] ==b"S":
                startpos = (i,j)
            if desc[i,j] == b"G":
                xf = i
                yf = j

    global start
    start = time.time()

    visitados = {}
    cola = [(0, (startpos, []))]                            
    while cola:

        cost, (pos,path) = heapq.heappop(cola)
        if pos in visitados:
            continue

        visitados[(pos[0],pos[1])] = True
        if desc[pos[0],pos[1]] != b"H" and desc[pos[0],pos[1]]!=b"G":
            estados_explorados +=1

            if pos[0]-1>0 and (pos[0]-1,pos[1]) not in visitados.keys(): # me movi hacia arriba en fila
                hip = calcular_hipotenusa((pos[0]-1,pos[1]),(xf,yf))
                heapq.heappush(cola,(cost+10+hip,((pos[0]-1,pos[1]),path + [3])))

            if pos[0]+1<rows and (pos[0]+1,pos[1]) not in visitados.keys(): #me movi hacia abajo en fila
                hip = calcular_hipotenusa((pos[0]+1,pos[1]),(xf,yf))
                heapq.heappush(cola,(cost+10+hip,((pos[0]+1,pos[1]),path + [1])))
                

            if pos[1]-1>0 and (pos[0],pos[1]-1) not in visitados.keys(): #me movi hacia la izquierda en columna
                hip = calcular_hipotenusa((pos[0],pos[1]-1),(xf,yf))
                heapq.heappush(cola,(cost +1+hip,((pos[0],pos[1]-1),path + [0])))

            if pos[1]+1<cols and (pos[0],pos[1]+1) not in visitados.keys(): #me movi hacia derecha en columna
                hip = calcular_hipotenusa((pos[0],pos[1]+1),(xf,yf))
                heapq.heappush(cola,(cost+1+hip,((pos[0],pos[1]+1),path + [2])))

        if desc[pos[0],pos[1]]==b"G":
            return (startpos,path,estados_explorados)
    
    return (startpos,path,estados_explorados)