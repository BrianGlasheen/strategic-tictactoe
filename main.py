### Use your mouse to place X's on the Tic Tac Toe board.
### Each time that you move, the space that you choose will
### determine the next tile that your opponent can choose.

import tkinter as tk

root = tk.Tk()
root.wm_geometry("941x941")

main_frame = tk.Frame(root, height=760, width=760, background='black')
main_frame.pack()

player = 'O'

class Board(tk.Canvas):
    def __init__(self, master, coords, *args, **kwargs):
        tk.Canvas.__init__(self, master=master, *args, **kwargs)
        self.grid(row=coords[0], column=coords[1], padx=5, pady=5)

        self.LOCATION = coords
        self.playable = False
        self.board_over = False

        if coords == (1,1):
            self.playable = True

        self.current_color = 'black'
        self.draw_border(self.current_color)

        self.board = [['', '', ''],
                      ['', '', ''],
                      ['', '', '']]

        self.turn()

        self.bind("<Button-1>", self.click)

    def turn(self):
        if self.playable and not self.board_over:
            self.draw_border('green')

    def draw_border(self, color):
        self.create_line(100, 0, 100, 300, fill=color, width=3)
        self.create_line(200, 0, 200, 300, fill=color, width=3)
        self.create_line(0, 100, 300, 100, fill=color, width=3)
        self.create_line(0, 200, 300, 200, fill=color, width=3)

    def click(self, e):
        global player

        x = int((e.x) // 100)
        y = int((e.y) // 100)

        if self.playable and not self.board[y][x]:
            if player == 'X':
                player = 'O'
            else:
                player = 'X'

            self.draw_letter(x, y, player)
            self.board[y][x] = player
            self.check_win(self.board, x, y)
            self.draw_border('black')
            self.playable = False
            next_move(x, y)

    def check_win(self, board, x, y):
        global board_map, boards
        win = False
        # horizontal win
        for i in range(3):
            temp = set(board[i])
            if len(temp) == 1 and ('X' in temp or 'O' in temp):
                win = True
        #verticle win
        for i in range(3):
            temp = set([board[0][i], board[1][i], board[2][i]])
            if len(temp) == 1 and ('X' in temp or 'O' in temp):
                win = True
        # diagonal win
        temp = set([board[0][0], board[1][1], board[2][2]])
        if len(temp) == 1 and ('X' in temp or 'O' in temp):
            win = True
        temp = set([board[0][2], board[1][1], board[2][0]])
        if len(temp) == 1 and ('X' in temp or 'O' in temp):
            win = True

        if win:
            if board == board_map:
                print(f"{player} wins, game over")
                for i in boards:
                    for board in i:
                        board.playable = False
                        board.board_over = True
                        board.draw_border('black')
            else:
                print(f"{player} wins board {x, y}")
                self.board_over = True
                self.create_text(150, 150, font=("Purisa", 250), text=player)
                board_map[x][y] = player
                self.check_win(board_map, x, y)

    def draw_letter(self, x, y, letter):
        x = x * 100 + 50
        y = y * 100 + 50
        self.create_text(x, y, font=("Purisa", 50), text=letter)

def next_move(x, y):
    if boards[x][y].board_over:
        for i in boards:
            for board in i:
                if not board.board_over:
                    board.playable = True
                    board.turn()
    else:
        for i in boards:
            for board in i:
                board.playable = False
                board.draw_border('black')
        boards[x][y].playable = True
        boards[x][y].turn()

coords = [[(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)]]
boards = [[Board(main_frame, coords[i][j], width=300, height=300) for i in range(3)] for j in range(3)]
board_map = [['', '', ''],
             ['', '', ''],
             ['', '', '']]

root.mainloop()