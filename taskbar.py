import tkinter as tk
from tkinter import messagebox
import json
import os

# Default settings
DEFAULT_SETTINGS = {
    "text_size": 12,
    "text_color": "white",
    "text_font": "Arial",
    "bg_color": "#003399",
    "taskbar_width": 800,
    "taskbar_height": 60,
    "corner_radius": 10,
    "position": "bottom",  # Options: top, bottom, left, right
    "orientation": "horizontal"  # Options: horizontal, vertical
}

# File path for settings
SETTINGS_FILE = 'taskbar settings.txt'

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            return json.load(file)
    else:
        return DEFAULT_SETTINGS

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file, indent=4)

class XPTaskbarApp:
    def __init__(self, root):
        self.settings = load_settings()
        self.root = root
        self.apply_settings()

        # Create the start button
        self.start_button = tk.Button(
            root,
            text="Start",
            command=self.open_start_menu,
            bg=self.settings['bg_color'],
            fg=self.settings['text_color'],
            font=(self.settings['text_font'], self.settings['text_size']),
            relief='flat'
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Create system tray icons
        self.system_tray_frame = tk.Frame(
            root,
            bg=self.settings['bg_color']
        )
        self.system_tray_frame.pack(side=tk.RIGHT, padx=5)

        # Add dummy system tray icons
        self.create_system_tray_icon("A")
        self.create_system_tray_icon("B")

        # Create application buttons
        self.apps_frame = tk.Frame(
            root,
            bg=self.settings['bg_color']
        )
        self.apps_frame.pack(side=tk.LEFT, padx=5)

        self.create_app_button("My Computer")
        self.create_app_button("Recycle Bin")

        # Create a settings button to change settings
        self.settings_button = tk.Button(
            root,
            text="Settings",
            command=self.open_settings_menu,
            bg=self.settings['bg_color'],
            fg=self.settings['text_color'],
            font=(self.settings['text_font'], self.settings['text_size']),
            relief='flat'
        )
        self.settings_button.pack(side=tk.RIGHT, padx=5)

    def apply_settings(self):
        self.root.configure(bg=self.settings['bg_color'])
        if self.settings['position'] == 'top':
            self.root.geometry(f"{self.settings['taskbar_width']}x{self.settings['taskbar_height']}+0+0")
        elif self.settings['position'] == 'bottom':
            self.root.geometry(f"{self.settings['taskbar_width']}x{self.settings['taskbar_height']}+0+{self.root.winfo_screenheight() - self.settings['taskbar_height']}")
        elif self.settings['position'] == 'left':
            self.root.geometry(f"{self.settings['taskbar_height']}x{self.settings['taskbar_width']}+0+0")
        elif self.settings['position'] == 'right':
            self.root.geometry(f"{self.settings['taskbar_height']}x{self.settings['taskbar_width']}+{self.root.winfo_screenwidth() - self.settings['taskbar_height']}+0")

        if self.settings['orientation'] == 'vertical':
            self.start_button.pack(side=tk.TOP, padx=5)
            self.system_tray_frame.pack(side=tk.LEFT, padx=5)
            self.apps_frame.pack(side=tk.LEFT, padx=5)
        else:
            self.start_button.pack(side=tk.LEFT, padx=5)
            self.system_tray_frame.pack(side=tk.RIGHT, padx=5)
            self.apps_frame.pack(side=tk.LEFT, padx=5)

    def open_start_menu(self):
        messagebox.showinfo("Start Menu", "This is where the start menu would appear.")

    def create_system_tray_icon(self, label):
        icon_button = tk.Button(
            self.system_tray_frame,
            text=label,
            bg=self.settings['bg_color'],
            fg=self.settings['text_color'],
            font=(self.settings['text_font'], self.settings['text_size']),
            relief='flat'
        )
        icon_button.pack(side=tk.LEFT, padx=2)

    def create_app_button(self, app_name):
        app_button = tk.Button(
            self.apps_frame,
            text=app_name,
            bg=self.settings['bg_color'],
            fg=self.settings['text_color'],
            font=(self.settings['text_font'], self.settings['text_size']),
            relief='flat'
        )
        app_button.pack(side=tk.LEFT, padx=2)

    def open_settings_menu(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        
        # Font size
        tk.Label(settings_window, text="Text Size:").pack(pady=5)
        size_entry = tk.Entry(settings_window)
        size_entry.insert(0, str(self.settings['text_size']))
        size_entry.pack(pady=5)
        
        # Text color
        tk.Label(settings_window, text="Text Color:").pack(pady=5)
        color_entry = tk.Entry(settings_window)
        color_entry.insert(0, self.settings['text_color'])
        color_entry.pack(pady=5)
        
        # Font type
        tk.Label(settings_window, text="Text Font:").pack(pady=5)
        font_entry = tk.Entry(settings_window)
        font_entry.insert(0, self.settings['text_font'])
        font_entry.pack(pady=5)
        
        # Background color
        tk.Label(settings_window, text="Background Color:").pack(pady=5)
        bg_color_entry = tk.Entry(settings_window)
        bg_color_entry.insert(0, self.settings['bg_color'])
        bg_color_entry.pack(pady=5)
        
        # Width and Height
        tk.Label(settings_window, text="Taskbar Width:").pack(pady=5)
        width_entry = tk.Entry(settings_window)
        width_entry.insert(0, str(self.settings['taskbar_width']))
        width_entry.pack(pady=5)
        
        tk.Label(settings_window, text="Taskbar Height:").pack(pady=5)
        height_entry = tk.Entry(settings_window)
        height_entry.insert(0, str(self.settings['taskbar_height']))
        height_entry.pack(pady=5)

        # Position
        tk.Label(settings_window, text="Position:").pack(pady=5)
        position_var = tk.StringVar(value=self.settings['position'])
        position_menu = tk.OptionMenu(settings_window, position_var, "top", "bottom", "left", "right")
        position_menu.pack(pady=5)

        # Orientation
        tk.Label(settings_window, text="Orientation:").pack(pady=5)
        orientation_var = tk.StringVar(value=self.settings['orientation'])
        orientation_menu = tk.OptionMenu(settings_window, orientation_var, "horizontal", "vertical")
        orientation_menu.pack(pady=5)
        
        # Save Button
        save_button = tk.Button(settings_window, text="Save", command=lambda: self.save_settings(size_entry, color_entry, font_entry, bg_color_entry, width_entry, height_entry, position_var, orientation_var))
        save_button.pack(pady=10)

    def save_settings(self, size_entry, color_entry, font_entry, bg_color_entry, width_entry, height_entry, position_var, orientation_var):
        self.settings['text_size'] = int(size_entry.get())
        self.settings['text_color'] = color_entry.get()
        self.settings['text_font'] = font_entry.get()
        self.settings['bg_color'] = bg_color_entry.get()
        self.settings['taskbar_width'] = int(width_entry.get())
        self.settings['taskbar_height'] = int(height_entry.get())
        self.settings['position'] = position_var.get()
        self.settings['orientation'] = orientation_var.get()
        
        save_settings(self.settings)
        self.apply_settings()

        # Update buttons with new settings
        self.start_button.configure(
            bg=self.settings['bg_color'],
            fg=self.settings['text_color'],
            font=(self.settings['text_font'], self.settings['text_size'])
        )
        for widget in self.system_tray_frame.winfo_children():
            widget.configure(
                bg=self.settings['bg_color'],
                fg=self.settings['text_color'],
                font=(self.settings['text_font'], self.settings['text_size'])
            )
        for widget in self.apps_frame.winfo_children():
            widget.configure(
                bg=self.settings['bg_color'],
                fg=self.settings['text_color'],
                font=(self.settings['text_font'], self.settings['text_size'])
            )
        self.settings_button.configure(
            bg=self.settings['bg_color'],
            fg=self.settings['text_color'],
            font=(self.settings['text_font'], self.settings['text_size'])
        )

if __name__ == "__main
