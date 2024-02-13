import time
import os

# король - king
# ферзь - queen
# ладья - rook
# слон - bishop
# конь - kNight
# пешка - pawn

color = 0  # 0 - White 1 - Black
pos_field = {
    8: ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    7: ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    6: ['.', '.', '.', '.', '.', '.', '.', '.'],
    5: ['.', '.', '.', '.', '.', '.', '.', '.'],
    4: ['.', '.', '.', '.', '.', '.', '.', '.'],
    3: ['.', '.', '.', '.', '.', '.', '.', '.'],
    2: ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    1: ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
}


def draw_field():

    global pos_field
    let = '\033[1m' + '   A B C D E F G H' + '\033[0m'

    print(let)

    for row in pos_field:
        print(f'{row:<2}', *pos_field[row], f'{row:>2}')

    print(let)


def upd_field():
    os.system('cls' if os.name == 'nt' else 'clear')


# coordinate metod LN - L1N1
# step format start_pos(LN) where_pos(L1N1)

def let2num(letter):
    let_num = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    return let_num[letter]


def get_possible_steps(fig, x, y):
    def queen_moves(x, y):
        var_moves = []

        # horizontal
        for i in range(8):

            if i != x:
                var_moves.append([i + 1, y])

        # vertical
        for i in range(9):
            if i != y:
                var_moves.append([x + 1, i])

        # diagonal
        for i in range(1, 8):

            if 0 <= x + i <= 8 and 0 <= y + i <= 8:
                var_moves.append([x + i + 1, y + i])

            if 0 <= x - i <= 8 and 0 <= y - i <= 8:
                var_moves.append([x - i + 1, y - i])

            if 0 <= x + i <= 8 and 0 <= y - i <= 8:
                var_moves.append([x + i + 1, y - i])

            if 0 <= x - i <= 8 and 0 <= y + i <= 8:
                var_moves.append([x - i + 1, y + i])

        return var_moves

    def rook_moves(x, y):

        var_moves = []

         # horizontal
        for i in range(8):

            if i != x:
                var_moves.append([i + 1, y])

        # vertical
        for i in range(9):
            if i != y:
                var_moves.append([x + 1, i])

        return var_moves

    def bishop_moves(x, y):

        var_moves = []

        # diagonal
        for i in range(1, 8):

            if 0 <= x + i <= 8 and 0 <= y + i <= 8:
                var_moves.append([x + i + 1, y + i])

            if 0 <= x - i <= 8 and 0 <= y - i <= 8:
                var_moves.append([x - i + 1, y - i])

            if 0 <= x + i <= 8 and 0 <= y - i <= 8:
                var_moves.append([x + i + 1, y - i])

            if 0 <= x - i <= 8 and 0 <= y + i <= 8:
                var_moves.append([x - i + 1, y + i])

        return var_moves

    global pos_field
    variants_unchecked = {

        'P': [[x + 1, y + 1], [x + 1, y + 2]] if y == 2 else [[x + 1, y + 1]],
        'K': [[x - 1, y - 1], [x - 1, y], [x - 1, y + 1], [x, y - 1], [x, y + 1], [x + 1, y - 1], [x + 1, y],
              [x + 1, y + 1]],
        'Q': queen_moves(x, y),
        'N': [[x + 2, y + 2], [x + 2, y - 2], [x, y + 2], [x, y - 2], [x + 3, y + 1], [x + 3, y - 1],
              [x - 1, y + 1], [x - 1, y - 1]],
        'R': rook_moves(x, y),
        'B': bishop_moves(x, y),


        'p': [[x + 1, y - 1], [x + 1, y - 2]] if y==7 else [[x + 1, y - 1]],
        'k': [[x - 1, y - 1], [x - 1, y], [x - 1, y + 1], [x, y - 1], [x, y + 1], [x + 1, y - 1], [x + 1, y],
              [x + 1, y + 1]],
        'q': queen_moves(x, y),
        'n': [[x + 2, y + 2], [x + 2, y - 2], [x, y + 2], [x, y - 2], [x + 3, y + 1], [x + 3, y - 1],
              [x - 1, y + 1], [x - 1, y - 1]],
        'r': rook_moves(x, y),
        'b': bishop_moves(x, y)
    }

    fig_steps = variants_unchecked[fig]
    variants_checked = []

    for comb in fig_steps:
        # проверка на фигуру в клетке

        if 1 <= comb[1] <= 8 and 0 <= comb[0] <= 8:

            fig_in_cell = pos_field[comb[1]][comb[0] - 1]

            if fig_in_cell == '.':
                variants_checked.append(comb)

            elif fig_in_cell != '.' and fig_in_cell.isupper() == fig.isupper():
                continue

            elif fig_in_cell != '.' and fig_in_cell.isupper() != fig.isupper():
                # съедаем фигуру в клетке
                variants_checked.append(comb)

    return variants_checked



