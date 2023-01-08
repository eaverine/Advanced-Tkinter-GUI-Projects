from configparser import ConfigParser
import sys
import configurations
from tkinter import Toplevel, colorchooser
from tkinter.ttk import Label, Button
from random import choice


class PreferencesWindow():
    def __init__(self, view):
        self.parent = view.parent
        self.view = view

        self.fill_preference_colors()
        self.create_preferences_window()

    def fill_preference_colors(self):
        self.BOARD_COLOR_1 = configurations.BOARD_COLOR_1
        self.BOARD_COLOR_2 = configurations.BOARD_COLOR_2
        self.HIGHLIGHT_COLOR = configurations.HIGHLIGHT_COLOR

    def create_preferences_window(self):
        self.pref_window = Toplevel(self.parent)
        self.pref_window.title('Set Chess Preferences')
        self.color = choice([self.BOARD_COLOR_1, self.BOARD_COLOR_2, self.HIGHLIGHT_COLOR])
        self.pref_window.config(background = self.color)

        self.create_preferences_list()
        self.pref_window.transient(self.parent)

        x = self.parent.winfo_x()
        y = self.parent.winfo_y()

        w = self.pref_window.winfo_width() + 270
        h = self.pref_window.winfo_height() + 140
        self.pref_window.geometry('{}x{}+{}+{}'.format(w, h, x, y))

        self.parent.attributes('-disabled', True)

        def release_main():
            self.parent.attributes('-disabled', False)
            self.pref_window.destroy()

        self.pref_window.protocol('WM_DELETE_WINDOW', release_main)

    def create_preferences_list(self):
        def on_cancel_button_clicked():
            self.parent.attributes('-disabled', False)
            self.pref_window.destroy()

        Label(self.pref_window, text = 'Board Color 1', background = self.color).grid(row = 0, sticky = 'w', padx = 5, pady = 5)
        self.board_color_1_button = Button(self.pref_window, text = 'Select Board Color 1', command = self.set_color_1)
        self.board_color_1_button.grid(row = 0, column = 1, columnspan=2, sticky = 'e', padx = 5, pady = 5)

        Label(self.pref_window, text = 'Board Color 2', background = self.color).grid(row = 1, sticky = 'w', padx = 5, pady = 5)
        self.board_color_2_button = Button(self.pref_window, text = 'Select Board Color 2', command = self.set_color_2)
        self.board_color_2_button.grid(row = 1, column = 1, columnspan=2, sticky = 'e', padx = 5, pady = 5)

        Label(self.pref_window, text = 'Highlight Color', background = self.color).grid(row = 2, sticky = 'w', padx = 5, pady = 5)
        self.highlight_color_button = Button(self.pref_window, text = 'Select Highlight Color', command = self.set_highlight_color)
        self.highlight_color_button.grid(row = 2, column = 1, columnspan=2, sticky = 'e', padx = 5, pady = 5)

        Button(self.pref_window, text = 'Save', command = self.on_save_button_clicked).grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 5)
        Button(self.pref_window, text = 'Cancel', command = on_cancel_button_clicked).grid(row = 3, column = 2, sticky = 'e', padx = 5, pady = 5)

    def set_color_1(self):
        color = colorchooser.askcolor(initialcolor = self.BOARD_COLOR_1)[-1]
        if color != None:
            self.BOARD_COLOR_1 = color

    def set_color_2(self):
        color = colorchooser.askcolor(initialcolor = self.BOARD_COLOR_2)[-1]
        if color != None:
            self.BOARD_COLOR_2 = color

    def set_highlight_color(self):
        color = colorchooser.askcolor(initialcolor = self.HIGHLIGHT_COLOR)[-1]
        if color != None:
            self.HIGHLIGHT_COLOR = color

    def on_save_button_clicked(self):
        self.set_new_values()

        self.parent.attributes('-disabled', False)
        self.pref_window.destroy()
        
        self.view.reload_colors(self.BOARD_COLOR_1, self.BOARD_COLOR_2, self.HIGHLIGHT_COLOR)


    def set_new_values(self):
        config = ConfigParser()

        try:
            config.read('chess_options.ini')

            config.set('chess_colors', 'BOARD_COLOR_1', str(self.BOARD_COLOR_1))
            config.set('chess_colors', 'BOARD_COLOR_2', str(self.BOARD_COLOR_2))
            config.set('chess_colors', 'HIGHLIGHT_COLOR', str(self.HIGHLIGHT_COLOR))

            with open('chess_options.ini', 'w') as config_file:
                config.write(config_file)

        except:   #Just in case the settings file gets deleted or corrupted
            with open('chess_options.ini', 'w') as config_file:
                config_file.write(
                '[chess_colors]'
                f'board_color_1 = {self.BOARD_COLOR_1}'
                f'board_color_2 = {self.BOARD_COLOR_2}'
                f'highlight_color = {self.HIGHLIGHT_COLOR}')


        configurations.BOARD_COLOR_1 = self.BOARD_COLOR_1
        configurations.BOARD_COLOR_2 = self.BOARD_COLOR_2
        configurations.HIGHLIGHT_COLOR = self.HIGHLIGHT_COLOR
