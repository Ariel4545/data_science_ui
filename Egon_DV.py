# imports
import numpy, pandas
import matplotlib.pyplot as plt
import customtkinter, tkinter
from tkinter import messagebox, filedialog
from PIL import Image


# global functions for common things
def upload(entry):
    file_name = filedialog.askopenfilename(title='Open file', filetypes=(('All', '*.*'), ('CSV', 'csv.*')))
    if file_name:
        entry.delete(0, tkinter.END)
        stuff = pandas.read_csv(file_name)

        p = 0
        for val in stuff:
            entry.insert(p, val)
            p += len(val)


def open_app(application):
    app = application()
    app.mainloop()


def title_condition(entry):
    if entry.get():
        return entry.get()
    else:
        return False


def make_array(entry):
    return numpy.array(entry.get().split(' '))


# main menu - open kinds of data visualizations options
class MainMenu(customtkinter.CTk):
    WIDTH = 275
    HEIGHT = 540
    plt.style.use('dark_background')

    def __init__(self):
        super().__init__()
        self.title('Egon data visualization')
        self.geometry(f'{MainMenu.WIDTH}x{MainMenu.HEIGHT}')
        self.minsize(275, MainMenu.HEIGHT - 110)
        self.maxsize(275, MainMenu.HEIGHT)

        title = customtkinter.CTkLabel(self, text='Applications:',
                                       text_font='young 14 underline')
        self.open_graphMaker = customtkinter.CTkButton(self, text='Graph maker', command=lambda: open_app(GraphMaker))
        self.open_histogramMaker = customtkinter.CTkButton(self, text='Histogram maker', command=lambda: open_app(
            HistogramMaker))
        self.open_barMaker = customtkinter.CTkButton(self, text='Bar maker', command=lambda: open_app(BarMaker))
        self.open_pieMaker = customtkinter.CTkButton(self, text='Pie maker', command=lambda: open_app(PieMaker))
        self.open_stemMaker = customtkinter.CTkButton(self, text='Stem maker', command=lambda: open_app(StemMaker))
        self.open_scatterPlotMaker = customtkinter.CTkButton(self, text='Scatter plot maker', command=lambda: open_app(
            ScatterPlotMaker))
        self.open_imShowBarMaker = customtkinter.CTkButton(self, text='ImShow maker', command=lambda: open_app(
            ImShowMaker))
        self.open_contourMaker = customtkinter.CTkButton(self, text='Contour maker', command=lambda: open_app(
            ContourfMaker))
        self.open_errorBarMaker = customtkinter.CTkButton(self, text='Error bar maker', command=lambda: open_app(
            ErrorBarMaker))
        self.open_bloxPlotMaker = customtkinter.CTkButton(self, text='Plot box maker', command=lambda: open_app(
            BoxPlot))
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
        self.open_imShowBarMaker.pack(pady=5)
        self.open_contourMaker.pack(pady=5)
        self.open_errorBarMaker.pack(pady=5)
        self.open_bloxPlotMaker.pack(pady=5)

        s_title.pack(pady=2)
        theme_title.pack(pady=1)
        theme_select.pack(pady=1)

    def change_theme(self, theme):
        if theme == 'light':
            customtkinter.set_appearance_mode('light')
            plt.style.use('default')
        else:
            customtkinter.set_appearance_mode('dark')
            plt.style.use('dark_background')


