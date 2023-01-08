import tkinter as tk
from tkinter import filedialog, messagebox
import os

root = tk.Tk()
root.geometry('600x400')
PROGRAM_NAME = 'Footprint Editor'
root.title(PROGRAM_NAME)

file_name = None

from images import about_icon, copy_icon, cut_icon, find_text_icon, new_file_icon, open_file_icon, paste_icon, redo_icon, save_icon, undo_icon

my_menu = tk.Menu(root)

file_menu = tk.Menu(my_menu, tearoff = 0)

def cut():
    content_text.event_generate('<<Cut>>')
    on_content_changed()
    return 'break'

def copy():
    content_text.event_generate('<<Copy>>')
    return 'break'

def paste():
    content_text.event_generate('<<Paste>>')
    on_content_changed()
    return 'break'

def undo():
    content_text.event_generate('<<Undo>>')
    on_content_changed()
    return 'break'

def redo(event = None):
    content_text.event_generate('<<Redo>>')
    on_content_changed()
    return 'break'

def select_all():
    content_text.event_generate('<<SelectAll>>')
    return 'break'

def find_text(event = None):
    search_toplevel = tk.Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)

    tk.Label(search_toplevel, text = 'Find Text: ').grid(row = 0, column = 0, sticky = 'e')
    search_entry_widget = tk.Entry(search_toplevel, width = 25)
    search_entry_widget.grid(row = 0, column = 1, padx = 2, pady = 2, sticky = 'we')
    search_entry_widget.focus_set()

    ignore_case_value = tk.IntVar()
    ignore_case_value.set(1)
    tk.Checkbutton(search_toplevel, text = 'Ignore Case', variable = ignore_case_value).grid(row = 1, column = 1, sticky = 'e',
                                                                                             padx = 2, pady = 2)
    tk.Button(search_toplevel, text = 'Find', underline = 0, width = 7,
              command = lambda: search_output(search_entry_widget.get(), ignore_case_value.get(), content_text, search_toplevel,
                                              search_entry_widget)
              ).grid(row = 0, column = 2, sticky = 'we', padx = 4, pady = 2)

    def close_search_window():
        content_text.tag_remove('match', '1.0', tk.END)
        search_toplevel.destroy()

    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return 'break'

def search_output(needle, ignore_case_value, content_text, search_toplevel, search_entry_widget):
    content_text.tag_remove('match', '1.0', tk.END)

    matches_found = 0

    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle, start_pos, nocase = ignore_case_value, stopindex = tk.END)

            if not start_pos:
                break
            end_pos = '{} + {}c'.format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos

        content_text.tag_config('match', foreground = 'red', background = 'yellow')

    search_entry_widget.focus_set()
    if matches_found == 1:
        search_toplevel.title('1 match found')
    elif matches_found > 1:
        search_toplevel.title('{} matches found'.format(matches_found))
    else:
        search_toplevel.title('Find Text')

def open_file(event = None):
    input_file_name = filedialog.askopenfilename(defaultextension = '.txt', filetypes = [('Text Documents', '*.txt'), ('All Files', '*.*')])

    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))

        content_text.delete('1.0', tk.END)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())

    on_content_changed()

    return 'break'

def save(event = None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return 'break'

def save_as(event = None):
    input_file_name = filedialog.asksaveasfilename(defaultextension = '.txt', filetypes = [('Text Documents', '*.txt'), ('All Files', '*.*')])

    if input_file_name:
        global file_name
        file_name = input_file_name

        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))

    return 'break'

def write_to_file(file_name):
    try:
        content = content_text.get(1.0, tk.END)
        with open(file_name, 'w') as the_file:
            the_file.write(content)

    except IOError:
        messagebox.showerror(title = 'Error', message = 'Save?', detail = 'Could not save the file')

def new_file(event = None):
    root.title('Untitled - {}'.format(PROGRAM_NAME))
    global file_name
    file_name = None
    content_text.delete(1.0, tk.END)

    on_content_changed()

    return 'break'

