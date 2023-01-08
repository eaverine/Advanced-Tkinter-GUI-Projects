from os import path
from tkinter import PhotoImage

IMAGE_DIRECTORY = path.dirname(__file__)

about_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'about.gif'))
copy_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'copy.gif'))
cut_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'cut.gif'))
find_text_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'find_text.gif'))
new_file_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'new_file.gif'))
open_file_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'open_file.gif'))
paste_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'paste.gif'))
redo_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'redo.gif'))
save_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'save.gif'))
undo_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'undo.gif'))
