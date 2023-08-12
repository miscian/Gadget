# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 13:56:25 2023

@author: miscian
"""


import tkinter as tk
from tkinter import simpledialog, messagebox
from colorsys import hsv_to_rgb  # NEW
import colorsys

class CountdownApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master)
        self.canvas.pack(fill="both", expand=True)
        self.square_ids = [[None for _ in range(100)] for _ in range(100)]
        self.time_text_id = None
        self.start_button = tk.Button(master, text="Start", command=self.start_countdown)
        self.start_button.pack()
        self.is_pinned = tk.BooleanVar()
        self.is_pinned.trace('w', self.pin_to_top)
        self.pin_button = tk.Checkbutton(master, text="Pin to top", variable=self.is_pinned)
        self.pin_button.pack()
        self.master.bind("<Configure>", self.resize)
        self.master.title("Countdown Square by Miscian")

    def start_countdown(self):
        self.start_button['state'] = 'disabled'
        entered_time = simpledialog.askstring("Input", "Enter the time (e.g., 1.30.0 for 1 hour 30 minutes 0 second)")
        hours, minutes, seconds = map(int, entered_time.split('.'))
        total_seconds = hours * 3600 + minutes * 60 + seconds
        self.update_squares(total_seconds, total_seconds)
    def pin_to_top(self, *args):
        if self.is_pinned.get():
            self.master.attributes('-topmost', 1)
        else:
            self.master.attributes('-topmost', 0)

    def resize(self, event):
        self.canvas.delete("all")
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        self.square_ids = [[self.canvas.create_rectangle(i*width//100, j*height//100, (i+1)*width//100, (j+1)*height//100, fill='white', outline='white') for i in range(100)] for j in range(100)]  
        self.time_text_id = self.canvas.create_text(width//2, height//2, text="", fill="black", font=("Arial", width//20, "bold"))  # NEW

        #色彩过渡部分
    def get_colour(self, num_squares_remaining):
        total_squares = 10000
        if num_squares_remaining > total_squares * 5/8:  # first 3/8
            if num_squares_remaining > total_squares * 6/8:  # first 2/8
                hue = ((num_squares_remaining - total_squares * 6/8) / (total_squares * 2/8)) * 60 + 120  # normalize to [120, 180] cyan to green
            else:  # second 1/8
                hue = ((num_squares_remaining - total_squares * 5/8) / (total_squares * 1/8)) * 60 + 60  # normalize to [60, 120] green to yellow
        else:  # last 5/8
            hue = (num_squares_remaining / (total_squares * 5/8)) * 60  # normalize to [0, 60] yellow to red
        saturation = 1.0  # maximum saturation
        value = 1.0  # maximum value
        rgb = colorsys.hsv_to_rgb(hue/360, saturation, value)
        r = int(rgb[0] * 255)  # red component
        g = int(rgb[1] * 255)  # green component
        b = int(rgb[2] * 255)  # blue component
        return '#%02x%02x%02x' % (r, g, b)  # convert RGB to hexadecimal
        #色彩过渡部分
    def update_squares(self, remaining_seconds, total_seconds):
        if remaining_seconds >= 0:
            percent_remaining = remaining_seconds / total_seconds
            num_squares_remaining = round(percent_remaining * 10000)
            square_color = self.get_colour(num_squares_remaining)  # NEW
            for j in range(100):
                for i in range(100):
                    if (99 - i) * 100 + j < num_squares_remaining:
                        self.canvas.itemconfig(self.square_ids[i][j], fill=square_color, outline=square_color)
                    else:
                        self.canvas.itemconfig(self.square_ids[i][j], fill='white', outline='white')
            hours, remainder = divmod(remaining_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.canvas.itemconfig(self.time_text_id, text=f"{hours:02}:{minutes:02}:{seconds:02}")
            if num_squares_remaining > 5000:  # NEW
                self.canvas.itemconfig(self.time_text_id, fill="white")  # NEW
            else:  # NEW
                self.canvas.itemconfig(self.time_text_id, fill="light gray")  # NEW
            self.master.after(1000, self.update_squares, remaining_seconds - 1, total_seconds)
        else:
            messagebox.showinfo("Message", "Countdown complete!")
            self.start_button['state'] = 'normal'

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()