import tkinter as tk

import tkinter as tk
from tkinter import ttk  # For advanced widgets like tabs

class GUI:
    background = "#2F3842"

    def __init__(self):
        # initialize window
        self.window = tk.Tk()
        self.window.title("Auto Gambler")

        # Set the default window size
        self.window.geometry("500x500")  # Set the size to 820x768 (width x height)


        # Configure grid layout for window
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        # Create a central frame
        center_frame = tk.Frame(self.window, bg=self.background)
        center_frame.grid(sticky="nsew")

        # Configure grid layout for center_frame
        center_frame.columnconfigure(0, weight=1)
        center_frame.rowconfigure(1, weight=1)

        # Label "The Model"
        model_label = tk.Label(center_frame, text="The Model", bg=self.background, fg="white", font=("Helvetica", 16))
        model_label.grid(row=0, column=0, pady=(20, 0))

        # Tabs for sports
        tab_control = ttk.Notebook(center_frame)
        nfl_tab = ttk.Frame(tab_control)
        ncaab_tab = ttk.Frame(tab_control)
        nhl_tab = ttk.Frame(tab_control)

        tab_control.add(nfl_tab, text='NFL')
        tab_control.add(ncaab_tab, text='NCAAB')
        tab_control.add(nhl_tab, text='NHL')

        tab_control.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Input field and Submit button inside each tab
        for tab in [nfl_tab, ncaab_tab, nhl_tab]:
            self.input_field = tk.Entry(tab, width=60)
            self.input_field.grid(row=0, column=0, padx=10, pady=10)

            submit_button = tk.Button(tab, text="Submit", command=self.submit_button_callback)
            submit_button.grid(row=1, column=0, padx=10, pady=10)


        # Configure default background color
        self.window.configure(bg=self.background)

    def change_background_color(self, color):
        self.window.configure(bg=color)

    def submit_button_callback(self):
        hex_value = self.input_field.get()
        self.change_background_color(hex_value)

    def run(self):
        self.window.mainloop()

    def close(self):
        pass