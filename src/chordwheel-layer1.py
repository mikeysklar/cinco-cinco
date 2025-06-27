import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# Define finger data and visualization settings
fingers = ['Pinky', 'Ring', 'Middle', 'Index', 'Thumb']
finger_colors = ['#d62728', '#ff7f0e', '#ffdb58', '#2ca02c', '#1f77b4']
finger_markers = ['o', 's', '^', 'D', '*']

# Chord data: fingers pressed per letter (P, R, M, I, T)
chords = {
    'A': [0,1,0,0,0],
    'B': [1,0,0,0,1],
    'C': [1,0,0,1,0],
    'D': [0,1,1,1,0],
    'E': [0,0,1,0,0],
    'F': [0,1,1,0,1],
    'G': [0,0,1,0,1],
    'H': [0,1,0,0,1],
    'I': [0,0,1,0,0],
    'J': [0,1,1,1,1],
    'K': [1,0,1,0,1],
    'L': [1,0,1,0,0],
    'M': [0,0,1,0,1],
    'N': [0,1,1,0,0],
    'O': [0,1,0,1,0],
    'P': [1,1,1,0,0],
    'Q': [1,1,1,1,1],
    'R': [0,0,1,1,0],
    'S': [0,0,0,0,1],
    'T': [1,1,0,0,0],
    'U': [1,1,1,1,0],
    'V': [1,1,0,0,1],
    'W': [0,1,0,1,1],
    'X': [1,0,0,1,1],
    'Y': [0,0,1,1,1],
    'Z': [1,1,1,0,1]
}

num_chords = len(chords)
angle_per_chord = 2 * np.pi / num_chords

fig, ax = plt.subplots(figsize=(10,10), subplot_kw=dict(polar=True))
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim(0, 7)

ring_radii = [2, 3, 4, 5, 6]

# Draw colored concentric rings
for i, r in enumerate(ring_radii):
    ax.fill_between(np.linspace(0, 2*np.pi, 500), r, r+0.7, 
                    color=finger_colors[i], alpha=0.15)

# Draw radial lines separating wedges
for i in range(num_chords):
    angle = i * angle_per_chord
    ax.plot([angle, angle], [ring_radii[0], ring_radii[-1] + 0.7], color='lightgray', lw=0.8)

# Plot finger dots
for i, (letter, fingers_pressed) in enumerate(chords.items()):
    angle = i * angle_per_chord + angle_per_chord / 2
    for j, pressed in enumerate(fingers_pressed):
        if pressed:
            ax.plot(angle, ring_radii[j] + 0.35, finger_markers[j], markersize=18, 
                    color=finger_colors[j], markeredgecolor='k', markeredgewidth=0.8)

# Letter labels
label_radius = ring_radii[-1] + 1.1
for i, letter in enumerate(chords.keys()):
    angle = i * angle_per_chord + angle_per_chord / 2

    ha = 'center'
    if np.pi / 4 < angle < 3 * np.pi / 4:
        ha = 'center'
    elif 3 * np.pi / 4 <= angle <= 5 * np.pi / 4:
        ha = 'right'
    elif 5 * np.pi / 4 < angle < 7 * np.pi / 4:
        ha = 'center'
    else:
        ha = 'left'

    ax.text(angle, label_radius, letter, fontsize=16, fontweight='bold',
            horizontalalignment=ha, verticalalignment='center')

# Smaller legend/key below the plot
legend_elements = [Line2D([0], [0], marker=m, color='w', label=f, 
                          markerfacecolor=c, markeredgecolor='k', markersize=12, markeredgewidth=0.8) 
                   for m, c, f in zip(finger_markers, finger_colors, fingers)]

ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.1),
          fontsize=12, frameon=False, ncol=5, title="Fingers")

ax.legend_.get_title().set_fontsize('14')
ax.legend_.get_title().set_fontweight('bold')

ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])

plt.savefig("chord_wheel_clean.svg", format="svg", bbox_inches='tight')
plt.show()
