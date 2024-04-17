import tkinter as tk
from tkinter import ttk

def CreateMenuButton(current_master, button_text, button_command, padx_size, pady_size):
    new_button = tk.Button(master = current_master, text = button_text, font = ("Comic Sans", 14), command = button_command)
    new_button.pack(padx = 30, pady = 10, ipadx = padx_size, ipady = pady_size)
    return new_button

class TrainTextFrame(tk.Text):
    def __init__(self):
        self.text = ""

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

    def Change(self, another):
        self.close()
        self = another

    def show(self):
        self.mainloop()

    def MoveToTrainWindow(self):
        self.Change(TextSelectingWindow())
        
    def MoveToLoadListWindow(self):
        print("I have moved to load window")

class MainMenuWindow(Window):
    def __init__(self):
        super().__init__()
        self.title("Тестовый запуск игры")
        self.minsize(700, 700)
        self.greeting = tk.Label(text = "New Fast Typing Trainer!", font = ("Comic Sans", 20))
        self.greeting.pack(pady = 20)
        self.start_button = CreateMenuButton(self, "Start new game!", lambda: self.MoveToTrainWindow(), 106, 10)
        self.move_to_load_button = CreateMenuButton(self, "Check list of downloaded text files", lambda: self.MoveToLoadListWindow(), 10, 10)

    def close(self):
        self.start_button.pack_forget()
        self.move_to_load_button.pack_forget()
        self.greeting.pack_forget()

class TextSelectingWindow():
    def __init__(self):
        super().__init__()
        self.select_title = tk.Label(text = "Select text for typing", font = ("Comic Sans", 20))
        self.select_title.pack(pady = 20)
        self.text_list = tk.Listbox()
        self.text_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.list_scrollbar = ttk.Scrollbar(orient="vertical", command=self.text_list.yview)
        self.list_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.text_list["yscrollcommand"]=self.list_scrollbar.set
    def close(self):
        self.select_title.pack_forget()
        self.text_list.pack_forget()
        self.list_scrollbar.pack_forget()

if __name__ == '__main__':
    Main_Menu = MainMenuWindow()
    Main_Menu.show()
