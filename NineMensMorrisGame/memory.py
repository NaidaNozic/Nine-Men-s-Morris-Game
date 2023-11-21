from tkinter import *
from tkinter import filedialog
from typing import TextIO


class MemoryMeta(type):
    _instances = {}

    # Use only one instance of Memory class for all purposes, code structure courtesy of Refactoring Guru

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Memory(metaclass=MemoryMeta):
    allmoves: list[str]
    index_of_move: int

    def __init__(self):
        self.allmoves = list()
        self.allmoves.append("0")
        self.stream = None
        self.index_of_move = 0

    def write_move(self, move: str):
        self.allmoves = self.allmoves[:self.index_of_move]
        self.allmoves.append(move)
        self.index_of_move = self.index_of_move + 1
    pass

    def save_game(self):
        savefile = filedialog.asksaveasfilename(confirmoverwrite=TRUE, initialdir="/",
                                                title="Save current game",
                                                filetypes=(("Text files",
                                                            "*.txt*"),
                                                           ("all files",
                                                            "*.*")))
        if savefile:
            self.stream = open(savefile, 'w+')
            for move in self.allmoves:
                self.stream.write(move + "\n")
            self.stream.close()

    def load_game(self):
        loadgamepath = filedialog.askopenfilename()

        if loadgamepath:
            with open(loadgamepath) as savedgame:
                self.allmoves = savedgame.read().splitlines()
                self.index_of_move = len(self.allmoves) - 1
                return self.index_of_move
        return -1

    def see_moves(self):
        print("Moves: " + str(len(self.allmoves)))
        for move in self.allmoves:
            print(move)

    def undo(self):
        if self.index_of_move >= len(self.allmoves):
            self.index_of_move = len(self.allmoves)-1
            return self.index_of_move
        if self.index_of_move >= 0:
            self.index_of_move = self.index_of_move - 1
            self.see_moves()
            return self.index_of_move
        return -2

    def redo(self):
        if self.index_of_move < len(self.allmoves) - 1:
            self.index_of_move = self.index_of_move + 1
            self.see_moves()
            return self.index_of_move
        return -1

    def get_moves(self):
        return self.allmoves