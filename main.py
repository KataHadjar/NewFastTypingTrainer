import os
import time

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from src.constans import SPECIAL_SYMBOLS


class Window(tk.Tk):

    def __init__(self):
        super().__init__()

    def change(self, another):
        self.close()
        self = another
        self.show()

    def move_to_selection_window(self):
        self.close()
        self = CONST_WINDOW_LIST[1]
        self.show()

    def move_to_train_window(self, name):
        self.change(TrainingWindow(name))

    def move_to_game_finished_window(self, previous):
        self.change(FinishedGameWindow(previous))

    def move_to_statistic_window(self):
        self.change(StatisticWindow())

    def move_to_main_window(self):
        self.close()
        self = CONST_WINDOW_LIST[0]
        self.show()


class MainMenuWindow(Window):
    def __init__(self):
        super().__init__()
        self.title("Тестовый запуск игры")
        self.minsize(800, 810)
        self.greeting = tk.Label(text="New Fast Typing Trainer!", font=("Comic Sans", 20))
        self.start_button = tk.Button(text="Start new game!", font=("Comic Sans", 14),
                                      command=lambda: self.move_to_selection_window())
        self.move_to_load_button = tk.Button(text="Check game history",
                                             font=("Comic Sans", 14),
                                             command=lambda: self.move_to_statistic_window())

    def show(self):
        self.greeting.pack(pady=30)
        self.start_button.pack(padx=30, pady=10, ipadx=106, ipady=10)
        self.move_to_load_button.pack(padx=30, pady=10, ipadx=87, ipady=10)

    def close(self):
        self.start_button.pack_forget()
        self.move_to_load_button.pack_forget()
        self.greeting.pack_forget()


class TextSelectingWindow(Window):
    def selected(self, event):
        selected_indices = self.text_listbox.curselection()
        selected_text = self.text_listbox.get(selected_indices[0])
        self.move_to_train_window(selected_text)

    def __init__(self):
        self.select_title = tk.Label(text="Select text for typing", font=("Comic Sans", 20))
        text_directory = "./texts"
        self.texts = os.listdir(text_directory)
        for i in range(len(self.texts)):
            self.texts[i] = self.texts[i][:-4]
        text_helper = tk.Variable(value=self.texts)
        self.text_listbox = tk.Listbox(listvariable=text_helper, font=("Comic Sans", 15))
        self.text_listbox.bind("<<ListboxSelect>>", self.selected)
        self.list_scrollbar = ttk.Scrollbar(orient="vertical", command=self.text_listbox.yview)
        self.text_listbox["yscrollcommand"] = self.list_scrollbar.set

    def show(self):
        self.select_title.pack(pady=20)
        self.text_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def close(self):
        self.select_title.pack_forget()
        self.text_listbox.pack_forget()
        self.list_scrollbar.pack_forget()


CONST_WINDOW_LIST = [MainMenuWindow(), TextSelectingWindow()]


