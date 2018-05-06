from Board import Board
from Cell import Cell

dict_heuristic = {
    B: dictionaryB
    C: dictionaryC
    D: dictionaryD
}
dict_move_list = {
    "(3,1)": dictionaryB_coords
    "(3,0)": dictionaryC_coords
    "(2,4)": dictionaryD_coords
}


class AI:

    def __init__(self, initial_board_state, player_symbol):
        self.player_symbol = player_symbol
        self.current_moves = self.generate_moves(initial_board_state)
        self.graph = {initial_board_state: self.current_moves}

        self.weight_grid = [[16.16, -3.03, 0.99, 0.43, 0.43, 0.99, -3.03, 16.16],
                            [-4.12, -5.81, -0.08, -0.27, -0.27, -0.08, -5.81, -4.12],
                            [1.33, -0.04, 0.51, 0.07, 0.07, 0.51, -0.04, 1.33],
                            [0.63, -0.18, -0.04, -0.01, -0.01, -0.04, -0.18, 0.63],
                            [0.63, -0.18, -0.04, -0.01, -0.01, -0.04, -0.18, 0.63],
                            [1.33, -0.04, 0.51, 0.07, 0.07, 0.51, -0.04, 1.33],
                            [-4.12, -5.81, -0.08, -0.27, -0.27, -0.08, -5.81, -4.12],
                            [16.16, -3.03, 0.99, 0.43, 0.43, 0.99, -3.03, 16.16]]

    def generate_moves(self, board):
        valid_moves = []
        for row in board:
            for cell in row:
                if board.is_valid_move(cell, self.playersymbol):
                    valid_moves.append(cell)
        self.current_moves = valid_moves
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

def stringify_coordinate(string_coord):
    