class BoxPlot(customtkinter.CTk):
    WIDTH = 600
    HEIGHT = 300

    def __init__(self):
        super().__init__()
        self.title('Egon Box plot')
        self.geometry(f'{BoxPlot.WIDTH}x{BoxPlot.HEIGHT}')
        self.resizable(False, False)
        self.pa_var = tkinter.IntVar()
        self.notch_var = tkinter.IntVar()
        self.line_var = tkinter.StringVar()
        ls_values = [' ', 'solid', 'dashed', 'dashdot', 'dotted']

        title = customtkinter.CTkLabel(self, text='Graphical user interface for BoxPlots',
                                       text_font='young 14 underline')
        data_title = customtkinter.CTkLabel(self, text='data values:', text_font='young 10 underline')
        self.data_entry1 = customtkinter.CTkEntry(self)
        self.data_entry2 = customtkinter.CTkEntry(self)
        self.data_entry3 = customtkinter.CTkEntry(self)
        patchA_checkbox = customtkinter.CTkCheckBox(self, text='Patch artist', variable=self.pa_var)
        notch_checkbox = customtkinter.CTkCheckBox(self, text='Notch', variable=self.notch_var)
        lines_title = customtkinter.CTkLabel(self, text='Lines:', text_font='young 12 bold')
        line_width_title = customtkinter.CTkLabel(self, text='line width:', text_font='young 10 underline')
        line_style_title = customtkinter.CTkLabel(self, text='line style:', text_font='young 10 underline')
        self.line_width = customtkinter.CTkEntry(self)
        self.line_style = customtkinter.CTkComboBox(self, values=ls_values, variable=self.line_var)
        names_title = customtkinter.CTkLabel(self, text='Names:', text_font='young 12 bold')
        title_title = customtkinter.CTkLabel(self, text='main title:', text_font='young 10 underline')
        x_val_title = customtkinter.CTkLabel(self, text='X-axis names:', text_font='young 10 underline')
        self.title = customtkinter.CTkEntry(self)
        x_values_names = customtkinter.CTkEntry(self, state=tkinter.DISABLED)
        boxplot_button = customtkinter.CTkButton(self, text='Make box plot', command=self.make_boxplot)

        title.grid(row=0, column=1)
        data_title.grid(row=1, column=1)
        self.data_entry1.grid(row=2, column=0)
        self.data_entry2.grid(row=2, column=1)
        self.data_entry3.grid(row=2, column=2)
        patchA_checkbox.grid(row=3, column=0)
        notch_checkbox.grid(row=3, column=2)
        lines_title.grid(row=4, column=1)
        line_style_title.grid(row=4, column=0)
        line_width_title.grid(row=4, column=2)
        self.line_style.grid(row=5, column=0)
        self.line_width.grid(row=5, column=2)
        names_title.grid(row=6, column=1)
        title_title.grid(row=7, column=0)
        x_val_title.grid(row=7, column=2)
        self.title.grid(row=8, column=0)
        x_values_names.grid(row=8, column=2)
        boxplot_button.grid(row=10, column=1)

    def make_boxplot(self):
        plt.clf()
        x = plt.boxplot(self.data_values(), patch_artist=self.pa_var.get(), notch=self.notch_var.get())
        # lines management
        for whisker in x['whiskers']:
            whisker.set(linewidth=self.line_w(), linestyle=self.lineStyle(self.line_style.get()))
        if title_condition(self.title):
            plt.title(title_condition(self.title))
        # if self.title_():
        #     pass
        plt.show()

    def data_values(self):
        self.data = []
        if self.data_entry1.get():
            self.data.append(numpy.array(self.data_entry1.get().split(' '), dtype='int'))
        if self.data_entry2.get():
            self.data.append(numpy.array(self.data_entry2.get().split(' '), dtype='int'))
        if self.data_entry3.get():
            self.data.append(numpy.array(self.data_entry3.get().split(' '), dtype='int'))
        return self.data

    def line_w(self):
        if self.line_width.get():
            return float(self.line_width.get())
        else:
            return 3.0

    def x_names(self):
        if self.title.get():
            stitle = make_array(self.title)
            return stitle
        else:
            return False

    def lineStyle(self, style):
        if style:
            return style
        else:
            '--'


