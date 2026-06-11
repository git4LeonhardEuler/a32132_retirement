import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

# -------- Roue avec rayons --------
def dessiner_roue(x, y, r):
    cercle = plt.Circle((x, y), r, fill=False, linewidth=2)
    ax.add_patch(cercle)

    for angle in np.linspace(0, 2*np.pi, 20, endpoint=False):
        ax.plot([x, x + r*np.cos(angle)],
                [y, y + r*np.sin(angle)], linewidth=0.6)

# -------- Positions --------
roue_arriere = (-3, 0)
tube_direction = (1.5, 2)
roue_avant = (tube_direction[0], 0)

dessiner_roue(*roue_arriere, 1)
dessiner_roue(*roue_avant, 1)

# -------- CADRE --------
boitier = (-0.8, 0)
tube_selle = (-1.6, 2)

ax.plot([boitier[0], tube_selle[0]],
        [boitier[1], tube_selle[1]], linewidth=2)

ax.plot([tube_selle[0], tube_direction[0]],
        [tube_selle[1], tube_direction[1]], linewidth=2)

ax.plot([tube_direction[0], boitier[0]],
        [tube_direction[1], boitier[1]], linewidth=2)

ax.plot([boitier[0], roue_arriere[0]],
        [boitier[1], roue_arriere[1]], linewidth=2)

ax.plot([tube_selle[0], roue_arriere[0]],
        [tube_selle[1], roue_arriere[1]], linewidth=2)

# -------- FOURCHE SIMPLE --------
pivot = tube_direction
ax.plot([pivot[0], roue_avant[0]],
        [pivot[1], roue_avant[1]],
        linewidth=2)

# -------- GUIDON --------
potence = (pivot[0], pivot[1] + 0.4)
ax.plot([pivot[0], potence[0]],
        [pivot[1], potence[1]], linewidth=2)

angle = np.deg2rad(10)
longueur = 0.8

x_gauche = potence[0] - longueur * np.cos(angle)
y_gauche = potence[1] + longueur * np.sin(angle)

x_droite = potence[0] + longueur * np.cos(angle)
y_droite = potence[1] - longueur * np.sin(angle)

ax.plot([x_gauche, x_droite],
        [y_gauche, y_droite], linewidth=2)

# -------- SELLE --------
haut_selle = (tube_selle[0], tube_selle[1] + 0.5)

ax.plot([tube_selle[0], haut_selle[0]],
        [tube_selle[1], haut_selle[1]], linewidth=2)

ax.plot([haut_selle[0] - 0.5, haut_selle[0] + 0.5],
        [haut_selle[1], haut_selle[1]], linewidth=2)

# -------- PEDALIER --------
cercle = plt.Circle(boitier, 0.3, fill=False, linewidth=2)
ax.add_patch(cercle)

angle_p = np.pi / 4
x1 = boitier[0] + 0.7 * np.cos(angle_p)
y1 = boitier[1] + 0.7 * np.sin(angle_p)

x2 = boitier[0] - 0.7 * np.cos(angle_p)
y2 = boitier[1] - 0.7 * np.sin(angle_p)

ax.plot([boitier[0], x1], [boitier[1], y1], linewidth=2)
ax.plot([boitier[0], x2], [boitier[1], y2], linewidth=2)

# -------- FONCTION TEXTE EN ARC (corrigée) --------

def texte_en_arc(texte, rayon, angle_debut, angle_fin, y_offset=0):
    angles = np.linspace(angle_debut, angle_fin, len(texte))

    for i, char in enumerate(texte):
        x = rayon * np.cos(angles[i])
        y = rayon * np.sin(angles[i]) + y_offset

        # rotation douce mais jamais à l'envers
        rotation = np.degrees(angles[i] - np.pi/2)
        if rotation < -90:
            rotation += 180
        if rotation > 90:
            rotation -= 180

        ax.text(x, y, char,
                rotation=rotation,
                ha='center', va='center',
                fontsize=12)


# Texte principal
texte_en_arc("Bon départ en retraite Jean-François", rayon=4,
             angle_debut=np.pi*0.9, angle_fin=np.pi*0.1, y_offset=1)

# -------- MOTS AUTOUR --------
mots = ["MMC", "MAP","SALOME","Scibian", "T24", "GITLAB", "COLLEGUES", "Renardières","Armoric","Maillage"]

angles = np.linspace(0, 2*np.pi, len(mots), endpoint=False)
rayon_mots = 4.8

for i, mot in enumerate(mots):
    x = rayon_mots * np.cos(angles[i])
    y = rayon_mots * np.sin(angles[i]) + 1

    ax.text(x, y, mot,
            rotation=np.degrees(angles[i]) + 90,
            ha='center', va='center',
            fontsize=10, fontweight='bold')

# -------- AFFICHAGE --------
ax.set_aspect('equal')
ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-3, 5.5)
ax.axis('off')

plt.show()