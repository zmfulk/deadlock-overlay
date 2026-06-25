import customtkinter as ctk
import json
import os

# Set UI Theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class OverlayController(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Deadlock Overlay Controller")
        self.geometry("450x760") # Slightly taller to accommodate the new buttons
        self.resizable(False, False)

        # File path for JSON data
        self.json_path = "data.json"

        # --- WEEKLY RECORD SECTION ---
        self.record_frame = ctk.CTkFrame(self)
        self.record_frame.pack(padx=20, pady=15, fill="x")
        
        self.record_label = ctk.CTkLabel(self.record_frame, text="Weekly Record", font=("Arial", 16, "bold"))
        self.record_label.grid(row=0, column=0, columnspan=2, pady=5, padx=10, sticky="w")

        # Record Headers
        self.wins_label = ctk.CTkLabel(self.record_frame, text="Wins", font=("Arial", 12, "bold"))
        self.wins_label.grid(row=1, column=0, padx=10, pady=(5, 0))
        
        self.losses_label = ctk.CTkLabel(self.record_frame, text="Losses", font=("Arial", 12, "bold"))
        self.losses_label.grid(row=1, column=1, padx=10, pady=(5, 0))

        # Record Inputs
        self.wins_entry = ctk.CTkEntry(self.record_frame, placeholder_text="0", width=180)
        self.wins_entry.grid(row=2, column=0, padx=10, pady=(0, 10))
        
        self.losses_entry = ctk.CTkEntry(self.record_frame, placeholder_text="0", width=180)
        self.losses_entry.grid(row=2, column=1, padx=10, pady=(0, 10))

        # --- CHARACTER STATS SECTION ---
        self.chars_frame = ctk.CTkFrame(self)
        self.chars_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.chars_label = ctk.CTkLabel(self.chars_frame, text="Character Stats", font=("Arial", 16, "bold"))
        self.chars_label.pack(pady=10, padx=10, anchor="w")

        # Column Headers
        header_frame = ctk.CTkFrame(self.chars_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(0, 5))

        char_header = ctk.CTkLabel(header_frame, text="Character", font=("Arial", 12, "bold"), width=150, anchor="w")
        char_header.grid(row=0, column=0, padx=5)

        games_header = ctk.CTkLabel(header_frame, text="Games Played", font=("Arial", 12, "bold"), width=100, anchor="center")
        games_header.grid(row=0, column=1, padx=5)

        wins_header = ctk.CTkLabel(header_frame, text="Games Won", font=("Arial", 12, "bold"), width=100, anchor="center")
        wins_header.grid(row=0, column=2, padx=5)

        # Complete Deadlock Character List
        self.character_list = [
            "Abrams", "Apollo", "Bebop", "Billy", "Calico", "Celeste", 
            "The Doorman", "Drifter", "Dynamo", "Graves", "Grey Talon", 
            "Haze", "Holliday", "Infernus", "Ivy", "Kelvin", "Lady Geist", 
            "Lash", "McGinnis", "Mina", "Mirage", "Mo & Krill", "Paige", 
            "Paradox", "Pocket", "Rem", "Seven", "Shiv", "Silver", 
            "Sinclair", "Venator", "Victor", "Vindicta", "Viscous", 
            "Vyper", "Warden", "Wraith", "Yamato"
        ]
        
        # Container specifically for the dynamic rows
        self.rows_frame = ctk.CTkFrame(self.chars_frame, fg_color="transparent")
        self.rows_frame.pack(fill="x", pady=0)

        self.char_rows = []
        
        # Initialize with 3 default rows
        for _ in range(3):
            self.add_char_row()

        # Add / Remove Buttons Container
        self.action_btn_frame = ctk.CTkFrame(self.chars_frame, fg_color="transparent")
        self.action_btn_frame.pack(pady=10)

        self.add_btn = ctk.CTkButton(self.action_btn_frame, text="+ Add Character", width=120, command=self.add_char_row)
        self.add_btn.grid(row=0, column=0, padx=10)

        self.remove_btn = ctk.CTkButton(self.action_btn_frame, text="- Remove Character", width=120, fg_color="#b91c1c", hover_color="#991b1b", command=self.remove_char_row)
        self.remove_btn.grid(row=0, column=1, padx=10)

        # --- SETTINGS SECTION ---
        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame.pack(padx=20, pady=(10, 0), fill="x")

        self.show_leaderboard_var = ctk.BooleanVar(value=True) 
        self.leaderboard_toggle = ctk.CTkCheckBox(
            self.settings_frame, 
            text="Show Top Characters Leaderboard", 
            variable=self.show_leaderboard_var,
            font=("Arial", 13, "bold")
        )
        self.leaderboard_toggle.pack(anchor="w", padx=10)

        # --- SAVE BUTTON ---
        self.save_btn = ctk.CTkButton(self, text="Update Overlay", command=self.save_data, height=40, font=("Arial", 14, "bold"))
        self.save_btn.pack(padx=20, pady=15, fill="x")

        # Load existing data (will override the 3 default rows if data exists)
        self.load_existing_data()

    def add_char_row(self, name_val=None, games_val="", wins_val=""):
        # Prevent adding an absurd number of rows that break the window height
        if len(self.char_rows) >= 7:
            return 

        row_frame = ctk.CTkFrame(self.rows_frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=10, pady=5)

        # Assign a different default character based on row number so they aren't all "Abrams"
        default_index = len(self.char_rows) % len(self.character_list)
        default_name = self.character_list[default_index]

        name_menu = ctk.CTkOptionMenu(row_frame, values=self.character_list, width=150)
        name_menu.set(name_val if name_val else default_name)
        name_menu.grid(row=0, column=0, padx=5)

        games_entry = ctk.CTkEntry(row_frame, placeholder_text="Games", width=100)
        if games_val: games_entry.insert(0, games_val)
        games_entry.grid(row=0, column=1, padx=5)

        char_wins_entry = ctk.CTkEntry(row_frame, placeholder_text="Wins", width=100)
        if wins_val: char_wins_entry.insert(0, wins_val)
        char_wins_entry.grid(row=0, column=2, padx=5)

        self.char_rows.append({
            "frame": row_frame, # Save the frame so we can destroy it later
            "name": name_menu,
            "games": games_entry,
            "wins": char_wins_entry
        })

    def remove_char_row(self):
        # Prevent removing all rows (keep at least 1)
        if len(self.char_rows) > 1:
            last_row = self.char_rows.pop()
            last_row["frame"].destroy() # Deletes the row from the GUI

    def save_data(self):
        data = {
            "settings": {
                "show_leaderboard": self.show_leaderboard_var.get()
            },
            "weekly_record": {
                "wins": self.wins_entry.get() or "0",
                "losses": self.losses_entry.get() or "0"
            },
            "characters": []
        }

        for row in self.char_rows:
            games_str = row["games"].get() or "0"
            wins_str = row["wins"].get() or "0"
            
            try:
                games_num = int(games_str)
                wins_num = int(wins_str)
            except ValueError:
                games_num = 0
                wins_num = 0

            if games_num > 0:
                win_percentage = round((wins_num / games_num) * 100)
                winrate_str = f"{win_percentage}%"
            else:
                winrate_str = "0%"

            data["characters"].append({
                "name": row["name"].get(),
                "games": games_str,
                "wins": wins_str,       
                "winrate": winrate_str 
            })

        with open(self.json_path, "w") as f:
            json.dump(data, f, indent=4)
        
        print("Overlay data successfully updated!")

    def load_existing_data(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    data = json.load(f)
                
                show_board = data.get("settings", {}).get("show_leaderboard", True)
                self.show_leaderboard_var.set(show_board)

                self.wins_entry.insert(0, data["weekly_record"]["wins"])
                self.losses_entry.insert(0, data["weekly_record"]["losses"])

                loaded_chars = data.get("characters", [])
                
                # If there are characters saved in the JSON, overwrite the defaults
                if loaded_chars:
                    # Clear the 3 default rows first
                    while self.char_rows:
                        self.char_rows.pop()["frame"].destroy()
                    
                    # Rebuild rows based on exact JSON data
                    for char_data in loaded_chars:
                        self.add_char_row(
                            name_val=char_data["name"],
                            games_val=char_data["games"],
                            wins_val=char_data.get("wins", "")
                        )

            except Exception as e:
                print(f"Error loading existing JSON: {e}")

if __name__ == "__main__":
    app = OverlayController()
    app.mainloop()