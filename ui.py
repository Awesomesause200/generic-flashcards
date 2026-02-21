from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton

# Following custom frames for a more modular framework
class App(CTk):
    def __init__(self):
        super().__init__()

        self.title("Grid Configuration Demo")
        self.geometry("600x400")

        # 1. Configure the main window's grid
        # We want the sidebar (Col 0) to be fixed, and the content (Col 1) to expand.
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. Create and place the Sidebar Frame
        self.sidebar = SidebarFrame(master=self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # 3. Create a simple "Main Content" label
        self.label = CTkLabel(self, text="Main Content Area (Expands)", font=("Arial", 20))
        self.label.grid(row=0, column=1, sticky="nsew")

class SidebarFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # --- GRID CONFIGURATION INSIDE THE FRAME ---
        # We want the buttons to stay at the top, but let an empty middle row 
        # (Row 2) expand to push the "Logout" button to the bottom.
        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure(0, weight=1) # Buttons fill the width

        # Widgets
        self.title_label = CTkLabel(self, text="Menu", font=("Arial", 18, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        self.btn_1 = CTkButton(self, text="Dashboard")
        self.btn_1.grid(row=1, column=0, padx=20, pady=10)

        # Row 2 is empty but has weight=1, so it acts as a flexible spacer!
        
        self.btn_logout = CTkButton(self, text="Logout", fg_color="red", command=lambda: rand("NOT WHATEVER BRO!!!!"))
        self.btn_logout.grid(row=3, column=0, padx=20, pady=20)

def rand(msg: str = "WHATEVER BRO") -> None:
    print(msg)
    return None
