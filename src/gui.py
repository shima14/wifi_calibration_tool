
# import tkinter as tk
# from tkinter import filedialog
# from PIL import Image, ImageTk
# import math
# import os
# import json

# class App:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Kalibrierungs-Tool")
#         self.root.configure(bg='#f0f0f0')

#         # Canvas und Button erstellen
#         self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
#         self.canvas.pack()

#         self.button_frame = tk.Frame(root, bg='#f0f0f0')
#         self.button_frame.pack(side=tk.TOP, pady=10)

#         self.calibrate_button = tk.Button(self.button_frame, text="Kalibrierung", command=self.calibrate)
#         self.calibrate_button.pack(side=tk.LEFT, padx=10)

#         self.reset_button = tk.Button(self.button_frame, text="Zurücksetzen", command=self.reset)
#         self.reset_button.pack(side=tk.LEFT, padx=10)

#         self.origin_button = tk.Button(self.button_frame, text="Origin", command=self.enable_set_origin)
#         self.origin_button.pack(side=tk.LEFT, padx=10)

#         self.measure_button = tk.Button(self.button_frame, text="Punkt messen", command=self.enable_measure_point)
#         self.measure_button.pack(side=tk.LEFT, padx=10)

#         # Feld zur Anzeige des Abstands in Pixeln
#         self.distance_label = tk.Label(self.button_frame, text="Pixelabstand: ", bg='#f0f0f0')
#         self.distance_label.pack(side=tk.LEFT, padx=10)

#         # Neues Textfeld für die Eingabe des realen Abstands in Metern
#         self.distance_entry_label = tk.Label(self.button_frame, text="Eingabe Meter: ", bg='#f0f0f0')
#         self.distance_entry_label.pack(side=tk.LEFT, padx=10)
#         self.distance_entry = tk.Entry(self.button_frame)
#         self.distance_entry.pack(side=tk.LEFT, padx=10)

#         # Neues Label zur Anzeige der berechneten Meter pro Pixel
#         self.meter_per_pixel_label = tk.Label(self.button_frame, text="Meter pro Pixel: ", bg='#f0f0f0')
#         self.meter_per_pixel_label.pack(side=tk.LEFT, padx=10)

#         # Label zur Anzeige des gemessenen Abstands in Metern
#         self.measured_distance_label = tk.Label(self.button_frame, text="Gemessene Distanz: ", bg='#f0f0f0')
#         self.measured_distance_label.pack(side=tk.LEFT, padx=10)

#         # Variablen zur Speicherung der Referenzpunkte und berechneter Werte
#         self.points = []
#         self.origin_point = None  # Speichert den Ursprungspunkt
#         self.distance = None  # Speichert den Abstand in Pixeln
#         self.text_item = None  # Speichert die ID des Textobjekts auf der Linie
#         self.origin_text_item = None  # Speichert die ID des Ursprungs-Textobjekts
#         self.meter_per_pixel = None  # Speichert den berechneten Meter-pro-Pixel-Wert
#         self.measuring_point = False  # Kontrolliert, ob ein Punkt gemessen wird

#         # Event zum Hinzufügen von Punkten
#         self.canvas.bind("<Button-1>", self.add_point)

#         # Bildvariablen
#         self.floorplan_image = None
#         self.image_path = None

#         # Laden der gespeicherten Daten
#         self.load_image()
#         self.load_saved_points()

#     def add_point(self, event):
#         if self.measuring_point:
#             # Punkt messen und Distanz berechnen
#             if self.origin_point and self.meter_per_pixel:
#                 x, y = event.x - self.origin_point[0], event.y - self.origin_point[1]
#                 distance_px = math.sqrt(x**2 + y**2)
#                 distance_m = distance_px * self.meter_per_pixel
#                 self.measured_distance_label.config(text=f"Gemessene Distanz: {distance_m:.2f} m")

#                 # Zeichne den Punkt und die Linie zum Ursprung
#                 self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill="blue")
#                 self.canvas.create_line(self.origin_point[0], self.origin_point[1], event.x, event.y, fill="green", width=2)

#             # Messmodus deaktivieren
#             self.measuring_point = False
#         else:
#             # Referenzpunkte für die Kalibrierung setzen
#             if len(self.points) < 2:
#                 x, y = event.x, event.y
#                 if self.origin_point:
#                     x -= self.origin_point[0]
#                     y -= self.origin_point[1]
#                 self.points.append((x, y))

