import tkinter as tk
from tkinter import ttk

def style_buttons(root):
    # Style für Buttons definieren
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10, relief="raised",
                    background="#4CAF50", foreground="#000000")
    style.map("TButton",
              background=[("pressed", "#45a049"), ("active", "#000000")])

    # Erstelle ein Frame für die Buttons
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=20)

    return button_frame

def create_buttons(button_frame, load_command, scan_command, end_command):
    # Buttons erstellen
    load_button = ttk.Button(button_frame, text="Load Floorplan", command=load_command)
    load_button.pack(side=tk.LEFT, padx=10)

    scan_button = ttk.Button(button_frame, text="Start WiFi Scan", command=scan_command)
    scan_button.pack(side=tk.LEFT, padx=10)

    end_button = ttk.Button(button_frame, text="End/Save", command=end_command)
    end_button.pack(side=tk.LEFT, padx=10)

def create_canvas(root):
    # Canvas erstellen
    canvas = tk.Canvas(root, width=800, height=600, bg='white')
    canvas.pack()
    return canvas
