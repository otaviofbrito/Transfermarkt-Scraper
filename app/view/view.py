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


        self.menu_bar = tk.Menu(root)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Add the Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.undo_action)
        self.edit_menu.add_command(label="Redo", command=self.redo_action)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Display the menu
        self.root.config(menu=self.menu_bar)



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


    #Menu options

    def new_file(self):
        messagebox.showinfo("New File", "New file created!")

    def open_file(self):
        messagebox.showinfo("Open File", "File opened!")

    def save_file(self):
        messagebox.showinfo("Save File", "File saved!")

    def exit_app(self):
        self.root.quit()

    def undo_action(self):
        messagebox.showinfo("Undo", "Undo action!")

    def redo_action(self):
        messagebox.showinfo("Redo", "Redo action!")

if __name__ == "__main__":
    root = tk.Tk()
    app = View(root)
    root.mainloop()
