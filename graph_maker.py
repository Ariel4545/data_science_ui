# imports
import numpy, pandas, sklearn, scipy
import matplotlib.pyplot as plt
import customtkinter, tkinter
from tkinter import messagebox


# window creations

class Window(customtkinter.CTk):
    WIDTH = 600
    HEIGHT = 430

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
        self.i = customtkinter.IntVar(value=3)
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
        marker_select = customtkinter.CTkComboBox(self, state='readonly', variable=self.marker_var,
                                                  values=self.marker_v,
                                                  fg_color='black', command=self.change_marker)
        line_style_title = customtkinter.CTkLabel(self, text='Choose line style',
                                                  text_font='young 10 underline')
        line_select = customtkinter.CTkComboBox(self, state='readonly', variable=self.line_var, values=self.line_v,
                                                fg_color='black', command=self.change_line)
        sizes_title = customtkinter.CTkLabel(self, text='Change sizes!',
                                             text_font='young 12 bold')
        dot_title = customtkinter.CTkLabel(self, text='Choose dot size',
                                           text_font='young 10 underline')
        self.dot_select = customtkinter.CTkEntry(self)
        line_title = customtkinter.CTkLabel(self, text='Choose line size',
                                            text_font='young 10 underline')
        self.line_select = customtkinter.CTkEntry(self)
        titles_title = customtkinter.CTkLabel(self, text='Change titles!',
                                              text_font='young 12 bold')
        main_title_ = customtkinter.CTkLabel(self, text='Write main title',
                                             text_font='young 10 underline')
        self.main_title_entry = customtkinter.CTkEntry(self)
        x_title_ = customtkinter.CTkLabel(self, text='Write x-label title',
                                          text_font='young 10 underline')
        self.x_title_entry = customtkinter.CTkEntry(self)
        y_title_ = customtkinter.CTkLabel(self, text='Write y-label title',
                                          text_font='young 10 underline')
        self.y_title_entry = customtkinter.CTkEntry(self)
        grid_title = customtkinter.CTkLabel(self, text='Change grid modes!',
                                              text_font='young 12 bold')
        x_grid = customtkinter.CTkRadioButton(self, text='x', variable=self.i, value=1)
        y_grid = customtkinter.CTkRadioButton(self, text='y', variable=self.i, value=2)
        both_grid = customtkinter.CTkRadioButton(self, text='Both', variable=self.i, value=3)
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
        titles_title.grid(row=9, column=1)
        main_title_.grid(row=10, column=1)
        x_title_.grid(row=10, column=0)
        y_title_.grid(row=10, column=2)
        self.x_title_entry.grid(row=11, column=0)
        self.main_title_entry.grid(row=11, column=1)
        self.y_title_entry.grid(row=11, column=2)
        grid_title.grid(row=12, column=1)
        x_grid.grid(row=13, column=0)
        both_grid.grid(row=13, column=1)
        y_grid.grid(row=13, column=2)
        graph_button.grid(row=14, column=1, pady=10)

    # create the graph:
    def make_graph(self):
        self.change_grid_modes()
        x_values = numpy.array(self.x_entry.get().split(' '))
        y_values = numpy.array(self.y_entry.get().split(' '))
        try:
            plt.plot(x_values, y_values, marker=self.change_marker(self.marker_var.get()), ms=self.change_dot_size(),
                     linewidth=self.change_line_size(), linestyle=self.change_line(self.line_var.get()))
            # titles set
            if self.change_x_title():
                plt.xlabel(self.chosen_x_title)
            if self.change_y_title():
                plt.ylabel(self.chosen_y_title)
            if self.change_main_title():
                plt.title(self.chosen_main_title)
            # grid option set
            plt.grid(axis=self.change_grid_modes())
            # open the graph window
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

    def change_x_title(self):
        self.chosen_x_title = self.x_title_entry.get()
        if self.chosen_x_title:
            return True
        else:
            return False

    def change_y_title(self):
        self.chosen_y_title = self.y_title_entry.get()
        if self.chosen_y_title:
            return True
        else:
            return False

    def change_main_title(self):
        self.chosen_main_title = self.main_title_entry.get()
        if self.chosen_main_title:
            return True
        else:
            return False

    def change_grid_modes(self):
        if self.i.get() == 1:
           return 'x'
        elif self.i.get() == 2:
            return 'y'
        else:
            return 'both'

    # close the application  when the 'x' is pressed
    def on_close(self, event=0):
        self.destroy()


if __name__ == '__main__':
    app = Window()
    app.mainloop()