def display_about_messagebox(event = None):
    about_message = PROGRAM_NAME
    about_detail = ('Author - Mukhtar Raji \n\nThis Is A Basic Text Editor\n'
                    '->Utilized Editing Functionality From Tkinter \n   GUI Application Development Blueprints')

    messagebox.showinfo(title = 'About', message = about_message, detail = about_detail )

def display_help_messagebox(event = None):
    help_message = PROGRAM_NAME
    help_detail = ('Author - Mukhtar Raji \n' 'For assistance, please contact the author\n oladuaraji@gmail.com')

    messagebox.showinfo(title = 'Help', message = help_message, detail = help_detail )

def exit_editor(event = None):
    if messagebox.askokcancel(title = 'Quit?', message = 'Really Quit?'):
        root.destroy()

root.protocol('WM_DELETE_WINDOW', exit_editor)

def on_content_changed(event = None):
    update_line_numbers()
    update_cursor_info_bar()

def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = content_text.index('end').split('.')

        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output

def update_line_numbers(event = None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state = 'normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state = 'disabled')
    
def highlight_line(interval = 100):
    content_text.tag_remove('active_line', 1.0, 'end')
    content_text.tag_add('active_line', 'insert linestart', 'insert lineend+1c')
    content_text.after(interval, toggle_highlight)
    
def undo_highlight():
    content_text.tag_remove('active_line', 1.0, 'end')
    
def toggle_highlight(event = None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()
        
def show_cursor_info_bar():
    if show_cursor_location.get():
        cursor_info_bar.pack(expand = 'no', fill = None, side = 'right', anchor = 'se')
    else:
        cursor_info_bar.pack_forget()
        
def update_cursor_info_bar(event = None):
    row, col = content_text.index(tk.INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col) + 1) #column starts at 0, row at 1
    infotext = 'Line: {0} | Column: {1}'.format(line_num, col_num)
    cursor_info_bar.config(text = infotext)
    
def change_theme(event = None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    foreground_color, background_color = fg_bg_colors.split('.')
    content_text.configure(foreground = foreground_color, background = background_color)
    
def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)

file_menu.add_command(label = 'New', accelerator = 'Ctrl+N', compound = 'left',image = new_file_icon, underline = 0, command = new_file)
file_menu.add_command(label = 'Open...', accelerator = 'Ctrl+O', compound = 'left',image = open_file_icon, underline = 0, command = open_file)
file_menu.add_command(label = 'Save', accelerator = 'Ctrl+S', compound = 'left',image = save_icon, underline = 0, command = save)
file_menu.add_command(label = 'Save As...', accelerator = 'Shift+Ctrl+S', command = save_as)
file_menu.add_separator()
file_menu.add_command(label = 'Exit', accelerator = 'Alt+F4', command = exit_editor)

my_menu.add_cascade(label = 'File', menu = file_menu)

edit_menu = tk.Menu(my_menu, tearoff = 0)

edit_menu.add_command(label = 'Undo', accelerator = 'Ctrl+Z', compound = 'left', image = undo_icon, command = undo)
edit_menu.add_command(label = 'Redo', accelerator = 'Ctrl+Y', compound = 'left', image = redo_icon, command = redo)
edit_menu.add_separator()
edit_menu.add_command(label = 'Cut', accelerator = 'Ctrl+X', compound = 'left', image = cut_icon, command = cut)
edit_menu.add_command(label = 'Copy', accelerator = 'Ctrl+C', compound = 'left', image = copy_icon, command = copy)
edit_menu.add_command(label = 'Paste', accelerator = 'Ctrl+V', compound = 'left', image = paste_icon, command = paste)
edit_menu.add_separator()
edit_menu.add_command(label = 'Find...', accelerator = 'Ctrl+F', underline = 0, compound = 'left', image = find_text_icon, command = find_text)
edit_menu.add_separator()
edit_menu.add_command(label = 'Select All', accelerator = 'Ctrl+A', compound = 'left', underline = 7, command = select_all)

my_menu.add_cascade(label = 'Edit', menu = edit_menu)

view_menu = tk.Menu(my_menu, tearoff = 0)

show_line_number = tk.IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label = 'Show Line Number', variable = show_line_number, command = update_line_numbers)

