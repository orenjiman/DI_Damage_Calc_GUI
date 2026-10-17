import tkinter as tk
from typing import Literal


class WTab(tk.Frame):
    """Ein eigenes Widget, das Textfeld, Zahlenfeld und Lösch-Button kombiniert."""

    def __init__(self, parent, delete, main_window):
        super().__init__(parent)
        self.delete = delete
        self.main_window = main_window
        self.is_active = tk.BooleanVar(value=True)

        # Variables with Observers (trace) for automatic recalculation
        self.is_active = tk.BooleanVar(value=True)
        self.is_active.trace_add("write", self.on_value_changed)

        self.name_var = tk.StringVar()
        self.name_var.trace_add("write", self.on_value_changed)

        self.dmg_var = tk.StringVar(value="0")
        self.dmg_var.trace_add("write", self.on_value_changed)

        self.max_occ_var = tk.StringVar()
        self.max_occ_var.trace_add("write", self.on_value_changed)

        # Input for name of damage instance
        tk.Label(self, text="Name:").pack(side=tk.LEFT, padx=2)
        self.name_entry = tk.Entry(self, width=15, textvariable=self.name_var)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        # Input for damage value
        tk.Label(self, text="Damage:").pack(side=tk.LEFT, padx=2)
        self.dmg_spin = tk.Spinbox(self, from_=0, to=500, width=6, textvariable=self.dmg_var)
        self.dmg_spin.pack(side=tk.LEFT, padx=5)

        # Intercept spinbox arrow clicks to trigger calculations immediately
        self.dmg_spin.bind("<<Increment>>", self.on_arrow_clicked)
        self.dmg_spin.bind("<<Decrement>>", self.on_arrow_clicked)

        # Input for max occurrence
        tk.Label(self, text="Max Occ.:").pack(side=tk.LEFT, padx=2)
        self.max_occ_entry = tk.Entry(self, validate="key", validatecommand=(self.register(self.validate_number), "%P"), width=6, textvariable=self.max_occ_var)
        self.max_occ_entry.pack(side=tk.LEFT, padx=5)

        # Checkboxes for if the tab is active.
        self.active_cb = tk.Checkbutton(self, variable=self.is_active, command=self.toggle_state)
        self.active_cb.pack(side=tk.LEFT, padx=5)

        # Delete button
        self.del_btn = tk.Button(self, text="❌", fg="red", command=self.entfernen)
        self.del_btn.pack(side=tk.LEFT, padx=5)

    def on_value_changed(self, *args):
        self.main_window.update_notebook()

    def on_arrow_clicked(self, event):
        # Force Tkinter to internally update the spinbox value BEFORE running calculations
        self.main_window.root.update_idletasks()
        self.main_window.update_notebook()

    def toggle_state(self):
        state: Literal["normal", "disabled"] = "normal" if self.is_active.get() else "disabled"
        self.name_entry.config(state=state)
        self.dmg_spin.config(state=state)
        self.max_occ_entry.config(state=state)

    def entfernen(self):
        self.delete(self)
        self.destroy()

    @staticmethod
    def validate_number(text):
        if text == "":
            return True
        if text.isdigit():
            return True

        return False

    def is_valid(self):
        try:
            dmg = int(self.dmg_spin.get())
        except ValueError:
            dmg = 0

        return dmg > 0 and len(self.name_entry.get()) > 0 and self.is_active.get()