#                 self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
#                 if len(self.points) == 2:
#                     self.draw_line()

#     def draw_line(self):
#         # Zeichne eine Linie zwischen den beiden Punkten
#         p1, p2 = self.points
#         self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="blue", width=2)

#         # Berechne die Mitte der Linie, um dort den Text anzuzeigen
#         mid_x = (p1[0] + p2[0]) / 2
#         mid_y = (p1[1] + p2[1]) / 2

#         if self.distance and self.distance_entry.get():
#             real_distance = float(self.distance_entry.get())
#             text = f"{real_distance:.2f} m, {self.distance:.2f} px"
#             if self.text_item:
#                 self.canvas.delete(self.text_item)
#             self.text_item = self.canvas.create_text(mid_x, mid_y, text=text, fill="black")

#     def calibrate(self):
#         if len(self.points) == 2:
#             p1, p2 = self.points
#             self.distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p1[1] - p2[1]) ** 2)
#             self.distance_label.config(text=f"Pixelabstand: {self.distance:.2f} px")

#             try:
#                 real_distance = float(self.distance_entry.get())
#                 self.meter_per_pixel = real_distance / self.distance
#                 self.meter_per_pixel_label.config(text=f"Meter pro Pixel: {self.meter_per_pixel:.4f} m/px")
#                 self.draw_line()
#             except ValueError:
#                 self.meter_per_pixel_label.config(text="Ungültige Eingabe für Meter.")
#             self.save_points()

#     def load_image(self):
#         self.image_path = filedialog.askopenfilename()
#         if self.image_path:
#             self.floorplan_image = ImageTk.PhotoImage(Image.open(self.image_path).resize((800, 600)))
#             self.canvas.create_image(0, 0, anchor=tk.NW, image=self.floorplan_image)

#     def load_saved_points(self):
#         if os.path.exists("points.json"):
#             with open("points.json", "r") as f:
#                 data = json.load(f)
#                 self.points = data.get("points", [])
#                 self.distance = data.get("distance", None)
#                 real_distance = data.get("real_distance", None)

#                 for point in self.points:
#                     self.canvas.create_oval(point[0]-5, point[1]-5, point[0]+5, point[1]+5, fill="red")

#                 if len(self.points) == 2:
#                     self.draw_line()
#                     self.distance_label.config(text=f"Pixelabstand: {self.distance:.2f} px")
#                     if real_distance:
#                         real_distance = float(real_distance)
#                         self.distance_entry.insert(0, str(real_distance))
#                         self.meter_per_pixel = real_distance / self.distance
#                         self.meter_per_pixel_label.config(text=f"Meter pro Pixel: {self.meter_per_pixel:.4f} m/px")
#                         self.draw_line()

#     def save_points(self):
#         real_distance = self.distance_entry.get() if self.distance_entry.get() else None
#         with open("points.json", "w") as f:
#             json.dump({"points": self.points, "distance": self.distance, "real_distance": real_distance}, f)

#     def reset(self):
#         self.points.clear()
#         self.origin_point = None
#         self.distance = None
#         self.meter_per_pixel = None
#         self.distance_label.config(text="Pixelabstand: ")
#         self.meter_per_pixel_label.config(text="Meter pro Pixel: ")
#         self.canvas.delete("all")
#         self.load_image()
#         self.distance_entry.delete(0, tk.END)
#         self.canvas.bind("<Button-1>", self.add_point)
#         self.origin_button.config(state=tk.NORMAL)
#         if self.origin_text_item:
#             self.canvas.delete(self.origin_text_item)
#             self.origin_text_item = None

#     def enable_set_origin(self):
#         self.canvas.bind("<Button-1>", self.set_origin)
#         self.origin_button.config(state=tk.DISABLED)

#     def set_origin(self, event):
#         self.origin_point = (event.x, event.y)
#         self.canvas.create_oval(self.origin_point[0]-5, self.origin_point[1]-5, self.origin_point[0]+5, self.origin_point[1]+5, fill="green")
#         self.origin_text_item = self.canvas.create_text(self.origin_point[0] + 30, self.origin_point[1] + 10, text="Origin", fill="black")
#         self.canvas.unbind("<Button-1>")

