from tkinter import filedialog, messagebox, Tk, Frame, Canvas, Button, Listbox, Scrollbar, IntVar, Radiobutton, Menu
from tkinter.ttk import Scale, Separator
import model
import player
from os import path, walk
from itertools import cycle
from seekbar import Seekbar
from helpers import *
from Pmw import Balloon


SEEKBAR_WIDTH = 360

class View:
    current_track_index = 0
    toggle_play_pause = cycle(['pause', 'play'])
    toggle_mute_unmute = cycle(['mute', 'unmute'])

    def __init__(self, root, model, player):
        self.root = root
        self.model = model
        self.player = player

        self.create_gui()

        self.root.bind('<<SeekbarPositionChanged>>', self.seek_new_position)
        self.root.protocol('WM_DELETE_WINDOW', self.close_player)

    def create_gui(self):
        self.root.title(PROGRAMNAME)
        self.balloon = Balloon(self.root)
        self.create_top_display()
        self.create_button_stack_frame()
        self.create_list_box()
        self.create_bottom_frame()
        self.create_context_menu()

    def create_top_display(self):
        frame = Frame(self.root)

        self.canvas = Canvas(frame, width = 370, height = 90)
        self.canvas.grid(row = 0)

        self.console = self.canvas.create_image(0, 10, anchor = 'nw', image = glass_frame)

        self.track_name = self.canvas.create_text(50, 35, anchor = 'w', fill='#9CEDAC', text=f'"Currently playing: None"')

        self.clock = self.canvas.create_text(125, 68, anchor = 'w', fill = '#CBE4F6', text = "00:00")
        self.track_length_text = self.canvas.create_text(167, 68, anchor = 'w', fill = '#CBE4F6', text = "of    00:00")

        self.seek_bar = Seekbar(frame, background = 'black', width = SEEKBAR_WIDTH, height = 10)
        self.seek_bar.grid(row = 1, sticky = 'ew', padx = 5)

        frame.grid(row = 0, pady = 5)


    def create_button_stack_frame(self):
        frame = Frame(self.root)

        previous_track_button = Button(frame, image = previous_track_icon, borderwidth = 0, command = self.on_previous_track_button_clicked)
        previous_track_button.grid(row = 0, column = 0, sticky = 'w')
        self.balloon.bind(previous_track_button, 'Previous Song')

        rewind_button = Button(frame, image = rewind_icon, borderwidth = 0, command = self.on_rewind_button_clicked)
        rewind_button.grid(row = 0, column = 1, sticky = 'w', padx = 7)
        self.balloon.bind(rewind_button, 'Rewind')

        stop_button = Button(frame, image = stop_icon, borderwidth = 0, command = self.on_stop_button_clicked)
        stop_button.grid(row = 0, column = 2, sticky = 'w')
        self.balloon.bind(stop_button, 'Stop')

        self.play_pause_button = Button(frame, image = play_icon, borderwidth = 0, command = self.on_play_pause_button_clicked)
        self.play_pause_button.grid(row = 0, column = 3, sticky = 'w', padx = 7)
        self.balloon.bind(self.play_pause_button, 'Play')

        fast_forward_button = Button(frame, image = fast_forward_icon, borderwidth = 0, command = self.on_fast_forward_button_clicked)
        fast_forward_button.grid(row = 0, column = 4, sticky = 'w')
        self.balloon.bind(fast_forward_button, 'Fast Forward')

        next_track_button = Button(frame, image = next_track_icon, borderwidth = 0, command = self.on_next_track_button_clicked)
        next_track_button.grid(row = 0, column = 5, sticky = 'w', padx = 7)
        self.balloon.bind(next_track_button, 'Next Song')

        self.mute_unmute_button = Button(frame, image = unmute_icon, borderwidth = 0, command = self.on_mute_unmute_button_clicked)
        self.mute_unmute_button.grid(row = 0, column = 6, sticky = 'w', padx = 3)
        self.balloon.bind(self.mute_unmute_button, 'Mute')

        self.volume_scale = Scale(frame, from_ = 0.0, to_ = 1.0, command = self.on_volume_scale_changed)
        self.volume_scale.set(0.6)
        self.volume_scale.grid(row = 0, column = 7, sticky = 'e', padx = 7, ipadx = 15)

        frame.grid(row = 1, sticky = 'w', padx = 5)

    def on_previous_track_button_clicked(self):
        self.current_track_index = max(0, self.current_track_index - 1)
        self.start_play()

    def on_rewind_button_clicked(self):
        self.player.rewind()

    def on_stop_button_clicked(self):
        self.player.stop()
        self.seek_bar.slide_to_position(0)
        self.play_pause_button.config(image = play_icon)

        self.toggle_play_pause = cycle(['play', 'pause'])   #This is to reset this output to play
        self.balloon.bind(self.play_pause_button, 'Play')   #Since it was previously in Pause

    def start_play(self):
        try:
            audio_file = self.model.get_file_to_play(self.current_track_index)
        except IndexError:
            return

        self.play_pause_button.config(image = pause_icon)
        self.balloon.bind(self.play_pause_button, 'Pause')
        self.player.play_media(audio_file)

        self.manage_one_time_track_updates_on_play_start()
        self.manage_periodic_updates_during_play()

    def manage_one_time_track_updates_on_play_start(self):
        self.update_now_playing_text()
        self.display_track_duration()

    def update_now_playing_text(self):
        current_track = self.model.play_list[self.current_track_index]
        file_path, file_name = path.split(current_track)
        truncated_track_name = truncate_text(file_name, 50)
        self.canvas.itemconfig(self.track_name, text = truncated_track_name)

    def display_track_duration(self):
        track_length = self.player.track_length
        minutes, seconds = get_time_in_minutes_seconds(track_length)

        track_length_string = 'of    {0:02d}:{1:02d}'.format(minutes, seconds)
        self.canvas.itemconfig(self.track_length_text, text = track_length_string)

    def manage_periodic_updates_during_play(self):
        self.update_clock()
        self.update_seek_bar()

        if not self.player.is_playing():
            if self.not_to_loop():
                return
        self.root.after(1000, self.manage_periodic_updates_during_play)

    def update_clock(self):
        elapsed_play_duration = self.player.elapsed_play_duration
        minutes, seconds = get_time_in_minutes_seconds(elapsed_play_duration)

        current_time_string = '{0:02d}:{1:02d}'.format(minutes, seconds)
        self.canvas.itemconfig(self.clock, text = current_time_string)

    def update_seek_bar(self):
        seek_bar_position = SEEKBAR_WIDTH * self.player.elapsed_play_duration/self.player.track_length
        self.seek_bar.slide_to_position(seek_bar_position)

    def seek_new_position(self, event = None):
        time = self.player.track_length * event.x/SEEKBAR_WIDTH
        self.player.seek(time)
        self.update_clock()

    def not_to_loop(self):
        selected_loop_choice = self.loop_value.get()

        if selected_loop_choice == 1:   #No loop
            return True
        elif selected_loop_choice == 2: #Loop current
            self.start_play()
            return False
        elif selected_loop_choice == 3: #Loop all
            self.play_next_track()
            return True

    def on_play_pause_button_clicked(self):
        if not self.player.is_playing():
            return

        action = next(self.toggle_play_pause)
        if action == 'play':
            self.player.play()
            self.play_pause_button.config(image = pause_icon)
            self.balloon.bind(self.play_pause_button, 'Pause')
        elif action == 'pause':
            self.player.pause()
            self.play_pause_button.config(image = play_icon)
            self.balloon.bind(self.play_pause_button, 'Play')

    def on_fast_forward_button_clicked(self):
        self.player.fast_forward()

    def on_next_track_button_clicked(self):
        self.play_next_track()

    def play_next_track(self):
        self.current_track_index = min(self.list_box.size() - 1, self.current_track_index + 1)
        self.start_play()

    def on_mute_unmute_button_clicked(self):
        action = next(self.toggle_mute_unmute)
        if action == 'mute':
            self.volume_at_time_of_mute = self.player.volume
            self.player.mute()
            self.volume_scale.set(0.0)
            self.mute_unmute_button.config(image = mute_icon)
            self.balloon.bind(self.mute_unmute_button, 'Unmute')

        elif action == 'unmute':
            self.player.unmute(self.volume_at_time_of_mute)
            self.volume_scale.set(self.volume_at_time_of_mute)
            self.mute_unmute_button.config(image = unmute_icon)
            self.balloon.bind(self.mute_unmute_button, 'Mute')

    def on_volume_scale_changed(self, value):
        self.player.volume = self.volume_scale.get()

        if self.player.volume == 0.0:
            self.mute_unmute_button.config(image = mute_icon)
            self.balloon.bind(self.mute_unmute_button, 'Unmute')
        else:
            self.mute_unmute_button.config(image = unmute_icon)
            self.balloon.bind(self.mute_unmute_button, 'Mute')


    def create_list_box(self):
        frame = Frame(self.root)

        self.list_box = Listbox(frame, activestyle = 'none', height = 10, bg = '#1C3D7D', fg='#A0B9E9', cursor = 'hand2', selectmode = 'extended')
        self.list_box.pack(side = 'left', fill = 'both', expand = 1)
        self.list_box.bind('<Double-Button-1>', self.on_play_list_double_clicked)
        self.list_box.bind('<Button-3>', self.show_context_menu)

        scroll_bar = Scrollbar(frame)
        scroll_bar.pack(side = 'right', fill = 'both')

        self.list_box.config(yscrollcommand = scroll_bar.set)
        scroll_bar.config(command = self.list_box.yview)

        frame.grid(row = 2, sticky = 'ew', padx = 5, pady = 5)

    def on_play_list_double_clicked(self, event = None):
        list_items = self.list_box.curselection()
        if not list_items:
            return

        self.current_track_index = int(list_items[0])
        self.start_play()


    def create_bottom_frame(self):
        frame = Frame(self.root)

        add_file_button = Button(frame, image = add_file_icon, borderwidth = 0, command = self.on_add_file_button_clicked)
        add_file_button.grid(row = 0, column = 0)
        self.balloon.bind(add_file_button, 'Add Song')

        delete_selected_button = Button(frame, image = delete_selected_icon, borderwidth = 0, command = self.on_delete_selected_button_clicked)
        delete_selected_button.grid(row = 0, column = 1, padx = 3)
        self.balloon.bind(delete_selected_button, 'Delete Selected')

        add_directory_button = Button(frame, image = add_directory_icon, borderwidth = 0, command = self.on_add_directory_button_clicked)
        add_directory_button.grid(row = 0, column = 2)
        self.balloon.bind(add_directory_button, 'Add Directory')

        clear_playlist_button = Button(frame, image = clear_play_list_icon, borderwidth = 0, command = self.on_clear_playlist_button_clicked)
        clear_playlist_button.grid(row = 0, column = 3, padx = 3)
        self.balloon.bind(clear_playlist_button, 'Clear Playlist')

        Separator(frame, orient = 'vertical').grid(row = 0, column = 4, sticky = 'ns')

        loop_choices = [("No Loop", 1), ("Loop Current", 2), ("Loop All", 3)]
        self.loop_value = IntVar()
        self.loop_value.set(3)
        for txt, val in loop_choices:
            Radiobutton(frame, text = txt, variable = self.loop_value, value = val).grid(row = 0, column = 4 + val, padx = 2)

        frame.grid(row = 3, sticky = 'ew', padx = 5, pady = 3)

    def on_add_file_button_clicked(self):
        initial_directory = path.expanduser('~') + '\\My Music'
        audio_file = filedialog.askopenfilename(title = 'Select the target audio file', initialdir = initial_directory,
                                                filetypes = [('All Supported', '.mp3 .wav'), ('.mp3 files', '.mp3'), ('.wav files', '.wav')])

        if audio_file:
            self.model.add_to_play_list(audio_file)

            file_path, file_name = path.split(audio_file)
            self.list_box.insert('end', file_name)

    def on_delete_selected_button_clicked(self):
        self.delete_selected_files()

    def delete_selected_files(self):
        try:
            selected_indexes = self.list_box.curselection()
            for index in reversed(selected_indexes):
                self.list_box.delete(index)
                self.model.remove_item_from_playlist_at_index(index)

        except IndexError:
            pass

    def on_add_directory_button_clicked(self):
        directory_path = filedialog.askdirectory(title = 'Select the target audio folder')
        if not directory_path:
            return

        audio_files_in_directory = self.get_all_audio_files_from_directory(directory_path)
        for audio_file in audio_files_in_directory:
            self.model.add_to_play_list(audio_file)
            file_path, file_name = path.split(audio_file)
            self.list_box.insert('end', file_name)

    def get_all_audio_files_from_directory(self, directory_path):
        audio_files_in_directory = []
        for (dirpath, dirname, filenames) in walk(directory_path):
            for audio_file in filenames:
                if audio_file.endswith('.mp3') or audio_file.endswith('.wav'):
                    audio_files_in_directory.append(dirpath, '/', audio_file)

        return audio_files_in_directory

    def on_clear_playlist_button_clicked(self):
        self.model.clear_play_list()
        self.list_box.delete(0, 'end')


    def create_context_menu(self):
        self.context_menu = Menu(self.list_box, tearoff = 0)
        self.context_menu.add_command(label = 'Delete', command = self.on_delete_selected_context_menu_clicked)

    def on_delete_selected_context_menu_clicked(self):
        self.delete_selected_files()

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def close_player(self):
        self.player.stop()
        self.root.destroy()


if __name__ == '__main__':
    PROGRAMNAME = 'Tkinter Audio Player'
    root = Tk()
    root.resizable(width = False, height = False)

    from icons import *

    player = player.Player()
    model = model.Model()

    app = View(root, model, player)
    root.mainloop()
