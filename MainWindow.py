import os
import sys
import tkinter as tk
import json
from tkinter import ttk
from tkinter import filedialog
from Weapons_Tab import WTab
from ComboFinder import find_combos
from PopulateDMGSources import populate_dmg_sources


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Combo Finder")
        self.root.geometry("1280x800")

        # ---- AI Assisted Style Improvement
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TCombobox", selectbackground=self.style.lookup("TCombobox", "background"))
        self.style.configure("TCombobox", selectforeground=self.style.lookup("TCombobox", "foreground"))
        self.style.configure("TButton", focuscolor=self.style.lookup("TButton", "background"))
        self.style.layout("TNotebook.Tab", [
            ('Notebook.tab', {
                'sticky': 'nsew',
                'children': [
                    ('Notebook.padding', {
                        'side': 'top',
                        'sticky': 'nsew',
                        'children': [
                            ('Notebook.label', {'side': 'top', 'sticky': ''})
                        ]
                    })
                ]
            })
        ])

        # Standard-Schriftart für die gesamte App definieren
        default_font = ("Segoe UI", 10)
        self.root.option_add("*Font", default_font)

        # -----------------------------------
        # List of all the different sources of damage
        self.tab_list = []

        self.root.columnconfigure(0, weight=0, minsize=550)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Left side container for the input tabs
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Right side container for the calculation table
        self.right_frame = tk.Frame(root)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # ---- LEFT SIDE ----
        # Container for input elements, shifts elements to the top
        control_frame = tk.Frame(self.left_frame)
        control_frame.pack(pady=10, fill=tk.X)

        # NEW: Main horizontal container to hold Dropdowns (Left) and Health Input (Right) side-by-side
        selection_container = tk.Frame(self.left_frame)
        selection_container.pack(side=tk.TOP, fill=tk.X, anchor="nw", pady=(0, 10))

        # NEW: Left column container inside the main container for stacking the two dropdown rows
        dropdown_column = tk.Frame(selection_container)
        dropdown_column.pack(side=tk.LEFT, fill=tk.Y, anchor="nw")

        # Agent Selection Row (Now inside the dropdown column)
        agent_row_frame = tk.Frame(dropdown_column)
        agent_row_frame.pack(side=tk.TOP, fill=tk.X, anchor="nw", pady=(0, 0))

        agent_label = tk.Label(agent_row_frame, text="Select Agent:", font=("Arial", 10, "bold"), width=13, anchor="w")
        agent_label.pack(side=tk.LEFT, padx=(10, 5), pady=0)

        with open(resource_path("CommunityBalanceProfile.default.json"), "r", encoding="utf-8") as file:
            self.agent_data = json.load(file)
            print("File successfully loaded!")

        # Deceive Inc. Agents in your exact specified order
        self.agent_list = [
            "Custom",
            "Chavez", "Ace", "Squire", "Larcin",
            "Cavalière", "Madame Xiu", "Hans", "Yu-Mi",
            "Red", "Sasori", "Octo", "Vigil"
        ]

        self.gun_dict = {
            "Chavez": ("Sentinel", "Vigilante", "Duke"),
            "Ace": ("Queen of Diamond", "Jack of Diamond", "King of Diamond"),
            "Squire": ("Lance", "Trident", "Javelin"),
            "Larcin": ("Silence", "Cadence", "Violence"),
            "Cavalière": ("Dragoons", "Hydras", "Wyverns"),
            "Madame Xiu": ("Zhulong", "Longshen", "Xuanwu"),
            "Hans": ("The Hook", "The Jab", "The Uppercut"),
            "Yu-Mi": ("Tactical Slingshot", "Experimental Splitshot", "Heavy Longshot"),
            "Red": ("Heartbreaker", "Jack of Heart", "Lovebite"),
            "Sasori": ("Ame & Kage", "Hyo & Hanei", "Yuki & Hikari 0SE", "Yuki & Hikari 1SE", "Yuki & Hikari 2SE",
                       "Yuki & Hikari 3SE", "Yuki & Hikari 4SE"),
            "Octo": ("Pulpo", "Nautilo", "Calamari"),
            "Vigil": ("Caliburn", "Galantine", "Arondight"),
        }

        # Combobox for dropdown menu
        self.agent_dropdown = ttk.Combobox(agent_row_frame, values=self.agent_list, state="readonly")
        self.agent_dropdown.pack(side=tk.LEFT, padx=5, pady=0)
        self.agent_dropdown.set("Custom")

        # Separate Container for Weapon Row (Now inside the dropdown column)
        self.weapon_row_frame = tk.Frame(dropdown_column)
        # Note: We don't pack it here, it's handled dynamically in on_agent_selected

        # Label for weapon selection, hidden at start
        self.weapon_label = tk.Label(self.weapon_row_frame, text="Select Weapon:", font=("Arial", 10, "bold"), width=13,
                                     anchor="w")

        # SECOND DROPDOWN: Pre-created for weapons, but hidden at the start
        self.weapon_list = ["Weapon 1", "Weapon 2", "Weapon 3"]
        self.weapon_dropdown = ttk.Combobox(self.weapon_row_frame, values=self.weapon_list, state="readonly")

        # NEW: Right column container inside the main container for the Agent Health input
        health_frame = tk.Frame(selection_container)
        health_frame.pack(side=tk.LEFT, padx=(30, 10), anchor="nw")

        health_label = tk.Label(health_frame, text="Agent Health:", font=("Arial", 10, "bold"))
        health_label.pack(side=tk.LEFT, padx=(0, 5))

        # NEW: Tracking variable for live calculations with a default value of 100
        self.health_var = tk.StringVar(value="100")
        self.health_var.trace_add("write", lambda a, b, c: self.update_notebook())

        # NEW: Spinbox or Entry field for numbers (using Spinbox here to easily click up/down)
        self.health_spin = tk.Spinbox(
            health_frame,
            from_=1,
            to=500,
            width=6,
            textvariable=self.health_var
        )
        self.health_spin.pack(side=tk.LEFT)

        # Intercept spinbox arrow clicks for immediate updates
        self.health_spin.bind("<<Increment>>", lambda e: self.root.update_idletasks() or self.update_notebook())
        self.health_spin.bind("<<Decrement>>", lambda e: self.root.update_idletasks() or self.update_notebook())

        # Bind selection event to trigger template updates
        self.agent_dropdown.bind("<<ComboboxSelected>>", self.on_agent_selected)
        self.weapon_dropdown.bind("<<ComboboxSelected>>", self.on_weapon_selected)

        self.agent_dropdown.bind("<FocusOut>", lambda event: self.agent_dropdown.selection_clear())
        self.weapon_dropdown.bind("<FocusOut>", lambda event: self.weapon_dropdown.selection_clear())

        self.tab_list_frame = tk.Frame(self.left_frame)
        self.tab_list_frame.pack(pady=10, fill=tk.BOTH)

        # Adds empty damage tab at the start
        self.add_damage_tab()

        add_btn = ttk.Button(self.tab_list_frame, text="+ ADD DAMAGE INSTANCE", command=self.add_damage_tab)
        add_btn.pack(side=tk.BOTTOM, padx=10, pady=5, anchor="center")

        # Button to open the file dialog
        load_json_btn = ttk.Button(control_frame, text="Open Balance File", command=self.select_file_from_manager)
        load_json_btn.pack(side=tk.LEFT, padx=10, pady=(0, 10))
        # Label to display the selected file name
        self.file_name_label = tk.Label(
            control_frame, text="Default balancing file loaded", fg="gray", font=("Arial", 9)
        )
        self.file_name_label.pack(side=tk.LEFT, padx=5)

        # print_btn = ttk.Button(buttons_frame, text="Calculate", command=self.update_notebook)
        # print_btn.pack(side=tk.LEFT, padx=10)

        # ---- RIGHT SIDE ----
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        # Frames for each notebook tab
        # TODO: Backgrounds?
        self.base_tab = tk.Frame(self.notebook)
        self.gray_tab = tk.Frame(self.notebook)
        self.green_tab = tk.Frame(self.notebook)
        self.blue_tab = tk.Frame(self.notebook)
        self.purple_tab = tk.Frame(self.notebook)
        self.gold_tab = tk.Frame(self.notebook)
        self.unsurvivable_tab = tk.Frame(self.notebook)

        def create_tab_text(parent):
            txt = tk.Text(parent, font=("Consolas", 11), bg="#f8f9fa", relief="flat", padx=15, pady=15)
            txt.pack(fill=tk.BOTH, expand=True)
            txt.config(state="disabled")
            return txt

        self.base_text = create_tab_text(self.base_tab)
        self.gray_text = create_tab_text(self.gray_tab)
        self.green_text = create_tab_text(self.green_tab)
        self.blue_text = create_tab_text(self.blue_tab)
        self.purple_text = create_tab_text(self.purple_tab)
        self.gold_text = create_tab_text(self.gold_tab)
        self.unsurvivable_text = create_tab_text(self.unsurvivable_tab)

        self.notebook.add(self.base_tab, text="All Combos")
        self.notebook.add(self.gray_tab, text="Gray Health")
        self.notebook.add(self.green_tab, text="Green Health")
        self.notebook.add(self.blue_tab, text="Blue Health")
        self.notebook.add(self.purple_tab, text="Purple Health")
        self.notebook.add(self.gold_tab, text="Gold Health")
        self.notebook.add(self.unsurvivable_tab, text="Unsurvivable")

    def add_damage_tab(self, name="", value=None, max_occ=None):
        # Neues kombiniertes Widget erstellen
        new_tab = WTab(self.tab_list_frame, self.remove_damage_tab, self)
        new_tab.pack(pady=5, anchor="w", padx=10)
        new_tab.name_entry.insert(0, name)
        if value is not None:
            new_tab.dmg_spin.delete(0, tk.END)
            new_tab.dmg_spin.insert(0, str(value))
        if max_occ is not None:
            new_tab.max_occ_entry.insert(0, max_occ)

        # In der Liste registrieren
        self.tab_list.append(new_tab)

    def remove_damage_tab(self, tab):
        if tab in self.tab_list:
            self.tab_list.remove(tab)

    def update_notebook(self):
        if not any([t.is_valid() for t in self.tab_list]):
            return
        combos_text = ""
        gray_text = ""
        green_text = ""
        blue_text = ""
        purple_text = ""
        gold_text = ""
        unsurv_text = ""

        instances = []

        for tab in self.tab_list:
            dmg_inst_name = tab.name_entry.get().strip() or "Unnamed"

            try:
                dmg = int(tab.dmg_spin.get())
            except ValueError:
                dmg = 0

            try:
                max_occ = int(tab.max_occ_entry.get())
            except ValueError:
                max_occ = 0

            if not tab.is_valid():
                continue
            instances.append(
                (dmg, dmg_inst_name) if max_occ == 0 else (dmg, dmg_inst_name, max_occ)
            )

        try:
            agent_health = int(self.health_var.get())
        except ValueError:
            agent_health = 100

        for c in find_combos(instances, base_health=agent_health):
            value, setup = c
            combos_text += f"{value} = {setup}\n"

            if int(value) < agent_health + 5:
                gray_text += f"{value} = {setup}\n"
            elif 105 <= int(value) < agent_health + 8:
                green_text += f"{value} = {setup}\n"
            elif 108 <= int(value) < agent_health + 10:
                blue_text += f"{value} = {setup}\n"
            elif 110 <= int(value) < agent_health + 12:
                purple_text += f"{value} = {setup}\n"
            elif 112 <= int(value) < agent_health + 15:
                gold_text += f"{value} = {setup}\n"
            elif agent_health + 15 <= int(value):
                unsurv_text += f"{value} = {setup}\n"

        all_tabs = {
            self.base_text: combos_text,
            self.gray_text: gray_text,
            self.green_text: green_text,
            self.blue_text: blue_text,
            self.purple_text: purple_text,
            self.gold_text: gold_text,
            self.unsurvivable_text: unsurv_text
        }

        for text_widget, inhalt in all_tabs.items():
            text_widget.config(state="normal")  # Schreibschutz aufheben
            text_widget.delete("1.0", tk.END)  # Alten Inhalt löschen

            if inhalt:
                text_widget.insert(tk.END, inhalt)
            else:
                text_widget.insert(tk.END, "No unique combos can be survived by this chip")

            text_widget.config(state="disabled")  # Schreibschutz wieder aktivieren

        def count_combos(text_string):
            if not text_string:
                return 0
            # Split lines and filter out any accidental empty lines
            return len([line for line in text_string.split("\n") if line.strip()])

        # Update each tab header using self.notebook.tab()
        self.notebook.tab(self.base_tab, text=f"All Combos ({count_combos(combos_text)})")
        self.notebook.tab(self.gray_tab, text=f"Gray Health ({count_combos(gray_text)})")
        self.notebook.tab(self.green_tab, text=f"Green Health ({count_combos(green_text)})")
        self.notebook.tab(self.blue_tab, text=f"Blue Health ({count_combos(blue_text)})")
        self.notebook.tab(self.purple_tab, text=f"Purple Health ({count_combos(purple_text)})")
        self.notebook.tab(self.gold_tab, text=f"Gold Health ({count_combos(gold_text)})")
        self.notebook.tab(self.unsurvivable_tab, text=f"Unsurvivable ({count_combos(unsurv_text)})")

    def on_agent_selected(self, event):
        """Triggers automatically when the user selects an agent from the dropdown."""
        selected_agent = self.agent_dropdown.get()

        if selected_agent == "Custom":
            # Hide the weapon dropdown from the user interface
            self.weapon_row_frame.pack_forget()
            self.weapon_label.pack_forget()
            self.weapon_dropdown.pack_forget()
        else:
            self.weapon_row_frame.pack(
                side=tk.TOP,
                fill=tk.X,
                anchor="nw",
                pady=(10, 0),
            )

            # FIXED: Always clear and re-pack both elements in the correct order
            # to prevent the dropdown from getting lost or hidden.
            self.weapon_label.pack_forget()
            self.weapon_dropdown.pack_forget()
            # Show the weapon dropdown next to the agent dropdown
            # Reset weapon selection to default when agent changes
            self.weapon_label.pack(side=tk.LEFT, padx=(10, 5), pady=0)
            self.weapon_dropdown.pack(side=tk.LEFT, padx=5)
            self.weapon_dropdown.set("Choose a Weapon")

            new_weapons = self.gun_dict[selected_agent]

            self.weapon_dropdown['values'] = new_weapons

        # Get rid of the blue background after selecting a weapon
        self.root.focus()
        self.agent_dropdown.selection_clear()

    def on_weapon_selected(self, event):
        """Triggers when the user selects a weapon for the active agent."""
        selected_agent = self.agent_dropdown.get()
        selected_weapon = MainWindow.translate_name(self.weapon_dropdown.get())

        if selected_agent == "Yu-Mi":
            selected_agent = "Yumi"
        elif selected_agent == "Red":
            selected_agent = "Socialite"
        elif selected_agent == "Cavalière":
            selected_agent = "Cavaliere"
        elif selected_agent == "Madame Xiu":
            selected_agent = "Xiu"

        # Leere Damage Tabs
        for tab in self.tab_list:
            tab.destroy()
        self.tab_list = []
        populate_dmg_sources(self, selected_agent, selected_weapon, self.agent_data)

        self.update_notebook()

        # Get rid of the blue background after selecting a weapon
        self.root.focus()
        self.weapon_dropdown.selection_clear()

    def select_file_from_manager(self):
        # Opens the native file dialog explorer
        file_path = filedialog.askopenfilename(
            title="Select a JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        )

        # Check if the user cancelled the dialog
        if not file_path:
            print("No file was selected.")
            return

        # Try to load and parse the selected JSON file
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.agent_data = json.load(file)

                # NEW: Extract the file name and update the label
                file_name = os.path.basename(file_path)
                self.file_name_label.config(
                    text=f"Loaded: {file_name}", fg="green"
                )

        except json.JSONDecodeError:
            print("Error: The file is not a valid JSON format.")
        except Exception as e:
            print(f"An error occurred: {e}")

        for table in self.agent_data["overrides"]:
            if table["table"] == "DT_SpyShared_HealthPool" and table["row"] == "HealthPool_Low" and table['field'] == "HealthPool":
                hp_value = table['value']
                break
        else:
            hp_value = 100

        self.health_var.set(hp_value)

    @staticmethod
    def translate_name(name):
        with open("NameTranslations.json") as trans_table:
            translate_data = json.load(trans_table)
        return translate_data["translations"][name]


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
