from tkinter import Canvas, Tk, Frame

class Seekbar(Canvas):
    def __init__(self, parent, **options):
        Canvas.__init__(self, parent, options)

        from icons import seekbar_knob_image

        self.parent = parent
        self.width = options['width']
        self.blue_rectangle = self.create_rectangle(0, 0, 0, 0, fill = 'blue')
        self.seekbar_knob = self.create_image(0, 0, image = seekbar_knob_image)

        self.bind_mouse_button()

    def bind_mouse_button(self):
        self.bind('<Button-1>', self.on_seekbar_clicked)
        self.bind('<B1-Motion>', self.on_seekbar_clicked)

        self.tag_bind(self.blue_rectangle, '<B1-Motion>', self.on_seekbar_clicked)
        self.tag_bind(self.seekbar_knob, '<B1-Motion>', self.on_seekbar_clicked)

    def on_seekbar_clicked(self, event = None):
        self.slide_to_position(event.x)

    def slide_to_position(self, new_position):
        if 0 <= new_position <= self.width:
            self.coords(self.blue_rectangle, 0, 0, new_position, new_position)
            self.coords(self.seekbar_knob, new_position, 0)
            self.event_generate('<<SeekbarPositionChanged>>', x = new_position)


class TestSeekbar():
    def __init__(self):
        root = Tk()
        frame = Frame(root)
        frame.grid(padx = 10, pady = 10)

        c = Seekbar(frame, background = 'black', width = 360, height = 10)
        c.grid()

        root.bind('<<SeekbarPositionChanged>>', self.seek_new_position)
        root.mainloop()

    def seek_new_position(self, event):
        print(f'Dragged to x: {event.x}')

if __name__ == '__main__':
    TestSeekbar()
