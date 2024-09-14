# src/main.py
from src.wifi_scanner import scan_wifi
from src.heatmap import create_heatmap
from config.settings import FLOORPLAN_PATH
import numpy as np

def main():
    print("Starte WLAN-Scan...")
    wifi_data = scan_wifi()
    print("Gefundene WLANs: ", wifi_data)

    # Simuliere die WiFi-Signalstärke-Daten
    signal_data = np.random.random((100, 100))

    # Erstelle die Heatmap
    create_heatmap(signal_data, FLOORPLAN_PATH)

if __name__ == "__main__":
    main()