class ErrorBarMaker(customtkinter.CTk):
    WIDTH = 600
    HEIGHT = 250

    def __init__(self):
        super().__init__()
        self.title('Egon Error bar maker')
        self.geometry(f'{ErrorBarMaker.WIDTH}x{ErrorBarMaker.HEIGHT}')
        self.resizable(False, False)
        self.u_var = tkinter.IntVar()
        self.l_var = tkinter.IntVar()

        title = customtkinter.CTkLabel(self, text='Graphical user interface for ErrorBars',
                                       text_font='young 14 underline')
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         text_font='young 10 underline')
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         text_font='young 10 underline')
        self.x_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        xerr_title = customtkinter.CTkLabel(self, text='xerr value:',
                                            text_font='young 10 underline')
        yerr_title = customtkinter.CTkLabel(self, text='yerr value:',
                                            text_font='young 10 underline')
        self.xerr_entry = customtkinter.CTkEntry(self)
        self.yerr_entry = customtkinter.CTkEntry(self)
        upload_x = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
        upload_y = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))
        uplims_checkbox = customtkinter.CTkCheckBox(self, text='upper limits', variable=self.u_var)
        lolims_checkbox = customtkinter.CTkCheckBox(self, text='lower limits', variable=self.l_var)
        eb_button = customtkinter.CTkButton(self, text='make error bar', command=self.make_errorBar)

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0)
        y_title.grid(row=1, column=2)
        self.x_entry.grid(row=2, column=0)
        self.y_entry.grid(row=2, column=2)
        upload_x.grid(row=3, column=0)
        upload_y.grid(row=3, column=2)
        xerr_title.grid(row=4, column=0)
        yerr_title.grid(row=4, column=2)
        self.xerr_entry.grid(row=5, column=0)
        self.yerr_entry.grid(row=5, column=2)
        uplims_checkbox.grid(row=6, column=0)
        lolims_checkbox.grid(row=6, column=2)
        eb_button.grid(row=10, column=1)

    def make_errorBar(self):
        plt.clf()
        self.x_values = numpy.array(self.x_entry.get().split(' '), dtype='int32')
        self.y_values = numpy.array(self.y_entry.get().split(' '), dtype='int32')
        self.xerr_values = abs(float(self.xerr_entry.get()))
        self.yerr_values = abs(float(self.yerr_entry.get()))
        # self.xerr_values.reshape(1, len((self.xerr_values)))
        # self.yerr_values.reshape(1, len((self.yerr_values)))
        plt.errorbar(self.x_values, self.y_values, xerr=self.xerr_values, yerr=self.yerr_values,
                     uplims=self.u_var.get(), lolims=self.l_var.get())
        plt.show()


class ContourfMaker(customtkinter.CTk):
    WIDTH = 600
    HEIGHT = 250

    def __init__(self):
        super().__init__()
        self.title('Egon contourf Maker')
        self.geometry(f'{ContourfMaker.WIDTH}x{ContourfMaker.HEIGHT}')
        self.resizable(False, False)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for ContourF',
                                       text_font='young 14 underline')
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         text_font='young 10 underline')
        z_title = customtkinter.CTkLabel(self, text='z values:',
                                         text_font='young 10 underline')
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         text_font='young 10 underline')
        self.x_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        # z_frame = customtkinter.CTkFrame(self)
        self.z_entry = customtkinter.CTkEntry(self)
        self.z_entry2 = customtkinter.CTkEntry(self)
        self.z_entry3 = customtkinter.CTkEntry(self)
        self.z_entry4 = customtkinter.CTkEntry(self)
        upload_x = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
        upload_z = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.z_entry))
        upload_y = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))
        contour_button = customtkinter.CTkButton(self, text='make contourf', command=self.make_contourf)
        title_title = customtkinter.CTkLabel(self, text='title:', text_font='young 10 underline')
        title_entry = customtkinter.CTkEntry(self)

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0)
        z_title.grid(row=2, column=1)
        y_title.grid(row=1, column=2)
        self.x_entry.grid(row=2, column=0)
        self.z_entry.grid(row=3, column=1)
        self.z_entry2.grid(row=4, column=0)
        self.z_entry3.grid(row=4, column=1)
        self.z_entry4.grid(row=4, column=2)
        self.y_entry.grid(row=2, column=2)
        upload_x.grid(row=3, column=0, pady=3)
        upload_y.grid(row=3, column=2, pady=3)
        contour_button.grid(row=10, column=1)

    def make_contourf(self):
        self.x_values = make_array(self.x_entry)
        # must be 2x2 - D array!!!
        self.z_values = tuple(numpy.array((self.z_entry.get().split(' '), self.z_entry2.get().split(' '),
                                           self.z_entry3.get().split(' '), self.z_entry4.get().split()), dtype='int32'
                                          ).reshape(2, 2))
        self.y_values = make_array(self.y_entry)
        plt.contourf(self.x_values, self.y_values, self.z_values)
        plt.show()


