# imports
import numpy
import matplotlib.pyplot as plt
import customtkinter, tkinter
from tkinter import messagebox


# main menu - open kinds of data visualizations options
class MainMenu(customtkinter.CTk):
    WIDTH = 275
    HEIGHT = 400
    plt.style.use('dark_background')

    def __init__(self):
        super().__init__()
        self.title('Egon data visualization')
        self.geometry(f'{MainMenu.WIDTH}x{MainMenu.HEIGHT}')
        self.minsize(275, 280)
        self.maxsize(275, 400)

        title = customtkinter.CTkLabel(self, text='Applications:',
                                       text_font='young 14 underline')
        self.open_graphMaker = customtkinter.CTkButton(self, text='Graph maker', command=self.open_gm)
        self.open_histogramMaker = customtkinter.CTkButton(self, text='Histogram maker', command=self.open_hm)
        self.open_barMaker = customtkinter.CTkButton(self, text='Bar maker', command=self.open_bm)
        self.open_pieMaker = customtkinter.CTkButton(self, text='Pie maker', command=self.open_pm)
        self.open_stemMaker = customtkinter.CTkButton(self, text='Stem maker', command=self.open_sm)
        self.open_scatterPlotMaker = customtkinter.CTkButton(self, text='Scatter plot maker', command=self.open_spm)
        s_title = customtkinter.CTkLabel(self, text='Settings:',
                                         text_font='young 14 underline')
        theme_title = customtkinter.CTkLabel(self, text='theme color:',
                                             text_font='young 10')
        self.theme_v = customtkinter.StringVar()
        self.themes = ['dracula', 'light']
        theme_select = customtkinter.CTkComboBox(self, state='readonly', variable=self.theme_v,
                                                 values=self.themes, command=self.change_theme)

        title.pack(pady=10)
        self.open_graphMaker.pack(pady=5)
        self.open_histogramMaker.pack(pady=5)
        self.open_barMaker.pack(pady=5)
        self.open_pieMaker.pack(pady=5)
        self.open_stemMaker.pack(pady=5)
        self.open_scatterPlotMaker.pack(pady=5)
        s_title.pack(pady=2)
        theme_title.pack(pady=1)
        theme_select.pack(pady=1)

    def open_gm(self):
        app = GraphMaker()
        app.mainloop()

    def open_hm(self):
        app = HistogramMaker()
        app.mainloop()

    def open_bm(self):
        app = BarMaker()
        app.mainloop()

    def open_pm(self):
        app = PieMaker()
        app.mainloop()

    def open_sm(self):
        app = StemMaker()
        app.mainloop()

    def open_spm(self):
        app = ScatterPlotMaker()
        app.mainloop()

    def change_theme(self, theme):
        if theme == 'light':
            customtkinter.set_appearance_mode('light')
            plt.style.use('default')
        else:
            customtkinter.set_appearance_mode('dark')
            plt.style.use('dark_background')


class ScatterPlotMaker(customtkinter.CTk):
    WIDTH = 500
    HEIGHT = 200

    def __init__(self):
        super().__init__()
        self.title('Egon scatter plot maker')
        self.geometry(f'{ScatterPlotMaker.WIDTH}x{ScatterPlotMaker.HEIGHT}')
        self.resizable(False, False)

        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         text_font='young 10 underline')
        colors_title = customtkinter.CTkLabel(self, text='colors values:',
                                         text_font='young 10 underline')
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         text_font='young 10 underline')
        self.x_entry = customtkinter.CTkEntry(self)
        self.colors_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)

        styles_title = customtkinter.CTkLabel(self, text='Styles:', text_font='young 12 bold')
        transparency_title = customtkinter.CTkLabel(self, text='transparency:',
                                                    text_font='young 10 underline')
        size_title = customtkinter.CTkLabel(self, text='sizes:',
                                            text_font='young 10 underline')
        self.transparency = customtkinter.CTkSlider(self, from_=0, to=100, orient='horizontal')
        self.transparency.set(100)
        self.size = customtkinter.CTkEntry(self)

        color_maps_values = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
        color_maps_v = tkinter.StringVar()
        self.color_map = customtkinter.CTkComboBox(self, values=color_maps_values, variable=color_maps_v)

        self.make_scatter = customtkinter.CTkButton(self, command=self.make_scatter_plot, text='Make scatter plot')

        x_title.grid(row=1, column=0)
        colors_title.grid(row=1, column=1)
        y_title.grid(row=1, column=2)
        self.x_entry.grid(row=2, column=0)
        self.colors_entry.grid(row=2, column=1)
        self.y_entry.grid(row=2, column=2)
        styles_title.grid(row=3, column=1)
        size_title.grid(row=4, column=0)

        transparency_title.grid(row=4, column=2)
        self.size.grid(row=5, column=0)
        self.color_map.grid(row=5, column=1)
        self.transparency.grid(row=5, column=2)
        self.make_scatter.grid(row=10, column=1)

    def make_scatter_plot(self):
        self.x_values = numpy.array(self.x_entry.get().split(' '))
        y_values = numpy.array(self.y_entry.get().split(' '))
        plt.clf()
        plt.scatter(self.x_values, y_values, cmap=self.color_m(self.color_map.get()), alpha=self.trans(), s=self.size_(),
                    c=self.colors_())
        plt.colorbar()
        plt.show()

    def color_m(self, cm):
        if cm:
            return cm
        else:
            return 'inferno'

    def trans(self):
        self.trans_v = (self.transparency.get() / 100)
        return self.trans_v

    def size_(self):
        if self.size.get():
            return float(self.size.get())
        else:
            return 20

    def colors_(self):
        if self.colors_entry.get():
            colors_values = (self.colors_entry.get().split(' '))
            colors_values = list(map(int, colors_values))
            return colors_values
        else:
            colors_values = []
            for i in range(len(self.x_values)):
                colors_values.append(numpy.random.randint(1, 100))
            return colors_values


