# import pywifi
# import time
# import pandas as pd
# from datetime import datetime

# def scan_wifi():
#     wifi = pywifi.PyWiFi()
#     iface = wifi.interfaces()[0]
    
#     iface.scan()
#     time.sleep(2)  # Warten, bis der Scan abgeschlossen ist
    
#     scan_results = iface.scan_results()
    
#     wifi_data = []
#     for network in scan_results:
#         wifi_info = {
#             'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             'SSID': network.ssid,
#             'Signal Strength (dBm)': network.signal,
#             'BSSID': network.bssid
#         }
#         wifi_data.append(wifi_info)
    
#     return wifi_data

# def save_to_csv(data, filename):
#     df = pd.DataFrame(data)
#     df.to_csv(filename, index=False)

# def main():
#     print("Starte WLAN-Scan...")
#     wifi_data = scan_wifi()
    
#     if not wifi_data:
#         print("Keine WiFi-Daten gefunden.")
#         return

#     # Zeige die Daten im Terminal an
#     print("Gefundene WLANs:")
#     for data in wifi_data:
#         print(f"Zeit: {data['Timestamp']}, SSID: {data['SSID']}, Signalstärke: {data['Signal Strength (dBm)']} dBm, BSSID: {data['BSSID']}")

#     # Speichern der Daten in einer CSV-Datei
#     csv_filename = 'wifi_signal_strength.csv'
#     save_to_csv(wifi_data, csv_filename)
#     print(f"WiFi-Daten wurden in '{csv_filename}' gespeichert.")

# if __name__ == "__main__":
#     main()




import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math

class SignalMeasurement:
    def __init__(self, root):
        self.root = root
        self.root.title("Signalstärkemessung")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.TOP, pady=10)

        self.upload_button = tk.Button(self.button_frame, text="Bodenplan hochladen", command=self.load_image)
        self.upload_button.pack(side=tk.LEFT, padx=10)

        self.scan_button = tk.Button(self.button_frame, text="Signal scannen", command=self.scan_signal)
        self.scan_button.pack(side=tk.LEFT, padx=10)

        self.image_path = None

        self.canvas.bind("<Button-1>", self.set_point)

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.floorplan_image = ImageTk.PhotoImage(Image.open(self.image_path).resize((800, 600)))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.floorplan_image)

    def set_point(self, event):
        self.point = (event.x, event.y)
        self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill="blue")

    def scan_signal(self):
        signal_strength = -50  # Beispielwert
        self.canvas.create_text(self.point[0], self.point[1] - 10, text=f"Signal: {signal_strength} dBm", fill="black")


class Calibration:
    def __init__(self, root, update_pixel_per_meter_callback):
        self.root = root
        self.root.title("Kalibrierungs-Tool")
        self.root.configure(bg='#f0f0f0')

        # Callback zur Aktualisierung der Pixel pro Meter
        self.update_pixel_per_meter_callback = update_pixel_per_meter_callback

        # Canvas und Buttons erstellen
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.button_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.button_frame.pack(side=tk.TOP, pady=10)

        self.upload_button = tk.Button(self.button_frame, text="Bodenplan hochladen", command=self.load_image)
        self.upload_button.pack(side=tk.LEFT, padx=10)

        self.calibrate_button = tk.Button(self.button_frame, text="Kalibrierung", command=self.calibrate)
        self.calibrate_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.button_frame, text="Zurücksetzen", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.origin_button = tk.Button(self.button_frame, text="Origin setzen", command=self.enable_set_origin)
        self.origin_button.pack(side=tk.LEFT, padx=10)

        # Eingabefeld für Meter
        self.distance_entry_label = tk.Label(self.button_frame, text="Eingabe Meter: ", bg='#f0f0f0')
        self.distance_entry_label.pack(side=tk.LEFT, padx=10)

        self.distance_entry = tk.Entry(self.button_frame)
        self.distance_entry.pack(side=tk.LEFT, padx=10)

        # Label für Pixel pro Meter
        self.pixel_per_meter_label = tk.Label(self.button_frame, text="Pixel pro Meter: N/A", bg='#f0f0f0')
        self.pixel_per_meter_label.pack(side=tk.LEFT, padx=10)

        # Variablen zur Speicherung der Referenzpunkte und berechneter Werte
        self.points = []
        self.origin_point = None
        self.meter_per_pixel = None

        # Event zum Hinzufügen von Punkten
        self.canvas.bind("<Button-1>", self.add_point)

        # Bildvariablen
        self.floorplan_image = None
        self.image_path = None

    def add_point(self, event):
        if len(self.points) < 2:
            x, y = event.x, event.y
            if self.origin_point:
                x -= self.origin_point[0]
                y -= self.origin_point[1]
            self.points.append((x, y))

            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
            if len(self.points) == 2:
                self.draw_line()

    def draw_line(self):
        p1, p2 = self.points
        self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="blue", width=2)

        distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        self.canvas.create_text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 - 10,
                                 text=f"Pixelabstand: {distance:.2f} px", fill="black")
        if self.meter_per_pixel is not None:
            real_distance = self.meter_per_pixel * distance
            self.canvas.create_text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 10,
                                     text=f"Meter: {real_distance:.2f} m", fill="black")

            pixel_per_meter = 1 / self.meter_per_pixel
            self.update_pixel_per_meter_callback(pixel_per_meter)

    def calibrate(self):
        if len(self.points) == 2:
            p1, p2 = self.points
            distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p1[1] - p2[1]) ** 2)

            try:
                real_distance = float(self.distance_entry.get())
                self.meter_per_pixel = real_distance / distance
                self.draw_line()
            except ValueError:
                pass

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.floorplan_image = ImageTk.PhotoImage(Image.open(self.image_path).resize((800, 600)))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.floorplan_image)

    def reset(self):
        self.points.clear()
        self.origin_point = None
        self.canvas.delete("all")
        self.load_image()

    def enable_set_origin(self):
        self.canvas.bind("<Button-1>", self.set_origin)

    def set_origin(self, event):
        self.origin_point = (event.x, event.y)
        self.canvas.create_oval(self.origin_point[0]-5, self.origin_point[1]-5,
                                self.origin_point[0]+5, self.origin_point[1]+5, fill="green")


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WLAN Mess- und Kalibrierungs-App")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.TOP, pady=10)

        self.signal_button = tk.Button(self.button_frame, text="Signal messen", command=self.open_signal_measurement)
        self.signal_button.pack(side=tk.LEFT, padx=10)

        self.calibration_button = tk.Button(self.button_frame, text="Kalibrierung", command=self.open_calibration)
        self.calibration_button.pack(side=tk.LEFT, padx=10)

    def update_pixel_per_meter(self, pixel_per_meter):
        # Update the pixel per meter label in the calibration window
        if hasattr(self, 'calibration_window'):
            self.calibration_window.pixel_per_meter_label.config(text=f"Pixel pro Meter: {pixel_per_meter:.2f}")

    def open_signal_measurement(self):
        self.new_window = tk.Toplevel(self.root)
        SignalMeasurement(self.new_window)

    def open_calibration(self):
        self.calibration_window = tk.Toplevel(self.root)
        Calibration(self.calibration_window, self.update_pixel_per_meter)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