class ImShowMaker(customtkinter.CTk):
    WIDTH = 500
    HEIGHT = 200

    def __init__(self):
        super().__init__()
        self.title('Egon  Imshow maker')
        self.geometry(f'{ImShowMaker.WIDTH}x{ImShowMaker.HEIGHT}')
        self.resizable(False, False)
        self.im_up = False
        self.s_cmap = 'Accent'
        self.cmap_values = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu',
                            'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r',
                            'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired',
                            'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu',
                            'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r',
                            'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn',
                            'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r',
                            'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r',
                            'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r',
                            'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis',
                            'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix',
                            'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r',
                            'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r',
                            'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2',
                            'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno',
                            'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r',
                            'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow',
                            'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10',
                            'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain',
                            'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted',
                            'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'
                            ]
        interpolation_values = ['none', 'nearest', 'bilinear', 'bicubic', 'spline16',
                                'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
                                'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']
        self.cmap_var = tkinter.StringVar()
        self.interpolation_var = tkinter.StringVar()

        title = customtkinter.CTkLabel(self, text='Graphical user interface for ImageShow',
                                       text_font='young 14 underline')
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         text_font='young 10 underline')
        title_title = customtkinter.CTkLabel(self, text='add title:',
                                             text_font='young 10 underline')
        tr_title = customtkinter.CTkLabel(self, text='transparency:',
                                          text_font='young 10 underline')
        # self.x_entry = customtkinter.CTkEntry(self)
        self.title_entry = customtkinter.CTkEntry(self)
        self.transparency = customtkinter.CTkSlider(self, from_=0, to=100, orient='horizontal')
        self.transparency.set(100)
        upload_im = customtkinter.CTkButton(self, text='Upload (SG. png)', command=self.upload_image)
        upload_y = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))
        c_map_title = customtkinter.CTkLabel(self, text='cmap:', text_font='young 10 underline')
        cmap_combobox = customtkinter.CTkComboBox(self, variable=self.cmap_var, values=self.cmap_values,
                                                  command=self.change_cmap)
        interpolation_title = customtkinter.CTkLabel(self, text='interpolation:', text_font='young 10 underline')
        self.interpolation_c = customtkinter.CTkComboBox(self, values=interpolation_values,
                                                         variable=self.interpolation_var,
                                                         )
        # title_title = customtkinter.CTkLabel(self, text='add title:', text_font='young 10 underline')
        # self.title_entry = customtkinter.CTkEntry(self)
        imshow_button = customtkinter.CTkButton(self, text='make imshow', command=self.make_imshow)

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0)
        title_title.grid(row=1, column=1)
        tr_title.grid(row=1, column=2)
        # self.x_entry.grid(row=2, column=0)
        upload_im.grid(row=2, column=0)
        self.title_entry.grid(row=2, column=1)
        self.transparency.grid(row=2, column=2)
        upload_y.grid(row=3, column=2)
        c_map_title.grid(row=4, column=0)
        interpolation_title.grid(row=4, column=2)
        cmap_combobox.grid(row=5, column=0)
        self.interpolation_c.grid(row=5, column=2)
        imshow_button.grid(row=10, column=1)

    def make_imshow(self):
        # self.x_values = numpy.array(self.x_entry.get().split(' '))
        if self.im_up:
            plt.clf()
            if title_condition(self.title_entry):
                plt.title(title_condition(self.title_entry))
            x = plt.imshow(self.frame, cmap=self.s_cmap, alpha=self.trans(),
                           interpolation=self.get_interpolation(self.interpolation_c.get()))
            plt.colorbar(x)
            plt.show()
        else:
            tkinter.messagebox.showinfo('', 'please upload image')

    def upload_image(self):
        image_name = filedialog.askopenfilename(title='Open file', filetypes=(('All', '*.*'), ('PNG', '*.png')))
        if image_name:
            image = Image.open(image_name)
            self.frame = numpy.asarray(image)
            tkinter.messagebox.showinfo('', 'Successfully uploaded image')
            self.im_up = True
        else:
            tkinter.messagebox.showinfo('', 'failed to upload image')
            self.im_up = False

    def change_cmap(self, ccmap):
        if ccmap:
            self.s_cmap = ccmap
        else:
            self.s_cmap = self.cmap_values[0]

    def trans(self):
        self.trans_v = (self.transparency.get() / 100)
        return self.trans_v

    def get_interpolation(self, interpolation):
        if interpolation:
            return interpolation
        else:
            return 'none'