#     def enable_measure_point(self):
#         if not self.origin_point or not self.meter_per_pixel:
#             return
#         self.measuring_point = True
#         self.canvas.bind("<Button-1>", self.add_point)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = App(root)
#     root.mainloop()
                   

import tkinter as tk
from tkinter import filedialog, Toplevel, Label
from PIL import Image, ImageTk
from tkinter import messagebox
import math
import random
import pywifi
import time 
import datetime 
import json
import pickle
import os



class SignalMeasurement:
    def __init__(self, root):
        self.root = root
        self.root.title("Signalstärkemessung")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.TOP, pady=10)

        self.upload_button = tk.Button(self.button_frame, text="Floorplan hochladen", command=self.load_image)
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
        self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="blue")

    def scan_signal(self):
        wifi = pywifi.PyWiFi()  # Create a PyWiFi object
        iface = wifi.interfaces()[0]  # Get the first Wi-Fi interface
        iface.scan()  # Start scanning
        time.sleep(2)  # Wait for scan to finish
        results = iface.scan_results()  # Get scan results

        if results:
            # Get the current timestamp
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            wifi_data = {
                'timestamp': current_time,  # Add timestamp
                'ssid': results[0].ssid,  # Use the first result
                'signal': f"{results[0].signal} dBm",  # Signal strength
                'bssid': results[0].bssid,
                'auth': results[0].akm[0] if results[0].akm else "Unknown",
                'cipher': results[0].cipher[0] if results[0].cipher else "Unknown"
            }

            # Popup-Fenster erstellen
            popup = Toplevel(self.root)
            popup.title("WLAN-Informationen")

            # WLAN-Daten anzeigen
            Label(popup, text=f"Zeitpunkt: {wifi_data['timestamp']}").pack(pady=5)  # Display timestamp
            Label(popup, text=f"SSID: {wifi_data['ssid']}").pack(pady=5)
            Label(popup, text=f"Signalstärke: {wifi_data['signal']}").pack(pady=5)
            Label(popup, text=f"BSSID: {wifi_data['bssid']}").pack(pady=5)
            Label(popup, text=f"Authentifizierung: {wifi_data['auth']}").pack(pady=5)
            Label(popup, text=f"Verschlüsselung: {wifi_data['cipher']}").pack(pady=5)

            # Größe des Popup-Fensters anpassen
            popup.geometry("300x220")
        else:
            popup = Toplevel(self.root)
            popup.title("WLAN-Informationen")
            Label(popup, text="Keine WLAN-Netzwerke gefunden.").pack(pady=5)
            popup.geometry("300x100")


