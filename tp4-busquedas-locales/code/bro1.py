import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Parámetros ---
n_players = 40
n_iter = 20
dim = 2
x_min, x_max = -5, 5
elimination_threshold = 3      # derrotas consecutivas para eliminar
shrink_every = 5               # cada cuántas iteraciones encoger límites
max_step = 1.0                 # paso máximo por iteración
noise_scale = 0.05             # ruido aleatorio extra para dinamismo

# Función objetivo (Rastrigin 2D)
def rastrigin(x):
    return 20 + x[0]**2 - 10*np.cos(2*np.pi*x[0]) + x[1]**2 - 10*np.cos(2*np.pi*x[1])

# Inicialización de jugadores
positions = np.random.uniform(x_min, x_max, (n_players, dim))
positions += np.random.normal(0, 0.5, positions.shape)
fitness = np.array([rastrigin(p) for p in positions])

best_idx = np.argmin(fitness)
best_pos = positions[best_idx].copy()
damage = np.zeros(n_players, dtype=int)

# Guardar historial
history_positions = []
history_best_pos = []

for t in range(n_iter):
    new_positions = positions.copy()
    
    # --- Duelos entre vecinos ---
    for i in range(len(positions)):
        dists = np.linalg.norm(positions - positions[i], axis=1)
        dists[i] = np.inf
        neighbor_idx = np.argmin(dists)
        if fitness[i] < fitness[neighbor_idx]:
            winner, loser = i, neighbor_idx
        else:
            winner, loser = neighbor_idx, i
        
        damage[winner] = 0
        damage[loser] += 1
        
        # Movimiento guiado + ruido para dinamismo
        r = np.random.rand()
        step = r * (best_pos - positions[loser])
        noise = np.random.normal(0, noise_scale, dim)  # ruido extra
        step += noise
        step = np.clip(step, -max_step, max_step)
        new_positions[loser] += step
    
    # --- Eliminación por daño ---
    to_eliminate = np.where(damage >= elimination_threshold)[0]
    if len(to_eliminate) > 0:
        new_positions = np.delete(new_positions, to_eliminate, axis=0)
        damage = np.delete(damage, to_eliminate)
    
    # --- Reinyección para mantener población ---
    while len(new_positions) < n_players:
        new_pos = np.random.uniform(x_min, x_max, (1, dim))
        new_positions = np.vstack([new_positions, new_pos])
        damage = np.append(damage, 0)
    
    # --- Encogimiento de límites cada shrink_every iteraciones ---
    if (t+1) % shrink_every == 0:
        std_dev = np.std(new_positions, axis=0)
        x_min = best_pos - std_dev
        x_max = best_pos + std_dev
    
    # Evaluar fitness y actualizar mejor global
    fitness = np.array([rastrigin(p) for p in new_positions])
    best_idx = np.argmin(fitness)
    best_pos = new_positions[best_idx].copy()
    
    positions = new_positions.copy()
    history_positions.append(positions.copy())
    history_best_pos.append(best_pos.copy())

# --- Animación 2D ---
fig, ax = plt.subplots(figsize=(8,6))
ax.set_xlim(-5,5)
ax.set_ylim(-5,5)

scat = ax.scatter([], [], s=50, color='red', label='Jugadores')
best_scat = ax.scatter([], [], s=100, color='yellow', label='Mejor jugador')

def update(frame):
    pos = history_positions[frame]
    best = history_best_pos[frame]
    scat.set_offsets(pos)
    best_scat.set_offsets(best.reshape(1,2))
    ax.set_title(f"Iteración {frame+1} | Jugadores: {len(pos)}")
    return scat, best_scat

anim = FuncAnimation(fig, update, frames=len(history_positions), interval=700, blit=True)
anim.save("BRO_complete_2D_dynamic.gif", writer='pillow', dpi=150)
plt.close()