class TrainingWindow(Window):
    def __init__(self, text_name):
        self.words_number = 0
        self.letter_flag = False
        self.text_name = text_name
        self.train_name = tk.Label(text=text_name, font=("Comic Sans", 20))
        self.word_count = tk.Label(text="Words written: " + str(self.words_number), font=("Comic Sans", 20))
        self.train_window = ScrolledText(height=18, width=41, font=("Arial", 20), wrap='word')
        real_path = os.path.join("texts", text_name + ".txt")
        self.text = ""
        text_file = open(real_path)
        for line in text_file:
            self.text += line
        text_file.close()
        self.train_window.insert("1.0", self.text)
        self.train_window.config(state=tk.DISABLED)
        self.start_time = time.time()
        self.game_time = 0
        self.train_window.bind("<Key>", self.typing)

    def show(self):
        self.train_name.pack(anchor=tk.N)
        self.word_count.pack(anchor=tk.N)
        self.train_window.pack()

    @staticmethod
    def check_symbols(first, second):
        if (first == second):
            return True
        if (first == "Return" and ord(second) == 10):
            return True
        return (first in SPECIAL_SYMBOLS) and (SPECIAL_SYMBOLS[first] == second)

    def typing(self, event):
        new_symbol = event.keysym
        first_symbol = self.text[0][0]
        if self.check_symbols(new_symbol, first_symbol):
            if (self.letter_flag and (not first_symbol.isalpha())):
                self.words_number += 1
                self.word_count['text'] = 'Words written: ' + str(self.words_number)
            if first_symbol.isalpha():
                self.letter_flag = True
            else:
                self.letter_flag = False
            self.train_window.config(state=tk.NORMAL)
            self.text = self.text[1:]
            self.train_window.delete("1.0", tk.END)
            self.train_window.insert("1.0", self.text)
            self.train_window.config(state=tk.DISABLED)
            if (len(self.text) == 0 or (len(self.text) == 1
                                        and ord(self.text[0]) == 10)):
                if (len(self.text) > 0 and self.letter_flag):
                    self.words_number += 1
                self.game_time = round(time.time() - self.start_time, 2)
                history_file_path = os.path.join("history", "game_history.txt")
                history_file_read = open(history_file_path)
                line_number = 1
                for line in history_file_read:
                    line_number += 1
                history_file_read.close()
                history_file_write = open(history_file_path, 'a')
                result = "Game " + str(line_number) + ", text: " + str(self.text_name) + ", words: " + str(
                    self.words_number) + ", time: " + str(self.game_time) + "\n"
                history_file_write.write(result)
                history_file_write.close()
                self.move_to_game_finished_window(self)

    def close(self):
        self.train_name.pack_forget()
        self.word_count.pack_forget()
        self.train_window.pack_forget()


class StatisticWindow(Window):
    def __init__(self):
        self.button_frame = tk.Frame()
        self.back_button = tk.Button(master=self.button_frame, text="Back to main menu", font=("Comic Sans", 14),
                                     command=lambda: self.move_to_main_window())
        self.clear_button = tk.Button(master=self.button_frame, text="Clear history", font=("Comic Sans", 14),
                                      command=lambda: self.clear_history())
        self.statistic_window = ScrolledText(height=18, width=41, font=("Arial", 20), wrap='word')
        history_file_path = os.path.join("history", "game_history.txt")
        history_file = open(history_file_path, 'r')
        for line in history_file:
            self.statistic_window.insert(tk.END, line)
        self.statistic_window.config(state=tk.DISABLED)

    def show(self):
        self.button_frame.pack(fill=tk.X)
        self.back_button.pack(side=tk.LEFT)
        self.clear_button.pack(side=tk.RIGHT)
        self.statistic_window.pack()

    def clear_history(self):
        history_file_path = os.path.join("history", "game_history.txt")
        with open(history_file_path, 'wb'):
            pass
        self.statistic_window.config(state=tk.NORMAL)
        self.statistic_window.delete("1.0", tk.END)
        self.statistic_window.config(state=tk.DISABLED)

    def close(self):
        self.back_button.pack_forget()
        self.clear_button.pack_forget()
        self.statistic_window.pack_forget()


class FinishedGameWindow(Window):
    def __init__(self, previous):
        self.finish_text = tk.Label(text="Congratulations!", font=("Comic Sans", 20))
        self.finish_result = tk.Label(text="You have written " + str(previous.words_number) + " words",
                                      font=("Comic Sans", 20))
        self.time_result = tk.Label(text="and you done it in " + str(previous.game_time) + ' seconds!',
                                    font=("Comic Sans", 20))
        self.select_new_game = tk.Button(text="Play again!", font=("Comic Sans", 14),
                                         command=lambda: self.move_to_selection_window())
        self.menu_button = tk.Button(text="Go to main menu", font=("Comic Sans", 14),
                                     command=lambda: self.move_to_main_window())

    def show(self):
        self.finish_text.pack(anchor=tk.CENTER, pady=40)
        self.finish_result.pack(anchor=tk.CENTER)
        self.time_result.pack(anchor=tk.CENTER)
        self.select_new_game.pack(padx=30, pady=20, ipadx=143, ipady=10)
        self.menu_button.pack(padx=30, pady=20, ipadx=106, ipady=10)

    def close(self):
        self.time_result.pack_forget()
        self.finish_result.pack_forget()
        self.finish_text.pack_forget()
        self.select_new_game.pack_forget()
        self.menu_button.pack_forget()


if __name__ == '__main__':
    Main_Menu = CONST_WINDOW_LIST[0]
    Main_Menu.show()
    Main_Menu.mainloop()
