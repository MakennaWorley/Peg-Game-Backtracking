from copy import deepcopy as copy
import argparse
from animation import draw


class Node():
    def __init__(self, board, jumpfrom=None, jumpover=None, jumpto=None):
        self.board = board
        self.jumpfrom = jumpfrom
        self.jumpover = jumpover
        self.jumpto = jumpto


class peg:
    def __init__(self, start_row, start_col, rule):
        self.size = 5
        self.start_row, self.start_col, self.rule = start_row, start_col, rule
        # board
        self.board = [[1 for j in range(i + 1)] for i in range(self.size)]
        self.board[start_row][start_col] = 0
        self.start = Node(copy(self.board))
        # path
        self.path = [self.start]
        # Do some initialization work here if you need:

    def draw(self):
        if self.success():
            draw(self.path, self.start_row, self.start_col, self.rule)
        else:
            print("No solution were found!")

    def success(self):
        total = 0

        for row in self.board:
            total += sum(row)

        if total == 1:
            if self.rule == 1 and self.path[-1].jumpto != (self.start_row, self.start_col):
                return False
            return True
        return False

    def solve(self):
        if self.success():
            return True

        row_change = [-2, -2, 0, 0, 2, 2]
        col_change = [0, -2, -2, 2, 0, 2]

        board_copy = copy(self.board)

        for x, row in enumerate(self.board):
            for y, col in enumerate(row):
                if col != 1:
                    continue

                for i in range(6):
                    vertex_of_0 = (x + row_change[i], y + col_change[i])
                    jump_over_location = (x + row_change[i] // 2, y + col_change[i] // 2)

                    if not (0 <= vertex_of_0[0] < len(self.board) and
                            0 <= vertex_of_0[1] < len(self.board[vertex_of_0[0]])):
                        continue

                    if (self.board[jump_over_location[0]][jump_over_location[1]] != 1 or
                            self.board[vertex_of_0[0]][vertex_of_0[1]] != 0):
                        continue

                    new_board = copy(self.board)
                    new_board[x][y] = 0
                    new_board[jump_over_location[0]][jump_over_location[1]] = 0
                    new_board[vertex_of_0[0]][vertex_of_0[1]] = 1
                    n_board = Node(new_board, (x, y), jump_over_location, vertex_of_0)

                    self.board = n_board.board
                    self.path.append(n_board)

                    if self.solve():
                        return True

                    self.board = board_copy
                    self.path.pop()

        return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='peg game')

    parser.add_argument('-hole', dest='position', required=True, nargs='+', type=int,
                        help='initial position of the hole')
    parser.add_argument('-rule', dest='rule', required=True, type=int, help='index of rule')

    args = parser.parse_args()

    start_row, start_col = args.position
    if start_row > 4:
        print("row must be less or equal than 4")
        exit()
    if start_col > start_row:
        print("y must be less or equal than row")
        exit()

    # Example:
    # python peg.py -hole 0 0 -rule 0
    game = peg(start_row, start_col, args.rule)
    game.solve()
    game.draw()
