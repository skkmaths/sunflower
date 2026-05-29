
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==========================================================
# Equilateral triangle with area = 1
# ==========================================================

s = np.sqrt(4 / np.sqrt(3))
h = np.sqrt(3) * s / 2

A = np.array([0, 0])
B = np.array([s, 0])
C = np.array([s/2, h])

outer_triangle = np.array([A, B, C])

# ==========================================================
# Midpoint triangle
# ==========================================================

def midpoint_triangle(T):

    A, B, C = T

    M1 = (A + B)/2
    M2 = (B + C)/2
    M3 = (C + A)/2

    return np.array([M1, M2, M3])

# ==========================================================
# Top corner triangle
# ==========================================================

def top_triangle(T):

    A, B, C = T

    M1 = (A + B)/2
    M2 = (B + C)/2
    M3 = (C + A)/2

    return np.array([M3, M2, C])

# ==========================================================
# PARAMETERS
# ==========================================================

LEVELS_PER_STAGE = 2
NUM_STAGES = 10

TOTAL_TRIANGLES = LEVELS_PER_STAGE * NUM_STAGES

FRAMES_PER_STAGE = 120

# zoom-out frames
FINAL_ZOOMOUT_FRAMES = 180

# ==========================================================
# Generate triangles
# ==========================================================

triangles = []
regions = []

T = outer_triangle.copy()

for _ in range(TOTAL_TRIANGLES):

    inner = midpoint_triangle(T)

    triangles.append(inner)
    regions.append(T)

    T = top_triangle(T)

# ==========================================================
# Figure setup
# ==========================================================

fig, ax = plt.subplots(figsize=(8,8))

outer_pts = np.vstack([outer_triangle, outer_triangle[0]])

fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

# ==========================================================
# Draw helper
# ==========================================================

def draw_triangle(ax, T, number, show_text=True):

    pts = np.vstack([T, T[0]])

    ax.fill(
        pts[:,0],
        pts[:,1],
        color='yellow',
        alpha=0.5
    )

    ax.plot(
        pts[:,0],
        pts[:,1],
        color='darkgreen',
        linewidth=2
    )

    if show_text:

        centroid = np.mean(T, axis=0)

        ax.text(
            centroid[0],
            centroid[1],
            str(number),
            fontsize=15,
            fontweight='bold',
            ha='center',
            va='center',
            color='black'
        )

# ==========================================================
# Smooth easing
# ==========================================================

def smoothstep(t):

    return 6*t**5 - 15*t**4 + 10*t**3

def interpolate(a, b, t):

    return (1-t)*a + t*b

# ==========================================================
# Precompute zoom boxes
# ==========================================================

zoom_boxes = []

# Initial full view
zoom_boxes.append((
    (-0.1, s + 0.1),
    (-0.1, h + 0.1)
))

# Subsequent zooms
for stage in range(1, NUM_STAGES):

    idx = stage * LEVELS_PER_STAGE - 1

    Z = regions[idx]

    xmin = np.min(Z[:,0])
    xmax = np.max(Z[:,0])

    ymin = np.min(Z[:,1])
    ymax = np.max(Z[:,1])

    padx = 0.25 * (xmax - xmin)
    pady = 0.25 * (ymax - ymin)

    zoom_boxes.append((
        (xmin - padx, xmax + padx),
        (ymin - pady, ymax + pady)
    ))

# ==========================================================
# Animation setup
# ==========================================================

MAIN_FRAMES = NUM_STAGES * FRAMES_PER_STAGE

TOTAL_FRAMES = MAIN_FRAMES + FINAL_ZOOMOUT_FRAMES

# ==========================================================
# Animation function
# ==========================================================

