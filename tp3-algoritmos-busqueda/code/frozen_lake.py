import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from gymnasium import wrappers
import random

from gymnasium.utils import seeding

from collections import deque

import math

import heapq

import numpy as np

import argparse

import csv

import time

start = None


def generate_random_map_custom(
    size: int = 8, p: float = 0.8, seed: int | None = None
    ) -> list[str]:
    
    board = []  # initialize to make pyright happy

    np_random, _ = seeding.np_random(seed)

    p = min(1, p)
    board = np_random.choice(["F", "H"], (size, size), p=[p, 1 - p])
    
    posiciones_F = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 'F']

    s_pos, f_pos = np_random.choice(posiciones_F, size=2, replace=False)

    board[s_pos[0]][s_pos[1]] = 'S'
    board[f_pos[0]][f_pos[1]] = 'G'

    return ["".join(x) for x in board]

def busqueda_aleatoria(env):
    estados_explorados = 0
    desc = env.unwrapped.desc
    rows, cols = desc.shape

    for i in range(0,rows):
        for j in range(0,cols):
            if desc[i,j] ==b"S":
                startpos = (i,j)
    
    done = truncated = False
    path = []
    global start
    start = time.time()
    while not (done or truncated):
        estados_explorados = estados_explorados +1
        action = random.randint(0, 3)
        path.append(action)
        next_state, reward, done, truncated, _ = env.step(action)
        if reward == 1.0:
            return (startpos,path,estados_explorados)

    return (startpos,None,estados_explorados)

def busqueda_en_anchura(env): # PLAN BFS

    estados_explorados= 0
    desc = env.unwrapped.desc
    rows, cols = desc.shape

    for i in range(0,rows):
        for j in range(0,cols):
            if desc[i,j] ==b"S":
                startpos = (i,j)
    
    global start
    start = time.time()

    visitados = {}
    cola = deque([(startpos,[])])                               
    while cola:

        pos,path = cola.popleft()
        if pos in visitados:
            continue

        visitados[(pos[0],pos[1])] = True
        if desc[pos[0],pos[1]] != b"H" and desc[pos[0],pos[1]]!=b"G":
            estados_explorados +=1

            if pos[0]-1>0 and (pos[0]-1,pos[1]) not in visitados.keys(): # me movi hacia arriba en fila
                cola.append(((pos[0]-1,pos[1]),path + [3]))

            if pos[0]+1<rows and (pos[0]+1,pos[1]) not in visitados.keys(): #me movi hacia abajo en fila
                cola.append(((pos[0]+1,pos[1]),path + [1]))

            if pos[1]-1>0 and (pos[0],pos[1]-1) not in visitados.keys(): #me movi hacia la izquierda en columna
                cola.append(((pos[0],pos[1]-1),path + [0]))

            if pos[1]+1<cols and (pos[0],pos[1]+1) not in visitados.keys(): #me movi hacia derecha en columna
                cola.append(((pos[0],pos[1]+1),path + [2]))

        if desc[pos[0],pos[1]]==b"G":
            return (startpos,path,estados_explorados)
    
    return (startpos,None,estados_explorados)


def busqueda_en_profundidad(env): # PLAN DFS

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
    cola = deque([(startpos,[])])                               
    while cola:
        pos,path = cola.pop()
        if pos in visitados:
            continue

        visitados[(pos[0],pos[1])] = True
        if desc[pos[0],pos[1]] != b"H" and desc[pos[0],pos[1]]!=b"G":
            estados_explorados +=1
            if pos[0]-1>0 and (pos[0]-1,pos[1]) not in visitados.keys(): # me movi hacia arriba en fila
                cola.append(((pos[0]-1,pos[1]),path + [3]))

            if pos[0]+1<rows and (pos[0]+1,pos[1]) not in visitados.keys(): #me movi hacia abajo en fila
                cola.append(((pos[0]+1,pos[1]),path + [1]))

            if pos[1]-1>0 and (pos[0],pos[1]-1) not in visitados.keys(): #me movi hacia la izquierda en columna
                cola.append(((pos[0],pos[1]-1),path + [0]))

            if pos[1]+1<cols and (pos[0],pos[1]+1) not in visitados.keys(): #me movi hacia derecha en columna
                cola.append(((pos[0],pos[1]+1),path + [2]))

        if desc[pos[0],pos[1]]==b"G":
            return (startpos,path, estados_explorados)
    
    return (startpos,None,estados_explorados)


def busqueda_en_profundidad_limitada(env,limite): # PLAN DFSL
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
    cola = deque([(startpos,[])])                               
    while cola:
        pos,path = cola.pop()
        if pos in visitados or len(path)>limite:
            continue

        visitados[(pos[0],pos[1])] = True
        if desc[pos[0],pos[1]] != b"H" and desc[pos[0],pos[1]]!=b"G":
            estados_explorados +=1

            if pos[0]-1>0 and (pos[0]-1,pos[1]) not in visitados.keys(): # me movi hacia arriba en fila
                cola.append(((pos[0]-1,pos[1]),path + [3]))

            if pos[0]+1<rows and (pos[0]+1,pos[1]) not in visitados.keys(): #me movi hacia abajo en fila
                cola.append(((pos[0]+1,pos[1]),path + [1]))

            if pos[1]-1>0 and (pos[0],pos[1]-1) not in visitados.keys(): #me movi hacia la izquierda en columna
                cola.append(((pos[0],pos[1]-1),path + [0]))

            if pos[1]+1<cols and (pos[0],pos[1]+1) not in visitados.keys(): #me movi hacia derecha en columna
                cola.append(((pos[0],pos[1]+1),path + [2]))

        if desc[pos[0],pos[1]]==b"G":
            return (startpos,path,estados_explorados)
    
    return (startpos,None,estados_explorados)


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
    cola = [(0,(startpos,[]))]         
                       
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
    
    return (startpos,None,estados_explorados)


def executer(env,seed):
    global start 
    state = env.reset()
    #startpos,path,estados_explorados = busqueda_aleatoria(env)
    #startpos,path,estados_explorados = busqueda_en_anchura(env)
    #startpos,path,estados_explorados = busqueda_en_profundidad(env)
    #startpos,path,estados_explorados = busqueda_en_profundidad_limitada(env,50)
    #startpos,path,estados_explorados = busqueda_en_profundidad_limitada(env,75)
    #startpos,path,estados_explorados = busqueda_en_profundidad_limitada(env,100)
    #startpos,path,estados_explorados = busqueda_costo_uniforme(env)
    startpos,path,estados_explorados = a_estrella(env)
    end = time.time()
    cost = 0
    done = truncated = False
    if path!=None:
            
        for action in path:
            _, _, done, _, _ = env.step(action)
            if action in [1,3]:
                cost+=1
            else:
                cost+=1

            if done:
                break

        end = time.time()
        print(f"A*,{seed},{estados_explorados},{len(path)},{cost},{end-start},True")
    else:
        print(f"A*,{seed},{estados_explorados},{0},{0},{end-start},False")
        return
    

    

        










if __name__ == "__main__":
    # Parser de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True, help="Semilla para reproducibilidad")
    args = parser.parse_args()

    seedd = args.seed

    env = gym.make(
        "FrozenLake-v1",
        desc=generate_random_map_custom(size=100, p=0.92, seed=seedd),
        render_mode=None,
        is_slippery=False,
        max_episode_steps=1000
    )


    executer(env,seedd)








