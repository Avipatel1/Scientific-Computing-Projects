import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

if not os.path.exists("solar_system_data.txt"):
    print("Error: solar_system_data.txt missing. Execute C++ simulation first.")
    exit()

# 1. Parse raw data matrix (9 objects now = 18 columns)
raw_data = np.loadtxt("solar_system_data.txt")
total_steps = raw_data.shape[0]

# Metadata array including the Sun as an active moving actor
planets_metadata = [
    {"name": "Sun",     "color": "#FFD166", "size": 14},
    {"name": "Mercury", "color": "#888888", "size": 4},
    {"name": "Venus",   "color": "#E3BB7B", "size": 6},
    {"name": "Earth",   "color": "#2B82C9", "size": 7},
    {"name": "Mars",    "color": "#E05A47", "size": 5},
    {"name": "Jupiter", "color": "#D4A373", "size": 12},
    {"name": "Saturn",  "color": "#E9D8A6", "size": 10},
    {"name": "Uranus",  "color": "#A8DADC", "size": 9},
    {"name": "Neptune", "color": "#457B9D", "size": 9}
]

# 2. Setup Plot Window
fig, ax = plt.subplots(figsize=(9, 9), facecolor='#0B0C10')
ax.set_facecolor('#0B0C10')
ax.grid(True, color='#1F2833', linestyle='--', alpha=0.3)

# Initialize blank graphic arrays for all 9 moving systems
planet_dots = []
planet_trails = []

for p in planets_metadata:
    dot, = ax.plot([], [], 'o', color=p["color"], markersize=p["size"], label=p["name"])
    trail, = ax.plot([], [], '-', color=p["color"], alpha=0.4, linewidth=1)
    planet_dots.append(dot)
    planet_trails.append(trail)

# Set initial viewport coordinates
current_limit = 2.0
ax.set_xlim(-current_limit, current_limit)
ax.set_ylim(-current_limit, current_limit)
ax.set_aspect('equal')

# Style axes labels in white
ax.tick_params(colors='white', which='both', labelsize=10)
ax.set_xlabel("X Position (AU)", color='white', fontsize=11)
ax.set_ylabel("Y Position (AU)", color='white', fontsize=11)
for spine in ax.spines.values():
    spine.set_color('white')

scale_text = ax.text(0.02, 0.93, f"View Radius: {current_limit} AU\nControls: [+] Zoom Out | [-] Zoom In", 
                     transform=ax.transAxes, color='white', fontsize=10, 
                     bbox=dict(facecolor='#1F2833', alpha=0.6, edgecolor='#457B9D'))

ax.legend(loc="upper right", facecolor='#1F2833', edgecolor='#457B9D', labelcolor='white', framealpha=0.8)

# 3. Interactive Key Event Zoom Controller
def on_key(event):
    global current_limit
    if event.key == '+' or event.key == '=':
        current_limit *= 1.8
    elif event.key == '-' or event.key == '_':
        current_limit /= 1.8
    elif event.key == 'r' or event.key == 'R':
        current_limit = 2.0
        
    ax.set_xlim(-current_limit, current_limit)
    ax.set_ylim(-current_limit, current_limit)
    scale_text.set_text(f"View Radius: {current_limit:.1f} AU\nControls: [+] Zoom Out | [-] Zoom In")
    fig.canvas.draw_idle()

fig.canvas.mpl_connect('key_press_event', on_key)

# 4. Multi-Particle Vector Rendering Loop
def update(frame):
    step_idx = frame * 15 # Skipping frames to optimize workflow speeds
    if step_idx >= total_steps:
        step_idx = total_steps - 1

    for i in range(9):
        # Slice X/Y vectors out of matrix columns dynamically
        raw_x = raw_data[:step_idx, i*2]
        raw_y = raw_data[:step_idx, i*2 + 1]

        if len(raw_x) > 0:
            planet_dots[i].set_data([raw_x[-1]], [raw_y[-1]])
            trail_slice = slice(max(0, len(raw_x)-600), len(raw_x))
            planet_trails[i].set_data(raw_x[trail_slice], raw_y[trail_slice])

    return planet_dots + planet_trails + [scale_text, ax.get_legend()]

ani = animation.FuncAnimation(fig, update, frames=total_steps // 15, interval=12, blit=True, repeat=True)
plt.title("True O(N^2) Gravitational N-Body Solar Core", color='white', fontsize=13, pad=15)
plt.show()