show_cursor_location = tk.IntVar()
show_cursor_location.set(1)
view_menu.add_checkbutton(label = 'Show Cursor Location At Bottom', variable = show_cursor_location, command = show_cursor_info_bar)

to_highlight_line = tk.BooleanVar()
view_menu.add_checkbutton(label = 'Highlight Current Line', variable = to_highlight_line, onvalue = 1, offvalue = 0, command = toggle_highlight)

themes_menu = tk.Menu(my_menu, tearoff = 0)
view_menu.add_cascade(label = 'Themes', menu = themes_menu)

color_schemes = {
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',}

theme_choice = tk.StringVar()
theme_choice.set('Default')
for i in sorted(color_schemes):
    themes_menu.add_radiobutton(label = i, variable = theme_choice, command = change_theme)

my_menu.add_cascade(label = 'View', menu = view_menu)

about_menu = tk.Menu(my_menu, tearoff = 0)

about_menu.add_command(label = 'About...', compound = 'left',image = about_icon, command = display_about_messagebox)
about_menu.add_command(label = 'Help...', command = display_help_messagebox)

my_menu.add_cascade(label = 'About', menu = about_menu)

root.config(menu = my_menu)

shortcut_bar = tk.Frame(root, height = 25, background = 'light sea green')

icons = ('new_file_icon', 'open_file_icon', 'save_icon', 'cut_icon', 'copy_icon', 'paste_icon', 'undo_icon', 'redo_icon', 'find_text_icon')
for icon in icons:
    cmd = icon.replace('_icon', '')
    cmd = eval(cmd)   #The eval is to convert the string to an object

    tool_bar = tk.Button(shortcut_bar, image = eval(icon), command = cmd)
    tool_bar.pack(side = 'left')

shortcut_bar.pack(expand = 'no', fill = 'x')

line_number_bar = tk.Text(root, width = 4, padx = 3, takefocus = 0, border = 0, background = 'khaki', state = 'disabled', wrap = 'none',
                          cursor = 'arrow')
line_number_bar.pack(side = 'left', fill = 'y')

content_text = tk.Text(root, wrap = 'word', undo = 1)
content_text.pack(expand = 'yes', fill = 'both')

scroll_bar = tk.Scrollbar(content_text, cursor = 'cross')

content_text.config(yscrollcommand = scroll_bar.set)
scroll_bar.config(command = content_text.yview)

scroll_bar.pack(side = 'right', fill = 'y')

content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)

content_text.bind_all('<Control-f>', find_text)
content_text.bind_all('<Control-F>', find_text)

content_text.bind_all('<Control-o>', open_file)
content_text.bind_all('<Control-O>', open_file)

content_text.bind_all('<Control-s>', save)
content_text.bind_all('<Control-S>', save)

content_text.bind_all('<Shift-Control-s>', save_as)
content_text.bind_all('<Shift-Control-S>', save_as)

content_text.bind_all('<Control-n>', new_file)
content_text.bind_all('<Control-N>', new_file)

content_text.bind_all('<KeyPress-F1>', display_help_messagebox)

content_text.bind('<Any-KeyPress>', on_content_changed)

content_text.tag_configure('active_line', background = 'ivory2')

cursor_info_bar = tk.Label(content_text, text = 'Line: 1 | Column: 1')
cursor_info_bar.pack(expand = 'no', fill = None, side = 'right', anchor = 'se')

popup_menu = tk.Menu(content_text, tearoff = False)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    popup_menu.add_command(label = i, command = cmd)
    
popup_menu.add_separator()
popup_menu.add_command(label = 'Select All', underline = 7, command = select_all)

content_text.bind('<Button-3>', show_popup_menu)

content_text.focus_set()

root.mainloop()
