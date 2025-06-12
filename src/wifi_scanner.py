import pywifi
from pywifi import const
import time
import datetime 

def scan_wifi():
    # WiFi-Objekt erstellen
    wifi = pywifi.PyWiFi()
    # Erstes WLAN-Interface holen (meistens die eingebaute WLAN-Karte)
    iface = wifi.interfaces()[0]
    
    # WLAN-Interface scannen
    iface.scan()
    time.sleep(2)  # Kurze Pause, um die Scanergebnisse zu erhalten
    
    # Scanergebnisse abrufen
    scan_results = iface.scan_results()

    # Liste für gefundene Netzwerke
    networks = []
    for network in scan_results:
        ssid = network.ssid  # SSID des Netzwerks
        signal = network.signal  # Signalstärke in dBm
        bssid = network.bssid  # MAC-Adresse des Access Points
        auth = network.auth  # Authentifizierungstyp (z.B. WPA, WEP)
        cipher = network.cipher  # Verschlüsselungstyp (z.B. CCMP, TKIP)
        
        # Netzwerkinformationen speichern
        networks.append({
            'ssid': ssid,
            'signal': signal,
            'bssid': bssid,
            'auth': auth,
            'cipher': cipher
        })

    return networks
