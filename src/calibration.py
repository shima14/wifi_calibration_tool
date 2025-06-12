import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import math

import wifi_scan  # Assuming the existence of the wifi_scan module


class Calibration:
    def __init__(self, root, update_pixel_per_meter_callback):
        self.root = root
        self.root.title("Calibration Tool")
        self.root.configure(bg='#f0f0f0')

        self.update_pixel_per_meter_callback = update_pixel_per_meter_callback

        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.button_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.button_frame.pack(side=tk.TOP, pady=10)

        self.upload_button = tk.Button(
            self.button_frame, text="Upload Floorplan", command=self.load_image)
        self.upload_button.pack(side=tk.LEFT, padx=10)

        self.set_origin_button = tk.Button(
            self.button_frame, text="Set Origin Point", command=self.enable_set_origin)
        self.set_origin_button.pack(side=tk.LEFT, padx=10)

        self.set_point_b_button = tk.Button(
            self.button_frame, text="Set Point B", command=self.enable_set_point_b, state=tk.DISABLED)
        self.set_point_b_button.pack(side=tk.LEFT, padx=10)

        self.distance_label = tk.Label(
            self.button_frame, text="Real Distance (meters):", bg='#f0f0f0')
        self.distance_label.pack(side=tk.LEFT, padx=5)

        self.distance_entry = tk.Entry(self.button_frame, width=7)
        self.distance_entry.pack(side=tk.LEFT, padx=5)

        self.calibrate_button = tk.Button(
            self.button_frame, text="Calibrate", command=self.calibrate, state=tk.DISABLED)
        self.calibrate_button.pack(side=tk.LEFT, padx=10)

        self.wifi_scan_button = tk.Button(
            self.button_frame, text="WiFi Scan", command=self.start_wifi_scan, state=tk.DISABLED)
        self.wifi_scan_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(
            self.button_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.result_label = tk.Label(
            self.root, text="", bg='#f0f0f0', font=("Arial", 12))
        self.result_label.pack(pady=5)

        self.wifi_window = None

        self.floorplan_image = None
        self.image_path = None
        self.origin_point = None
        self.point_b = None
        self.pixel_per_meter = None

        self.setting_origin = False
        self.setting_point_b = False
        self.setting_wifi_point = False

        # Now we have a list for WiFi points
        # Each point: {"x": ..., "y": ..., "real_x": ..., "real_y": ..., "wifi_data": [...]}
        self.wifi_points = []

        self.origin_oval = None
        self.origin_text = None
        self.point_b_oval = None
        self.point_b_text = None
        self.line = None
        self.distance_text_pixel = None

        # Tooltip for displaying WiFi info
        self.tooltip = None

        self.canvas.bind("<Button-1>", self.canvas_click)
        # Show tooltip on WiFi points
        self.canvas.bind("<Motion>", self.canvas_motion)

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            pil_img = Image.open(self.image_path).resize((800, 600))
            self.floorplan_image = ImageTk.PhotoImage(pil_img)
            self.canvas.delete("all")
            self.canvas.create_image(
                0, 0, anchor=tk.NW, image=self.floorplan_image)
            self.reset_vars()
            self.update_buttons()

    def enable_set_origin(self):
        if not self.floorplan_image:
            messagebox.showwarning(
                "Warning", "Please upload a floorplan first!")
            return
        self.setting_origin = True
        self.setting_point_b = False
        self.setting_wifi_point = False
        self.result_label.config(text="Click to set Origin point (green).")
        self.update_buttons()

    def enable_set_point_b(self):
        if not self.origin_point:
            messagebox.showwarning(
                "Warning", "Please set the Origin point first!")
            return
        self.setting_point_b = True
        self.setting_origin = False
        self.setting_wifi_point = False
        self.result_label.config(text="Click to set Point B (red).")
        self.update_buttons()

    def start_wifi_scan(self):
        if not self.pixel_per_meter:
            messagebox.showwarning("Warning", "Please calibrate first!")
            return
        self.wifi_data = wifi_scan.scan_wifi()
        if not self.wifi_data:
            messagebox.showinfo("Info", "No WiFi networks found.")
            return
        self.setting_wifi_point = True
        self.setting_origin = False
        self.setting_point_b = False
        self.result_label.config(text="Click on the position for WiFi scan.")
        self.update_buttons()

    def canvas_click(self, event):
        x, y = event.x, event.y
        if self.setting_origin:
            self.set_origin_point(x, y)
        elif self.setting_point_b:
            self.set_point_b(x, y)
        elif self.setting_wifi_point:
            self.set_wifi_point(x, y)

    def set_origin_point(self, x, y):
        self.origin_point = (x, y)
        if self.origin_oval:
            self.canvas.delete(self.origin_oval)
        if self.origin_text:
            self.canvas.delete(self.origin_text)
        self.origin_oval = self.canvas.create_oval(
            x-7, y-7, x+7, y+7, fill="green")
        self.origin_text = self.canvas.create_text(
            x + 15, y, text="Origin (0,0)", fill="green", anchor=tk.W, font=("Arial", 10, "bold"))
        self.setting_origin = False
        self.result_label.config(text="Origin point set. Now select Point B.")
        self.set_point_b_button.config(state=tk.NORMAL)
        self.update_buttons()

    def set_point_b(self, x, y):
        self.point_b = (x, y)
        if self.point_b_oval:
            self.canvas.delete(self.point_b_oval)
        if self.point_b_text:
            self.canvas.delete(self.point_b_text)
        if self.line:
            self.canvas.delete(self.line)
        if self.distance_text_pixel:
            self.canvas.delete(self.distance_text_pixel)
        ox, oy = self.origin_point
        self.point_b_oval = self.canvas.create_oval(
            x-7, y-7, x+7, y+7, fill="red")
        self.point_b_text = self.canvas.create_text(
            x + 15, y, text=f"B ({x},{y})", fill="red", anchor=tk.W, font=("Arial", 10, "bold"))
        self.line = self.canvas.create_line(ox, oy, x, y, fill="blue", width=2)
        dist_pixel = math.sqrt((x - ox) ** 2 + (y - oy) ** 2)
        mid_x, mid_y = (ox + x) / 2, (oy + y) / 2
        self.distance_text_pixel = self.canvas.create_text(
            mid_x, mid_y - 15, text=f"Pixel Distance: {dist_pixel:.2f}px", fill="blue", font=("Arial", 10, "italic"))
        self.setting_point_b = False
        self.calibrate_button.config(state=tk.NORMAL)
        self.result_label.config(
            text="Point B set. Enter real distance and calibrate.")
        self.update_buttons()

    def set_wifi_point(self, x, y):
        real_x, real_y = self.convert_pixel_to_real(x, y)
        # Save new WiFi point
        self.wifi_points.append({
            "x": x,
            "y": y,
            "real_x": real_x,
            "real_y": real_y,
            "wifi_data": self.wifi_data.copy()  # Copy WiFi scan data for this point
        })
        # Draw the point on the Canvas
        self.canvas.create_oval(
            x-7, y-7, x+7, y+7, fill="purple", tags="wifi_point")
        self.canvas.create_text(x + 15, y, text=f"WiFi Point\n({real_x:.2f},{real_y:.2f})m",
                                fill="purple", anchor=tk.W, font=("Arial", 10, "bold"), tags="wifi_point")

        self.show_wifi_results(real_x, real_y, self.wifi_data)

        self.setting_wifi_point = False
        self.result_label.config(text="WiFi scan point set.")
        self.update_buttons()

    def convert_pixel_to_real(self, x, y):
        ox, oy = self.origin_point
        dx = (x - ox) / self.pixel_per_meter
        dy = (y - oy) / self.pixel_per_meter
        return dx, dy

    def calibrate(self):
        try:
            real_distance = float(self.distance_entry.get())
            ox, oy = self.origin_point
            bx, by = self.point_b
            dist_pixel = math.sqrt((bx - ox) ** 2 + (by - oy) ** 2)
            self.pixel_per_meter = dist_pixel / real_distance
            self.result_label.config(
                text=f"Calibration successful! Pixels per meter: {self.pixel_per_meter:.3f}")
            self.calibrate_button.config(state=tk.DISABLED)
            self.wifi_scan_button.config(state=tk.NORMAL)
            self.update_pixel_per_meter_callback(self.pixel_per_meter)
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid real distance!")

    def show_wifi_results(self, real_x, real_y, wifi_data):
        if self.wifi_window:
            self.wifi_window.destroy()

        self.wifi_window = tk.Toplevel(self.root)
        self.wifi_window.title("WiFi Scan Results")
        self.wifi_window.geometry("300x400")

        label = tk.Label(self.wifi_window, text=f"WiFi Point at ({real_x:.2f}, {real_y:.2f}) meters", font=(
            "Arial", 12, "bold"))
        label.pack(pady=5)

        for net in wifi_data:
            ssid = net.get("SSID", "Unknown")
            signal = net.get("Signal", "N/A")
            info = f"SSID: {ssid}, Signal Strength: {signal} dBm"
            net_label = tk.Label(self.wifi_window, text=info, anchor="w")
            net_label.pack(fill='x', padx=10, pady=2)

    def reset_vars(self):
        self.origin_point = None
        self.point_b = None
        self.pixel_per_meter = None
        self.wifi_points.clear()

        self.setting_origin = False
        self.setting_point_b = False
        self.setting_wifi_point = False

        self.canvas.delete("all")
        if self.floorplan_image:
            self.canvas.create_image(
                0, 0, anchor=tk.NW, image=self.floorplan_image)

        # Delete previous shapes
        if self.origin_oval:
            self.canvas.delete(self.origin_oval)
        if self.origin_text:
            self.canvas.delete(self.origin_text)
        if self.point_b_oval:
            self.canvas.delete(self.point_b_oval)
        if self.point_b_text:
            self.canvas.delete(self.point_b_text)
        if self.line:
            self.canvas.delete(self.line)
        if self.distance_text_pixel:
            self.canvas.delete(self.distance_text_pixel)
        self.origin_oval = self.origin_text = None
        self.point_b_oval = self.point_b_text = None
        self.line = None
        self.distance_text_pixel = None

        self.calibrate_button.config(state=tk.DISABLED)
        self.set_point_b_button.config(state=tk.DISABLED)
        self.wifi_scan_button.config(state=tk.DISABLED)

        self.result_label.config(text="")

        if self.wifi_window:
            self.wifi_window.destroy()
            self.wifi_window = None

        self.update_buttons()

    def reset(self):
        self.reset_vars()

    def update_buttons(self):
        # Only update button states based on current situation
        self.set_origin_button.config(
            state=tk.NORMAL if not self.origin_point else tk.DISABLED)
        self.set_point_b_button.config(
            state=tk.NORMAL if self.origin_point and not self.point_b else tk.DISABLED)
        self.calibrate_button.config(
            state=tk.NORMAL if self.origin_point and self.point_b and not self.pixel_per_meter else tk.DISABLED)
        self.wifi_scan_button.config(
            state=tk.NORMAL if self.pixel_per_meter else tk.DISABLED)

    def canvas_motion(self, event):
        # Show tooltip if mouse is over a WiFi point
        x, y = event.x, event.y
        radius = 7
        found_point = None
        for pt in self.wifi_points:
            px, py = pt["x"], pt["y"]
            if (px - radius) <= x <= (px + radius) and (py - radius) <= y <= (py + radius):
                found_point = pt
                break

        if found_point:
            self.show_tooltip(event.x_root, event.y_root, found_point)
        else:
            self.hide_tooltip()

    def show_tooltip(self, x_root, y_root, point):
        text_lines = [
            f"Position: ({point['real_x']:.2f}m, {point['real_y']:.2f}m)"]
        for net in point["wifi_data"]:
            ssid = net.get("SSID", "Unknown")
            signal = net.get("Signal", "N/A")
            text_lines.append(f"{ssid}: {signal} dBm")
        text = "\n".join(text_lines)

        if self.tooltip is None:
            self.tooltip = tk.Toplevel(self.root)
            self.tooltip.wm_overrideredirect(True)
            label = tk.Label(self.tooltip, text=text, justify=tk.LEFT,
                             background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                             font=("Arial", 10))
            label.pack(ipadx=1)

        self.tooltip.wm_geometry(f"+{x_root + 10}+{y_root + 10}")

        # Update tooltip text
        for widget in self.tooltip.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(text=text)

    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


def update_pixel_per_meter(pixels):
    print(f"Updated pixels per meter: {pixels}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Calibration(root, update_pixel_per_meter)
    root.mainloop()
