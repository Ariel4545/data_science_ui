# imports
import numpy, pandas, sklearn, scipy
import matplotlib.pyplot as plt
import customtkinter, tkinter
from tkinter import messagebox


# window creations

class Window(customtkinter.CTk):
    WIDTH = 700
    HEIGHT = 520

    def __init__(self):
        super().__init__()
        # customtkinter.set_appearance_mode('dark')
        # customtkinter.set_default_color_theme('dark-blue')
        # root = customtkinter.CTk()

        # create window
        self.title('Ariel\'s GDS')
        self.geometry(f'{Window.WIDTH}x{Window.HEIGHT}')
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.resizable(False, False)
        # variables
        self.marker_var = customtkinter.StringVar()
        self.marker_v = ['o', '*', '.', ',', 'x', 'X', '+', 'P', 's', 'D', 'd', 'p', 'H', 'h', 'v', '^', '<', '>', '1',
                         '2',
                         '3', '4', '|', '_']
        self.line_var = customtkinter.StringVar()
        self.line_v = ['-', ':', '--', '-.', '']

        # make ui components
        title = customtkinter.CTkLabel(self, text='Graphical user interface for Matplotlib',
                                       text_font='young 14 underline')
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                       text_font='young 10 underline')
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                       text_font='young 10 underline')
        self.x_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        graph_button = customtkinter.CTkButton(self, text='Make a graph', command=self.make_graph)
        styles_title = customtkinter.CTkLabel(self, text='Change styles!',
                                              text_font='young 12 bold')
        marker_title = customtkinter.CTkLabel(self, text='Choose marker_var',
                                              text_font='young 10 underline')
        marker_select = customtkinter.CTkComboBox(self, state='readonly', variable=self.marker_var, values=self.marker_v,
                                                  fg_color='black', command=self.change_marker)
        line_style_title = customtkinter.CTkLabel(self, text='Choose line_var style',
                                              text_font='young 10 underline')
        line_select = customtkinter.CTkComboBox(self, state='readonly', variable=self.line_var, values=self.line_v,
                                                fg_color='black', command=self.change_line)
        sizes_title = customtkinter.CTkLabel(self, text='Change sizes!',
                                              text_font='young 12 bold')
        dot_title = customtkinter.CTkLabel(self, text='Choose dot size',
                                              text_font='young 10 underline')
        self.dot_select = customtkinter.CTkEntry(self)
        line_title = customtkinter.CTkLabel(self, text='Choose line_var size',
                                           text_font='young 10 underline')
        self.line_select = customtkinter.CTkEntry(self)
        # place ui components
        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0)
        y_title.grid(row=1, column=2)
        self.x_entry.grid(row=2, column=0)
        self.y_entry.grid(row=2, column=2)
        styles_title.grid(row=3, column=1)
        marker_title.grid(row=4, column=0)
        line_style_title.grid(row=4, column=2)
        marker_select.grid(row=5, column=0)
        line_select.grid(row=5, column=2)
        sizes_title.grid(row=6, column=1)
        dot_title.grid(row=7, column=0)
        line_title.grid(row=7, column=2)
        self.dot_select.grid(row=8, column=0)
        self.line_select.grid(row=8, column=2)
        graph_button.grid(row=10, column=1)

    # create the graph:
    def make_graph(self):
        x_values = numpy.array(self.x_entry.get().split(' '))
        y_values = numpy.array(self.y_entry.get().split(' '))
        print(self.change_dot_size())
        try:
            plt.plot(x_values, y_values, marker=self.change_marker(self.marker_var.get()), ms=self.change_dot_size(),
                     linewidth=self.change_line_size(), linestyle=self.change_line(self.line_var.get()))
            plt.show()
        except BaseException:
            messagebox.showerror('error', 'an error occurred')

    # change some basic options:
    def change_marker(self, marker):
        if marker:
            self.chosen_marker = marker
            return self.chosen_marker
        else:
            self.chosen_marker = 'o'
            return self.chosen_marker

    def change_line(self, line_style):
        if line_style:
            self.chosen_line = line_style
            return self.chosen_line
        else:
            self.chosen_line = '-'
            return self.chosen_line

    def change_dot_size(self):
        self.chosen_dot_size = self.dot_select.get()
        if str(self.chosen_dot_size).isdigit():
            self.dot_value = self.chosen_dot_size
            return self.dot_value
        else:
            self.dot_value = 10
            return self.dot_value

    def change_line_size(self):
        self.chosen_line_size = self.line_select.get()
        if str(self.chosen_line_size).isdigit():
            self.line_value = self.chosen_line_size
            return self.line_value
        else:
            self.line_value = 2
            return self.line_value

    # close the application  when the 'x' is pressed
    def on_close(self, event=0):
        self.destroy()


if __name__ == '__main__':
    app = Window()
    app.mainloop()
