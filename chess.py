import random
import os

# король - king
# ферзь - queen
# ладья - rook
# слон - bishop
# конь - kNight
# пешка - pawn


class Field:
    turn = 'White'
    step_counter = 0
    def __init__(self):
        self.board = {
        8: ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        7: ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        6: ['.', '.', '.', '.', 'H', '.', '.', '.'],
        5: ['.', '.', '.', 'B', '.', '.', '.', '.'],
        4: ['.', '.', 'q', '.', '.', '.', '.', '.'],
        3: ['.', '.', '.', '.', '.', '.', '.', '.'],
        2: ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        1: ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    }

    def print(self):
        self.step_counter += 1
        let = '\033[1m' + '   A B C D E F G H' + '\033[0m'

        print(let)

        for row in self.board:
            print(f'{row:<2}', *self.board[row], f'{row:>2}')

        print(let)

    def update(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    green = '\033[42m'
    bold = '\033[1m'
    red = '\033[0;37;41m'
    end = '\033[0m'

    def color(self, coords):
        global green, bold, end
        Field.update()
        
        for comb in coords:
            self.board[comb[1]][comb[0]] = self.green + self.bold + self.board[comb[1]][comb[0]] + self.end

        Field.print()
        
    def uncolor(self):
        global green, bold, end, red

        for row in range(1, 9):
            for el in range(8):
                self.board[row][el] = (self.board[row][el].replace(self.green, '').replace(self.bold, '')
                                       .replace(self.end, '')).replace(self.red, '')

    def get_all_free_cells(self):
        free_cells = []

        for row in range(1, 9):
            for el in range(8):

                if self.board[row][el] == '.':
                    free_cells.append([el, row])

        return free_cells

    def change_turn(self):
        self.turn = 'Black' if self.turn == 'White' else 'White'

    def let2num(self, letter):
        let_num = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        return let_num[letter]

    def step_input(self):
        start_pos = input(f'''{self.turn}'s turn: ''')

        while len(start_pos) != 2 or start_pos[0] not in 'ABCDEFGH' or start_pos[1] not in '12345678':
            start_pos = input('Координаты введены неправильно. Введите заново: ')

        svert, shor = self.let2num(start_pos[0]), int(start_pos[1])  # обозначаем численные координаты
        figure_start = self.board[shor][svert]  # запоминаем тип фигуры

        while len(start_pos) != 2 or start_pos[0] not in 'ABCDEFGH' or start_pos[1] not in '12345678' or figure_start == '.':
            start_pos = input('Выбранная ячейка пуста. Введите координаты для ячейки с фигурой: ')
            svert, shor = self.let2num(start_pos[0]), int(start_pos[1])
            figure_start = self.board[shor][svert]

        return figure_start, svert, shor

    resur_counter = 0

    def make_step(self, fig_st, available_steps, start_x, start_y):
        
        global green, bold, end
        
        where_pos = input(f'Введите координату хода: ')

        while len(where_pos) != 2 or where_pos[0] not in 'ABCDEFGH' or where_pos[1] not in '12345678':
            where_pos = input('Координаты введены неправильно. Введите заново: ')

        y = int(where_pos[1])
        x = Field.let2num(where_pos[0])
        fig_end = Figure.uncolor_cell(Field.board[y][x])

        while (len(where_pos) != 2 or where_pos[0] not in 'ABCDEFGH' or where_pos[1] not in '12345678' or
               [x, y] not in available_steps or
               (fig_end != '.' and fig_end.isupper() == fig_st.isupper())# доп условие потому что некорректно с черными фигурами и точкой
               or len(set(CurF.get_passed_cells(x, y)) - {'.'}) >= 2):
            where_pos = input('Данный ход невозможен. Введите координаты заново: ')
            y = int(where_pos[1])
            x = Field.let2num(where_pos[0])
            fig_end = Field.board[y][x]


        if fig_end == 'H' and self.resur_counter < 2:
            new_coords = random.sample(Field.get_all_free_cells(), 1)[0]
            Field.board[new_coords[1]][new_coords[0]] = 'H'
            self.resur_counter += 1

        Field.board[y][x] = fig_st
        Field.board[start_y][start_x] = '.'

class Figure:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
        self.color = 'B' if self.name.islower() else 'W'

    @staticmethod
    def uncolor_cell(fig):
        green = '\033[42m'
        bold = '\033[1m'
        red = '\033[0;37;41m'
        end = '\033[0m'
        return fig.replace(green, '').replace(bold, '').replace(red, '').replace(end, '')

    def get_passed_cells(self, where_x, where_y):

        if self.name.lower() == 'q':

            if where_x == self.x: # moving on y, x is const

                column = [Figure.uncolor_cell(Field.board[row][where_x]) for row in Field.board] # picking vertical


                if self.y < where_y:

                    filtered_column = [column[i] for i in range(len(column)) if self.y < i <= where_y]

                if self.y > where_y:
                    column = column[::-1]
                    filtered_column = [column[i] for i in range(len(column)) if where_y <= i + 1 < self.y]

                return filtered_column

            elif where_y == self.y: # moving on x
                if self.x < where_x:
                    filtered_row = [Field.board[where_y][i] for i in range(8) if self.x < i <= where_x]

                else:
                    filtered_row = [Field.board[where_y][i] for i in range(8) if where_x < i <= self.x]

                return filtered_row

            else: # moving on diag
                delta_x =  where_x - self.x
                delta_y =  where_y - self.y

                filtered_diagonal = []
                step_x = 1 if delta_x > 0 else -1
                step_y = 1 if delta_y > 0 else -1

                for i in range(1, abs(delta_x) + 1):
                    passed_x = self.x + i * step_x
                    passed_y = self.y + i * step_y
                    filtered_diagonal.append(Figure.uncolor_cell(Field.board[passed_y][passed_x]))

                return filtered_diagonal

        if self.name.lower() == 'r':

            if where_x == self.x:  # moving on y, x is const

                column = [Figure.uncolor_cell(Field.board[row][where_x]) for row in Field.board]  # picking vertical

                if self.y < where_y:
                    filtered_column = [column[i] for i in range(len(column)) if self.y < i <= where_y]

                if self.y > where_y:
                    column = column[::-1]
                    filtered_column = [column[i] for i in range(len(column)) if where_y <= i + 1 < self.y]

                return filtered_column

            elif where_y == self.y:  # moving on x
                if self.x < where_x:
                    filtered_row = [Field.board[where_y][i] for i in range(8) if self.x < i <= where_x]

                else:
                    filtered_row = [Field.board[where_y][i] for i in range(8) if where_x < i <= self.x]

                return filtered_row

        elif self.name.lower() == 'b':

            delta_x = where_x - self.x
            delta_y = where_y - self.y

            filtered_diagonal = []
            step_x = 1 if delta_x > 0 else -1
            step_y = 1 if delta_y > 0 else -1

            for i in range(1, abs(delta_x) + 1):
                passed_x = self.x + i * step_x
                passed_y = self.y + i * step_y
                filtered_diagonal.append(Figure.uncolor_cell(Field.board[passed_y][passed_x]))
            return filtered_diagonal

        else:

            return {'.'}


    def threatened_figures(self):

        figure_classes = {'P': Pawn, 'K': King, 'Q': Queen, 'N': Knight, 'R': Rook, 'B': Bishop, 'S': SuperPawn,
                          'J': Ninja, 'H': Phoenix,
                          'p': Pawn, 'k': King, 'q': Queen, 'n': Knight, 'r': Rook, 'b': Bishop, 's': SuperPawn,
                          'j': Ninja, "h": Phoenix}

        for y in range(1, 9):
            for x in range(8):

                if Field.board[y][x] != '.' and Field.board[y][x].islower() == self.name.islower():
                    threat_fig = figure_classes[Field.board[y][x]](Field.board[y][x], x, y)
                    threat_cells = threat_fig.get_possible_steps()

                    for coord in threat_cells:
                        threat_cell = Field.board[coord[1]][coord[0]]


                        if (threat_cell != '.' and threat_cell.islower() != Field.board[y][x].islower() and
                                len(set(threat_fig.get_passed_cells(coord[0], coord[1])) - {'.'}) <= 1):
                            Field.board[y][x] = '\033[0;37;41m' + Field.board[y][x] + '\033[0m'


    def get_steps(self):
        figure_classes = {'P': Pawn, 'K': King, 'Q': Queen, 'N': Knight, 'R': Rook, 'B': Bishop, 'S': SuperPawn, 'J': Ninja,
                          'H': Phoenix,
                          'p': Pawn, 'k': King, 'q': Queen, 'n': Knight, 'r': Rook, 'b': Bishop, 's': SuperPawn, 'j': Ninja,
                          "h": Phoenix}

        self.current_class = figure_classes[self.name](self.name, self.x, self.y)
        self.steps = self.current_class.get_possible_steps()
        self.filtered = []

        for coord in self.steps:

            ex, ey = coord[0], coord[1]
            fig_in = Field.board[ey][ex]

            if fig_in == '.':
                self.filtered.append([ex, ey])

            elif fig_in.isupper() == self.name.isupper():
                continue
            elif fig_in.isupper() != self.name.isupper():
                self.filtered.append([ex, ey])

        return self.filtered


class Pawn(Figure):

    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.pawns = {'W': [[self.x, y + 1], [self.x, self.y + 2]] if self.y == 2 else [[self.x, self.y + 1]],
             'B': [[self.x, self.y - 1], [self.x, self.y - 2]] if self.y == 7 else [[self.x, self.y - 1]]}
        self.kill_steps = {'W': [[self.x + 1, self.y + 1], [self.x - 1, self.y + 1]],
                     'B': [[self.x - 1, self.y - 1], [self.x + 1, self.y - 1]]}

        self.colored = self.pawns[self.color]# фильтруем возможные ходы по цвету
        self.kill_check()

    def kill_check(self): # проверим, можем ли съесть кого либо
        self.filtered_kill = [coord for coord in self.kill_steps[self.color] if
                              0 <= coord[0] <= 7 and 1 <= coord[1] <= 8]
        for coord in self.filtered_kill:
            e_x, e_y = coord[0], coord[1]
            if Field.board[e_y][e_x] != '.':
                self.colored.append([e_x, e_y])

    def get_possible_steps(self):
        self.colored = [coord for coord in self.colored if 0 <= coord[0] <= 8 and 1 <= coord[1] <= 8]
        return self.colored

class King(Figure):

    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.colored = [[x - 1, y - 1], [x - 1, y], [x - 1, y + 1], [x, y - 1], [x, y + 1], [x + 1, y - 1], [x + 1, y],
              [x + 1, y + 1]]

    def get_possible_steps(self):
        self.colored = [coord for coord in self.colored if 0 <= coord[0] <= 7 and 1 <= coord[1] <= 8]
        return self.colored

class Queen(Figure):

    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.colored = self.queen_moves()

    def queen_moves(self):
        var_moves = []

        # horizontal
        for i in range(8):

            if i != self.x:
                var_moves.append([i, self.y])

        # vertical
        for i in range(9):
            if i != self.y:
                var_moves.append([self.x, i])

        # diagonal
        for i in range(1, 8):

            if 0 <= self.x + i <= 8 and 0 <= self.y + i <= 8:
                var_moves.append([self.x + i, self.y + i])

            if 0 <= self.x - i <= 8 and 0 <= self.y - i <= 8:
                var_moves.append([self.x - i, self.y - i])

            if 0 <= self.x + i <= 8 and 0 <= self.y - i <= 8:
                var_moves.append([self.x + i, self.y - i])

            if 0 <= self.x - i <= 8 and 0 <= self.y + i <= 8:
                var_moves.append([self.x - i, self.y + i])

        return var_moves

    def get_possible_steps(self):
        self.colored = [coord for coord in self.colored if 0 <= coord[0] <= 7 and 1 <= coord[1] <= 8]
        return self.colored

class Rook(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.colored = self.rook_moves()

    def rook_moves(self):

        var_moves = []

         # horizontal
        for i in range(8):

            if i != self.x:
                var_moves.append([i, self.y])

        # vertical
        for i in range(9):
            if i != self.y:
                var_moves.append([self.x, i])

        return var_moves

    def get_possible_steps(self):
        self.colored = [coord for coord in self.colored if 0 <= coord[0] <= 7 and 1 <= coord[1] <= 8]
        return self.colored

class Bishop(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.colored = self.bishop_moves()

    def bishop_moves(self):
        var_moves = []

        # diagonal
        for i in range(1, 8):

            if 0 <= self.x + i <= 8 and 0 <= self.y + i <= 8:
                var_moves.append([self.x + i, self.y + i])

            if 0 <= self.x - i <= 8 and 0 <= self.y - i <= 8:
                var_moves.append([self.x - i, self.y - i])

            if 0 <= self.x + i <= 8 and 0 <= self.y - i <= 8:
                var_moves.append([self.x + i, self.y - i])

            if 0 <= self.x - i <= 8 and 0 <= self.y + i <= 8:
                var_moves.append([self.x - i, self.y + i])

        return var_moves

    def get_possible_steps(self):
        self.colored = [coord for coord in self.colored if 0 <= coord[0] <= 7 and 1 <= coord[1] <= 8]
        return self.colored

class Knight(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.colored = [[x + 1, y + 2], [x + 1, y - 2], [x - 1, y + 2], [x - 1, y - 2], [x + 2, y + 1], [x + 2, y - 1],
        [x - 2, y + 1], [x - 2, y - 1]]

    def get_possible_steps(self):
        self.colored = [coord for coord in self.colored if 0 <= coord[0] <= 7 and 1 <= coord[1] <= 8]
        return self.colored

class SuperPawn(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.pawns = {'W': [[self.x, y + 1], [self.x, self.y + 2]],
                      'B': [[self.x, self.y - 1], [self.x, self.y - 2]]}
        self.kill_steps = {'W': [[self.x + 1, self.y + 1], [self.x - 1, self.y + 1],
                                 [self.x + 1, self.y + 2], [self.x - 1, self.y + 2]],
                           'B': [[self.x - 1, self.y - 1], [self.x + 1, self.y - 1],
                                 [self.x - 1, self.y - 2], [self.x + 1, self.y - 2]]}
        self.colored = self.pawns[self.color]  # фильтруем возможные ходы по цвету
        self.kill_check()

    def kill_check(self):  # проверим, можем ли съесть кого либо
        self.filtered_kill = [coord for coord in self.kill_steps[self.color]  if 0 <= coord[0] <= 7 and 1 <= coord[1] <= 8]
        for coord in self.filtered_kill:
            e_x, e_y = coord[0], coord[1]
            if Field.board[e_y][e_x] != '.':
                self.colored.append([e_x, e_y])

    def get_possible_steps(self):
        self.colored = [coord for coord in self.colored if 0 <= coord[0] <= 7 and 1 <= coord[1] <= 8]
        return self.colored

class Ninja(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.colored = [[self.x + 1, self.y + 1], [self.x + 1, self.y - 1], [self.x - 1, self.y - 1],
                        [self.x - 1, self.y + 1]]

    def get_possible_steps(self):
        self.colored = [coord for coord in self.colored if 0 <= coord[0] <= 7 and 1 <= coord[1] <= 8]
        return self.colored

class Phoenix(Figure):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.colored = [[self.x + 1, self.y + 1], [self.x + 1, self.y - 1], [self.x - 1, self.y - 1],
                        [self.x - 1, self.y + 1], [self.x, self.y + 1], [self.x, self.y - 1], [self.x + 1, self.y],
                        [self.x - 1, self.y - 1], [self.x - 1, self.y]]

    def get_possible_steps(self):
        self.colored = [coord for coord in self.colored if 0 <= coord[0] <= 7 and 1 <= coord[1] <= 8]
        return self.colored

Field = Field() # make field class
while True:


    Field.print() # print field
    figure_picked, start_x, start_y = Field.step_input() # taking figure
    CurF = Figure(figure_picked, start_x, start_y)

    available_steps = CurF.get_steps() # got possible steps
    CurF.threatened_figures() # threatened figures
    Field.color(available_steps) # colored
    Field.make_step(figure_picked, available_steps, start_x, start_y) # make step
    Field.uncolor()
    Field.change_turn()

    Field.update() 
