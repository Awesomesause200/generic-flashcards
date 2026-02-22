from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton

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
        CTkLabel(self, text="Settings Menu", font=("Arial", 20)).pack(expand=True)

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
