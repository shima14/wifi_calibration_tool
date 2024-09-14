# src/wifi_scanner.py
import pywifi
import time

def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Zugriff auf die erste Netzwerkschnittstelle
    iface.scan()
    time.sleep(3)
    results = iface.scan_results()
    wifi_data = []
    for network in results:
        wifi_data.append({
            'ssid': network.ssid,
            'bssid': network.bssid,
            'signal': network.signal  # Signalstärke
        })
    return wifi_data
