# heatmap_generator.py
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image

def generate_heatmap(floorplan_path, points, signal_strengths):
    # Erstelle eine neue Abbildung
    plt.figure(figsize=(10, 8))

    # Extrahiere X- und Y-Koordinaten sowie Signalstärken
    x, y = zip(*points)
    signal_strength = signal_strengths

    # Erstelle die Heatmap
    plt.scatter(x, y, c=signal_strength, cmap='viridis', s=100, alpha=0.75)
    plt.colorbar(label='Signal Strength (dBm)')
    plt.title('WiFi Signal Strength Heatmap')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    # Speichern der Heatmap als Bilddatei
    plt.savefig('heatmap.png')
    plt.show()
