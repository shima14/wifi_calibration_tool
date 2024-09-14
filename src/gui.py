import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk
from floorplan import Floorplan
from wifi_scanner import scan_wifi
from heatmap_generator import generate_heatmap

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Survey App")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.load_button = tk.Button(root, text="Load Floorplan", command=self.load_floorplan)
        self.load_button.pack()

        self.scan_button = tk.Button(root, text="Start WiFi Scan", command=self.start_wifi_scan)
        self.scan_button.pack()

        self.points = []  # Liste für die Koordinaten der Klicks

    def load_floorplan(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            print(f"Lade Bild von: {file_path}")  # Debug-Ausgabe
        try:    
            self.floorplan = Floorplan(file_path)
            self.floorplan_image = self.floorplan.resize_image(800, 600)
            self.floorplan_image = ImageTk.PhotoImage(self.floorplan_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.floorplan_image)
            self.canvas.bind("<Button-1>", self.set_point)  # Klick-Event binden
        except Exception as e:
            print(f"Fehler beim Laden des Bildes: {e}")
        

    def set_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))  # Koordinaten speichern
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")  # Punkt auf dem Canvas markieren

    def start_wifi_scan(self):
        networks = scan_wifi()  # WLAN-Scan durchführen
        signal_strengths = [network['Signal Strength'] for network in networks]
        
        # Überprüfe, ob die Anzahl der Punkte und Signalstärken übereinstimmt
        if len(self.points) == len(signal_strengths):
            generate_heatmap(self.floorplan.path, self.points, signal_strengths)
        else:
            print("Die Anzahl der Punkte und Signalstärken stimmt nicht überein.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
