from Board import Board
from AI import AI

def symbol_toggle(player_symbol):
    if player_symbol == "B":
        return "W"
    elif player_symbol == "W":
        return "B"
    else:
        return True

def main():
    b_or_w = input("Would you prefer W in the top left or B in the top left? (Enter W or B)")
    board = Board(b_or_w)
    turn = 0
    if b_or_w == "B":
        turn = 1

    intelligence = AI(board, symbol_toggle(b_or_w))

    while board.gameOver() == False:
        board.display()
        if turn % 2 == 0:
            player_symbol = "W"
            print("It is W's turn")
            if b_or_w == "B":
                board.AI_move(intelligence, "W")
            else:
                is_sure = "N"
                while is_sure != "Y":
                    row = int(input("Please enter a row: "))
                    col = int(input("Please enter a column: "))
                    cell = board.grid[row][col]
                    valid_move = board.is_valid_move(cell, player_symbol)
                    coordinates = cell.getCoordinates().__str__()
                    while not valid_move:
                        print("Invalid move! ", coordinates ," is not a valid move for ", player_symbol, ".", sep="")
                        row = int(input("Please enter a row: "))
                        col = int(input("Please enter a column: "))
                        cell = board.grid[row][col]
                        valid_move = board.is_valid_move(cell, player_symbol)
                        coordinates = cell.getCoordinates().__str__()
                    sure_string = "Are you sure you want to make the move at "
                    sure_string += str(coordinates) + "? (Y or N)"
                    is_sure = input(sure_string)
                board.make_move(row,col, player_symbol)

        else:
            player_symbol = "B"
            print("It is B's turn")
            if b_or_w == "W":
                board.AI_move(intelligence, "B")
            else:
                is_sure = "N"
                while is_sure != "Y":
                    row = int(input("Please enter a row: "))
                    col = int(input("Please enter a column: "))
                    cell = board.grid[row][col]
                    valid_move = board.is_valid_move(cell, player_symbol)
                    coordinates = cell.getCoordinates().__str__()
                    while not valid_move:
                        print("Invalid move! ", coordinates, " is not a valid move for ", player_symbol, ".", sep="")
                        row = int(input("Please enter a row: "))
                        col = int(input("Please enter a column: "))
                        cell = board.grid[row][col]
                        valid_move = board.is_valid_move(cell, player_symbol)
                        coordinates = cell.getCoordinates().__str__()
                    sure_string = "Are you sure you want to make the move at "
                    sure_string += str(coordinates) + "? (Y or N)"
                    is_sure = input(sure_string)
                board.make_move(row, col, player_symbol)
        turn += 1



main()
