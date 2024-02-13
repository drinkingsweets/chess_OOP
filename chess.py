import time
import os

# король - king
# ферзь - queen
# ладья - rook
# слон - bishop
# конь - kNight
# пешка - pawn

class Field:
    def __init__(self):
        self.board = {
        8: ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        7: ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        6: ['.', '.', '.', '.', '.', '.', '.', '.'],
        5: ['.', '.', '.', '.', '.', '.', '.', '.'],
        4: ['.', '.', '.', '.', '.', '.', '.', '.'],
        3: ['.', '.', '.', '.', '.', '.', '.', '.'],
        2: ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        1: ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    }
    def change_field(self, st_x, st_y, where_x, where_y):
        self.board[where_y][where_x] = self.board[st_y][st_x]
        self.board[st_y][st_x] = '.'

    def print(self):
        let = '\033[1m' + '   A B C D E F G H' + '\033[0m'

        print(let)

        for row in self.board:
            print(f'{row:<2}', *self.board[row], f'{row:>2}')

        print(let)

    def update(self):
        


while True:
    Board = Field()
    Board.print()
