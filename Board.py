from Coordinates import Coordinates
from Cell import Cell
from termcolor import colored, cprint
from AI import AI

class Board:
    def __init__(self, b_or_w):
        self.grid = []
        for row in range(8):
            self.grid.append([])
            for col in range(8):
                coordinates = Coordinates(row, col)
                cell = Cell(coordinates,"-")
                self.grid[row].append(cell)
        if b_or_w == "B":
            self.grid[3][3].setSymbol("B")
            self.grid[3][4].setSymbol("W")
            self.grid[4][4].setSymbol("B")
            self.grid[4][3].setSymbol("W")
        if b_or_w == "W":
            self.grid[3][3].setSymbol("W")
            self.grid[3][4].setSymbol("B")
            self.grid[4][4].setSymbol("W")
            self.grid[4][3].setSymbol("B")

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

        #check below cell
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

    def AI_move(self, intelligence, player_symbol):

        moves = intelligence.generate_moves(self.grid)
        if moves == []:
            print("No moves available")
            return

        best_move = intelligence.determine_best_move()
        coordinates = best_move.getCoordinates()
        row = coordinates.getRow()
        col = coordinates.getCol()
        self.make_move(row, col, player_symbol)

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

def symbol_toggle(player_symbol):
    if player_symbol == "B":
        return "W"
    elif player_symbol == "W":
        return "B"
    else:
        return True