# class Calibration:
    # def __init__(self, root):
    #     self.root = root
    #     self.root.title("Kalibrierungs-Tool")
    #     self.root.configure(bg='#f0f0f0')

    #     # Canvas und Buttons erstellen
    #     self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
    #     self.canvas.pack()

    #     self.button_frame = tk.Frame(root, bg='#f0f0f0')
    #     self.button_frame.pack(side=tk.TOP, pady=10)

    #     self.upload_button = tk.Button(self.button_frame, text="Bodenplan hochladen", command=self.load_image)
    #     self.upload_button.pack(side=tk.LEFT, padx=10)

    #     self.calibrate_button = tk.Button(self.button_frame, text="Kalibrierung", command=self.calibrate)
    #     self.calibrate_button.pack(side=tk.LEFT, padx=10)

    #     self.reset_button = tk.Button(self.button_frame, text="Zurücksetzen", command=self.reset)
    #     self.reset_button.pack(side=tk.LEFT, padx=10)

    #     self.origin_button = tk.Button(self.button_frame, text="Origin setzen", command=self.enable_set_origin)
    #     self.origin_button.pack(side=tk.LEFT, padx=10)

    #     self.distance_entry_label = tk.Label(self.button_frame, text="Eingabe Meter: ", bg='#f0f0f0')
    #     self.distance_entry_label.pack(side=tk.LEFT, padx=10)
    #     self.distance_entry = tk.Entry(self.button_frame)
    #     self.distance_entry.pack(side=tk.LEFT, padx=10)

    #     # Label für Pixel pro Meter hinzufügen
    #     self.pixel_per_meter_label = tk.Label(self.button_frame, text="Pixel pro Meter: N/A", bg='#f0f0f0')
    #     self.pixel_per_meter_label.pack(side=tk.LEFT, padx=10)

    #     # Variablen zur Speicherung der Referenzpunkte und berechneter Werte
    #     self.points = []
    #     self.origin_point = None
    #     self.meter_per_pixel = None
    #     self.text_items = []  # ذخیره آیتم‌های متنی برای پاک کردن

    #     # Event zum Hinzufügen von Punkten
    #     self.canvas.bind("<Button-1>", self.add_point)

    #     # Bildvariablen
    #     self.floorplan_image = None
    #     self.image_path = None

    #     # Daten beim Start laden
    #     self.load_saved_data()

    # def add_point(self, event):
    #     if len(self.points) < 2:
    #         x, y = event.x, event.y
    #         if self.origin_point:
    #             x -= self.origin_point[0]
    #             y -= self.origin_point[1]
    #         self.points.append((x, y))

    #         self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
    #         if len(self.points) == 2:
    #             self.draw_line()

    # def draw_line(self):
    #     # Zeichne eine Linie zwischen den beiden Punkten
    #     p1, p2 = self.points
    #     self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="blue", width=2)

    # def calibrate(self):
    #     if len(self.points) == 2:
    #         # حذف آیتم‌های متنی قبلی
    #         for item in self.text_items:
    #             self.canvas.delete(item)
    #         self.text_items.clear()

    #         p1, p2 = self.points
    #         distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    #         try:
    #             real_distance = float(self.distance_entry.get())
    #             self.meter_per_pixel = real_distance / distance
    #             self.pixel_per_meter_label.config(text=f"Pixel pro Meter: {self.meter_per_pixel:.4f} m/px")

    #             # Zeige die Eingabemeter auf der Linie an
    #             text_item_meters = self.canvas.create_text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 15,
    #                                                        text=f"Meter: {real_distance:.2f} m", fill="black")
    #             text_item_pixels = self.canvas.create_text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 30,
    #                                                        text=f"Pixel: {distance:.2f} px", fill="black")

    #             # ذخیره آیتم‌های متنی برای پاک کردن در کالیبراسیون بعدی
    #             self.text_items.extend([text_item_meters, text_item_pixels])

    #             self.draw_line()

    #             # Daten speichern
    #             self.save_data()
    #         except ValueError:
    #             self.pixel_per_meter_label.config(text="Ungültige Eingabe für Meter.")

    # def load_image(self):
    #     self.image_path = filedialog.askopenfilename()
    #     if self.image_path:
    #         self.floorplan_image = ImageTk.PhotoImage(Image.open(self.image_path).resize((800, 600)))
    #         self.canvas.create_image(0, 0, anchor=tk.NW, image=self.floorplan_image)

    # def reset(self):
    #     self.points.clear()
    #     self.origin_point = None
    #     self.canvas.delete("all")
    #     self.load_image()

    # def enable_set_origin(self):
    #     self.canvas.bind("<Button-1>", self.set_origin)

    # def set_origin(self, event):
    #     self.origin_point = (event.x, event.y)
    #     self.canvas.create_oval(self.origin_point[0]-5, self.origin_point[1]-5, self.origin_point[0]+5, self.origin_point[1]+5, fill="green")

    # def save_data(self):
    #     data = {
    #         "points": self.points,
    #         "origin_point": self.origin_point,
    #         "meter_per_pixel": self.meter_per_pixel,
    #         "image_path": self.image_path
    #     }
    #     with open("calibration_data.pkl", "wb") as file:
    #         pickle.dump(data, file)

    # def load_saved_data(self):
    #     if os.path.exists("calibration_data.pkl"):
    #         with open("calibration_data.pkl", "rb") as file:
    #             data = pickle.load(file)
    #             self.points = data["points"]
    #             self.origin_point = data["origin_point"]
    #             self.meter_per_pixel = data["meter_per_pixel"]
    #             self.image_path = data["image_path"]

    #             # بارگذاری تصویر
    #             if self.image_path:
    #                 self.load_image()

    #             # نمایش نقاط و خط
    #             if self.points:
    #                 for point in self.points:
    #                     self.canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, fill="red")
                    
    #                 # اگر دو نقطه داریم، خط و اعداد را نمایش می‌دهیم
    #                 if len(self.points) == 2:
    #                     self.draw_line()

    #                     # محاسبه فاصله بین دو نقطه
    #                     p1, p2 = self.points
    #                     distance_pixels = math.sqrt((p2[0] - p1[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    #                     # اگر فاصله برحسب متر مشخص شده است، نمایش می‌دهیم
    #                     if self.meter_per_pixel is not None:
    #                         distance_meters = distance_pixels * self.meter_per_pixel
    #                         self.pixel_per_meter_label.config(text=f"Pixel pro Meter: {self.meter_per_pixel:.4f} m/px")

    #                         # نمایش فاصله به متر و پیکسل روی خط
    #                         text_item_meters = self.canvas.create_text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 - 15,
    #                                                                    text=f"Meter: {distance_meters:.2f} m", fill="black")
    #                         text_item_pixels = self.canvas.create_text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 15,
    #                                                                    text=f"Pixel: {distance_pixels:.2f} px", fill="black")
    #                         self.text_items.extend([text_item_meters, text_item_pixels])