class StemMaker(customtkinter.CTk):
    WIDTH = 450
    HEIGHT = 200

    def __init__(self):
        super().__init__()
        self.title('Egon stem maker')
        self.geometry(f'{StemMaker.WIDTH}x{StemMaker.HEIGHT}')
        self.resizable(False, False)

        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         text_font='young 10 underline')
        bottom_title = customtkinter.CTkLabel(self, text='bottom value:',
                                              text_font='young 10 underline')
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         text_font='young 10 underline')
        self.x_entry = customtkinter.CTkEntry(self)
        self.bottom_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        stem_button = customtkinter.CTkButton(self, text='Make a graph', command=self.make_stem)

        styles_title = customtkinter.CTkLabel(self, text='Styles:', text_font='young 12 bold')
        line_title = customtkinter.CTkLabel(self, text='lines format:', text_font='young 10 underline')
        marker_title = customtkinter.CTkLabel(self, text='marker format:', text_font='young 10 underline')

        line_values = ['-', '--', '_.', ':']
        marker_values = ['ro', 'r-', 'g--', 'm:']
        line_var = tkinter.StringVar()
        marker_var = tkinter.StringVar()
        self.line = customtkinter.CTkComboBox(self, values=line_values, variable=line_var)
        self.marker = customtkinter.CTkComboBox(self, values=marker_values, variable=marker_var)

        x_title.grid(row=1, column=0)
        bottom_title.grid(row=1, column=1)
        y_title.grid(row=1, column=2)
        self.x_entry.grid(row=2, column=0)
        self.bottom_entry.grid(row=2, column=1)
        self.y_entry.grid(row=2, column=2)
        styles_title.grid(row=3, column=1)
        line_title.grid(row=4, column=0)
        marker_title.grid(row=4, column=2)
        self.line.grid(row=5, column=0)
        self.marker.grid(row=5, column=2)

        stem_button.grid(row=10, column=1)

    def make_stem(self):
        x_values = numpy.array(self.x_entry.get().split(' '))
        y_values = numpy.array(self.y_entry.get().split(' '))
        plt.clf()
        plt.stem(x_values, y_values, bottom=self.bottom(), linefmt=self.change_line(self.line.get()),
                 markerfmt=self.change_marker(self.marker.get()))
        plt.show()

    def bottom(self):
        if self.bottom_entry.get():
            return self.bottom_entry.get()
        else:
            return 0

    def change_marker(self, marker):
        if marker:
            return marker
        else:
            return 'ro'

    def change_line(self, line):
        if line:
            return line
        else:
            return '-'


