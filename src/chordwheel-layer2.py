import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# Layer 2 chords with correct finger presses
chords_layer2 = {
    'ONE':       [0, 0, 0, 1, 0],      # Idx
    'TWO':       [0, 0, 1, 0, 0],      # Mid
    'THREE':     [0, 1, 0, 0, 0],      # Rng
    'FOUR':      [1, 0, 0, 0, 0],      # Pky
    'FIVE':      [0, 0, 1, 1, 0],      # Mid, Idx
    'SIX':       [0, 1, 1, 0, 0],      # Rng, Mid
    'SEVEN':     [1, 1, 0, 0, 0],      # Pky, Rng
    'EIGHT':     [0, 0, 1, 1, 0],      # Mid, Idx
    'NINE':      [1, 0, 1, 0, 0],      # Pky, Mid
    'ZERO':      [1, 1, 1, 0, 0],      # Pky, Rng, Mid
    'UP_ARROW':  [0, 0, 0, 1, 1],      # Idx, Thm
    'DOWN_ARROW':[0, 0, 1, 0, 1],      # Mid, Thm
    'RIGHT_ARROW':[0, 1, 0, 0, 1],     # Rng, Thm
    'LEFT_ARROW':[1, 0, 0, 0, 1],      # Pky, Thm
    'PAGE_UP':   [0, 0, 1, 1, 1],      # Mid, Idx, Thm
    'PAGE_DOWN': [1, 1, 0, 0, 1],      # Pky, Rng, Thm
    'END':       [1, 1, 1, 1, 0],      # Pky, Rng, Mid, Idx
    'DELETE':    [1, 0, 1, 1, 0],      # Pky, Mid, Idx
    'INSERT':    [1, 0, 1, 0, 1],      # Pky, Mid, Thm
    'HOME':      [1, 1, 1, 0, 1],      # Pky, Rng, Mid, Thm
}

fingers = ['Pinky', 'Ring', 'Middle', 'Index', 'Thumb']
finger_colors = ['#d62728', '#ff7f0e', '#ffdb58', '#2ca02c', '#1f77b4']  # red, orange, yellow, green, blue
finger_markers = ['o', 's', '^', 'D', '*']  # circle, square, triangle_up, diamond, star

num_chords = len(chords_layer2)
angle_per_chord = 2 * np.pi / num_chords

fig, ax = plt.subplots(figsize=(12,12), subplot_kw=dict(polar=True))
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim(0, 7)

ring_radii = [2, 3, 4, 5, 6]  # concentric rings Pinky (2) to Thumb (6)

# Draw colored rings for fingers
for i, r in enumerate(ring_radii):
    ax.fill_between(np.linspace(0, 2*np.pi, 500), r, r+0.7,
                    color=finger_colors[i], alpha=0.15)

# Radial separators between wedges
for i in range(num_chords):
    angle = i * angle_per_chord
    ax.plot([angle, angle], [ring_radii[0], ring_radii[-1]+0.7], color='lightgray', lw=0.8)

# Plot finger dots per chord
for i, (label, pressed) in enumerate(chords_layer2.items()):
    angle = i * angle_per_chord + angle_per_chord/2
    for j, val in enumerate(pressed):
        if val:
            ax.plot(angle, ring_radii[j] + 0.35, finger_markers[j], markersize=18,
                    color=finger_colors[j], markeredgecolor='k', markeredgewidth=0.8)

# Letter labels outside the outer ring
label_radius = ring_radii[-1] + 1.1
for i, label in enumerate(chords_layer2.keys()):
    angle = i * angle_per_chord + angle_per_chord/2
    ha = 'center'
    if np.pi/4 < angle < 3*np.pi/4:
        ha = 'center'
    elif 3*np.pi/4 <= angle <= 5*np.pi/4:
        ha = 'right'
    elif 5*np.pi/4 < angle < 7*np.pi/4:
        ha = 'center'
    else:
        ha = 'left'
    ax.text(angle, label_radius, label, fontsize=12, fontweight='bold',
            horizontalalignment=ha, verticalalignment='center')

# Legend below the wheel
legend_elements = [Line2D([0], [0], marker=m, color='w', label=f,
                          markerfacecolor=c, markeredgecolor='k', markersize=12, markeredgewidth=0.8)
                   for m, c, f in zip(finger_markers, finger_colors, fingers)]

ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.1),
          fontsize=12, frameon=False, ncol=5, title="Fingers")

# Remove grid and ticks
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])

plt.savefig("chord_wheel_layer2_corrected.svg", format="svg", bbox_inches='tight')
plt.show()
