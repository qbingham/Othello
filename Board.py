from Coordinates import Coordinates
from Cell import Cell
import time
from termcolor import colored, cprint
from AIBoard import AIBoard
from copy import deepcopy

class Board:
    def __init__(self, b_or_w):
        self.grid = []
        for row in range(8):
            self.grid.append([])
            for col in range(8):
                coordinates = Coordinates(row, col)
                cell = Cell(coordinates,"-")
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

        self.current_moves = []

        self.weight_grid = [[1616, -303, 99, 43, 43, 99, -303, 1616],
                            [-412, -581, -8, -27, -27, -8, -581, -412],
                            [133, -4, 51, 7, 7, 51, -4, 133],
                            [63, -18, -4, -1, -1, -4, -18, 63],
                            [63, -18, -4, -1, -1, -4, -18, 63],
                            [133, -4, 51, 7, 7, 51, -4, 133],
                            [-412, -581, -8, -27, -27, -8, -581, -412],
                            [1616, -303, 99, 43, 43, 99, -303, 1616]]
        self.late_tree = {}
        self.mid_tree = {}
        self.node_list = []

    def is_valid_move(self, cell, player_symbol):

        emptycell = self.check_for_empty_cell(cell)

        topvert = self.check_top_vertical(cell, player_symbol)
        botvert = self.check_bottom_vertical(cell, player_symbol)

        lefthoriz = self.check_left_horizontal(cell, player_symbol)
        righthoriz = self.check_right_horizontal(cell, player_symbol)

        topleft = self.check_top_left_diagonal(cell,player_symbol)
        topright = self.check_top_right_diagonal(cell,player_symbol)

        botleft = self.check_bot_left_diagonal(cell,player_symbol)
        botright = self.check_bot_right_diagonal(cell,player_symbol)

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

    def check_top_vertical(self, cell, player_symbol):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on top perimeter do not go further
        if row == 0:
            return False

        # check above cell
        i = row - 1
        if self.grid[i][col].__str__() == symbol_toggle(player_symbol):
            while i >= 0:
                if self.grid[i][col].__str__() == "-":
                    break
                if self.grid[i][col].__str__() == player_symbol:
                    return True
                i = i - 1
        return False

    def check_bottom_vertical(self, cell, player_symbol):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on bottom perimeter do not go further
        if row == 7:
            return False

        # check below cell
        i = row + 1
        if self.grid[i][col].__str__() == symbol_toggle(player_symbol):
            i = i + 1
            while i < 8:
                if self.grid[i][col].__str__() == "-":
                    break
                if self.grid[i][col].__str__() == player_symbol:
                    return True
                i = i + 1
        return False

    def check_left_horizontal(self, cell, player_symbol):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on left perimeter do not go further
        if col == 0:
            return False

        # check left of cell
        i = col - 1
        if self.grid[row][i].__str__() == symbol_toggle(player_symbol):
            i = i - 1
            while i >= 0:
                if self.grid[row][i].__str__() == "-":
                    break
                if self.grid[row][i].__str__() == player_symbol:
                    return True
                i = i - 1
        return False

    def check_right_horizontal(self, cell, player_symbol):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on right perimeter do not go further
        if col == 7:
            return False

        # check right of cell
        i = col + 1
        if self.grid[row][i].__str__() == symbol_toggle(player_symbol):
            i = i + 1
            while i < 8:
                if self.grid[row][i].__str__() == "-":
                    break
                if self.grid[row][i].__str__() == player_symbol:
                    return True
                i = i + 1
        return False

    def check_top_left_diagonal(self, cell, player_symbol):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on top left corner do not go further
        if row == 0 or col == 0:
            return False

        # check top left diagonal
        i = row - 1
        j = col - 1
        if self.grid[i][j].__str__() == symbol_toggle(player_symbol):
            i = i - 1
            j = j - 1
            while i >= 0 and j >= 0:
                if self.grid[i][j].__str__() == "-":
                    break
                if self.grid[i][j].__str__() == player_symbol:
                    return True
                i = i - 1
                j = j - 1
        return False

    def check_top_right_diagonal(self, cell, player_symbol):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on the bottom or right perimeter do not go further
        if row == 0 or col == 7:
            return False

        # check top right diagonal
        i = row - 1
        j = col + 1
        if self.grid[i][j].__str__() == symbol_toggle(player_symbol):
            i = i - 1
            j = j + 1
            while i >= 0 and j < 8:
                if self.grid[i][j].__str__() == "-":
                    break
                if self.grid[i][j].__str__() == player_symbol:
                    return True
                i = i - 1
                j = j + 1
        return False

    def check_bot_left_diagonal(self, cell, player_symbol):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        # if cell is on the bottom or left perimeter do not go further
        if row == 7 or col == 0:
            return False

        # check bottom left diagonal
        i = row + 1
        j = col - 1
        if self.grid[i][j].__str__() == symbol_toggle(player_symbol):
            i = i + 1
            j = j - 1
            while i < 8 and j >= 0:
                if self.grid[i][j].__str__() == "-":
                    break
                if self.grid[i][j].__str__() == player_symbol:
                    return True
                i = i + 1
                j = j - 1
        return False

    def check_bot_right_diagonal(self, cell, player_symbol):
        row = cell.getCoordinates().getRow()
        col = cell.getCoordinates().getCol()

        if row == 7 or col == 7:
            return False

        # check bottom right diagonal
        i = row + 1
        j = col + 1
        if self.grid[i][j].__str__() == symbol_toggle(player_symbol):
            i = i + 1
            j = j + 1
            while i < 8 and j < 8:
                if self.grid[i][j].__str__() == "-":
                    break
                if self.grid[i][j].__str__() == player_symbol:
                    return True
                i = i + 1
                j = j + 1
        return False

    def gameOver(self):
        for row in self.grid:
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

    def make_move(self, row, col, player_symbol):
        for move_row in self.grid:
            for move_cell in move_row:
                move_cell.setRecentMove(False)

        cell = self.grid[row][col]

        topvert = self.check_top_vertical(cell, player_symbol)
        botvert = self.check_bottom_vertical(cell, player_symbol)

        lefthoriz = self.check_left_horizontal(cell, player_symbol)
        righthoriz = self.check_right_horizontal(cell, player_symbol)

        topleft = self.check_top_left_diagonal(cell, player_symbol)
        topright = self.check_top_right_diagonal(cell, player_symbol)

        botleft = self.check_bot_left_diagonal(cell, player_symbol)
        botright = self.check_bot_right_diagonal(cell, player_symbol)

        self.grid[row][col].setSymbol(player_symbol)
        self.grid[row][col].setRecentMove(True)

        if topvert:
            i = row - 1
            while self.grid[i][col].__str__() != player_symbol:
                self.grid[i][col].setSymbol(player_symbol)
                self.grid[i][col].setRecentMove(True)
                i -= 1

        if botvert:
            i = row + 1
            while self.grid[i][col].__str__() != player_symbol:
                self.grid[i][col].setSymbol(player_symbol)
                self.grid[i][col].setRecentMove(True)
                i += 1

        if lefthoriz:
            j = col - 1
            while self.grid[row][j].__str__() != player_symbol:
                self.grid[row][j].setSymbol(player_symbol)
                self.grid[row][j].setRecentMove(True)
                j -= 1

        if righthoriz:
            j = col + 1
            while self.grid[row][j].__str__() != player_symbol:
                self.grid[row][j].setSymbol(player_symbol)
                self.grid[row][j].setRecentMove(True)
                j += 1

        if topleft:
            i = row - 1
            j = col - 1
            while self.grid[i][j].__str__() != player_symbol:
                self.grid[i][j].setSymbol(player_symbol)
                self.grid[i][j].setRecentMove(True)
                i -= 1
                j -= 1

        if topright:
            i = row - 1
            j = col + 1
            while self.grid[i][j].__str__() != player_symbol:
                self.grid[i][j].setSymbol(player_symbol)
                self.grid[i][j].setRecentMove(True)
                i -= 1
                j += 1

        if botleft:
            i = row + 1
            j = col - 1
            while self.grid[i][j].__str__() != player_symbol:
                self.grid[i][j].setSymbol(player_symbol)
                self.grid[i][j].setRecentMove(True)
                i += 1
                j -= 1

        if botright:
            i = row + 1
            j = col + 1
            while self.grid[i][j].__str__() != player_symbol:
                self.grid[i][j].setSymbol(player_symbol)
                self.grid[i][j].setRecentMove(True)
                i += 1
                j += 1

    def display(self):
        rownum = 0
        print("   A  B  C  D  E  F  G  H")
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

    def get_score(self):
        w_score = 0
        b_score = 0
        for row in self.grid:
            for cell in row:
                if cell.getSymbol() == "W":
                    w_score += 1
                elif cell.getSymbol() == "B":
                    b_score += 1
        score_tuple = (w_score, b_score)
        return score_tuple

    def AI_early_move(self, player_symbol):
        moves = self.generate_moves(self.grid, player_symbol)
        if moves == []:
            print("No moves available")
            return

        best_move = self.determine_best_move()
        coordinates = best_move.getCoordinates()
        row = coordinates.getRow()
        col = coordinates.getCol()

        self.make_move(row, col, player_symbol)

    def AI_mid_move(self, player_symbol):
        ai_board = AIBoard(player_symbol)
        self.node_list = []
        self.mid_tree = {}
        depth = 5
        grid = deepcopy(self.grid)
        self.mid_tree.update({"": self.generate_mid_tree(player_symbol, depth, ai_board, grid)})
        # self.mid_tree[""] = self.generate_mid_tree(player_symbol, depth, ai_board, self.grid)

        maxVal = self.maxVal(self.mid_tree, "", 'null', 'null')

        possible_moves = self.generate_moves(self.grid, player_symbol)
        print(len(possible_moves))
        best_move = possible_moves[0].getCoordinates()
        index = 0
        for node in self.node_list:
            if isinstance(node, float):
                if node == maxVal:
                    break
            index += 1
        for i in range(index):
            if self.node_list[i] in possible_moves:
                best_move = self.node_list[i]

        row = best_move.getRow()
        col = best_move.getCol()

        self.current_moves = deepcopy(possible_moves)

        if (row == 0 and (col == 1 or col == 6)) or (row == 1 and (col == 1 or col == 6 or col == 0 or col == 7)) or \
                (row == 6 and (col == 1 or col == 6 or col == 0 or col == 7)) or (row == 7 and (col == 1 or col == 6)):
            self.AI_early_move(player_symbol)
        else:
            self.make_move(row, col, player_symbol)

    def maxVal(self, graph, node, alpha, beta):
        self.node_list.append(node)
        if isinstance(graph.get(node), int):
            return graph.get(node)
        else:
            v = float("-inf")
            for child in graph.get(node):
                v1 = self.minVal(graph, child, alpha, beta)
                if v == 'null' or v1 > v:
                    v = v1
                if beta != 'null':
                    if v1 >= beta:
                        return v
                if alpha == 'null' or v1 > alpha:
                    alpha = v1
            return v
        # if isinstance(node, int):
        #     return node
        # else:
        #     v = float("-inf")
        #     for child in graph.get(node):
        #         v1 = self.minVal(graph, child, alpha, beta)
        #         if v == 'null' or v1 > v:
        #             v = v1
        #         if beta != 'null':
        #             if v1 >= beta:
        #                 return v
        #         if alpha == 'null' or v1 > alpha:
        #             alpha = v1
        #     return v

    def minVal(self, graph, node, alpha, beta):
        self.node_list.append(node)
        if isinstance(graph.get(node), int):
            return graph.get(node)
        else:
            v = float("inf")
            for child in graph.get(node):
                v1 = self.maxVal(graph, child, alpha, beta)
                if v == 'null' or v1 < v:
                    v = v1
                if alpha != 'null':
                    if v1 <= alpha:
                        return v
                if beta == 'null' or v1 < beta:
                    beta = v1
            return v

    def generate_mid_tree(self, player_symbol, depth, ai_board, grid):

        if depth <= 1:
            moves = ai_board.generate_moves(grid, symbol_toggle(player_symbol))
            total_value = 0
            for move in moves:
                coordinate = move.getCoordinates()
                row = coordinate.getRow()
                col = coordinate.getCol()
                total_value += self.weight_grid[row][col]
            return total_value
        else:
            moves = ai_board.generate_moves(grid, player_symbol)
            coordinates = []
            for move in moves:
                coordinate = move.getCoordinates()
                coordinates.append(coordinate)
            for move in moves:
                coordinate = move.getCoordinates()
                row = coordinate.getRow()
                col = coordinate.getCol()
                self.mid_tree.update({coordinate: self.generate_mid_tree(symbol_toggle(player_symbol),
                                                                         depth-1, ai_board,
                                                                         ai_board.make_move(row, col, player_symbol, grid))})
                # self.mid_tree[coordinate] = self.generate_mid_tree(symbol_toggle(player_symbol),
                #                                                              depth-1, ai_board,
                #                                                            ai_board.make_move(row, col, player_symbol, grid))
            return coordinates

    def AI_late_move(self, player_symbol, turn):
        self.generate_late_tree(player_symbol, turn)
        self.node_list = []
        maxVal = self.maxVal(self.late_tree, "", 'null', 'null')

        possible_moves = self.generate_moves(self.grid, player_symbol)
        best_move = possible_moves[0].getCoordinates()
        index = 0
        for node in self.node_list:
            if isinstance(node, int):
                if node == maxVal:
                    break
            index += 1
        for i in range(index):
            if self.node_list[i] in possible_moves:
                best_move = self.node_list[i]

        row = best_move.getRow()
        col = best_move.getCol()

        if (row == 0 and (col == 1 or col == 6)) or (row == 1 and (col == 1 or col == 6 or col == 0 or col == 7)) or \
                (row == 6 and (col == 1 or col == 6 or col == 0 or col == 7)) or (row == 7 and (col == 1 or col == 6)):
            self.AI_early_move(player_symbol)
        else:
            self.make_move(row, col, player_symbol)

    def generate_late_tree(self, player_symbol, turn):
        ai_board = AIBoard(player_symbol)
        grid = deepcopy(self.grid)
        self.late_tree.update({"": self.generate_late_tree_helper(player_symbol, grid, ai_board, turn)})
        # self.late_tree[""] = self.generate_late_tree_helper(player_symbol, self.grid, ai_board, turn)

    def generate_late_tree_helper(self, player_symbol, grid, ai_board, turn):
        if turn >= 62:
            score_tuple = ai_board.get_score(grid)
            if self.AI_symbol == "W":
                return score_tuple[0]
            else:
                return score_tuple[1]
        moves = ai_board.generate_moves(grid, player_symbol)
        opponent_moves = ai_board.generate_moves(grid, symbol_toggle(player_symbol))
        coordinates = []
        if opponent_moves == []:
            for move in moves:
                coordinate = move.getCoordinates()
                coordinates.append(coordinate)
            for move in moves:
                coordinate = move.getCoordinates()
                row = coordinate.getRow()
                col = coordinate.getCol()
                self.late_tree.update({coordinate: self.generate_late_tree_helper(player_symbol,
                                                                                  ai_board.make_move(row, col, player_symbol, grid),
                                                                                  ai_board, turn+1)})
                # self.late_tree[coordinate] = self.generate_late_tree_helper(player_symbol,
                #                                                             ai_board.make_move(row, col, player_symbol, grid),
                #                                                             ai_board, turn + 1)
        else:
            for move in moves:
                coordinate = move.getCoordinates()
                coordinates.append(coordinate)
            for move in moves:
                coordinate = move.getCoordinates()
                row = coordinate.getRow()
                col = coordinate.getCol()
                self.late_tree.update({coordinate: self.generate_late_tree_helper(symbol_toggle(player_symbol),
                                                                                  ai_board.make_move(row, col, player_symbol, grid),
                                                                                  ai_board, turn + 1)})
                # self.late_tree[coordinate] = self.generate_late_tree_helper(symbol_toggle(player_symbol),
                #                                                             ai_board.make_move(row, col, player_symbol, grid),
                #                                                             ai_board, turn + 1)
        return coordinates

    def generate_moves(self, board, player_symbol):
        valid_moves = []
        for row in board:
            for cell in row:
                if self.is_valid_move(cell, player_symbol):
                    valid_moves.append(cell)
        self.current_moves = deepcopy(valid_moves)
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

    def no_valid_moves(self, player_symbol):
        for row in self.grid:
            for cell in row:
                if self.is_valid_move(cell, player_symbol):
                    return False
        return True

def symbol_toggle(player_symbol):
    if player_symbol == "B":
        return "W"
    elif player_symbol == "W":
        return "B"
    else:
        return True
