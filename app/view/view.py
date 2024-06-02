import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from settings import *
from utils.docker_utils import *


class View:
    def __init__(self, root):
        self.root = root
        self.root.title("Transfermarkt Scraper")
        self.root.geometry(WINDOW_SIZE)

        self.start_button = tk.Button(
            root, text="Start MySQL", command=self.start_mysql)
        self.start_button.pack(pady=10)

        # self.start_button = tk.Button(root, text="Start Scraping", command=self.stop_containers)
        # self.start_button.pack(pady=10)

        self.stop_button = tk.Button(
            root, text="Stop Scraping", command=self.stop_containers)
        self.stop_button.pack(pady=10)


    def start_mysql(self):
        try:
            start_mysql_container()
            messagebox.showinfo("Success", "Containers started successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_containers(self):
        try:
            stop_all_containers()
            messagebox.showinfo("Success", "Containers stopped successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = View(root)
    root.mainloop()
