import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Configuration ---
NUM_DOTS = 600
GOLDEN_RATIO = (1 + 5**0.5) / 2

# We create a range of ratios and insert a "pause" at the Golden Ratio
ratios_start = np.linspace(1.60, GOLDEN_RATIO, 100)
pause = np.full(60, GOLDEN_RATIO)  # 60-frame pause (~3 seconds)
ratios_end = np.linspace(GOLDEN_RATIO, 1.64, 100)
ALL_RATIOS = np.concatenate([ratios_start, pause, ratios_end])

# Setup the figure
fig, ax = plt.subplots(figsize=(9, 9), facecolor='black')
ax.set_aspect('equal')
ax.axis('off')

# Scatter object for yellow seeds
scatter = ax.scatter([], [], s=60, color='yellow', edgecolors='black', linewidth=0.4)
# Text labels
text_ratio = ax.text(-28, 28, "", fontsize=14, fontweight='bold', family='monospace')
text_note = ax.text(-28, 25.5, "", fontsize=11, family='monospace')

def get_positions(ratio):
    indices = np.arange(NUM_DOTS)
    angle = 2 * np.pi * (1 - 1 / ratio)
    
    # Radius growth (sqrt for even packing)
    r = np.where(indices < 3, 1.0, np.sqrt(indices + 2))
    theta = indices * angle
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def update(frame):
    current_ratio = ALL_RATIOS[frame]
    x, y = get_positions(current_ratio)
    scatter.set_offsets(np.c_[x, y])
    
    text_ratio.set_text(f"Ratio: {current_ratio:.5f}")
    
    # Logic for visual feedback during the pause
    if current_ratio == GOLDEN_RATIO:
        text_ratio.set_color('red')
        text_note.set_text("GOLDEN RATIO: Optimal Packing Found")
        scatter.set_color('gold') # Highlight the "perfect" state
    else:
        text_ratio.set_color('yellow')
        text_note.set_text("Rational Ratio: Notice the 'Spokes'")
        scatter.set_color('yellow')
        
    return scatter, text_ratio, text_note

# Create Animation
ani = FuncAnimation(fig, update, frames=len(ALL_RATIOS), interval=150, repeat=True)

ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
#print("Saving GIF... please wait.")
#ani.save('sunflower_evolution.gif', writer='pillow', fps=20)
plt.show()