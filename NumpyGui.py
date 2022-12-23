import tkinter
import pyperclip
from customtkinter import *
import numpy
from scipy import constants


class Window(CTk):
    width = 725
    height = 500

    def __init__(self):
        super().__init__()
        # window
        self.geometry(f'{self.width}x{self.height}')
        self.title('Gui for numpy')
        # text boxes
        self.number_input = tkinter.Text(self, width=90, height=20, wrap=WORD)
        self.number_input.pack(fill=BOTH, expand=True)
        self.snumber_input = tkinter.Text(self, width=90, height=10, wrap=WORD)
        self.snumber_input.pack(fill=BOTH, expand=True)
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
        rounding_menu.add_command(label='Fix', command=lambda: self.round('fix'))
        rounding_menu.add_command(label='Rint', command=lambda: self.round('rint'))

        trigonometry_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label='Trigonometry', menu=trigonometry_menu)
        trigonometry_menu.add_command(label='Sin', command=lambda: self.trigonometry('Sin'))
        trigonometry_menu.add_command(label='Cos', command=lambda: self.trigonometry('Cos'))
        trigonometry_menu.add_command(label='Tan', command=lambda: self.trigonometry('Tan'))
        trigonometry_menu.add_command(label='Degrees Into Radians', command=lambda: self.trigonometry('d2r'))
        trigonometry_menu.add_command(label='Radians to Degrees', command=lambda: self.trigonometry('r2d'))
        trigonometry_menu.add_separator()
        trigonometry_menu.add_command(label='Sinh', command=lambda: self.trigonometry('sinh'))
        trigonometry_menu.add_command(label='Cosh', command=lambda: self.trigonometry('cosh'))
        trigonometry_menu.add_command(label='Tanh', command=lambda: self.trigonometry('tanh'))
        trigonometry_menu.add_command(label='angles via sinh', command=lambda: self.trigonometry('arcsinh'))
        trigonometry_menu.add_command(label='angles via cosh', command=lambda: self.trigonometry('arccosh'))
        trigonometry_menu.add_command(label='angles via tanh', command=lambda: self.trigonometry('arctanh'))

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
        random_menu.add_command(label='Randint', command=lambda: self.random('Randint'))
        random_menu.add_command(label='Sample', command=lambda: self.random('sample'))
        random_menu.add_command(label='permutation', command=lambda: self.random('permutation'))


        data_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label='Data operations', menu=data_menu)
        data_menu.add_command(label='Filter by sizes', command=lambda: self.data_operations(mode='size'))
        data_menu.add_command(label='Filter by parity', command=lambda: self.data_operations(mode='parity'))
        data_menu.add_command(label='Sort', command=lambda: self.data_operations(mode='sort'))
        data_menu.add_command(label='Search', command=lambda: self.data_operations(mode='search'))
        data_menu.add_command(label='Get shape', command=lambda: self.data_operations(mode='Get shape'))
        data_menu.add_command(label='Difference', command=lambda: self.data_operations(mode='Difference'))
        data_menu.add_command(label='Product', command=lambda: self.data_operations(mode='Product'))
        data_menu.add_command(label='LCM', command=lambda: self.data_operations(mode='LCM'))
        data_menu.add_command(label='GCD', command=lambda: self.data_operations(mode='GCD'))
        data_menu.add_command(label='Unique', command=lambda: self.data_operations(mode='Unique'))

        ns_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label='Number systems', menu=ns_menu)
        ns_menu.add_command(label='Binary', command=lambda: self.number_system(mode='Binary'))
        ns_menu.add_command(label='Octal', command=lambda: self.number_system(mode='Octal'))
        ns_menu.add_command(label='Hexadecimal', command=lambda: self.number_system(mode='Hexadecimal'))

        exp_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label='Exponents', menu=exp_menu)
        exp_menu.add_command(label='Exp', command=lambda: self.ex('exp'))
        exp_menu.add_command(label='Exp -1', command=lambda: self.ex('exp-1'))
        exp_menu.add_command(label='Exp 2', command=lambda: self.ex('exp2'))
        exp_menu.add_command(label='Log 10', command=lambda: self.ex('log'))
        exp_menu.add_command(label='Log 2', command=lambda: self.ex('log2'))

        const_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label='Constant', menu=const_menu)
        const_menu.add_command(label='Pi', command=lambda: self.const(numpy.pi))
        const_menu.add_command(label='E', command=lambda: self.const(numpy.e))
        const_menu.add_command(label='Golden ratio', command=lambda: self.const(constants.golden))
        const_menu.add_command(label='Speed of light', command=lambda: self.const(constants.speed_of_light))
        const_menu.add_command(label='E0', command=lambda: self.const(constants.epsilon_0))
        const_menu.add_command(label='MU0', command=lambda: self.const(constants.golden))
        const_menu.add_command(label='G', command=lambda: self.const(constants.G))

        self.generate_op_num()

    def turn_into_array(self):
        self.content = (self.number_input.get('1.0', 'end'))
        self.list = (self.content).split(' ')
        # for i in self.list:
        #     # if not(str(i).isdigit()):
        #     #     self.list.remove(i)
        self.array = numpy.array(self.list, dtype='int32')
        print(self.list)
        print(self.array)
        try:
            self.scontent = (self.snumber_input.get('1.0', 'end'))
            self.slist = (self.scontent).split(' ')
            # for x in self.slist:
            #     if not (str(x).isdigit()):
            #         self.slist.remove(x)
            self.sarray = numpy.array(self.slist, dtype='int32')
            return self.sarray
        except:
            pass
        return self.array

    def arithmetics(self, mode):
        self.turn_into_array()
        if mode == 'Addition':
            result = (numpy.add(self.array, self.sarray))
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
        elif mode == 'rint':
            result = numpy.rint(self.array)
        elif mode == 'fix':
            result = numpy.fix(self.array)
        if self.array:
            self.result_page(result)

    def trigonometry(self, mode):
        self.turn_into_array()
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
        elif mode == 'sinh':
            result = numpy.sinh(self.array)
        elif mode == 'cosh':
            result = numpy.cosh(self.array)
        elif mode == 'tanh':
            result = numpy.tanh(self.array)
        elif mode == 'arcsinh':
            result = numpy.arcsinh(self.array)
        elif mode == 'arccosh':
            result = numpy.arccosh(self.array)
        elif mode == 'arctanh':
            result = numpy.arctanh(self.array)
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
        elif mode == 'Randint':
            result = numpy.random.randint(self.array, self.sarray)
        elif mode == 'sample':
            result = numpy.random.random_sample(self.array[0])
        elif mode == 'permutation':
            result = numpy.random.permutation(self.array)

        self.result_page(result)

    def data_operations(self, mode):
        self.turn_into_array()
        if mode == 'size':
            def change_condition():
                if self.size_con_value == '>':
                    self.size_con_value = '<'
                else:
                    self.size_con_value = '>'
                condition_button.configure(text=self.size_con_value)

            def enter():
                filter_array = []
                conditional_number = int(condition_input.get())
                for element in self.array:
                    if self.size_con_value == '>':
                        if element > conditional_number:
                            filter_array.append(True)
                        else:
                            filter_array.append(False)
                    else:
                        if element < conditional_number:
                            filter_array.append(True)
                        else:
                            filter_array.append(False)
                result = self.array[filter_array]
                print(self.array, filter_array)
                self.result_page(result)
                size_root.destroy()

            self.size_con_value = '>'
            size_root = CTkToplevel()
            size_root.title('filter by sizes')
            condition_input = CTkEntry(size_root)
            condition_button = CTkButton(size_root, text=self.size_con_value, command=change_condition)
            condition_label = CTkLabel(size_root, text='your Array')
            enter_button = CTkButton(size_root, text='Enter', command=enter)
            condition_input.grid(row=1, column=0)
            condition_button.grid(row=1, column=1)
            condition_label.grid(row=1, column=2)
            enter_button.grid(row=2, column=1)
        elif mode == 'parity':
            def change_condition():
                if self.parity_con_value == 'even':
                    self.parity_con_value = 'odd'
                else:
                    self.parity_con_value = 'even'
                condition_button.configure(text=self.parity_con_value)

            def enter():
                filter_array = []
                for element in self.array:
                    if self.parity_con_value == 'even':
                        if element % 2 == 0:
                            filter_array.append(True)
                        else:
                            filter_array.append(False)
                    else:
                        if element % 2 != 0:
                            filter_array.append(True)
                        else:
                            filter_array.append(False)
                result = self.array[filter_array]
                self.result_page(result)

            parity_root = CTkToplevel()
            self.parity_con_value = 'even'
            parity_root.title('filter by parity')
            condition_button = CTkButton(parity_root, text=self.parity_con_value, command=change_condition)
            condition_text = CTkLabel(parity_root, text='filter by:')
            enter_button = CTkButton(parity_root, text='Enter', command=enter)
            condition_text.grid(row=1, column=0)
            condition_button.grid(row=1, column=1)
            enter_button.grid(row=2, column=1)

        elif mode == 'sort':
            result = numpy.sort(self.array)
            self.result_page(result)

        elif mode == 'search':
            def enter():
                searched_value = int(search_input.get())
                result = numpy.where(self.array == searched_value)[0]
                self.result_page(result)

            search_root = CTkToplevel()
            search_root.title('search')
            search_input = CTkEntry(search_root)
            enter_button = CTkButton(search_root, text='Enter', command=enter)
            search_input.grid(row=1, column=1)
            enter_button.grid(row=2, column=1)

        elif mode == 'Get shape':
            self.result_page(self.array.shape)
        elif mode == 'Difference':
            self.result_page(numpy.diff(self.array))
        elif mode == 'Product':
            self.result_page(numpy.product(self.array))
        elif mode == 'LCM':
            self.result_page(numpy.lcm(self.array, self.sarray))
        elif mode == 'GCD':
            self.result_page(numpy.gcd(self.array, self.sarray))
        elif mode == 'Unique':
            self.result_page(numpy.unique(self.array))

    def number_system(self, mode):
        self.turn_into_array()
        result = []
        for i in self.array:
            if mode == 'Binary':
                result.append(bin(i))
            elif mode == 'Hexadecimal':
                result.append(hex(i))
            elif mode == 'Octal':
                result.append(oct(i))
            if result:
                self.result_page(result)

    def ex(self, mode):
        self.turn_into_array()
        if mode == 'exp':
            result = numpy.exp(self.array)
        elif mode == 'exp-1':
            result = numpy.expm1(self.array)
        elif mode == 'exp2':
            result = numpy.exp2(self.array)
        elif mode == 'log':
            result = numpy.log10(self.array)
        elif mode == 'log2':
            result = numpy.log2(self.array)

        if result:
            self.result_page(result)

    def const(self, val):
        pos = self.number_input.index(INSERT)
        self.number_input.insert(pos, val)

    def result_page(self, result):
        result_root = tkinter.Toplevel()
        result_root.title('Result:')
        frame = CTkFrame(result_root)
        result_output = CTkLabel(frame, text=f'{result}', fg_color='black')
        copy_button = CTkButton(frame, text='Copy', command=lambda: pyperclip.copy(str(result)), width=10)
        frame.pack(expand=True, fill=BOTH)
        result_output.pack(expand=True, fill=BOTH)
        copy_button.pack(pady=2)

    def generate_op_num(self):
        num = numpy.random.randint(0, 10000, numpy.random.randint(1, 5)).tolist()
        int_num = [int(i) for i in num]
        self.number_input.insert('1.0', int_num)


if __name__ == '__main__':
    win = Window()
    win.mainloop()