class ScatterPlotMaker(customtkinter.CTk):
    WIDTH = 675
    HEIGHT = 250

    def __init__(self):
        super().__init__()
        self.title('Egon scatter plot maker')
        self.geometry(f'{ScatterPlotMaker.WIDTH}x{ScatterPlotMaker.HEIGHT}')
        self.resizable(False, False)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for ScatterPlot',
                                       text_font='young 14 underline')
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         text_font='young 10 underline')
        colors_title = customtkinter.CTkLabel(self, text='colors values:',
                                              text_font='young 10 underline')
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         text_font='young 10 underline')
        self.x_entry = customtkinter.CTkEntry(self)
        self.colors_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        upload_y = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))
        upload_x = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
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

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0)
        colors_title.grid(row=1, column=1)
        y_title.grid(row=1, column=2)
        self.x_entry.grid(row=2, column=0)
        self.colors_entry.grid(row=2, column=1)
        self.y_entry.grid(row=2, column=2)
        upload_x.grid(row=3, column=0)
        upload_y.grid(row=3, column=2)
        styles_title.grid(row=4, column=1)
        size_title.grid(row=5, column=0)

        transparency_title.grid(row=5, column=2)
        self.size.grid(row=6, column=0)
        self.color_map.grid(row=6, column=1)
        self.transparency.grid(row=6, column=2)
        self.make_scatter.grid(row=10, column=1)

    def make_scatter_plot(self):
        self.x_values = make_array(self.x_entry)
        self.y_values = make_array(self.y_entry)
        plt.clf()
        plt.scatter(self.x_values, self.y_values, cmap=self.color_m(self.color_map.get()), alpha=self.trans(), s=self.size_()
                    , c=self.colors_())
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
    WIDTH = 575
    HEIGHT = 275

    def __init__(self):
        super().__init__()
        self.title('Egon stem maker')
        self.geometry(f'{StemMaker.WIDTH}x{StemMaker.HEIGHT}')
        self.resizable(False, False)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Stem',
                                       text_font='young 14 underline')
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         text_font='young 10 underline')
        bottom_title = customtkinter.CTkLabel(self, text='bottom value:',
                                              text_font='young 10 underline')
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         text_font='young 10 underline')
        self.x_entry = customtkinter.CTkEntry(self)
        self.bottom_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        upload_x = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
        upload_y = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))
        stem_button = customtkinter.CTkButton(self, text='Make a stem', command=self.make_stem)

        styles_title = customtkinter.CTkLabel(self, text='Styles:', text_font='young 12 bold')
        line_title = customtkinter.CTkLabel(self, text='lines format:', text_font='young 10 underline')
        marker_title = customtkinter.CTkLabel(self, text='marker format:', text_font='young 10 underline')

        line_values = ['-', '--', '_.', ':']
        marker_values = ['ro', 'r-', 'g--', 'm:']
        line_var = tkinter.StringVar()
        marker_var = tkinter.StringVar()
        self.line = customtkinter.CTkComboBox(self, values=line_values, variable=line_var)
        self.marker = customtkinter.CTkComboBox(self, values=marker_values, variable=marker_var)

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0)
        bottom_title.grid(row=1, column=1)
        y_title.grid(row=1, column=2)
        self.x_entry.grid(row=2, column=0)
        self.bottom_entry.grid(row=2, column=1)
        self.y_entry.grid(row=2, column=2)
        upload_x.grid(row=3, column=0)
        upload_y.grid(row=3, column=2)
        styles_title.grid(row=4, column=1)
        line_title.grid(row=5, column=0)
        marker_title.grid(row=5, column=2)
        self.line.grid(row=6, column=0)
        self.marker.grid(row=6, column=2)

        stem_button.grid(row=10, column=1)

    def make_stem(self):
        x_values = make_array(self.x_entry)
        y_values = make_array(self.y_entry)
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
        percentages_values = make_array(self.percentage_entry)

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
        x_upload = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
        y_upload = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))

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
        x_upload.grid(row=3, column=0)
        y_upload.grid(row=3, column=2)
        titles_title.grid(row=4, column=1)
        x_title_.grid(row=5, column=0)
        main_title_.grid(row=5, column=1)
        y_title_.grid(row=5, column=2)
        self.x_title_entry.grid(row=6, column=0)
        self.main_title_entry.grid(row=6, column=1)
        self.y_title_entry.grid(row=6, column=2)
        grid_title.grid(row=7, column=1)
        x_grid.grid(row=8, column=0)
        both_grid.grid(row=8, column=1)
        y_grid.grid(row=8, column=2)
        histogram_button.grid(row=10, column=1, pady=10)

    def make_histogram(self):
        x_values = make_array(self.x_entry)
        y_values = make_array(self.y_entry)
        try:
            plt.clf()
            plt.hist(x_values, y_values)

            if title_condition(self.x_title_entry):
                plt.xlabel(title_condition(self.x_title_entry))
            if title_condition(self.y_title_entry):
                plt.ylabel(title_condition(self.y_title_entry))
            if title_condition(self.main_title_entry):
                plt.title(title_condition(self.main_title_entry))

            plt.grid(axis=self.grid_modes())

            plt.show()
        except ValueError:
            tkinter.messagebox.showerror('error', 'y values must increase monotonically')

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
        y_upload = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))
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
        y_upload.grid(row=3, column=2)
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
        x_values = make_array(self.bar_name_entry)
        y_values = make_array(self.y_entry)
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
    HEIGHT = 550

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
        upload_x = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
        upload_y = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
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
        upload_x.grid(row=3, column=0)
        upload_y.grid(row=3, column=2)
        styles_title.grid(row=4, column=1)
        marker_title.grid(row=5, column=0)
        line_style_title.grid(row=5, column=2)
        marker_select.grid(row=6, column=0)
        line_select.grid(row=6, column=2)
        sizes_title.grid(row=7, column=1)
        dot_title.grid(row=8, column=0)
        line_title.grid(row=8, column=2)
        self.dot_select.grid(row=9, column=0)
        self.line_select.grid(row=9, column=2)
        titles_title.grid(row=10, column=1)
        main_title_.grid(row=11, column=1)
        x_title_.grid(row=11, column=0)
        y_title_.grid(row=11, column=2)
        self.x_title_entry.grid(row=12, column=0)
        self.main_title_entry.grid(row=12, column=1)
        self.y_title_entry.grid(row=12, column=2)
        grid_title.grid(row=13, column=1)
        x_grid.grid(row=14, column=0)
        both_grid.grid(row=14, column=1)
        y_grid.grid(row=14, column=2)
        inf_line_title.grid(row=15, column=1)
        inf_line_x_t.grid(row=16, column=0)
        # inf_line_slope_t.grid(row=15, column=1)
        inf_line_y_t.grid(row=16, column=2)
        self.inf_line_value.grid(row=17, column=0)
        # self.inf_line_slope.grid(row=16, column=1)
        self.inf_line_mode.grid(row=17, column=2)
        graph_button.grid(row=18, column=1, pady=10)

    # create the graph:
    def make_graph(self):

        self.change_grid_modes()
        x_values = make_array(self.x_entry)
        y_values = make_array(self.y_entry)
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
            if title_condition(self.x_title_entry):
                plt.xlabel(title_condition(self.x_title_entry))
            if title_condition(self.y_title_entry):
                plt.ylabel(title_condition(self.y_title_entry))
            if title_condition(self.main_title_entry):
                plt.title(title_condition(self.main_title_entry))
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
