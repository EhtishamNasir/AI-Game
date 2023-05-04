from tkinter import *
from tkinter import ttk
from functools import partial
import tkinter.scrolledtext as scrolledtext
from PIL import Image, ImageTk
from tkinter import messagebox as mb
import tkinter as tk


class gui():
    def __init__(self, gameEngine, gameState):
        self.gameEngine = gameEngine
        self.gameState = gameState
        self.board_buttons = [[0 for x in range(7)] for y in range(7)]

        self.root = Tk()
        self.root.title("Strategic Board Game")  # title of the GUI window
        self.root.maxsize(530, 540)  # specify the max size the window can expand to
        self.root.config(bg="light grey")
        self.bg_color = "grey"
        self.left_frame = Frame(self.root, width=800, height=400, bg=self.bg_color, borderwidth=2, relief="groove")
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)
        self.blabel1 = Label(self.left_frame, text="                                                 ",
                             bg=self.bg_color)
        self.blabel1.grid(row=0, column=0, padx=5, pady=5)  # blank labels to add space
        self.start_button = Button(self.left_frame, command=self.startGame, text="Start Game")
        self.start_button.configure(width=15, height=2)
        self.start_button.grid(row=1, column=0, padx=5, pady=5)
        self.blabel2 = Label(self.left_frame, text="                                                 ",
                             bg=self.bg_color)
        self.blabel2.grid(row=2, column=0, padx=5, pady=5)  # blank labels to add space
        self.label1 = Label(self.left_frame, text="AI", fg='white', bg='grey')
        self.label1.grid(row=3, column=0, padx=5, pady=5)
        self.label2 = Label(self.left_frame, text="0", fg='white', bg='grey')
        self.label2.grid(row=4, column=0, padx=5, pady=5)
        self.blabel3 = Label(self.left_frame, text="                                                 ",
                             bg=self.bg_color)
        self.blabel3.grid(row=5, column=0, padx=5, pady=5)  # blank labels to add space
        self.label3 = Label(self.left_frame, text="Human:", fg='white', bg='grey')
        self.label3.grid(row=6, column=0, padx=5, pady=5)
        self.label4 = Label(self.left_frame, text="0", fg='white', bg='grey')
        self.label4.grid(row=7, column=0, padx=5, pady=5)
        self.blabel4 = Label(self.left_frame, text="                                                 ",
                             bg=self.bg_color)
        self.blabel4.grid(row=8, column=0, padx=5, pady=5)  # blank labels to add space

        self.right_frame = Frame(self.root, width=850, height=400, bg='white', borderwidth=2, relief="groove")

        self.right_frame.grid(row=0, column=1, padx=10, pady=15)
        self.bottom_frame = Frame(self.root, width=1250, height=400, bg='light grey', borderwidth=2, relief="groove")
        self.bottom_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        self.label5 = Label(self.bottom_frame, text="Message Area:", bg='light grey').grid(row=5, column=0, padx=5,
                                                                                           pady=5)
        self.txt = scrolledtext.ScrolledText(self.bottom_frame, height=10, width=60, undo=True)
        self.txt.config(fg="white", bg="#1E1E1E")
        self.txt.see(tk.END)  # code to update scroll text to latest line
        self.txt.grid()
        self.image = Image.open("blank.png")
        self.photo = ImageTk.PhotoImage(self.image)

        for i in range(7):
            for j in range(7):
                self.frame = Frame(
                    master=self.right_frame,
                    relief='flat',
                    borderwidth=1
                )
                self.frame.grid(row=i, column=j, padx=3, pady=3)
                action_with_arg = partial(self.play, i, j)

                self.board_buttons[i][j] = Button(master=self.frame, command=action_with_arg)
                self.board_buttons[i][j].config(image=self.photo)
                self.board_buttons[i][j].pack()
                self.board_buttons[i][j].grid()

        self.updateBoard()

    def startGame(self):
        self.gameEngine.startGame()
        self.start_button.config(text="Game Started", state=DISABLED)

    def updateBoard(self):
        self.label2.config(text=str(self.gameState.ai_score()))
        self.label4.config(text=str(self.gameState.human_score()))
        self.image1 = Image.open("triangle.png")
        self.photo1 = ImageTk.PhotoImage(self.image1)
        self.image2 = Image.open("circle.png")
        self.photo2 = ImageTk.PhotoImage(self.image2)
        for i in range(7):
            for j in range(7):
                if (i, j) in self.gameState.playerAi.values():
                    self.board_buttons[j][i].config(image=self.photo1)
                    pass
                elif (i, j) in self.gameState.playerHuman.values():
                    self.board_buttons[j][i].config(image=self.photo2)
                else:
                    self.board_buttons[j][i].config(image=self.photo)
        self.txt.see(tk.END)  # code to update scroll text to latest line

    def show_msg(self, msg):
        self.txt.insert(INSERT, msg + "\n")

    def highlight_button(self, i, j):
        self.board_buttons[i][j].config(bg="yellow")

    def un_highlight_button(self, i, j):
        self.board_buttons[i][j].config(bg="white")

    def play(self, i, j):
        print(i, j)
        self.gameEngine.play(i, j)

    def run(self):
        self.root.mainloop()

    def stop(self):
        # pass

        for i in range(7):
            for j in range(7):
                self.board_buttons[i][j].config(state=DISABLED)