class Calibration:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalibrierungs-Tool")
        self.root.configure(bg='#f0f0f0')

        # Canvas und Buttons erstellen
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.button_frame = tk.Frame(root, bg='#f0f0f0')
        self.button_frame.pack(side=tk.TOP, pady=10)

        self.upload_button = tk.Button(self.button_frame, text="Bodenplan hochladen", command=self.load_image)
        self.upload_button.pack(side=tk.LEFT, padx=10)

        self.calibrate_button = tk.Button(self.button_frame, text="Kalibrierung", command=self.start_calibration)
        self.calibrate_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.button_frame, text="Zurücksetzen", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Neue Schaltfläche für die Berechnung der relativen Koordinaten
        self.relative_button = tk.Button(self.button_frame, text="Koordinaten", command=self.start_relative_coordinates_calculation)
        self.relative_button.pack(side=tk.LEFT, padx=10)

        self.distance_entry_label = tk.Label(self.button_frame, text="Meter-Eingabe: ", bg='#f0f0f0')
        self.distance_entry_label.pack(side=tk.LEFT, padx=10)
        self.distance_entry = tk.Entry(self.button_frame)
        self.distance_entry.pack(side=tk.LEFT, padx=10)

        # Label für Pixel pro Meter hinzufügen
        self.pixel_per_meter_label = tk.Label(self.button_frame, text="Pixel pro Meter: N/A", bg='#f0f0f0')
        self.pixel_per_meter_label.pack(side=tk.LEFT, padx=10)

        # Variablen zur Speicherung der Referenzpunkte und berechneter Werte
        self.points = []
        self.origin_point = None
        self.meter_per_pixel = None
        self.text_items = []  # Text-Elemente zum Löschen speichern

        # Event zum Hinzufügen von Punkten
        self.canvas.bind("<Button-1>", self.add_point)

        # Bildvariablen
        self.floorplan_image = None
        self.image_path = None

        # Flags für die Berechnungsprozesse
        self.calibration_active = False
        self.relative_calculation_active = False

        # Daten beim Start laden
        self.load_saved_data()

    def add_point(self, event):
        x, y = event.x, event.y

        if self.calibration_active:
            if len(self.points) < 2:
                self.points.append((x, y))
                self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
                if len(self.points) == 2:
                    self.draw_line()

        elif self.relative_calculation_active:
            if self.origin_point is None:
                # Setzt نقطه مرجع
                self.origin_point = (x, y)
                self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="green")
                messagebox.showinfo("Nachricht", "Origin-Punkt gesetzt! Bitte wählen Sie nun den Punkt für die relativen Koordinaten.")
            else:
                
                relative_x = x - self.origin_point[0]
                relative_y = y - self.origin_point[1]
                self.points.append((relative_x, relative_y))
                self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
                self.display_relative_coordinates()
                self.relative_calculation_active = False
        else:
            messagebox.showinfo("Nachricht", "Wählen Sie zuerst eine Funktion: Kalibrierung oder relative Koordinaten.")

    def start_calibration(self):
        """Aktiviert den Kalibrierungsmodus"""
        self.calibration_active = True
        self.relative_calculation_active = False
        self.points.clear()
        self.canvas.delete("all")
        self.load_image()

        messagebox.showinfo("Nachricht", "Bitte wählen Sie zwei Punkte für die Kalibrierung.")

    def start_relative_coordinates_calculation(self):
        """Aktiviert den Modus für die Berechnung der relativen Koordinaten"""
        self.relative_calculation_active = True
        self.calibration_active = False
        messagebox.showinfo("Nachricht", "Bitte wählen Sie den Ursprungspunkt.")

    def display_relative_coordinates(self):
        """Zeigt die relativen Koordinaten des Punktes im Vergleich zum Ursprungspunkt an"""
        if self.origin_point and len(self.points) >= 1:
            last_point = self.points[-1]
            relative_x, relative_y = last_point[0], last_point[1]
            text = f"ΔX: {relative_x} px, ΔY: {relative_y} px"
            text_item = self.canvas.create_text(self.origin_point[0] + last_point[0] + 10,
                                                self.origin_point[1] + last_point[1] + 10,
                                                text=text, fill="blue")
            self.text_items.append(text_item)

    def draw_line(self):
        p1, p2 = self.points
        self.canvas.create_line(p1[0] + self.origin_point[0], p1[1] + self.origin_point[1],
                                p2[0] + self.origin_point[0], p2[1] + self.origin_point[1], fill="blue", width=2)

    def calibrate(self):
        if len(self.points) == 2:
            for item in self.text_items:
                self.canvas.delete(item)
            self.text_items.clear()

            p1, p2 = self.points
            distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p1[1] - p2[1]) ** 2)

            try:
                real_distance = float(self.distance_entry.get())
                self.meter_per_pixel = real_distance / distance
                self.pixel_per_meter_label.config(text=f"Pixel pro Meter: {self.meter_per_pixel:.4f} m/px")

                text_item_meters = self.canvas.create_text((p1[0] + p2[0]) / 2 + self.origin_point[0],
                                                           (p1[1] + p2[1]) / 2 + self.origin_point[1] + 15,
                                                           text=f"Meter: {real_distance:.2f} m", fill="black")
                text_item_pixels = self.canvas.create_text((p1[0] + p2[0]) / 2 + self.origin_point[0],
                                                           (p1[1] + p2[1]) / 2 + self.origin_point[1] + 30,
                                                           text=f"Pixel: {distance:.2f} px", fill="black")

                self.text_items.extend([text_item_meters, text_item_pixels])
                self.save_data()
            except ValueError:
                self.pixel_per_meter_label.config(text="Ungültige Eingabe für Meter.")

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

    def save_data(self):
        data = {
            "points": self.points,
            "origin_point": self.origin_point,
            "meter_per_pixel": self.meter_per_pixel,
            "image_path": self.image_path
        }
        with open("calibration_data.pkl", "wb") as file:
            pickle.dump(data, file)

    def load_saved_data(self):
        if os.path.exists("calibration_data.pkl"):
            with open("calibration_data.pkl", "rb") as file:
                data = pickle.load(file)
                self.points = data.get("points", [])
                self.origin_point = data.get("origin_point", None)
                self.meter_per_pixel = data.get("meter_per_pixel", None)
                self.image_path = data.get("image_path", None)

            if self.image_path:
                self.floorplan_image = ImageTk.PhotoImage(Image.open(self.image_path).resize((800, 600)))
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.floorplan_image)

            if self.meter_per_pixel is not None:
                self.pixel_per_meter_label.config(text=f"Pixel pro Meter: {self.meter_per_pixel:.4f} m/px")




class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WLAN Mess- und Kalibrierungs-App")
        self.root.geometry("600x400")  

    
        self.button_frame = tk.Frame(root, bg='lightgrey', padx=20, pady=20)  
        self.button_frame.pack(side=tk.TOP, pady=130)

        
        self.signal_button = tk.Button(self.button_frame, text="Signal messen", command=self.open_signal_measurement, 
                                       width=15, height=2, bg='blue', fg='white', font=('Arial', 12))
        self.signal_button.pack(side=tk.LEFT, padx=10)

        self.calibration_button = tk.Button(self.button_frame, text="Kalibrierung", command=self.open_calibration, 
                                            width=15, height=2, bg='green', fg='white', font=('Arial', 12))
        self.calibration_button.pack(side=tk.LEFT, padx=10)

    def open_signal_measurement(self):
        self.new_window = tk.Toplevel(self.root)
        SignalMeasurement(self.new_window)

    def open_calibration(self):
        self.new_window = tk.Toplevel(self.root)
        Calibration(self.new_window)



if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
