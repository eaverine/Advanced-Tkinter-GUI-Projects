from os import path
from tkinter import PhotoImage

IMAGE_DIRECTORY = path.dirname(__file__)

open_file_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'openfile.gif'))
play_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'play.gif'))
signature_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'signature.gif'))