def animate(frame):

    ax.clear()

    # ======================================================
    # FINAL ZOOM OUT
    # ======================================================

    if frame >= MAIN_FRAMES:

        local = frame - MAIN_FRAMES

        t = local / FINAL_ZOOMOUT_FRAMES

        t = smoothstep(t)

        # start from deepest zoom
        start_xlim, start_ylim = zoom_boxes[-1]

        # end at full triangle
        end_xlim, end_ylim = zoom_boxes[0]

        xmin = interpolate(start_xlim[0], end_xlim[0], t)
        xmax = interpolate(start_xlim[1], end_xlim[1], t)

        ymin = interpolate(start_ylim[0], end_ylim[0], t)
        ymax = interpolate(start_ylim[1], end_ylim[1], t)

        ax.fill(
            outer_pts[:,0],
            outer_pts[:,1],
            color='blue',
            alpha=0.35
        )

        ax.plot(
            outer_pts[:,0],
            outer_pts[:,1],
            color='blue',
            linewidth=3
        )

        # show ALL triangles without text
        for k in range(TOTAL_TRIANGLES):

            draw_triangle(
                ax,
                triangles[k],
                k + 1,
                show_text=False
            )

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        ax.set_aspect('equal')

        ax.axis('off')

        return

    # ------------------------------------------------------
    # Current stage
    # ------------------------------------------------------

    stage = frame // FRAMES_PER_STAGE

    if stage >= NUM_STAGES:
        stage = NUM_STAGES - 1

    # ------------------------------------------------------
    # Local frame inside current stage
    # ------------------------------------------------------

    local_frame = frame % FRAMES_PER_STAGE

    # ------------------------------------------------------
    # PHASES INSIDE EACH STAGE
    # ------------------------------------------------------

    zoom_fraction = 0.7

    zoom_end = int(zoom_fraction * FRAMES_PER_STAGE)

    # ------------------------------------------------------
    # Smooth zoom parameter
    # ------------------------------------------------------

    if local_frame <= zoom_end:

        t_zoom = local_frame / zoom_end

    else:

        t_zoom = 1.0

    t_zoom = smoothstep(t_zoom)

    # ------------------------------------------------------
    # Previous and target zoom boxes
    # ------------------------------------------------------

    if stage == 0:

        prev_xlim, prev_ylim = zoom_boxes[0]
        target_xlim, target_ylim = zoom_boxes[0]

    else:

        prev_xlim, prev_ylim = zoom_boxes[stage - 1]
        target_xlim, target_ylim = zoom_boxes[stage]

    # ------------------------------------------------------
    # Smooth zoom interpolation
    # ------------------------------------------------------

    xmin = interpolate(prev_xlim[0], target_xlim[0], t_zoom)
    xmax = interpolate(prev_xlim[1], target_xlim[1], t_zoom)

    ymin = interpolate(prev_ylim[0], target_ylim[0], t_zoom)
    ymax = interpolate(prev_ylim[1], target_ylim[1], t_zoom)

    # ------------------------------------------------------
    # Draw outer triangle
    # ------------------------------------------------------

    ax.fill(
        outer_pts[:,0],
        outer_pts[:,1],
        color='blue',
        alpha=0.35
    )

    ax.plot(
        outer_pts[:,0],
        outer_pts[:,1],
        color='blue',
        linewidth=3
    )

    # ------------------------------------------------------
    # Determine how many triangles to reveal
    # ------------------------------------------------------

    completed = stage * LEVELS_PER_STAGE

    if local_frame <= zoom_end:

        reveal = 0

    else:

        reveal_progress = (
            (local_frame - zoom_end)
            / (FRAMES_PER_STAGE - zoom_end)
        )

        reveal = int(reveal_progress * LEVELS_PER_STAGE)

    current_triangle = min(
        completed + reveal,
        TOTAL_TRIANGLES
    )

    # ------------------------------------------------------
    # Draw triangles
    # ------------------------------------------------------

    for k in range(current_triangle):

        draw_triangle(
            ax,
            triangles[k],
            k + 1,
            show_text=True
        )

    # ------------------------------------------------------
    # Apply zoom
    # ------------------------------------------------------

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.set_aspect('equal')

    ax.axis('off')

# ==========================================================
# Create animation
# ==========================================================

ani = FuncAnimation(
    fig,
    animate,
    frames=TOTAL_FRAMES,
    interval=40,
    repeat=False
)

plt.show()