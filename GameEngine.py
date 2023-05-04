from GameState import GameState
from Gui import gui
import time


class GameEngine:
    def __init__(self):
        self.gameState = GameState()
        self.turn = "ai"
        self.gui = gui(self, self.gameState)
        self.piece_choosen = None
        self.moves_made = 0
        self.forbidden = []
        self.gameStarted = False

    def updateBoard(self):
        self.gui.updateBoard()

    def move_ai(self):
        self.gui.updateBoard()
        ai_pieces = len(self.gameState.playerAi)
        moves, dead_pieces_ai, dead_pieces_human = self.gameState.move_ai()
        for piece in dead_pieces_ai:
            self.gui.show_msg(f"AI looses piece #{piece} ")
        for piece in dead_pieces_human:
            self.gui.show_msg(f"Human player looses piece #{piece} ")
        for move in moves:
            piece = move[0]
            x, y = move[1]
            self.gui.show_msg(f"AI played piece # {piece} to {x + 1, y + 1}")
            if self.gameState.game_winner() != "continue":
                self.gui.show_msg(f"{self.gameState.game_winner()} wins the game")
                self.gui.updateBoard()
                self.gui.stop()
                return;

        self.gui.updateBoard()


    def startGame(self):
        if self.gameStarted:
            return
        self.gameStarted = True
        if self.turn == "ai":
            self.move_ai()
            if self.gameState.game_winner() != "continue":
                return
            self.moves_made = 0
            self.forbidden = []
            self.gui.show_msg(f"AI completed turn")
            self.gui.show_msg(f"It is now Human Player's turn")
            self.turn = "human"


    def play(self, i, j):
        if not self.gameStarted:
            return

        if self.turn == "human":
            if self.piece_choosen == None and (j, i) not in self.forbidden and (
            j, i) in self.gameState.get_piece_values(self.turn):
                self.gui.highlight_button(i, j)
                self.piece_choosen = self.gameState.get_piece_choosen(j, i, self.turn)
                self.gui.show_msg(f"P2 choosed piece # {self.piece_choosen}")
            elif self.piece_choosen != None and (j, i) in self.gameState.possible_moves(self.piece_choosen, self.turn):
                self.gui.un_highlight_button(self.gameState.get_pieces(self.turn)[self.piece_choosen][1],
                                             self.gameState.get_pieces(self.turn)[self.piece_choosen][0])
                self.gameState.get_pieces(self.turn)[self.piece_choosen] = (j, i)
                self.gui.show_msg(f"P2 moved piece# {self.piece_choosen} to {j + 1, i + 1}")
                self.piece_choosen = None
                self.forbidden = [(j, i)]
                self.moves_made += 1
                dead_pieces1, dead_pieces2 = self.gameState.clear_dead_pieces()
                for piece in dead_pieces1:
                    self.gui.show_msg(f"Player 2 looses piece #{piece} ")
                for piece in dead_pieces2:
                    self.gui.show_msg(f"Player 1 looses piece #{piece} ")
                if self.gameState.game_winner() != "continue":
                    self.gui.show_msg(f"{self.gameState.game_winner()} wins the game")
                    self.gui.updateBoard()
                    self.gui.stop()
                    return;

                if self.moves_made == self.gameState.get_moves_allowable(self.turn):
                    self.gui.show_msg(f"Human Player completed turn")
                    self.gui.show_msg(f"It is now AI's turn")
                    self.gui.updateBoard()
                    self.turn = "ai"
                    if self.turn == "ai":
                        self.move_ai()
                        if self.gameState.game_winner() != "continue":
                            return
                        self.moves_made = 0
                        self.forbidden = []
                        self.gui.show_msg(f"AI completed turn")
                        self.gui.show_msg(f"It is now Human Player's turn")
                        self.turn = "human"

                self.gui.updateBoard()
            elif self.piece_choosen != None and (j, i) == self.gameState.get_pieces(self.turn)[self.piece_choosen]:
                self.gui.un_highlight_button(self.gameState.get_pieces(self.turn)[self.piece_choosen][1],
                                             self.gameState.get_pieces(self.turn)[self.piece_choosen][0])
                self.gui.show_msg(f"P2 unchoosed piece # {self.piece_choosen}")
                self.piece_choosen = None

    def run(self):
        self.gui.run()