class PieMaker(customtkinter.CTk):
    WIDTH = 650
    HEIGHT = 350

    def __init__(self):
        super().__init__()
        self.title('Egon pie-chart maker')
        self.geometry(f'{PieMaker.WIDTH}x{PieMaker.HEIGHT}')
        self.resizable(False, False)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Pie-charts',
                                       text_font='young 14 underline')
        percentage_title = customtkinter.CTkLabel(self, text='values:',
                                                  text_font='young 10 underline')
        self.percentage_entry = customtkinter.CTkEntry(self)
        names_title = customtkinter.CTkLabel(self, text='Names:',
                                             text_font='young 10 underline')
        self.names_entry = customtkinter.CTkEntry(self)

        self.s_var = tkinter.IntVar()
        self.l_var = tkinter.IntVar()
        styles_title = customtkinter.CTkLabel(self, text='Styles',
                                              text_font='young 12 bold')
        shadows = customtkinter.CTkCheckBox(self, text='Shadows', variable=self.s_var)
        sa_title = customtkinter.CTkLabel(self, text='start angle:',
                                          text_font='young 10 underline')
        self.start_angle = customtkinter.CTkEntry(self)
        legend_tt = customtkinter.CTkLabel(self, text='Legend title:',
                                           text_font='young 10 underline')
        legend_title = customtkinter.CTkLabel(self, text='Legend:',
                                              text_font='young 12 bold')
        legend = customtkinter.CTkCheckBox(self, text='Legend', variable=self.l_var)
        self.legend_selected_title = customtkinter.CTkEntry(self)
        explode_title = customtkinter.CTkLabel(self, text='Explode values:',
                                               text_font='young 10 underline')
        self.explode_entry = customtkinter.CTkEntry(self)

        pie_button = customtkinter.CTkButton(self, text='Make a pie-chart', command=self.pie_maker)

        title.grid(row=0, column=1)
        percentage_title.grid(row=1, column=0)
        names_title.grid(row=1, column=2)
        self.percentage_entry.grid(row=2, column=0)
        self.names_entry.grid(row=2, column=2)
        legend_title.grid(row=4, column=1)
        legend_tt.grid(row=5, column=2)
        legend.grid(row=6, column=0)
        self.legend_selected_title.grid(row=6, column=2, pady=10)
        styles_title.grid(row=9, column=1)
        explode_title.grid(row=10, column=1)
        sa_title.grid(row=10, column=2)
        shadows.grid(row=11, column=0)
        self.explode_entry.grid(row=11, column=1)
        self.start_angle.grid(row=11, column=2)

        pie_button.grid(row=12, column=1, pady=10)

    def pie_maker(self):
        percentages_values = numpy.array(self.percentage_entry.get().split(' '))

        if self.labels():
            plt.pie(percentages_values, explode=self.explode(), labels=self.labels(), shadow=self.s_var.get(),
                    startangle=self.angle())
        else:
            plt.pie(percentages_values, explode=self.explode(), shadow=self.s_var.get(), startangle=self.angle())

        if self.l_var.get() == 1:
            plt.legend(title=self.legend())
        plt.show()

    def explode(self):
        if self.explode_entry.get():
            explode_values = (self.explode_entry.get().split(' '))
            for f in explode_values:
                explode_values.remove(f)
                explode_values.append(float(f))
            print(explode_values)
            return (explode_values)
        # else:
        #     print(numpy.zeros(int(len(self.percentage_entry.get()))))

    def labels(self):
        if self.names_entry.get():
            names_values = (self.names_entry.get().split(' '))
            print(self.names_entry.get(), names_values)
            return names_values
        else:
            return False

    def legend(self):
        if self.legend_selected_title.get():
            return self.legend_selected_title.get()
        else:
            ''

    def angle(self):
        if self.start_angle.get():
            return int(self.start_angle.get())
        else:
            return 0