def step_input(col_str):

    global pos_field

    start_pos = input(f'Введите координату для выбора фигуры {col_str}: ')

    while len(start_pos) != 2 or start_pos[0] not in 'ABCDEFGH' or start_pos[1] not in '12345678':
        start_pos = input('Координаты введены неправильно. Введите заново: ')


    svert, shor = let2num(start_pos[0]), int(start_pos[1])  # обозначаем численные координаты
    figure_start = pos_field[shor][svert]  # запоминаем тип фигуры

    while len(start_pos) != 2 or start_pos[0] not in 'ABCDEFGH' or start_pos[1] not in '12345678' or figure_start == '.':

        start_pos = input('Выбранная ячейка пуста. Введите координаты для ячейки с фигурой: ')
        svert, shor = let2num(start_pos[0]), int(start_pos[1])
        figure_start = pos_field[shor][svert]

    return figure_start, svert, shor

green = '\033[42m'
bold = '\033[1m'
end = '\033[0m'

def color_field(coords):
    global pos_field

    for comb in coords:

        pos_field[comb[1]][comb[0] - 1] =  green + bold + pos_field[comb[1]][comb[0] - 1] + end

def make_step(fig_st, available_steps, start_x, start_y):
    global pos_field

    def get_passed_cells(figure, where_x, where_y, start_x, start_y):

        global pos_field

        if figure.lower() == 'q':

            if where_x == start_x: # moving on y, x is const

                column = [pos_field[row][where_x] for row in pos_field] # picking vertical
                filtered_column = [column[i] for i in range(len(column)) if start_y < i + 1 <= where_y] # filtering needed cells

                return filtered_column

            elif where_y == start_y: # moving on x

                filtered_row = [pos_field[where_y][i] for i in range(8) if start_x < i <= where_x]
                return filtered_row

            else: # moving on diag
                delta_x =  where_x - start_x
                delta_y =  where_y - start_y

                filtered_diagonal = []
                step_x = 1 if delta_x > 0 else -1
                step_y = 1 if delta_y > 0 else -1

                for i in range(1, abs(delta_x) + 1):
                    passed_x = start_x + i * step_x
                    passed_y = start_y + i * step_y
                    filtered_diagonal.append(pos_field[passed_y][passed_x])

                return filtered_diagonal

        if figure.lower() == 'r':

            if where_x == start_x: # moving on y, x is const

                column = [pos_field[row][where_x] for row in pos_field] # picking vertical
                filtered_column = [column[i] for i in range(len(column)) if start_y < i + 1 <= where_y] # filtering needed cells

                return filtered_column

            elif where_y == start_y: # moving on x

                filtered_row = [pos_field[where_y][i] for i in range(8) if start_x < i <= where_x]
                return filtered_row

        elif figure.lower() == 'b':

            delta_x = where_x - start_x
            delta_y = where_y - start_y

            filtered_diagonal = []
            step_x = 1 if delta_x > 0 else -1
            step_y = 1 if delta_y > 0 else -1

            for i in range(1, abs(delta_x) + 1):
                passed_x = start_x + i * step_x
                passed_y = start_y + i * step_y
                filtered_diagonal.append(pos_field[passed_y][passed_x].replace('\x1b[42m\x1b[1m', '').replace('\x1b[0m', ''))

            return filtered_diagonal

        else:

            return {'.'}

    where_pos = input(f'Введите координату хода: ')

    while len(where_pos) != 2 or where_pos[0] not in 'ABCDEFGH' or where_pos[1] not in '12345678':
        where_pos = input('Координаты введены неправильно. Введите заново: ')

    y = int(where_pos[1])
    x = let2num(where_pos[0])
    fig_end = pos_field[y][x].replace(green, '').replace(bold, '').replace(end, '')

    while (len(where_pos) != 2 or where_pos[0] not in 'ABCDEFGH' or where_pos[1] not in '12345678' or
           [x + 1, y] not in available_steps or fig_end != '.' or
           (fig_end != '.' and fig_end.isupper() == fig_st.isupper()) # доп условие потому что некорректно с черными фигурами и точкой
           or set(get_passed_cells(fig_st, x, y, start_x, start_y)) != {'.'}):
        a = get_passed_cells(fig_st, x, y, start_x, start_y)
        where_pos = input('Данный ход невозможен. Введите координаты заново: ')

        y = int(where_pos[1])
        x = let2num(where_pos[0])
        fig_end = pos_field[y][x]



    pos_field[y][x] = fig_st


def uncolor_field():
    global pos_field

    for row in range(1, 9):
        for el in range(8):
            pos_field[row][el] = pos_field[row][el].replace(green, '').replace(bold, '').replace(end, '')


while True:
    draw_field()

    col_str = 'белых' if color == 0 else 'черных'

    # обработка подсветки позиции
    figure_picked, start_x, start_y = step_input(col_str)
    variety = get_possible_steps(figure_picked, start_x, start_y)

    # удаляем старое поле
    upd_field()

    # красим
    color_field(variety)

    # выводим новое поле
    draw_field()

    # ходим
    make_step(figure_picked, variety, start_x, start_y)

    # ставим стартовую фигуру точкой
    pos_field[start_y][start_x] = '.'

    # сбросим краску
    uncolor_field()

    # изменим игрока
    color = 0 if color == 1 else 1

    # обновим поле
    upd_field()