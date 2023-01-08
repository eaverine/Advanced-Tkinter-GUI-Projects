from configurations import *
import controller
from tkinter import Menu, Tk, Canvas, Frame, Label, messagebox
import exceptions
from preferences import PreferencesWindow


class View():
    selected_piece_position = None
    all_squares_to_be_highlighted = []
    images = {}

    board_color_1 = BOARD_COLOR_1
    board_color_2 = BOARD_COLOR_2
    highlight_color = HIGHLIGHT_COLOR

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.images = {}

        self.create_chess_base()

        self.start_new_game()

    def create_chess_base(self):
        self.create_top_menu()
        self.create_canvas()
        self.draw_board()
        self.create_bottom_frame()

    def create_top_menu(self):
        self.menu_bar = Menu(self.parent)

        self.file_menu = Menu(self.menu_bar, tearoff = 0)
        self.file_menu.add_command(label = 'New Game', command = self.on_new_game_menu_clicked)
        self.menu_bar.add_cascade(label = 'File', menu = self.file_menu)

        self.menu_bar.add_command(label = 'Preferences', command = self.on_preference_menu_clicked)

        self.menu_bar.add_command(label = 'About', command = self.on_about_menu_clicked)

        self.parent.config(menu = self.menu_bar)

    def on_new_game_menu_clicked(self):
        self.start_new_game()

    def on_preference_menu_clicked(self):
        PreferencesWindow(self)

    def on_about_menu_clicked(self):
        messagebox.showinfo(title ='About', message = PROGRAM_NAME,
        detail = 'Author - Mukhtar Raji\n\n   ->Utilized Chess Functionality From Tkinter \n    GUI Application Development Blueprints')

    def create_canvas(self):
        canvas_width = NUMBER_OF_COLUMNS * DIMENSION_OF_EACH_SQUARE
        canvas_height = NUMBER_OF_ROWS * DIMENSION_OF_EACH_SQUARE
        self.canvas = Canvas(self.parent, width = canvas_width, height = canvas_height)
        self.canvas.pack(padx = 8, pady = 8)

        self.canvas.bind('<Button-1>', self.on_square_clicked)

    def get_clicked_row_column(self, event):
        col_size = row_size = DIMENSION_OF_EACH_SQUARE
        clicked_row = event.y//row_size
        clicked_col = event.x//col_size
        return(clicked_row, clicked_col)

    def on_square_clicked(self, event):
        clicked_row, clicked_col = self.get_clicked_row_column(event)
        #print('Hey!, You clicked on ', clicked_row, clicked_col)

        position_of_click = self.controller.get_alphanumeric_position((clicked_row, clicked_col))
        if self.selected_piece_position: #on second click
            self.shift(self.selected_piece_position, position_of_click)
            self.selected_piece_position = None

        self.update_highlight_list(position_of_click)
        self.draw_board()
        self.draw_all_pieces()

    def shift(self, start_pos, end_pos):
        selected_piece = self.controller.get_piece_at(start_pos)
        piece_at_destination = self.controller.get_piece_at(end_pos)

        if not piece_at_destination or piece_at_destination.color != selected_piece.color:
            try:
                self.controller.pre_move_validation(start_pos, end_pos)
            except exceptions.ChessError as error:
                self.info_label['text'] = error.__class__.__name__
            else:
                self.update_label(selected_piece, start_pos, end_pos)

    def update_label(self, piece, start_pos, end_pos):
        turn = 'white' if piece.color == 'black' else 'black'
        self.info_label['text'] = f"{piece.color.capitalize()} : {start_pos}{end_pos}   {turn.capitalize()}'s turn"

    def update_highlight_list(self, position):
        self.all_squares_to_be_highlighted = None
        try:
            piece = self.controller.get_piece_at(position)
        except:
            piece = None

        if piece and (piece.color == self.controller.player_turn()):
            self. selected_piece_position = position
            self.all_squares_to_be_highlighted = list(map(self.controller.get_numeric_notation,
                                                        self.controller.get_piece_at(position).moves_available(position)))

    def draw_board(self):
        current_color = self.board_color_2

        for row in range(NUMBER_OF_ROWS):
            current_color = self.get_alternate_color(current_color)
            for col in range(NUMBER_OF_COLUMNS):
                x1, y1 = self.get_x_y_coordinate(row, col)
                x2, y2 = x1 + DIMENSION_OF_EACH_SQUARE, y1 + DIMENSION_OF_EACH_SQUARE

                if self.all_squares_to_be_highlighted and (row, col) in self.all_squares_to_be_highlighted:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill = self.highlight_color)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill = current_color)
                current_color = self.get_alternate_color(current_color)

    def get_alternate_color(self, current_color):
        if current_color == self.board_color_2:
            next_color = self.board_color_1
        else:
            next_color = self.board_color_2

        return next_color

    def get_x_y_coordinate(self, row, col):
        x = (col * DIMENSION_OF_EACH_SQUARE)
        y = (row * DIMENSION_OF_EACH_SQUARE)

        return (x, y)

    def create_bottom_frame(self):
        self.bottom_frame = Frame(self.parent, height = 64)

        self.info_label = Label(self.bottom_frame, text = '     White to Start The Game     ', fg = 'black')
        self.info_label.pack(side = 'right', padx = 8, pady = 5)

        self.bottom_frame.pack(fill = 'x', side = 'bottom')

    def draw_single_piece(self, position, piece):
        def calculate_piece_coordinate(row, col):
            x0 = (col * DIMENSION_OF_EACH_SQUARE) + int(DIMENSION_OF_EACH_SQUARE/2)
            y0 = (row * DIMENSION_OF_EACH_SQUARE) + int(DIMENSION_OF_EACH_SQUARE/2)
            return x0, y0

        x, y = self.controller.get_numeric_notation(position)
        if piece:
            image = f'{piece.name.lower()}_{piece.color}'
            if image not in self.images:
                self.images[image] = eval(image)

            x0, y0 = calculate_piece_coordinate(x,y)

            self.canvas.create_image(x0, y0, image = eval(image), tags = ('occupied'), anchor = 'c')

    def draw_all_pieces(self):
        self.canvas.delete('occupied')
        for position, piece in self.controller.get_all_pieces_on_board():
            self.draw_single_piece(position, piece)

    def start_new_game(self):
        self.controller.reset_game_data()
        self.controller.reset_to_initial_locations()
        self.draw_all_pieces()

        self.info_label.config(text = '     White to Start The Game     ')

    def reload_colors(self, color_1, color_2, highlight_color):
        self.board_color_1 = color_1
        self.board_color_2 = color_2
        self.highlight_color = highlight_color

        self.draw_board()
        self.draw_all_pieces()

if __name__ == '__main__':
    game_controller = controller.Controller()

    root = Tk()
    root.title(PROGRAM_NAME)

    from images import (king_white, king_black, queen_white, queen_black, bishop_white, bishop_black, knight_white, knight_black, rook_white, rook_black,
    pawn_white, pawn_black)

    View(root, game_controller)
    root.mainloop()
