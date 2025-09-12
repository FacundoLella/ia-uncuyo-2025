import random
import time

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