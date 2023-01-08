from tkinter import PhotoImage
from os import path
import sys

if getattr(sys, 'frozen', False):
    IMAGE_DIRECTORY = path.join(path.dirname(sys.executable), 'images')
else:
    IMAGE_DIRECTORY = path.dirname(__file__)

king_white = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'king_white.png'))
king_black = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'king_black.png'))

queen_white = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'queen_white.png'))
queen_black = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'queen_black.png'))

bishop_white = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'bishop_white.png'))
bishop_black = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'bishop_black.png'))

knight_white = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'knight_white.png'))
knight_black = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'knight_black.png'))

rook_white = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'rook_white.png'))
rook_black = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'rook_black.png'))

pawn_white = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'pawn_white.png'))
pawn_black = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'pawn_black.png'))
