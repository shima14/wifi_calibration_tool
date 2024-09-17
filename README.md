# wifi-survey-app

## Überblick
Die WiFi Survey App ist eine grafische Anwendung zur Durchführung von WiFi-Site-Umfragen. Der Benutzer kann einen Grundriss laden, Messpunkte setzen und die WLAN-Signalstärken an den markierten Positionen erfassen. Eine Heatmap zeigt die Signalstärke als Overlay auf dem Grundriss an.

## Funktionen
- Laden eines Grundrissbilds
- Setzen von Messpunkten durch Klicken auf die Karte
- Durchführung eines WLAN-Scans zur Messung der Signalstärke an den ausgewählten Punkten
- Anzeige einer Heatmap, die die Signalstärke visualisiert

## Voraussetzungen
- Python 3.8 oder höher
- Virtuelle Umgebung mit den folgenden Bibliotheken:
  - `Pillow`
  - `Tkinter`
  - `Matplotlib`
  - `pywifi`
  - `numpy`
  - `opencv-python`

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/username/wifi-survey-app.git
cd wifi-survey-app


Projekt ausführen 
python src/gui.py
