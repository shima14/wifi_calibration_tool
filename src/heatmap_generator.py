import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def generate_heatmap(floorplan_path, points, signal_strengths):
    floorplan = Image.open(floorplan_path)
    width, height = floorplan.size

    # Dummy-Daten für die Heatmap
    heatmap_data = np.zeros((height, width))
    for (x, y), strength in zip(points, signal_strengths):
        heatmap_data[y, x] = strength
    
    plt.imshow(heatmap_data, cmap='hot', interpolation='nearest', alpha=0.5, antialiased=True)
    plt.colorbar()
    plt.show()
