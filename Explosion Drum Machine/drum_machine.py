import tkinter as tk
from tkinter import Menu, Frame, Label, Spinbox, Entry, Button, filedialog, BooleanVar, messagebox
from tkinter import ttk
import os
import pygame
import time
import threading
import pickle

PROGRAM_NAME = ' Explosion Drum Machine'
MAX_NUMBER_OF_PATTERNS = 10
MAX_NUMBER_OF_DRUM_SAMPLES = 5

INITIAL_NUMBER_OF_UNITS = 4
MAX_NUMBER_OF_UNITS = 5

INITIAL_BPU = 4
MAX_BPU = 5

INITIAL_BEATS_PER_MINUTE = 240
MIN_BEATS_PER_MINUTE = 80
MAX_BEATS_PER_MINUTE = 360

COLOR_1 = 'grey55'
COLOR_2 = 'khaki'
BUTTON_CLICKED_COLOR = 'green'

class DrumMachine:
    def __init__(self, root):
        self.root = root
        self.root.title(PROGRAM_NAME)
        self.root.protocol('WM_DELETE_WINDOW', self.exit_app)

        self.beats_per_minute = INITIAL_BEATS_PER_MINUTE
        self.all_patterns = [None] * MAX_NUMBER_OF_PATTERNS
        self.drum_load_entry_widget = [None] * MAX_NUMBER_OF_DRUM_SAMPLES
        self.current_pattern_index = 0

        self.loop = True
        self.now_playing = False

        self.init_all_patterns()
        self.init_gui()

    def exit_app(self):
        self.now_playing = False
        if messagebox.askokcancel('Quit', 'Really Quit?'):
            self.root.destroy()

    def init_all_patterns(self):
        self.all_patterns = [
            {'list_of_drum_files': [None] * MAX_NUMBER_OF_DRUM_SAMPLES,
             'number_of_units': INITIAL_NUMBER_OF_UNITS,
             'bpu': INITIAL_BPU,
             'is_button_clicked_list': self.init_is_button_clicked_list(
                 MAX_NUMBER_OF_DRUM_SAMPLES, INITIAL_NUMBER_OF_UNITS * INITIAL_BPU)
                }
            for k in range(MAX_NUMBER_OF_PATTERNS)
            ]

    def init_is_button_clicked_list(self, num_of_rows, num_of_columns):
        return [[False] * num_of_columns for x in range(num_of_rows)]

    def get_current_pattern_dict(self):
        return self.all_patterns[self.current_pattern_index]

    def get_bpu(self):
        return self.get_current_pattern_dict()['bpu']

    def set_bpu(self):
        self.get_current_pattern_dict()['bpu'] = int(self.bpu_widget.get())

    def get_number_of_units(self):
        return self.get_current_pattern_dict()['number_of_units']

    def set_number_of_units(self):
        self.get_current_pattern_dict()['number_of_units'] = int(self.number_of_units_widget.get())

    def get_list_of_drum_files(self):
        return self.get_current_pattern_dict()['list_of_drum_files']

    def get_drum_file_path(self, drum_index):
        return self.get_list_of_drum_files()[drum_index]

    def set_drum_file_path(self, drum_index, file_path):
        self.get_list_of_drum_files()[drum_index] = file_path

    def get_is_button_clicked_list(self):
        return self.get_current_pattern_dict()['is_button_clicked_list']

    def set_is_button_clicked_list(self, num_of_rows, num_of_columns):
        self.get_current_pattern_dict()['is_button_clicked_list'] = [[False] * num_of_columns for x in range(num_of_rows)]

    def init_pygame(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

    def play_sound(self, sound_filename):
        if sound_filename is not None:
            pygame.mixer.Sound(sound_filename).play()

    def play_pattern(self):
        self.now_playing = True

        while self.now_playing:
            play_list = self.get_is_button_clicked_list()

            num_columns = len(play_list[0])
            for column_index in range(num_columns):
                column_to_play = self.get_column_from_matrix(play_list, column_index)

                for i, item in enumerate(column_to_play):
                    if item:
                        sound_filename = self.get_drum_file_path(i)
                        self.play_sound(sound_filename)
                time.sleep(self.time_to_play_each_column())

                if not self.now_playing:
                    break
            if not self.loop:
                break
        self.now_playing = False
        self.toggle_play_button_state()

    def get_column_from_matrix(self, matrix, i):
        return [row[i] for row in matrix]

    def time_to_play_each_column(self):
        beats_per_second = self.beats_per_minute / 60
        time_to_play_each_column = 1 / beats_per_second
        return time_to_play_each_column

    def play_in_thread(self):
        self.thread = threading.Thread(target = self.play_pattern)
        self.thread.start()


    def init_gui(self):
        self.create_top_menu()
        self.create_top_bar()
        self.create_left_drum_loader()
        self.create_right_button_matrix()
        self.create_play_bar()

    def create_top_menu(self):
        self.menu_bar = Menu(root)

        self.file_menu = Menu(self.menu_bar, tearoff = False)
        self.file_menu.add_command(label = 'Load Project', command = self.load_project)
        self.file_menu.add_command(label = 'Save Project', command = self.save_project)
        self.file_menu.add_separator()
        self.file_menu.add_command(label = 'Exit', command = self.exit_app)

        self.menu_bar.add_cascade(label = 'File', menu = self.file_menu)

        self.menu_bar.add_command(label = 'About', command = self.show_about)

        root.config(menu = self.menu_bar)

    def save_project(self):
        saveas_file_name = filedialog.asksaveasfilename(title = 'Save Project As', filetypes = [('All Files', '*'), ('Explosion Beat File', '*.ebt')])
        if not saveas_file_name:
            return

        pickle.dump(self.all_patterns, open(saveas_file_name, 'wb'))
        self.root.title(os.path.basename(saveas_file_name) + '-' + PROGRAM_NAME)

    def load_project(self):
        file_path = filedialog.askopenfilename(title = 'Load Project', filetypes = [('All Files', '*'), ('Explosion Beat File', '*.ebt')])
        if not file_path:
            return

        pickled_file_object = open(file_path, 'rb')

        try:
            self.all_patterns = pickle.load(pickled_file_object)
        except EOFError:
            messagebox.showerror(title = 'Error', message = 'Explosion File Seems Corrupted!')

        pickled_file_object.close()

        try:
            self.on_pattern_changed()
            self.root.title(os.path.basename(file_path) + '-' + PROGRAM_NAME)
        except:
            messagebox.showerror(title = 'Error', message = 'An Unexpected Error Occured\nWhile Processing The Beat File')

    def show_about(self):
        messagebox.showinfo(title ='About', message = PROGRAM_NAME,
                            detail = 'Author - Mukhtar Raji\n\nThis App Is Used For Creating Beat Patterns'
                            '\n->Utilized Beats Functionality From Tkinter\n   GUI Application Development Blueprints')

    def create_top_bar(self):
        topbar_frame = Frame(root, height = 25)
        topbar_frame.grid(row = 0, padx = 5, pady = 5, sticky = 'ew', columnspan = 7)

        Label(topbar_frame, text = 'Pattern Number: ').grid(row = 0, column = 1)
        self.pattern_index_widget = Spinbox(topbar_frame, from_ = 1, to = MAX_NUMBER_OF_PATTERNS, width = 5, command = self.on_pattern_changed)
        self.pattern_index_widget.grid(row = 0, column = 2)

        self.current_pattern_name_widget = Entry(topbar_frame)
        self.current_pattern_name_widget.grid(row = 0, column = 3, padx = 7, pady = 2)
        self.display_pattern_name()

        Label(topbar_frame, text = 'Number Of Units: ').grid(row = 0, column = 4)
        self.number_of_units_widget = Spinbox(topbar_frame, from_ = 1, to = MAX_NUMBER_OF_UNITS, width = 5, command = self.on_number_of_units_changed)
        self.number_of_units_widget.delete(0, 'end')
        self.number_of_units_widget.insert(0, INITIAL_NUMBER_OF_UNITS)
        self.number_of_units_widget.grid(row = 0, column = 5, padx = 5)

        Label(topbar_frame, text = 'BPUs: ').grid(row = 0, column = 6)
        self.bpu_widget = Spinbox(topbar_frame, from_ = 1, to = MAX_BPU, width = 5, command = self.on_bpu_changed)
        self.bpu_widget.delete(0, 'end')
        self.bpu_widget.insert(0, INITIAL_BPU)
        self.bpu_widget.grid(row = 0, column = 7)

    def on_pattern_changed(self):
        self.current_pattern_index = int(self.pattern_index_widget.get()) - 1
        #This is added since the widget is made to start from 1 for the User, but the list index starts from 0 therefore, the -1 is to get the real value
        self.display_pattern_name()
        self.create_left_drum_loader()
        self.display_all_drum_file_names()
        self.create_right_button_matrix()
        self.display_all_button_colors()

    def display_pattern_name(self):
        self.current_pattern_name_widget.config(state = 'normal')
        self.current_pattern_name_widget.delete(0, 'end')
        self.current_pattern_name_widget.insert(0, 'Pattern {}'.format(self.current_pattern_index + 1))
        #and +1 is for the User. Check on_pattern_changed for more
        self.current_pattern_name_widget.config(state = 'readonly')

    def on_number_of_units_changed(self):
        self.set_number_of_units()
        self.set_is_button_clicked_list(MAX_NUMBER_OF_DRUM_SAMPLES, self.find_number_of_columns())
        self.create_right_button_matrix()

    def on_bpu_changed(self):
        self.set_bpu()
        self.set_is_button_clicked_list(MAX_NUMBER_OF_DRUM_SAMPLES, self.find_number_of_columns())
        self.create_right_button_matrix()

    def create_left_drum_loader(self):
        left_frame = Frame(root)
        left_frame.grid(row = 1, column = 0, sticky = 'nsew')

        for i in range(MAX_NUMBER_OF_DRUM_SAMPLES):
            open_file_button = Button(left_frame, image = open_file_icon, command = self.on_open_file_button_clicked(i))
            open_file_button.grid(row = i, column = 0, padx = 5, pady = 4)

            self.drum_load_entry_widget[i] = Entry(left_frame)
            self.drum_load_entry_widget[i].grid(row = i, column = 1, padx = 7, pady = 4)

    def on_open_file_button_clicked(self, drum_index):
        def event_handler():
            file_path = filedialog.askopenfilename(defaultextension = '.wav', filetypes = [('Wave Files', '*.wav'), ('OGG Files', '*.ogg')])
            if not file_path:
                return

            self.set_drum_file_path(drum_index, file_path)
            self.display_all_drum_file_names()
        return event_handler

    def display_all_drum_file_names(self):
        for i, drum_name in enumerate(self.get_list_of_drum_files()):
            self.display_drum_name(i, drum_name)

    def display_drum_name(self, entry_widget_num, file_path):
        if file_path is None:
            return

        drum_name = os.path.basename(file_path)
        self.drum_load_entry_widget[entry_widget_num].delete(0, 'end')
        self.drum_load_entry_widget[entry_widget_num].insert(0, drum_name)


    def create_right_button_matrix(self):
        right_frame = Frame(root)
        right_frame.grid(row = 1, column = 1, sticky = 'nsew', padx = 15, pady = 4)

        self.buttons = [[None for x in range(self.find_number_of_columns())] for x in range(MAX_NUMBER_OF_DRUM_SAMPLES)]

        for row in range(MAX_NUMBER_OF_DRUM_SAMPLES):
            for col in range(self.find_number_of_columns()):
                self.buttons[row][col] = Button(right_frame, width = 2, command = self.on_button_clicked(row,col) )
                self.buttons[row][col].grid(row = row, column = col)
                self.display_button_color(row,col)

    def on_button_clicked(self, row, col):
        def event_handler():
            self.process_button_clicked(row, col)
        return event_handler

    def process_button_clicked(self, row, col):
        self.set_button_value(row, col, not self.get_button_value(row, col))
        self.display_button_color(row, col)

    def set_button_value(self, row, col, bool_value):
        self.all_patterns[self.current_pattern_index]['is_button_clicked_list'][row][col] = bool_value

    def find_number_of_columns(self):
        return int(self.number_of_units_widget.get()) * int(self.bpu_widget.get())

    def display_all_button_colors(self):
        number_of_columns = self.find_number_of_columns()
        for r in range(MAX_NUMBER_OF_DRUM_SAMPLES):
            for c in range(number_of_columns):
                self.display_button_color(r, c)

    def display_button_color(self, row, col):
        bpu = int(self.bpu_widget.get())

        original_color = COLOR_1 if ((col//bpu) % 2) else COLOR_2
        button_color = BUTTON_CLICKED_COLOR if self.get_button_value(row,col) else original_color
        self.buttons[row][col].config(background = button_color)

    def get_button_value(self, row, col):
        return self.all_patterns[self.current_pattern_index]['is_button_clicked_list'][row][col]


    def create_play_bar(self):
        playbar_frame = Frame(self.root, height = 15)
        start_row = MAX_NUMBER_OF_DRUM_SAMPLES + 10
        playbar_frame.grid(row = start_row, sticky = 'we', padx = 15, pady = 2, columnspan = 6)

        self.play_button = ttk.Button(playbar_frame, text = ' Play', compound = 'left', image = play_icon, width = 7, command = self.on_play_button_clicked)
        self.play_button.grid(row = 0, column = 1, padx = 2)
        ttk.Button(playbar_frame, text = 'Stop', command = self.on_stop_button_clicked).grid(row = 0, column = 2, padx = 2)
        ttk.Separator(playbar_frame, orient = 'vertical').grid(row = 0, column = 3, sticky = 'ns', padx = 5)

        self.loopbuttonvar = BooleanVar()
        self.loopbuttonvar.set(True)
        self.loopbutton = ttk.Checkbutton(playbar_frame, text = 'Loop', variable = self.loopbuttonvar, command = self.on_loop_button_toggled)
        self.loopbutton.grid(row = 0, column = 4, padx = 5)
        self.loopbutton.state(['selected'])
        ttk.Separator(playbar_frame, orient = 'vertical').grid(row = 0, column = 5, sticky = 'ns')


        Label(playbar_frame, text = 'Beats Per Minute').grid(row = 0, column = 6)
        self.beats_per_minute_widget = Spinbox(playbar_frame, from_ = MIN_BEATS_PER_MINUTE, to = MAX_BEATS_PER_MINUTE, width = 5, increment = 5.0,
                                                  command = self.on_beats_per_minute_widget_changed)
        self.beats_per_minute_widget.delete(0, 'end')
        self.beats_per_minute_widget.insert(0, INITIAL_BEATS_PER_MINUTE)
        self.beats_per_minute_widget.grid(row = 0, column = 7)
        ttk.Separator(playbar_frame, orient = 'vertical').grid(row = 0, column = 8, sticky = 'ns', padx = 5)


        label = Label(playbar_frame, image = signature_icon)
        label.grid(row = 0, column = 9, padx = 1, sticky = 'w')

    def toggle_play_button_state(self):
        if self.now_playing:
            self.play_button.config(state = 'disabled')
        else:
            self.play_button.config(state = 'normal')

    def on_play_button_clicked(self):
        self.start_play()
        self.toggle_play_button_state()

    def start_play(self):
        self.init_pygame()
        self.play_in_thread()

    def on_stop_button_clicked(self):
        self.stop_play()
        self.toggle_play_button_state

    def stop_play(self):
        self.now_playing = False

    def on_loop_button_toggled(self):
        self.loop = self.loopbuttonvar.get()

    def on_beats_per_minute_widget_changed(self):
        self.beats_per_minute = int(self.beats_per_minute_widget.get())

if __name__ == '__main__':
    root = tk.Tk()
    from images import open_file_icon, play_icon, signature_icon
    DrumMachine(root)
    root.mainloop()
