import os
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

def CreateMenuButton(current_master, button_text, button_command, padx_size, pady_size):
    new_button = tk.Button(master = current_master, text = button_text,
                           font = ("Comic Sans", 14), command = button_command)
    new_button.pack(padx = 30, pady = 10, ipadx = padx_size, ipady = pady_size)
    return new_button

class TrainTextFrame(tk.Text):
    def __init__(self):
        self.text = ""

class Window(tk.Tk):
    first_window = True
    
    def __init__(self):
        super().__init__()

    def Change(self, another):
        self.close()
        self = another

    def MoveToSelectionWindow(self):
        self.Change(TextSelectingWindow())

    def MoveToTrainWindow(self, name):
        self.Change(TrainingWindow(name))
        
    def MoveToLoadListWindow(self):
        print("I have moved to load window")

    def MoveToGameFinishedWindow(self, previous):
        self.Change(FinishedGameWindow(previous))

    def MoveToMainWindow():
        self.Change(MainMenuWindow())

class MainMenuWindow(Window):
    def __init__(self):
        if Window.first_window:
            super().__init__()
            Window.first_window = False
        self.title("Тестовый запуск игры")
        self.minsize(700, 700)
        self.greeting = tk.Label(text = "New Fast Typing Trainer!", font = ("Comic Sans", 20))
        self.greeting.pack(pady = 20)
        self.start_button = CreateMenuButton(self, "Start new game!",
                                             lambda: self.MoveToSelectionWindow(), 106, 10)
        self.move_to_load_button = CreateMenuButton(self, "Check list of downloaded text files",
                                                    lambda: self.MoveToLoadListWindow(), 10, 10)
        self.mainloop()

    def close(self):
        self.start_button.pack_forget()
        self.move_to_load_button.pack_forget()
        self.greeting.pack_forget()

class TextSelectingWindow(Window):
    #@classmethod
    def selected(self, event):
        selected_indices = self.text_listbox.curselection()
        selected_text = self.text_listbox.get(selected_indices[0])
        self.MoveToTrainWindow(selected_text)
    
    def __init__(self):
        #super().__init__()
        self.select_title = tk.Label(text = "Select text for typing", font = ("Comic Sans", 20))
        self.select_title.pack(pady = 20)
        text_directory = "./textes"
        self.textes = os.listdir(text_directory)
        for i in range(len(self.textes)):
            self.textes[i] = self.textes[i][:-4]
        print(self.textes)
        text_helper = tk.Variable(value=self.textes)
        self.text_listbox = tk.Listbox(listvariable = text_helper, font = ("Comic Sans", 15))
        self.text_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.text_listbox.bind("<<ListboxSelect>>", self.selected)
        self.list_scrollbar = ttk.Scrollbar(orient="vertical", command=self.text_listbox.yview)
        self.list_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.text_listbox["yscrollcommand"]=self.list_scrollbar.set
        
    def close(self):
        self.select_title.pack_forget()
        self.text_listbox.pack_forget()
        self.list_scrollbar.pack_forget()

class TrainingWindow(Window):
    def __init__(self, text_name):
        self.train_name = tk.Label(text = text_name, font = ("Comic Sans", 20))
        self.word_count = tk.Label(text = "Words written", font = ("Comic Sans", 20))
        self.train_name.pack(anchor = tk.NW)
        self.word_count.pack(anchor = tk.N)
        self.train_window = ScrolledText(height = 25, font = ("Arial", 20))
        real_path = "textes/" + text_name + ".txt"
        self.text = ""
        text_file = open(real_path)
        for line in text_file:
            self.text += line
        text_file.close()
        #for i in range(len(self.text)):
            #self.train_window.insert(tk.END, self.text[i])
        self.train_window.insert("1.0", self.text)
        self.train_window.config(state = tk.DISABLED)
        self.train_window.pack()
        self.train_window.bind("<Key>", self.typing);

    @staticmethod
    def check_symbols(first, second):
        if (first == second):
            return True
        if (first == "Return" and ord(second) == 10):
            return True
        special_symbols = {'exclam': '!', 'equal': '=', 'question': '?', 'space': " ", 'plus': '+','comma': ',',
                           'period': '.', 'minus': '-', 'underscore': '_', 'apostrophe': "'", 'colon': ':', 'semicolon': ';',
                           'parenleft': '(', 'parenright': ')', 'braceleft':'{', 'bracketleft':'[',
                           'braceright':'}', 'bracketright':']'}
        return (first in special_symbols) and (special_symbols[first] == second)

    def typing(self, event):
        new_symbol = event.keysym
        first_symbol = self.text[0][0]
        print(new_symbol, first_symbol)
        if self.check_symbols(new_symbol, first_symbol):
            self.train_window.config(state = tk.NORMAL)
            self.text = self.text[1:]
            self.train_window.delete("1.0", tk.END)
            self.train_window.insert("1.0", self.text)
            self.train_window.config(state = tk.DISABLED)
            #print(ord(self.text[0]))
            if (len(self.text) == 0 or (len(self.text) == 1
                                        and ord(self.text[0]) == 10)):
                #print("Game finished")
                self.MoveToGameFinishedWindow(self)

    def close(self):
        self.train_name.pack_forget()
        self.word_count.pack_forget()
        self.train_window.pack_forget()

class FinishedGameWindow(Window):
    def __init__(self, previous):
        self.finish_text = tk.Label(text = "Congragulations!", font = ("Comic Sans", 20))
        self.finish_text.pack(anchor = tk.CENTER)
        
        self.start_button = CreateMenuButton(self, "Start new game!",
                                             lambda: self.MoveToSelectionWindow(), 106, 10)
        self.move_to_load_button = CreateMenuButton(self, "Check list of downloaded text files",
                                                    lambda: self.MoveToLoadListWindow(), 10, 10)

if __name__ == '__main__':
    Main_Menu = MainMenuWindow()
