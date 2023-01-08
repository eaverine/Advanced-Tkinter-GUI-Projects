from tkinter import PhotoImage
from os import path
import sys

if getattr(sys, 'frozen', False):
    IMAGE_DIRECTORY = path.join(path.dirname(sys.executable), 'icons')
else:
    IMAGE_DIRECTORY = path.dirname(__file__)

glass_frame = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'glass_frame.gif'))

add_directory_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'add_directory.gif'))
add_file_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'add_file.gif'))

clear_play_list_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'clear_play_list.gif'))
delete_selected_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'delete_selected.gif'))

fast_forward_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'fast_forward.gif'))
rewind_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'rewind.gif'))

mute_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'mute.gif'))
unmute_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'unmute.gif'))

next_track_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'next_track.gif'))
previous_track_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'previous_track.gif'))

pause_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'pause.gif'))
play_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'play.gif'))
stop_icon = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'stop.gif'))

seekbar_knob_image = PhotoImage(file = path.join(IMAGE_DIRECTORY, 'seekbar_knob.gif'))
