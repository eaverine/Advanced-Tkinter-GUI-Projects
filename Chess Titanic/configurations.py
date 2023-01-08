from configparser import ConfigParser

PROGRAM_NAME = 'Chess Titanic'

NUMBER_OF_ROWS = 8
NUMBER_OF_COLUMNS = 8
DIMENSION_OF_EACH_SQUARE = 64 #Denoting 64 pixels

X_AXIS_LABELS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
Y_AXIS_LABELS = (1, 2, 3, 4, 5, 6, 7, 8)

START_PIECES_POSITION = {
'A1': 'r', 'B1': 'n', 'C1': 'b', 'D1': 'q', 'E1': 'k', 'F1': 'b', 'G1': 'n', 'H1': 'r',
'A2': 'p', 'B2': 'p', 'C2': 'p', 'D2': 'p', 'E2': 'p', 'F2': 'p', 'G2': 'p', 'H2': 'p',

'A7': 'P', 'B7': 'P', 'C7': 'P', 'D7': 'P', 'E7': 'P', 'F7': 'P', 'G7': 'P', 'H7': 'P',
'A8': 'R', 'B8': 'N', 'C8': 'B', 'D8': 'Q', 'E8': 'K', 'F8': 'B', 'G8': 'N', 'H8': 'R'
}

SHORT_NAME = {'R': 'Rook', 'N': 'Knight', 'B': 'Bishop', 'Q': 'Queen', 'K': 'King', 'P': 'Pawn'}

ORTHOGONAL_POSITIONS = ( (-1, 0), (0, 1), (1, 0), (0, -1) )
DIAGONAL_POSITIONS = ( (-1, -1), (-1, 1), (1, 1), (1, -1) )
KNIGHT_POSITIONS = ( (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1) )

config = ConfigParser()

config.read('chess_options.ini')
BOARD_COLOR_1 = config.get('chess_colors', 'BOARD_COLOR_1', fallback = '#DDB88C')
BOARD_COLOR_2 = config.get('chess_colors', 'BOARD_COLOR_2', fallback = '#A66D4F')
HIGHLIGHT_COLOR = config.get('chess_colors', 'HIGHLIGHT_COLOR', fallback ='#2EF70D')
