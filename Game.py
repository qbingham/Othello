from Board import Board
from AIBoard import AIBoard
# from Timer import Timer
from time import sleep
import threading
import random

import Timer as ti

def symbol_toggle(player_symbol):
    if player_symbol == "B":
        return "W"
    elif player_symbol == "W":
        return "B"
    else:
        return True

def main():
    b_or_w = input("Would you prefer W in the top left or B in the top left? (Enter W or B)")
    board = Board("W")
    turn = 1
    if b_or_w == "B":
        turn = 1

    while not board.gameOver():
        board.display()
        if turn % 2 == 0:
            player_symbol = "W"
            print("It is W's turn")
            if b_or_w == "B":
                if not board.no_valid_moves("W"):
                    if turn <= 16:
                        board.AI_early_move("W")
                    elif turn <= 50:
                        board.AI_mid_move("W")
                    else:
                        board.AI_late_move("W", turn)
                else:
                    print("No valid moves! Black gets to go again")
            else:
                is_sure = "N"
                if not board.no_valid_moves(player_symbol):
                    while is_sure != "Y":
                        col = input("Please enter a column: ")
                        row = input("Please enter a row: ")
                        letters = ['A','B','C','D','E','F','G','H']

                        while not row.isdigit() or not col.isalpha():
                            print("Invalid input for row or column. Try again")
                            row = input("Please enter a row: ")
                            col = input("Please enter a column: ")
                        row = int(row)
                        col = int(letters.index(col))
                        cell = board.grid[row][col]
                        valid_move = board.is_valid_move(cell, player_symbol)
                        coordinates = cell.getCoordinates().__str__()
                        while not valid_move:
                            print("Invalid move! ", coordinates ," is not a valid move for ", player_symbol, ".", sep="")
                            col = input("Please enter a column: ")
                            row = int(input("Please enter a row: "))
                            col = int(letters.index(col))
                            cell = board.grid[row][col]
                            valid_move = board.is_valid_move(cell, player_symbol)
                            coordinates = cell.getCoordinates().__str__()
                        sure_string = "Are you sure you want to make the move at "
                        sure_string += str(coordinates) + "? (Y or N)"
                        is_sure = input(sure_string)
                    board.make_move(row,col, player_symbol)
                else:
                    print("No valid moves! White gets to go again")

        else:
            player_symbol = "B"
            print("It is B's turn")
            if b_or_w == "W":
                if not board.no_valid_moves("B"):
                    if turn <= 16:
                        board.AI_early_move("B")
                    elif turn <= 50:
                        board.AI_mid_move("B")
                    else:
                        board.AI_late_move("B", turn)
                else:
                    print("No valid moves! White gets to go again")
            else:
                is_sure = "N"
                if not board.no_valid_moves(player_symbol):
                    while is_sure != "Y":
                        col = input("Please enter a column: ")
                        row = input("Please enter a row: ")
                        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                        while not row.isdigit() or not col.isalpha():
                            print("Invalid input for row or column. Try again")
                            col = input("Please enter a column: ")
                            row = input("Please enter a row: ")
                        row = int(row)
                        col = int(letters.index(col))
                        cell = board.grid[row][col]
                        valid_move = board.is_valid_move(cell, player_symbol)
                        coordinates = cell.getCoordinates().__str__()
                        while not valid_move:
                            print("Invalid move! ", coordinates, " is not a valid move for ", player_symbol, ".", sep="")
                            col = input("Please enter a column: ")
                            row = int(input("Please enter a row: "))
                            col = int(letters.index(col))
                            cell = board.grid[row][col]
                            valid_move = board.is_valid_move(cell, player_symbol)
                            coordinates = cell.getCoordinates().__str__()
                        sure_string = "Are you sure you want to make the move at "
                        sure_string += str(coordinates) + "? (Y or N)"
                        is_sure = input(sure_string)
                    board.make_move(row, col, player_symbol)
                else:
                    print("No valid moves! Black gets to go again")
        turn += 1

    board.display()

    score_tuple = board.get_score()
    w_score = score_tuple[0]
    b_score = score_tuple[1]
    if w_score > b_score:
        print("W wins! The final score was W: ", w_score, ", B: ", b_score)
    elif b_score > w_score:
        print("B wins! The final score was W: ", w_score, ", B: ", b_score)


def print_time():
   start = 10
   end_time = random.randint(7, 10)
   while start >= end_time:
       print(start)
       start -= 1
       sleep(1)


main()

