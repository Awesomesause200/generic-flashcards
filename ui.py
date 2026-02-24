from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, set_appearance_mode, CTkOptionMenu, CTkCanvas, CTkSwitch
import os
import json

# Following custom frames for a more modular framework
class SidebarFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configure the baseline grid
        self.grid_rowconfigure(4, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        # Widgets
        self.title_label = CTkLabel(self, text="Menu", font=("Arial", 18, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Main Dashboard
        self.btn_1 = CTkButton(self, text="Dashboard", command=lambda: self.change_page("Dashboard", self.btn_1))
        self.btn_1.grid(row=1, column=0, padx=20, pady=10)

        # Card Editor
        self.btn_2 = CTkButton(self, text="Card Group Editor", command=lambda: self.change_page("CardEditor", self.btn_2))
        self.btn_2.grid(row=2, column=0, padx=20, pady=10)

        # Settings
        self.btn_3 = CTkButton(self, text="Settings", command=lambda: self.change_page("Settings", self.btn_3))
        self.btn_3.grid(row=3, column=0, padx=20, pady=10)

        # Row 4 is empty but has weight=1, so it acts as a flexible spacer!
        
        # Exit button
        self.exit_button = CTkButton(self, text="Exit Program", fg_color="red", command=self.master.destroy)
        self.exit_button.grid(row=5, column=0, padx=20, pady=20)

        # Set default page to Dashboard
        self.change_page("Dashboard", self.btn_1)

    # Helper functions to stylize changing pages (button color changes)
    def change_page(self, page_name, clicked_button):
        for widget in self.winfo_children():
            if isinstance(widget, CTkButton) and widget != self.exit_button:
                if widget == clicked_button:
                    widget.configure(fg_color=("#e0a838", "#d19c34"))
                else:
                    widget.configure(fg_color=["#3B8ED0", "#1F6AA5"])

        # This calls the method in the App class
        self.master.show_frame(page_name)


# Below are placeholders for the various pages we will be making
class DashboardFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        CTkLabel(self, text="Dashboard View", font=("Arial", 20)).pack(expand=True)

class CardEditor(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        CTkLabel(self, text="Card Group Editor View", font=("Arial", 20)).pack(expand=True)

class SettingsFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.settings_path = "settings.json"
        
        # 1. Load/Initialize Settings Data
        # Default values as requested
        self.settings = {
            "appearance_mode": "System",
            "top_n": 3,
            "bottom_n": 3,
            "force_eval": False
        }
        self.load_settings_from_json()

        # 2. UI Header
        CTkLabel(self, text="Settings Menu", font=("Arial", 24, "bold")).pack(pady=20)

        # 3. Theme Selection
        CTkLabel(self, text="Appearance Mode", font=("Arial", 14)).pack(pady=(10, 0))
        self.theme_option = CTkOptionMenu(
            self, 
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode
        )
        self.theme_option.set(self.settings["appearance_mode"])
        self.theme_option.pack(pady=10)

        # 4. Color Indicators (Visual Feedback)
        self.color_container = CTkFrame(self, fg_color="transparent")
        self.color_container.pack(pady=10)
        self.draw_color_indicators()

        # 5. Dashboard N-Values (N-Value Steppers)
        self.create_stepper_ui("Top N Values", "top_n")
        self.create_stepper_ui("Bottom N Values", "bottom_n")

        # 6. Evaluation Toggle (Targeting self.master.force_user_evaluation)
        self.eval_switch = CTkSwitch(
            self, text="Force User Evaluation", 
            command=self.toggle_evaluation
        )
        if self.settings["force_eval"]: 
            self.eval_switch.select()
        self.eval_switch.pack(pady=20)

        # 7. Persistence
        self.save_btn = CTkButton(
            self, text="Save to Disk", 
            fg_color="#2cc985", hover_color="#23a06a",
            command=self.save_settings_to_json
        )
        self.save_btn.pack(pady=(20, 10))

    # --- Logic Methods ---

    def draw_color_indicators(self):
        """Creates the primary, secondary, and alert color circles."""
        palette = {"Primary": "#1f538d", "Secondary": "#2cc985", "Alert": "#e74c3c"}
        for label, color in palette.items():
            frame = CTkFrame(self.color_container, fg_color="transparent")
            frame.pack(side="left", padx=15)
            
            # Using a small canvas for the 'circle' look
            canvas = CTkCanvas(frame, width=20, height=20, highlightthickness=0, 
                                   bg=self._apply_appearance_mode(self.cget("fg_color")))
            canvas.create_oval(2, 2, 18, 18, fill=color, outline="")
            canvas.pack()
            CTkLabel(frame, text=label, font=("Arial", 11)).pack()

    def create_stepper_ui(self, label_text, key):
        """Helper to build the row UI for N-value adjustments."""
        row = CTkFrame(self)
        row.pack(pady=5, fill="x", padx=60)
        
        CTkLabel(row, text=label_text).pack(side="left", padx=10)
        
        # Display label for the number
        val_label = CTkLabel(row, text=str(self.settings[key]), font=("Arial", 12, "bold"))
        
        # Buttons call the shared update_n_value method
        CTkButton(row, text="+", width=30, command=lambda: self.update_n_value(key, 1, val_label)).pack(side="right", padx=5)
        val_label.pack(side="right", padx=5)
        CTkButton(row, text="-", width=30, command=lambda: self.update_n_value(key, -1, val_label)).pack(side="right", padx=5)

    def update_n_value(self, key, delta, label_widget):
        """Standalone function to handle increment/decrement and master update."""
        new_val = max(1, self.settings[key] + delta) # Prevent values below 1
        self.settings[key] = new_val
        label_widget.configure(text=str(new_val))
        
        # Update the dashboard attributes on the master
        if key == "top_n":
            self.master.dashboard.top_n_values = new_val
        else:
            self.master.dashboard.bottom_n_values = new_val

    def change_appearance_mode(self, new_mode):
        self.settings["appearance_mode"] = new_mode
        set_appearance_mode(new_mode)

    def toggle_evaluation(self):
        is_on = self.eval_switch.get() == 1
        self.settings["force_eval"] = is_on
        self.master.force_user_evaluation = is_on

    # --- JSON Handling ---

    def save_settings_to_json(self):
        with open(self.settings_path, "w") as f:
            json.dump(self.settings, f, indent=4)
        print(f"Settings archived to {self.settings_path}")

    def load_settings_from_json(self):
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r") as f:
                    saved_data = json.load(f)
                    self.settings.update(saved_data)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Sync the app state with loaded values immediately
        set_appearance_mode(self.settings["appearance_mode"])
        # Assuming these exist on your master setup
        if hasattr(self.master, 'dashboard'):
            self.master.dashboard.top_n_values = self.settings["top_n"]
            self.master.dashboard.bottom_n_values = self.settings["bottom_n"]
        self.master.force_user_evaluation = self.settings["force_eval"]

# Primary UI class
class App(CTk):
    def __init__(self):
        super().__init__()

        self.title("Flashcard Application")
        self.geometry("1280x720")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Save a dictionary of sub-frames we're making for the main content
        self.frames = {}

        # Create the container for this page
        self.container = CTkFrame(self)
        self.container.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create the frame page (will place all frames on top of each other)
        for F in (DashboardFrame, CardEditor, SettingsFrame):
            page_name = F.__name__.replace("Frame", "")
            frame = F(self.container)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Create sidebar now that we have all of the frames defined
        self.sidebar = SidebarFrame(master=self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Show the default frame
        self.show_frame("Dashboard")

    # Helper functions
    def show_frame(self, page_name):
        """Brings the requested frame to the front"""
        frame = self.frames[page_name]
        frame.tkraise()
