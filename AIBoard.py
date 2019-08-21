from Coordinates import Coordinates
from Cell import Cell
import time
from termcolor import colored, cprint

class AIBoard:

    def __init__(self, b_or_w):
        self.grid = []
        for row in range(8):
            self.grid.append([])
            for col in range(8):
                coordinates = Coordinates(row, col)
                cell = Cell(coordinates, "-")
                self.grid[row].append(cell)
        self.AI_symbol = ""
        if b_or_w == "B":
            self.grid[3][3].setSymbol("B")
            self.grid[3][4].setSymbol("W")
            self.grid[4][4].setSymbol("B")
            self.grid[4][3].setSymbol("W")
            self.AI_symbol = "W"
        if b_or_w == "W":
            self.grid[3][3].setSymbol("W")
            self.grid[3][4].setSymbol("B")
            self.grid[4][4].setSymbol("W")
            self.grid[4][3].setSymbol("B")
            self.AI_symbol = "B"

        self.graph = {}

        self.weight_grid = [[16.16, -3.03, 0.99, 0.43, 0.43, 0.99, -3.03, 16.16],
                            [-4.12, -5.81, -0.08, -0.27, -0.27, -0.08, -5.81, -4.12],
                            [1.33, -0.04, 0.51, 0.07, 0.07, 0.51, -0.04, 1.33],
                            [0.63, -0.18, -0.04, -0.01, -0.01, -0.04, -0.18, 0.63],
                            [0.63, -0.18, -0.04, -0.01, -0.01, -0.04, -0.18, 0.63],
                            [1.33, -0.04, 0.51, 0.07, 0.07, 0.51, -0.04, 1.33],
                            [-4.12, -5.81, -0.08, -0.27, -0.27, -0.08, -5.81, -4.12],
                            [16.16, -3.03, 0.99, 0.43, 0.43, 0.99, -3.03, 16.16]]

    def generate_move_tree(self, player_symbol, grid, coordinates, depth):
        if self.gameOver(grid) or depth == 0:
            return

        # if player_symbol == "W":
        #     move_list = self.generate_moves_coordinates(grid, player_symbol)
        #     for move in move_list:
        #         row = move.getRow()
        #         col = move.getCol()
        #         state_prime = self.make_move(row, col, player_symbol, grid)
        #         self.generate_move_tree(symbol_toggle(player_symbol), state_prime, depth-1)

        children = self.generate_moves_coordinates(grid, player_symbol)
        self.graph[coordinates] = children

        for child in children:
            self.generate_move_tree(symbol_toggle(player_symbol), grid, child, depth-1)


    def is_valid_move(self, cell, player_symbol, grid):

        emptycell = self.check_for_empty_cell(cell)

        topvert = self.check_top_vertical(cell, player_symbol, grid)
        botvert = self.check_bottom_vertical(cell, player_symbol, grid)

        lefthoriz = self.check_left_horizontal(cell, player_symbol, grid)
        righthoriz = self.check_right_horizontal(cell, player_symbol, grid)

        topleft = self.check_top_left_diagonal(cell, player_symbol, grid)
        topright = self.check_top_right_diagonal(cell, player_symbol, grid)

        botleft = self.check_bot_left_diagonal(cell, player_symbol, grid)
        botright = self.check_bot_right_diagonal(cell, player_symbol, grid)

        if emptycell and (topvert or botvert or lefthoriz or righthoriz
                          or topleft or topright or botleft or botright):
            return True
        else:
            return False

    def check_for_empty_cell(self, cell):
        sym = cell
        # check for empty cell
        if cell.__str__() == "-":
            return True
        else:
            return False

    def check_top_vertical(self, cell, player_symbol, grid):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on top perimeter do not go further
        if row == 0:
            return False

        # check above cell
        i = row - 1
        if grid[i][col].__str__() == symbol_toggle(player_symbol):
            while i >= 0:
                if grid[i][col].__str__() == "-":
                    break
                if grid[i][col].__str__() == player_symbol:
                    return True
                i = i - 1
        return False

    def check_bottom_vertical(self, cell, player_symbol, grid):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on bottom perimeter do not go further
        if row == 7:
            return False

        # check below cell
        i = row + 1
        if grid[i][col].__str__() == symbol_toggle(player_symbol):
            i = i + 1
            while i < 8:
                if grid[i][col].__str__() == "-":
                    break
                if grid[i][col].__str__() == player_symbol:
                    return True
                i = i + 1
        return False

    def check_left_horizontal(self, cell, player_symbol, grid):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on left perimeter do not go further
        if col == 0:
            return False

        # check left of cell
        i = col - 1
        if grid[row][i].__str__() == symbol_toggle(player_symbol):
            i = i - 1
            while i >= 0:
                if grid[row][i].__str__() == "-":
                    break
                if grid[row][i].__str__() == player_symbol:
                    return True
                i = i - 1
        return False

    def check_right_horizontal(self, cell, player_symbol, grid):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on right perimeter do not go further
        if col == 7:
            return False

        # check right of cell
        i = col + 1
        if grid[row][i].__str__() == symbol_toggle(player_symbol):
            i = i + 1
            while i < 8:
                if grid[row][i].__str__() == "-":
                    break
                if grid[row][i].__str__() == player_symbol:
                    return True
                i = i + 1
        return False

    def check_top_left_diagonal(self, cell, player_symbol, grid):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on top left corner do not go further
        if row == 0 or col == 0:
            return False

        # check top left diagonal
        i = row - 1
        j = col - 1
        if grid[i][j].__str__() == symbol_toggle(player_symbol):
            i = i - 1
            j = j - 1
            while i >= 0 and j >= 0:
                if grid[i][j].__str__() == "-":
                    break
                if grid[i][j].__str__() == player_symbol:
                    return True
                i = i - 1
                j = j - 1
        return False

    def check_top_right_diagonal(self, cell, player_symbol, grid):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on the bottom or right perimeter do not go further
        if row == 0 or col == 7:
            return False

        # check top right diagonal
        i = row - 1
        j = col + 1
        if grid[i][j].__str__() == symbol_toggle(player_symbol):
            i = i - 1
            j = j + 1
            while i >= 0 and j < 8:
                if grid[i][j].__str__() == "-":
                    break
                if grid[i][j].__str__() == player_symbol:
                    return True
                i = i - 1
                j = j + 1
        return False

    def check_bot_left_diagonal(self, cell, player_symbol, grid):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on the bottom or left perimeter do not go further
        if row == 7 or col == 0:
            return False

        # check bottom left diagonal
        i = row + 1
        j = col - 1
        if grid[i][j].__str__() == symbol_toggle(player_symbol):
            i = i + 1
            j = j - 1
            while i < 8 and j >= 0:
                if grid[i][j].__str__() == "-":
                    break
                if grid[i][j].__str__() == player_symbol:
                    return True
                i = i + 1
                j = j - 1
        return False

    def check_bot_right_diagonal(self, cell, player_symbol, grid):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        if row == 7 or col == 7:
            return False

        # check bottom right diagonal
        i = row + 1
        j = col + 1
        if grid[i][j].__str__() == symbol_toggle(player_symbol):
            i = i + 1
            j = j + 1
            while i < 8 and j < 8:
                if grid[i][j].__str__() == "-":
                    break
                if grid[i][j].__str__() == player_symbol:
                    return True
                i = i + 1
                j = j + 1
        return False

    def gameOver(self, grid):
        for row in grid:
            for cell in row:
                if cell.getSymbol() == "-":
                    return False
        print("No more available moves!")
        return True

    def get_winner(self):
        b_count = 0
        w_count = 0

        for row in self.grid:
            for col in row:
                if col == "B":
                    b_count += 1
                elif col == "W":
                    w_count += 1

        if b_count > w_count:
            return "B"
        elif w_count > b_count:
            return "W"
        else:
            return "D"

    def make_move(self, row, col, player_symbol, grid):
        for move_row in self.grid:
            for move_cell in move_row:
                move_cell.setRecentMove(False)

        cell = grid[row][col]

        grid_to_return = grid

        topvert = self.check_top_vertical(cell, player_symbol, grid)
        botvert = self.check_bottom_vertical(cell, player_symbol, grid)

        lefthoriz = self.check_left_horizontal(cell, player_symbol, grid)
        righthoriz = self.check_right_horizontal(cell, player_symbol, grid)

        topleft = self.check_top_left_diagonal(cell, player_symbol, grid)
        topright = self.check_top_right_diagonal(cell, player_symbol, grid)

        botleft = self.check_bot_left_diagonal(cell, player_symbol, grid)
        botright = self.check_bot_right_diagonal(cell, player_symbol, grid)

        grid_to_return[row][col].setSymbol(player_symbol)
        grid_to_return[row][col].setRecentMove(True)

        if topvert:
            i = row - 1
            while grid_to_return[i][col].__str__() != player_symbol:
                grid_to_return[i][col].setSymbol(player_symbol)
                grid_to_return[i][col].setRecentMove(True)
                i -= 1

        if botvert:
            i = row + 1
            while grid_to_return[i][col].__str__() != player_symbol:
                grid_to_return[i][col].setSymbol(player_symbol)
                grid_to_return[i][col].setRecentMove(True)
                i += 1

        if lefthoriz:
            j = col - 1
            while grid_to_return[row][j].__str__() != player_symbol:
                grid_to_return[row][j].setSymbol(player_symbol)
                grid_to_return[row][j].setRecentMove(True)
                j -= 1

        if righthoriz:
            j = col + 1
            while grid_to_return[row][j].__str__() != player_symbol:
                grid_to_return[row][j].setSymbol(player_symbol)
                grid_to_return[row][j].setRecentMove(True)
                j += 1

        if topleft:
            i = row - 1
            j = col - 1
            while grid_to_return[i][j].__str__() != player_symbol:
                grid_to_return[i][j].setSymbol(player_symbol)
                grid_to_return[i][j].setRecentMove(True)
                i -= 1
                j -= 1

        if topright:
            i = row - 1
            j = col + 1
            while grid_to_return[i][j].__str__() != player_symbol:
                grid_to_return[i][j].setSymbol(player_symbol)
                grid_to_return[i][j].setRecentMove(True)
                i -= 1
                j += 1

        if botleft:
            i = row + 1
            j = col - 1
            while grid_to_return[i][j].__str__() != player_symbol:
                grid_to_return[i][j].setSymbol(player_symbol)
                grid_to_return[i][j].setRecentMove(True)
                i += 1
                j -= 1

        if botright:
            i = row + 1
            j = col + 1
            while grid_to_return[i][j].__str__() != player_symbol:
                grid_to_return[i][j].setSymbol(player_symbol)
                grid_to_return[i][j].setRecentMove(True)
                i += 1
                j += 1

        return grid_to_return

    def AI_move(self, player_symbol):

        moves = self.generate_moves(self.grid, player_symbol)
        if moves == []:
            print("No moves available")
            return

        best_move = self.determine_best_move()
        coordinates = best_move.getCoordinates()
        row = coordinates.getRow()
        col = coordinates.getCol()
        self.make_move(row, col, player_symbol)

    def generate_moves(self, board, player_symbol):
        valid_moves = []
        for row in board:
            for cell in row:
                if self.is_valid_move(cell, player_symbol, board):
                    valid_moves.append(cell)
        return valid_moves

    def generate_moves_coordinates(self, board, player_symbol):
        valid_moves = []
        for row in board:
            for cell in row:
                if self.is_valid_move(cell, player_symbol, board):
                    valid_moves.append(cell.getCoordinates().__str__())
        return valid_moves

    def determine_best_move(self):
        best_move = self.current_moves[0]
        first_move_coordinates = best_move.getCoordinates()
        first_move_row = first_move_coordinates.getRow()
        first_move_col = first_move_coordinates.getCol()
        best_weight = self.weight_grid[first_move_row][first_move_col]

        for move in self.current_moves:
            coordinates = move.getCoordinates()
            row = coordinates.getRow()
            col = coordinates.getCol()
            if self.weight_grid[row][col] > best_weight:
                best_weight = self.weight_grid[row][col]
                best_move = move

        return best_move

    def display(self):
        rownum = 0
        print("   0  1  2  3  4  5  6  7")
        for row in self.grid:
            print(rownum, " ", end="")
            rownum += 1
            for cell in row:
                if cell.recent_move == True:
                    cprint(cell.__str__(), "red", end="  ")
                else:
                    print(cell.__str__(), end="  ")
            print("")
        score_tuple = self.get_score()
        w_score = score_tuple[0]
        b_score = score_tuple[1]
        print("W: ", w_score, ", B: ", b_score)

    def get_score(self, grid):
        w_score = 0
        b_score = 0
        for row in grid:
            for cell in row:
                if cell.getSymbol() == "W":
                    w_score += 1
                elif cell.getSymbol() == "B":
                    b_score += 1
        score_tuple = (w_score, b_score)
        return score_tuple


def symbol_toggle(player_symbol):
    if player_symbol == "B":
        return "W"
    elif player_symbol == "W":
        return "B"
    else:
        return True