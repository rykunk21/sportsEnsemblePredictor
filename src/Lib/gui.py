import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import numpy as np
from src.Lib import data, simulation, util



class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, _):
        if self.get() == self.placeholder:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, _):
        if not self.get():
            self.put_placeholder()

class GUI:
    background = "#2F3842"

    def __init__(self):
        self.parameters = {}

        self.window = tk.Tk()
        self.window.title("Auto Gambler")
        self.window.geometry("500x750")

        self.create_label("The Model", 20)

        frame = tk.Frame(self.window)
        frame.pack()

        counter_gen = self.counter()

        labels = ["Home ML Probability", "Home Spread Probability", "Away ML Probability", "Away Spread Probability", "Home Team", "Away Team"]
        for label in labels:
            self.create_label_entry_pair(frame, label, counter_gen)

        self.text_output = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=50, height=10)
        self.text_output.pack()

        self.window.configure(bg=self.background)

    def create_label(self, text, font_size):
        label = tk.Label(self.window, text=text, bg=self.background, fg="white", font=("Helvetica", font_size))
        label.pack()

    def create_label_entry_pair(self, frame, label_text, counter_gen):
        pair_frame = tk.Frame(frame, pady=10)
        pair_frame.rowconfigure(0, weight=1)
        pair_frame.rowconfigure(1, weight=1)

        row, col = next(counter_gen)
        label = tk.Label(pair_frame, text=label_text, bg=self.background, fg="white", font=("Helvetica", 16))
        label.grid(row=0, pady=(0, 5), sticky=tk.W)

        entry_placeholder = label_text.lower()
        entry_var = tk.StringVar()
        entry_var.set(entry_placeholder)
        entry = tk.Entry(pair_frame, textvariable=entry_var)
        entry.grid(row=1, pady=(5, 10), sticky=tk.W)

        # Bind the entry widget to remove the placeholder text on focus
        entry.bind("<FocusIn>", lambda event: entry_var.set(''))

        pair_frame.grid(row=row, column=col, sticky=tk.W + tk.E)

    def counter(self):
        for count in range(1, 7):
            if count < 1 or count > 6:
                raise ValueError("Count should be between 1 and 6")

            row = (count - 1) // 2
            column = (count - 1) % 2
            yield row, column
        
    def change_background_color(self, color):
        self.window.configure(bg=color)

    def submit_button_callback(self, spread, home_ml, home_spread, away_ml, away_spread, home_team, away_team):
        try:
            spread_val = float(spread.get())
            home_ml_prob_val = float(home_ml.get())
            home_spread_prob_val = float(home_spread.get())
            away_ml_prob_val = float(away_ml.get())
            away_spread_prob_val = float(away_spread.get())
            home_team_val = home_team.get()
            away_team_val = away_team.get()

            self.parameters = {
                "SPREAD": spread_val,
                "HOMEMLPROB": home_ml_prob_val,
                "HOMESPREADPROB": home_spread_prob_val,
                "AWAYMLPROB": away_ml_prob_val,
                "AWAYSPREADPROB": away_spread_prob_val,
                "HOME": home_team_val,
                "AWAY": away_team_val
            }

            # Clear the text output
            self.text_output.delete(1.0, tk.END)

            self.run_function_and_display_output()

        except ValueError:
            self.text_output.insert(tk.END, "Invalid input. Please enter valid numerical values.\n")
            self.text_output.yview(tk.END)

    def run_function_and_display_output(self):

        SPREAD = self.parameters["SPREAD"]
        HOMEMLPROB = self.parameters["HOMEMLPROB"]
        HOMESPREADPROB = self.parameters["HOMESPREADPROB"]
        AWAYMLPROB = self.parameters["AWAYMLPROB"]
        AWAYSPREADPROB = self.parameters["AWAYSPREADPROB"]
        HOME = self.parameters["HOME"]
        AWAY = self.parameters["AWAY"]

        home = data.simHandler.getTeam(HOME)
        away = data.simHandler.getTeam(AWAY)

        game = util.Game.NCAAB(home, away)

        sim = simulation.MonteCarlo(game)
        prob, spreads = sim.run(10000)

        spread_prob = sim.probability_of_value(spreads, SPREAD)

        output = f'{game.home} ML: {prob:.2f}\nSpread: {np.mean(spreads)}\n\n'
        output += f'Home ML: {prob - self.convertline(HOMEMLPROB):.2f}\n'
        output += f'Home Spread: {spread_prob - self.convertline(HOMESPREADPROB):.2f}\n\n'
        output += f'Away ML: {(1 - prob) - self.convertline(AWAYMLPROB):.2f}\n'
        output += f'Away Spread: {(1 - spread_prob) - self.convertline(AWAYSPREADPROB):.2f}\n'

        self.text_output.insert(tk.END, output)
        self.text_output.yview(tk.END)

    def convertline(self, line):
        if line < 0:
            line *= -1
            return line / (100 + line)
        else:
            return (100 / (100 + line))

    def run(self):
        self.window.mainloop()

    def close(self):
        pass
