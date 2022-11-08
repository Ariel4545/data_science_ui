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
        # text boxes
        self.number_input = tkinter.Text(self, width=80, height=20, wrap=WORD)
        self.number_input.pack()
        self.snumber_input = tkinter.Text(self, width=80, height=10, wrap=WORD)
        self.snumber_input.pack()
        # menus
        menu = tkinter.Menu(self)
        self.config(menu=menu)

        arithmetic_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label='arithmetic', menu=arithmetic_menu, state=ACTIVE)
        arithmetic_menu.add_command(label='Addition', command=lambda: self.arithmetics('Addition'))
        arithmetic_menu.add_command(label='Subtraction', command=lambda: self.arithmetics('Subtraction'))
        arithmetic_menu.add_command(label='Multiplication', command=lambda: self.arithmetics('Multiplication'))
        arithmetic_menu.add_command(label='Division', command=lambda: self.arithmetics('Division'))
        arithmetic_menu.add_separator()
        arithmetic_menu.add_command(label='Power', command=lambda: self.arithmetics('Power'))
        arithmetic_menu.add_command(label='square', command=lambda: self.arithmetics('square'))
        arithmetic_menu.add_command(label='square root', command=lambda: self.arithmetics('square root'))
        arithmetic_menu.add_command(label='Remainder', command=lambda: self.arithmetics('Remainder'))
        arithmetic_menu.add_command(label='Absolute', command=lambda: self.arithmetics('Absolute'))

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
        statistics_menu.add_command(label='Min', command=lambda: self.statistics('Min'))
        statistics_menu.add_command(label='Max', command=lambda: self.statistics('Max'))
        statistics_menu.add_command(label='Std', command=lambda: self.statistics('Std'))
        statistics_menu.add_command(label='Ptp', command=lambda: self.statistics('Ptp'))


        random_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label='Random', menu=random_menu)
        random_menu.add_command(label='Choice', command=lambda: self.random('Choice'))
        random_menu.add_command(label='Generate unit interval', command=lambda: self.random('Generate unit interval'))


    def turn_into_array(self):
        self.content = (self.number_input.get('1.0', 'end'))
        self.list = list(self.content)
        for i in self.list:
            if not(str(i).isdigit()):
                self.list.remove(i)
        self.array = numpy.array(self.list).astype(int)
        try:
            self.scontent = (self.snumber_input.get('1.0', 'end'))
            self.slist = list(self.scontent)
            for x in self.slist:
                if not (str(x).isdigit()):
                    self.slist.remove(x)
            self.sarray = numpy.array(self.slist).astype(int)
            return self.sarray
        except:
            pass
        return self.array

    def arithmetics(self, mode):
        self.turn_into_array()
        if mode == 'Addition':
            result = numpy.add(self.array, self.sarray)
        elif mode == 'Subtraction':
            result = numpy.subtract(self.array, self.sarray)
        elif mode == 'Multiplication':
            result = numpy.multiply(self.array, self.sarray)
        elif mode == 'Division':
            result = numpy.divide(self.array, self.sarray)
        elif mode == 'Power':
            result = numpy.power(self.array, self.sarray)
        elif mode == 'Remainder':
            result = numpy.remainder(self.array, self.sarray)
        elif mode == 'Absolute':
            result = numpy.abs(self.array)
        elif mode == 'square root':
            result = numpy.sqrt(self.array)
        elif mode == 'square':
            result = numpy.square(self.array)
        if self.array:
            self.result_page(result)

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
        if self.array:
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
        if self.array:
            self.result_page(result)

    def statistics(self, mode):
        self.turn_into_array()
        if mode == 'Median':
            result = numpy.median(self.array)
        elif mode == 'Average':
            result = numpy.average(self.array)
        elif mode == 'Mean':
            result = numpy.mean(self.array)
        elif mode == 'Min':
            result = numpy.min(self.array)
        elif mode == 'Max':
            result = numpy.max(self.array)
        elif mode == 'Std':
            result = numpy.std(self.array)
        elif mode == 'Ptp':
            result = numpy.ptp(self.array)
        if self.array:
            self.result_page(result)

    def random(self, mode):
        self.turn_into_array()
        if mode == 'Choice':
            result = numpy.random.choice(self.array)
        elif mode == 'Generate unit interval':
            result = numpy.random.rand()
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