class HistogramMaker(customtkinter.CTk):
    WIDTH = 650
    HEIGHT = 300

    def __init__(self):
        super().__init__()
        self.title('Egon histogram maker')
        self.geometry(f'{HistogramMaker.WIDTH}x{HistogramMaker.HEIGHT}')
        self.resizable(False, False)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Histograms',
                                       text_font='young 14 underline')
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         text_font='young 10 underline')
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         text_font='young 10 underline')
        self.x_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)

        # titles_title = customtkinter.CTkLabel(self, text='Change titles!',
        #                                       text_font='young 12 bold')

        titles_title = customtkinter.CTkLabel(self, text='Choose titles!',
                                              text_font='young 12 bold')
        main_title_ = customtkinter.CTkLabel(self, text='Write main title',
                                             text_font='young 10 underline')
        self.main_title_entry = customtkinter.CTkEntry(self)
        x_title_ = customtkinter.CTkLabel(self, text='Write x-label title',
                                          text_font='young 10 underline')
        self.x_title_entry = customtkinter.CTkEntry(self)
        y_title_ = customtkinter.CTkLabel(self, text='Write y-label title')
        self.y_title_entry = customtkinter.CTkEntry(self)

        grid_title = customtkinter.CTkLabel(self, text='Grid modes!', text_font='young 12 bold')
        self.g = customtkinter.IntVar(value=3)
        x_grid = customtkinter.CTkRadioButton(self, text='x', variable=self.g, value=1)
        y_grid = customtkinter.CTkRadioButton(self, text='y', variable=self.g, value=2)
        both_grid = customtkinter.CTkRadioButton(self, text='Both', variable=self.g, value=3)

        histogram_button = customtkinter.CTkButton(self, text='Make a histogram', command=self.make_histogram)

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0)
        y_title.grid(row=1, column=2)
        self.x_entry.grid(row=2, column=0)
        self.y_entry.grid(row=2, column=2)
        titles_title.grid(row=3, column=1)
        x_title_.grid(row=4, column=0)
        main_title_.grid(row=4, column=1)
        y_title_.grid(row=4, column=2)
        self.x_title_entry.grid(row=5, column=0)
        self.main_title_entry.grid(row=5, column=1)
        self.y_title_entry.grid(row=5, column=2)
        grid_title.grid(row=6, column=1)
        x_grid.grid(row=7, column=0)
        both_grid.grid(row=7, column=1)
        y_grid.grid(row=7, column=2)
        histogram_button.grid(row=10, column=1, pady=10)

    def make_histogram(self):
        x_values = numpy.array(self.x_entry.get().split(' '))
        y_values = numpy.array(self.y_entry.get().split(' '))
        try:
            plt.clf()
            plt.hist(x_values, y_values)

            if self.xtitle():
                plt.xlabel(self.xtitle())
            if self.ytitle():
                plt.ylabel(self.ytitle())
            if self.main_title():
                plt.title(self.main_title())

            plt.grid(axis=self.grid_modes())

            plt.show()
        except ValueError:
            tkinter.messagebox.showerror('error', 'y values must increase monotonically')

    def xtitle(self):
        if self.x_title_entry.get():
            return self.x_title_entry.get()
        else:
            return False

    def ytitle(self):
        if self.y_title_entry.get():
            return self.y_title_entry.get()
        else:
            return False

    def main_title(self):
        if self.main_title_entry.get():
            return self.main_title_entry.get()
        else:
            return False

    def grid_modes(self):
        if self.g.get() == 1:
            return 'x'
        elif self.g.get() == 2:
            return 'y'
        else:
            return 'both'


class BarMaker(customtkinter.CTk):
    WIDTH = 600
    HEIGHT = 300

    def __init__(self):
        super().__init__()
        self.title('Egon bar maker')
        self.geometry(f'{BarMaker.WIDTH}x{BarMaker.HEIGHT}')
        self.resizable(False, False)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Bars',
                                       text_font='young 14 underline')
        bar_name_title = customtkinter.CTkLabel(self, text='bar names:',
                                                text_font='young 10 underline')
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         text_font='young 10 underline')
        self.bar_name_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        graph_button = customtkinter.CTkButton(self, text='Make a bar', command=self.make_bar)

        self.change_width_title = customtkinter.CTkLabel(self, text='change bars width:',
                                                         text_font='young 10 underline')
        self.bar_width = customtkinter.CTkEntry(self)

        self.change_direction_title = customtkinter.CTkLabel(self, text='bars direction:',
                                                             text_font='young 12 bold')
        self.i2 = customtkinter.IntVar(value=1)
        horizontal = customtkinter.CTkRadioButton(self, text='horizontal', variable=self.i2, value=1)
        vertical = customtkinter.CTkRadioButton(self, text='vertical', variable=self.i2, value=2)

        self.l_var = tkinter.IntVar()
        legend_tt = customtkinter.CTkLabel(self, text='Legend title:',
                                           text_font='young 10 underline')
        legend_title = customtkinter.CTkLabel(self, text='Legend:',
                                              text_font='young 12 bold')
        legend = customtkinter.CTkCheckBox(self, text='Legend', variable=self.l_var)
        self.legend_selected_title = customtkinter.CTkEntry(self)

        title.grid(row=0, column=1)
        bar_name_title.grid(row=1, column=0)
        y_title.grid(row=1, column=2)
        self.bar_name_entry.grid(row=2, column=0)
        self.y_entry.grid(row=2, column=2)
        self.change_width_title.grid(row=1, column=1)
        self.bar_width.grid(row=2, column=1)
        self.change_direction_title.grid(row=5, column=1)
        horizontal.grid(row=6, column=0)
        vertical.grid(row=6, column=2)
        legend_title.grid(row=7, column=1)
        legend_tt.grid(row=8, column=0)
        legend.grid(row=9, column=2)
        self.legend_selected_title.grid(row=9, column=0)
        graph_button.grid(row=10, column=1, pady=10)

    def make_bar(self):
        x_values = numpy.array(self.bar_name_entry.get().split(' '))
        y_values = numpy.array(self.y_entry.get().split(' '))
        try:
            if self.i2.get() == 1:
                plt.clf()
                plt.bar(x_values, y_values, width=self.change_width())
            else:
                plt.barh(x_values, y_values, height=self.change_width())
            if self.l_var.get() == 1:
                plt.legend(title=self.legend())
            plt.show()
        except ValueError:
            tkinter.messagebox.showerror('error', 'y values must increase monotonically')

    def change_width(self):
        if self.bar_width.get():
            return float(self.bar_width.get())
        else:
            return 1

    def graph_direction(self):
        if self.i2.get() == 1:
            return 'h'
        elif self.i2.get() == 2:
            return 'v'

    def legend(self):
        if self.legend_selected_title.get():
            return self.legend_selected_title.get()
        else:
            ''


