from configurations import *
import model
import piece

class Controller():
    def __init__(self):
        self.init_model()

    def init_model(self):
        self.model = model.Model()

    def get_numeric_notation(self, position):
        return piece.get_numeric_notation(position)

    def get_all_pieces_on_board(self):
        return self.model.items()

    def reset_game_data(self):
        return self.model.reset_game_data()

    def reset_to_initial_locations(self):
        return self.model.reset_to_initial_locations()

    def get_alphanumeric_position(self, rowcolumntuple):
        return self.model.get_alphanumeric_position(rowcolumntuple)

    def get_piece_at(self, position_of_click):
        return self.model.get_piece_at(position_of_click)

    def pre_move_validation(self, start_pos, end_pos):
        return self.model.pre_move_validation(start_pos, end_pos)

    def player_turn(self):
        return self.model.player_turn

    def moves_available(self, position):
        return self.model.moves_available(position)
