import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Configuration ---
NUM_DOTS = 350
GOLDEN_RATIO = (1 + 5**0.5) / 2
GOLDEN_ANGLE = 2 * np.pi * (1 - 1 / GOLDEN_RATIO) 

# Fibonacci numbers (The spiral counts)
FIB_CW = 21  
FIB_CCW = 34 

# Setup the figure with a white background
fig, ax = plt.subplots(figsize=(9, 9), facecolor='black')
ax.set_xlim(-24, 24) 
ax.set_ylim(-24, 24)
ax.set_aspect('equal')
ax.axis('off')

# Scatter object for yellow seeds (darker edge for white background)
scatter = ax.scatter([], [], s=130, color='yellow', edgecolors='green', linewidth=0.5, zorder=3)

def get_positions(n_limit):
    indices = np.arange(n_limit)
    r = []
    for i in indices:
        if i < 3:
            r.append(1.2) # Tight initial circle
        else:
            r.append(np.sqrt(i + 2))
    
    r = np.array(r)
    theta = indices * GOLDEN_ANGLE
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def update(frame):
    # Animation Timing Logic
    if frame <= 2:
        n_to_show = frame + 1
    elif frame <= 15:
        n_to_show = 3 # Pause on the first three
    else:
        n_to_show = min(frame - 12, NUM_DOTS)

    x, y = get_positions(n_to_show)
    scatter.set_offsets(np.c_[x, y])
    
    # Reveal Spirals and Labels at the end
    if n_to_show == NUM_DOTS:
        # 1. Clockwise Spirals (BLUE)
        for i in range(FIB_CW):
            idx = np.arange(i, NUM_DOTS, FIB_CW)
            line_x, line_y = x[idx], y[idx]
            ax.plot(line_x, line_y, color='blue', alpha=0.9, lw=2, zorder=1)
            
            # Place blue numbers
            ax.text(line_x[-1]*1.1, line_y[-1]*1.1, str(i+1), 
                    color='blue', fontsize=10, ha='center', fontweight='bold')
        
        # 2. Anti-Clockwise Spirals (RED)
        for i in range(FIB_CCW):
            idx = np.arange(i, NUM_DOTS, FIB_CCW)
            line_x, line_y = x[idx], y[idx]
            ax.plot(line_x, line_y, color='green', alpha=0.9, lw=2, zorder=2)
            
            # Place red numbers
            ax.text(line_x[-1]*1.25, line_y[-1]*1.25, str(i+1), 
                    color='red', fontsize=9, ha='center', fontweight='bold')
            
        ani.event_source.stop()
            
    return [scatter]

# Set the speed (interval in ms)
total_frames = NUM_DOTS + 20
ani = FuncAnimation(fig, update, frames=total_frames, interval=25, blit=False, repeat=False)

plt.show()