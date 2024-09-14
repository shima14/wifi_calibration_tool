# src/heatmap.py
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def create_heatmap(signal_data, floorplan_path):
    floorplan = Image.open(floorplan_path)
    plt.imshow(floorplan, extent=[0, 100, 0, 100])
    plt.imshow(signal_data, cmap='jet', alpha=0.6, extent=[0, 100, 0, 100])
    plt.colorbar(label='Signalstärke (dBm)')
    plt.show()
