import tkinter
import pyperclip
from customtkinter import *
import numpy


class Window(CTk):
    width = 646
    height = 500

    def __init__(self):
        super().__init__()
        # window
        self.geometry(f'{self.width}x{self.height}')
        self.title('Gui for numpy')
        # text box
        self.number_input = tkinter.Text(self, width=80, height=30, wrap=WORD)
        self.number_input.pack()
        # menus
        menu = tkinter.Menu(self)
        self.config(menu=menu)

        arithmetic_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label='arithmetic', menu=arithmetic_menu, state=DISABLED)
        arithmetic_menu.add_command(label='Addition')
        arithmetic_menu.add_command(label='Subtraction')
        arithmetic_menu.add_command(label='Multiplication')
        arithmetic_menu.add_command(label='Division')
        arithmetic_menu.add_command(label='Power')
        arithmetic_menu.add_command(label='Remainder')

        rounding_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label='Rounding', menu=rounding_menu)
        rounding_menu.add_command(label='Truncation', command=lambda: self.round('Truncation'))
        rounding_menu.add_command(label='Rounding', command=lambda: self.round('Rounding'))
        rounding_menu.add_command(label='Floor', command=lambda: self.round('Floor'))
        rounding_menu.add_command(label='Ceil', command=lambda: self.round('Ceil'))

        trigonometry_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label='Trigonometry', menu=trigonometry_menu)
        trigonometry_menu.add_command(label='Sin', command=lambda: self.trigonometry('Sin'))
        trigonometry_menu.add_command(label='Cos', command=lambda: self.trigonometry('Cos'))
        trigonometry_menu.add_command(label='Tan', command=lambda: self.trigonometry('Tan'))
        trigonometry_menu.add_command(label='Degrees Into Radians', command=lambda: self.trigonometry('d2r'))
        trigonometry_menu.add_command(label='Radians to Degrees', command=lambda: self.trigonometry('r2d'))

        statistics_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label='Statistics', menu=statistics_menu)
        statistics_menu.add_command(label='Median', command=lambda: self.statistics('Median'))
        statistics_menu.add_command(label='Average', command=lambda: self.statistics('Average'))
        statistics_menu.add_command(label='Mean', command=lambda: self.statistics('Mean'))
        statistics_menu.add_command(label='Std', command=lambda: self.statistics('Std'))
        statistics_menu.add_command(label='Ptp', command=lambda: self.statistics('Ptp'))

    def turn_into_array(self):
        self.content = (self.number_input.get('1.0', 'end'))
        self.list = list(self.content)
        for i in self.list:
            if not(str(i).isdigit()):
                self.list.remove(i)
        self.array = numpy.array(self.list).astype(int)
        return self.array

    def round(self, mode):
        self.turn_into_array()
        if mode == 'Truncation':
            result = numpy.trunc(self.array)
        elif mode == 'Rounding':
            result = numpy.round(self.array)
        elif mode == 'Floor':
            result = numpy.floor(self.array)
        elif mode == 'Ceil':
            result = numpy.ceil(self.array)
        self.result_page(result)

    def trigonometry(self, mode):
        if mode == 'Sin':
            result = numpy.sin(self.array)
        elif mode == 'Cos':
            result = numpy.cos(self.array)
        elif mode == 'Tan':
            result = numpy.tan(self.array)
        elif mode == 'd2r':
            result = numpy.deg2rad(self.array)
        elif mode == 'r2d':
            result = numpy.rad2deg(self.array)
        self.result_page(result)

    def statistics(self, mode):
        self.turn_into_array()
        if mode == 'Median':
            result = numpy.median(self.array)
        elif mode == 'Average':
            result = numpy.average(self.array)
        elif mode == 'Mean':
            result = numpy.mean(self.array)
        elif mode == 'Std':
            result = numpy.std(self.array)
        elif mode == 'Ptp':
            result = numpy.ptp(self.array)
        self.result_page(result)

    def result_page(self, result):
        result_root = tkinter.Toplevel()
        result_root.title('Result')
        result_output = CTkLabel(result_root, text=f'{result}', fg_color='black')
        copy_button = CTkButton(result_root, text='Copy', command=lambda: pyperclip.copy(str(result)), width=10)
        result_output.pack()
        copy_button.pack()

if __name__ == '__main__':
    win = Window()
    win.mainloop()
