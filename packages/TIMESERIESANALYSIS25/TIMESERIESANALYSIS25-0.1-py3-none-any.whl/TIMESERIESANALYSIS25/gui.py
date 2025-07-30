import tkinter as tk
from tkinter import messagebox

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Time Series Analysis")

    def show_message(self, message):
        messagebox.showinfo("Info", message)

    def run(self):
        self.root.mainloop()