# graph maker window creations
class GraphMaker(customtkinter.CTk):
    WIDTH = 600
    HEIGHT = 525

    def __init__(self):
        super().__init__()
        # customtkinter.set_appearance_mode('dark')
        # customtkinter.set_default_color_theme('dark-blue')
        # root = customtkinter.CTk()

        # create window
        self.title('Egon graph maker')
        self.geometry(f'{GraphMaker.WIDTH}x{GraphMaker.HEIGHT}')
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
        title = customtkinter.CTkLabel(self, text='Graphical user interface for Graphs',
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
        marker_title = customtkinter.CTkLabel(self, text='Choose marker',
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
        '''
        I know some of the things with the infinite line seems not in place.
        I did this intentionally because of the fail attempt to make this feature more modern.
        so It's like a reminder for next time.
        '''
        inf_line_title = customtkinter.CTkLabel(self, text='Make an infinite line!',
                                                text_font='young 12 bold')
        inf_line_x_t = customtkinter.CTkLabel(self, text='Write value',
                                              text_font='young 10 underline')
        inf_line_y_t = customtkinter.CTkLabel(self, text='select mode',
                                              text_font='young 10 underline')
        # inf_line_slope_t = customtkinter.CTkLabel(self, text='Write slope value',
        # text_font='young 10 underline')
        self.inf_line_value = customtkinter.CTkEntry(self)
        self.inf_line_v = tkinter.StringVar()
        self.sinf_line = ['vertical', 'horizontal']
        self.inf_line_mode = customtkinter.CTkComboBox(self, state='readonly', variable=self.inf_line_v,
                                                       values=self.sinf_line)
        # self.inf_line_slope = customtkinter.CTkEntry(self)
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
        inf_line_title.grid(row=14, column=1)
        inf_line_x_t.grid(row=15, column=0)
        # inf_line_slope_t.grid(row=15, column=1)
        inf_line_y_t.grid(row=15, column=2)
        self.inf_line_value.grid(row=16, column=0)
        # self.inf_line_slope.grid(row=16, column=1)
        self.inf_line_mode.grid(row=16, column=2)
        graph_button.grid(row=17, column=1, pady=10)

    # create the graph:
    def make_graph(self):

        self.change_grid_modes()
        x_values = numpy.array(self.x_entry.get().split(' '))
        y_values = numpy.array(self.y_entry.get().split(' '))
        try:
            plt.clf()

            # infinite line set
            if self.inf_line():
                if self.inf_line() == 'vertical':
                    plt.axvline(x=self.infv1, linestyle='--')
                elif self.inf_line() == 'horizontal':
                    plt.axhline(y=self.infv1, linestyle='--')

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

    def inf_line(self):
        if self.inf_line_value.get():
            self.infv1 = self.inf_line_value.get()
            if self.inf_line_mode.get():
                return self.inf_line_mode.get()
        else:
            return False

    # close the application  when the 'x' is pressed
    def on_close(self, event=0):
        self.destroy()


if __name__ == '__main__':
    mm = MainMenu()
    mm.mainloop()
