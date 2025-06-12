# wifi-survey-app

#  WiFi Kalibrierungstool

Ein grafisches Python-Tool zur Kalibrierung von Gebäudekarten und Erfassung von WiFi-Signalen an bestimmten Punkten. Ideal für die Erstellung von Signalstärke-Heatmaps.

---

##  1. Benötigte Bibliotheken (Installation)

Stellen Sie sicher, dass Python 3.x installiert ist. Installieren Sie anschließend die benötigten Bibliotheken mit:

```bash
pip install pillow

## Voraussetzungen
- Python 3.8 oder höher
- Virtuelle Umgebung mit den folgenden Bibliotheken:
  - `Pillow`
  - `Tkinter`
  - `Matplotlib`
  - `pywifi`
  - `numpy`
  - `opencv-python`



### 1. Repository klonen

```bash
git clone https://github.com/username/wifi-survey-app.git
cd wifi-survey-app


#Projekt ausführen 
#Virtuelle Umgebung aktivieren
source venv/Scripts/activate
python src/calibration.py
.............


 3. Schritt-für-Schritt Anleitung zur Nutzung



Bodenplan hochladen
Klicken Sie auf „Bodenplan hochladen“, wählen Sie ein Bild (im ordner images)(z. B. JPG oder PNG) Ihres Gebäudeplans.
Das Bild wird auf 800×600 Pixel skaliert.

2. Ursprungspunkt setzen (Origin)
Klicken Sie auf „Setze Punkt Origin“, dann auf eine Stelle im Bild, die als (0,0)-Startpunkt gelten soll (z. B. linke untere Ecke).

 3. Zweiten Punkt setzen (Punkt B)
Klicken Sie auf „Setze Punkt B“ und wählen Sie einen zweiten Punkt im Bild aus, dessen echter Abstand zum Ursprungspunkt bekannt ist.

4. Reale Distanz eingeben
Geben Sie im Feld „Abstand real (Meter)“ die tatsächliche Distanz zwischen Ursprung und Punkt B ein (z. B. 100).

 5. Kalibrierung durchführen
Klicken Sie auf „Kalibriere“. Das Programm berechnet, wie viele Pixel einem Meter entsprechen und speichert den Umrechnungsfaktor.

 6. WiFi Scan durchführen
Klicken Sie auf „WiFi Scan“.

Klicken Sie auf eine Position im Gebäudeplan, an der Sie sich befinden.

Das Tool scannt verfügbare Netzwerke (über wifi_scan.py) und speichert die Signalstärken an dieser Stelle.

 7. Ergebnisse anzeigen
Es öffnet sich ein Fenster mit den Scan-Ergebnissen (SSID und Signalstärke in dBm).

Wenn Sie mit der Maus über gespeicherte Punkte fahren, wird ein Tooltip mit Informationen angezeigt.

 8. Zurücksetzen
Klicken Sie auf „Zurücksetzen“, um das Bild und alle gesetzten Punkte zurückzusetzen und von vorne zu beginnen.

