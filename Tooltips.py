import tkinter as tk


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

        # Bindet die Maus-Ereignisse
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return

        # Berechnet die Position direkt unter dem Mauszeiger
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20

        # Erstellt ein rahmenloses Fenster (Toplevel)
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)  # Entfernt Fensterrahmen
        self.tip_window.wm_geometry(f"+{x}+{y}")

        # Das Label für den Text
        label = tk.Label(
            self.tip_window,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",  # Klassisches Gelb für Tooltips
            relief=tk.SOLID,
            borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
