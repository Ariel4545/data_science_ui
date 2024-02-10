# imports
import numpy, pandas
import matplotlib.pyplot as plt
import customtkinter, tkinter
from numpy import array, asarray
from numpy import random as np_random
from tkinter import messagebox, filedialog, IntVar, StringVar, END, DISABLED
from PIL import Image
from random import choice as ran_choice
from random import randint

# universal variables / functions
main_title = ('young', 16, 'underline')
sub_title = ('young', 12, 'underline')
med_bold_title = ('young', 14, 'bold')
resize_v = False
middle_v = True
fun_numbers_v = False
button_bg = '#1F6AA5'
button_fg = 'white'
opened_programs = []

'''+ 
make all the comboboxes filled with the default options \ work but don;t show
add fun numbers settings + made to all main things
countorf input filter +/ explanation
'''

def get_transparency(class_='imshow'):
    if class_ == 'imshow':
        trans_widget = im_transparency
    else:
        trans_widget = sc_transparency
    trans_v = (trans_widget.get() / 100)
    return trans_v

def change_marker(marker, class_='stem'):
    if marker:
        return marker
    else:
        if class_ == 'stem':
            return 'ro'
        else:
            return 'o'

def get_legend(chosen_legend=False):
    if not(chosen_legend):
        return ''
    else:
        return chosen_legend

def change_line(line):
    if line:
        return line
    else:
        return '-'

# global functions for common things
def upload(entry):
    file_name = filedialog.askopenfilename(title='Open file', filetypes=(('All', '*.*'), ('CSV', 'csv.*')))
    if file_name:
        entry.delete(0, END)
        stuff = pandas.read_csv(file_name)

        p = 0
        for val in stuff:
            entry.insert(p, val)
            p += len(val)

def place_w_middle(window):
    win_w = window.winfo_screenwidth()
    win_h = window.winfo_screenheight()
    width, height = window.winfo_width(), window.winfo_height()
    placement_x = round((win_w / 2) - (width / 2))
    placement_y = round((win_h / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{placement_x}+{placement_y}')

def open_app(application):
    app = application()
    app.mainloop()


def title_condition(entry):
    if entry.get():
        return entry.get()
    else:
        return False


def make_array(entry):
    return array(entry.get().split(' '))


# main menu - open kinds of data visualizations options
class MainMenu(customtkinter.CTk):
    plt.style.use('dark_background')
    global main_title, sub_title, med_bold_title, resize_v, middle_v, opened_programs, fun_numbers_v

    def __init__(self):
        super().__init__()
        self.title('Data visualization')
        self.protocol('WM_DELETE_WINDOW', self.on_close)
        tabview = customtkinter.CTkTabview(self)
        tabview.pack()
        app_frame = tabview.add('Apps')
        settings_frame = tabview.add('Options')
        tabview.set('Apps')

        a_title = customtkinter.CTkLabel(app_frame, text='Applications:',
                                       font=main_title)
        self.open_graphMaker = customtkinter.CTkButton(app_frame, text='Graph maker', command=lambda: open_app(GraphMaker), text_color=button_fg)
        self.open_histogramMaker = customtkinter.CTkButton(app_frame, text='Histogram maker', command=lambda: open_app(
            HistogramMaker))
        self.open_barMaker = customtkinter.CTkButton(app_frame, text='Bar maker', command=lambda: open_app(BarMaker))
        self.open_pieMaker = customtkinter.CTkButton(app_frame, text='Pie maker', command=lambda: open_app(PieMaker))
        self.open_stemMaker = customtkinter.CTkButton(app_frame, text='Stem maker', command=lambda: open_app(StemMaker))
        self.open_scatterPlotMaker = customtkinter.CTkButton(app_frame, text='Scatter plot maker', command=lambda: open_app(
            ScatterPlotMaker))
        self.open_imShowBarMaker = customtkinter.CTkButton(app_frame, text='ImShow maker', command=lambda: open_app(
            ImShowMaker))
        self.open_contourMaker = customtkinter.CTkButton(app_frame, text='Contour maker', command=lambda: open_app(
            ContourfMaker))
        self.open_errorBarMaker = customtkinter.CTkButton(app_frame, text='Error bar maker', command=lambda: open_app(
            ErrorBarMaker))
        self.open_bloxPlotMaker = customtkinter.CTkButton(app_frame, text='Plot box maker', command=lambda: open_app(
            BoxPlot))
        open_random_button = customtkinter.CTkButton(app_frame, text='Random tool', command=self.open_random)
        s_title = customtkinter.CTkLabel(settings_frame, text='Settings:',
                                         font=main_title)
        theme_title = customtkinter.CTkLabel(settings_frame, text='theme color:',
                                             font=sub_title)
        self.theme_v = customtkinter.StringVar()
        self.fonts_v = customtkinter.StringVar()
        self.topmost_v = customtkinter.BooleanVar()
        self.middle_v = customtkinter.BooleanVar()
        self.limit_sizes_v = customtkinter.BooleanVar()
        self.fun_numbers_v = customtkinter.BooleanVar()
        self.tr_v = customtkinter.IntVar()
        self.theme_v.set('dracula')
        self.fonts_v.set('normal')
        self.middle_v.set(True)
        self.limit_sizes_v.set(True)
        font_sizes = ['normal', 'big', 'large']
        self.themes = ['dracula', 'light']
        theme_select = customtkinter.CTkComboBox(settings_frame, state='readonly', variable=self.theme_v,
                                                 values=self.themes, command=self.change_theme)
        font_title = customtkinter.CTkLabel(settings_frame, text='font sizes:', font=sub_title)
        font_size_box = customtkinter.CTkComboBox(settings_frame, state='readonly', variable=self.fonts_v,
                                                 values=font_sizes, command=self.font_sizes)
        button_colors_title = customtkinter.CTkLabel(settings_frame, text='Button colors:', font=sub_title)
        fg_button = customtkinter.CTkButton(settings_frame, text='Button foreground', command=None, state=DISABLED)
        bg_button = customtkinter.CTkButton(settings_frame, text='Button background', command=None, state=DISABLED)
        check_marks_title = customtkinter.CTkLabel(settings_frame, text='Others:', font=sub_title)
        topmost_check = customtkinter.CTkCheckBox(settings_frame, text='TopMost', variable=self.topmost_v, command=
                                                  self.change_tp)
        middle_check = customtkinter.CTkCheckBox(settings_frame, text='Open in the middle', variable=self.middle_v,
                                                 command=self.middle_v_set)
        limit_sizes_check = customtkinter.CTkCheckBox(settings_frame, text='Limit window sizes', variable=self.limit_sizes_v
                                                           , command=self.resize_op)
        fun_numbers_check = customtkinter.CTkCheckBox(settings_frame, text='Fun numbers', variable=self.fun_numbers_v,
                                                      command=self.fun_v_set)
        transparency_title = customtkinter.CTkLabel(settings_frame, text='Transparency:', font=sub_title)
        self.trans_progress = customtkinter.CTkSlider(settings_frame, from_=25, to=100, variable=self.tr_v, command=self.change_tr)
        self.trans_progress.set(100)
        placeholder = customtkinter.CTkLabel(settings_frame, text='')

        a_title.pack(pady=10)
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
        open_random_button.pack(pady=5)

        s_title.pack(pady=2)
        theme_title.pack(pady=1)
        theme_select.pack(pady=1)
        font_title.pack(pady=1)
        font_size_box.pack(pady=1)
        button_colors_title.pack(pady=1)
        fg_button.pack(pady=2)
        bg_button.pack(pady=2)
        transparency_title.pack(pady=2)
        self.trans_progress.pack(pady=2)
        check_marks_title.pack(pady=1)
        topmost_check.pack(pady=3)
        middle_check.pack(pady=3)
        limit_sizes_check.pack(pady=3)
        fun_numbers_check.pack(pady=3)
        placeholder.pack()

        self.update()
        self.HEIGHT = self.winfo_height()
        self.resize_op(initial=True)

        self.sub_title_list = theme_title, font_title, button_colors_title, check_marks_title, transparency_title
        self.main_title_list = s_title, a_title

    # close the application  when the 'x' is pressed
    def on_close(self, event=0):
        for app in opened_programs:
            app.destroy()
        self.destroy()

    def fun_v_set(self):
        global fun_numbers_v
        fun_numbers_v = self.fun_numbers_v.get()

    def middle_v_set(self):
        global middle_v
        middle_v = self.middle_v.get()

    def resize_op(self, initial=False):
        global resize_v
        if not(initial):
            resize_v = not(self.limit_sizes_v.get())
        if not(resize_v):
            self.minsize(275, 100)
            self.maxsize(275, self.HEIGHT)
            if initial:
                place_w_middle(self)
        else:
            self.minsize(0, 0)
            self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())


    def font_sizes(self, event):
        global main_title, sub_title, med_bold_title
        if self.fonts_v.get() == 'normal':
            main_title = ('young', 16, 'underline')
            sub_title = ('young', 12, 'underline')
            med_bold_title = ('young', 14, 'bold')
        elif self.fonts_v.get() == 'big':
            main_title = ('young', 18, 'underline')
            sub_title = ('young', 14, 'underline')
            med_bold_title = ('young', 16, 'bold')
        elif self.fonts_v.get() == 'large':
            main_title = ('young', 20, 'underline')
            sub_title = ('young', 16, 'underline')
            med_bold_title = ('young', 14, 'bold')
        for stitle in self.sub_title_list:
            stitle.configure(font=sub_title)
        for mtitle in self.main_title_list:
            mtitle.configure(font=main_title)

    def change_tp(self):
        self.attributes('-topmost', self.topmost_v.get())

    def change_tr(self, event):
        # global opened_programs
        alpha_value = self.trans_progress.get() / 100
        self.attributes('-alpha', alpha_value)
        for app in opened_programs:
            app.attributes('-alpha', alpha_value)

    def change_theme(self, theme):
        if theme == 'light':
            customtkinter.set_appearance_mode('light')
            plt.style.use('default')
        else:
            customtkinter.set_appearance_mode('dark')
            plt.style.use('dark_background')

    def open_random(self):
        classes_list = [GraphMaker, HistogramMaker, BarMaker, PieMaker, StemMaker, ScatterPlotMaker, ImShowMaker,
        ContourfMaker, ErrorBarMaker, BoxPlot]

        cls = ran_choice(classes_list)
        open_app(cls)


class BoxPlot(customtkinter.CTk):
    global opened_programs


    def __init__(self):
        super().__init__()
        global opened_programs
        self.title('Egon Box plot')
        if not(resize_v):
            self.resizable(False, False)
        self.pa_var = IntVar()
        self.notch_var = IntVar()
        self.line_var = customtkinter.StringVar()
        ls_values = [' ', 'solid', 'dashed', 'dashdot', 'dotted']
        default_line_var = ran_choice(ls_values)
        self.line_var.set(default_line_var)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for BoxPlots',
                                       font=main_title)
        data_title = customtkinter.CTkLabel(self, text='data values:', font=sub_title)
        self.data_entry1 = customtkinter.CTkEntry(self)
        self.data_entry2 = customtkinter.CTkEntry(self)
        self.data_entry3 = customtkinter.CTkEntry(self)
        patchA_checkbox = customtkinter.CTkCheckBox(self, text='Patch artist', variable=self.pa_var)
        notch_checkbox = customtkinter.CTkCheckBox(self, text='Notch', variable=self.notch_var)
        lines_title = customtkinter.CTkLabel(self, text='Lines:', font=med_bold_title)
        line_width_title = customtkinter.CTkLabel(self, text='line app_width:', font=sub_title)
        line_style_title = customtkinter.CTkLabel(self, text='line style:', font=sub_title)
        self.line_width = customtkinter.CTkEntry(self)
        self.line_style = customtkinter.CTkComboBox(self, state='readonly', variable=self.line_var, values=ls_values)
        names_title = customtkinter.CTkLabel(self, text='Names:', font=med_bold_title)
        title_title = customtkinter.CTkLabel(self, text='main title:', font=sub_title)
        x_val_title = customtkinter.CTkLabel(self, text='X-axis names:', font=sub_title)
        self.title = customtkinter.CTkEntry(self)
        x_values_names = customtkinter.CTkEntry(self, state=DISABLED)
        boxplot_button = customtkinter.CTkButton(self, text='Make box plot', command=self.make_boxplot)

        title.grid(row=0, column=1)
        data_title.grid(row=1, column=1)
        self.data_entry1.grid(row=2, column=0, padx=5)
        self.data_entry2.grid(row=2, column=1)
        self.data_entry3.grid(row=2, column=2, padx=5)
        patchA_checkbox.grid(row=3, column=0, pady=5)
        notch_checkbox.grid(row=3, column=2, pady=5)
        lines_title.grid(row=4, column=1)
        line_style_title.grid(row=4, column=0, pady=5)
        line_width_title.grid(row=4, column=2, pady=5)
        self.line_style.grid(row=5, column=0, pady=5)
        self.line_width.grid(row=5, column=2, pady=5)
        names_title.grid(row=6, column=1)
        title_title.grid(row=7, column=0, pady=5)
        x_val_title.grid(row=7, column=2, pady=5)
        self.title.grid(row=8, column=0, pady=5)
        x_values_names.grid(row=8, column=2, pady=5)
        boxplot_button.grid(row=10, column=1, pady=10)

        # self.line_style['current'] = self.line_var.get()

        if middle_v:
            self.update()
            place_w_middle(self)

        if fun_numbers_v:
            entry_1_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
            entry_2_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
            entry_3_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
            self.data_entry1.insert(END, entry_1_r)
            self.data_entry2.insert(END, entry_2_r)
            self.data_entry3.insert(END, entry_3_r)


        self.protocol('WM_DELETE_WINDOW', self.close_this)
        self.boxplot_root = self
        opened_programs.append(self.boxplot_root)

    def close_this(self):
        opened_programs.remove(self.boxplot_root)
        self.destroy()

    def make_boxplot(self):
        plt.clf()
        x = plt.boxplot(self.data_values(), patch_artist=self.pa_var.get(), notch=self.notch_var.get())
        # lines management
        for whisker in x['whiskers']:
            whisker.set(linewidth=self.line_w(), linestyle=change_line(self.line_style.get()))
        if title_condition(self.title):
            plt.title(title_condition(self.title))
        # if self.title_():
        #     pass
        plt.show()

    def data_values(self):
        self.data = []
        if self.data_entry1.get():
            self.data.append(array(self.data_entry1.get().split(' '), dtype='int'))
        if self.data_entry2.get():
            self.data.append(array(self.data_entry2.get().split(' '), dtype='int'))
        if self.data_entry3.get():
            self.data.append(array(self.data_entry3.get().split(' '), dtype='int'))
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


class ErrorBarMaker(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title('Egon Error bar maker')
        if not (resize_v):
            self.resizable(False, False)
        self.u_var = IntVar()
        self.l_var = IntVar()

        title = customtkinter.CTkLabel(self, text='Graphical user interface for ErrorBars',
                                       font=main_title)
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         font=sub_title)
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         font=sub_title)
        self.x_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        xerr_title = customtkinter.CTkLabel(self, text='xerr value:',
                                            font=sub_title)
        yerr_title = customtkinter.CTkLabel(self, text='yerr value:',
                                            font=sub_title)
        self.xerr_entry = customtkinter.CTkEntry(self)
        self.yerr_entry = customtkinter.CTkEntry(self)
        upload_x = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
        upload_y = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))
        uplims_checkbox = customtkinter.CTkCheckBox(self, text='upper limits', variable=self.u_var)
        lolims_checkbox = customtkinter.CTkCheckBox(self, text='lower limits', variable=self.l_var)
        eb_button = customtkinter.CTkButton(self, text='make error bar', command=self.make_errorBar)

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0, padx=5)
        y_title.grid(row=1, column=2, padx=5)
        self.x_entry.grid(row=2, column=0, padx=5)
        self.y_entry.grid(row=2, column=2, padx=5)
        upload_x.grid(row=3, column=0, pady=5, padx=5)
        upload_y.grid(row=3, column=2, pady=5, padx=5)
        xerr_title.grid(row=4, column=0, padx=5)
        yerr_title.grid(row=4, column=2, padx=5)
        self.xerr_entry.grid(row=5, column=0, padx=5)
        self.yerr_entry.grid(row=5, column=2, padx=5)
        uplims_checkbox.grid(row=6, column=0, padx=5)
        lolims_checkbox.grid(row=6, column=2, padx=5)
        eb_button.grid(row=10, column=1, pady=10)

        if middle_v:
            self.update()
            place_w_middle(self)

        if fun_numbers_v:
            entry_1_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
            entry_2_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
            self.x_entry.insert(END, entry_1_r)
            self.y_entry.insert(END, entry_2_r)

        self.protocol('WM_DELETE_WINDOW', self.close_this)
        self.errorbar_root = self
        opened_programs.append(self.errorbar_root)

    def close_this(self):
        opened_programs.remove(self.errorbar_root)
        self.destroy()

    def make_errorBar(self):
        plt.clf()
        self.x_values = array(self.x_entry.get().split(' '), dtype='int32')
        self.y_values = array(self.y_entry.get().split(' '), dtype='int32')
        self.xerr_values = abs(float(self.xerr_entry.get()))
        self.yerr_values = abs(float(self.yerr_entry.get()))
        # self.xerr_values.reshape(1, len((self.xerr_values)))
        # self.yerr_values.reshape(1, len((self.yerr_values)))
        plt.errorbar(self.x_values, self.y_values, xerr=self.xerr_values, yerr=self.yerr_values,
                     uplims=self.u_var.get(), lolims=self.l_var.get())
        plt.show()


class ContourfMaker(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title('Egon contourf Maker')
        if not (resize_v):
            self.resizable(False, False)
        main_frame = customtkinter.CTkFrame(self)
        title = customtkinter.CTkLabel(main_frame, text='Graphical user interface for ContourF',
                                       font=main_title)
        x_title = customtkinter.CTkLabel(main_frame, text='x values:',
                                         font=sub_title)
        z_title = customtkinter.CTkLabel(main_frame, text='z values:',
                                         font=sub_title)
        y_title = customtkinter.CTkLabel(main_frame, text='y values:',
                                         font=sub_title)
        self.x_entry = customtkinter.CTkEntry(main_frame)
        self.y_entry = customtkinter.CTkEntry(main_frame)
        z_frame = customtkinter.CTkFrame(self)
        self.z_entry = customtkinter.CTkEntry(main_frame)
        self.z_entry2 = customtkinter.CTkEntry(z_frame)
        self.z_entry3 = customtkinter.CTkEntry(z_frame)
        self.z_entry4 = customtkinter.CTkEntry(z_frame)
        upload_x = customtkinter.CTkButton(main_frame, text='Upload', command=lambda: upload(self.x_entry))
        upload_z = customtkinter.CTkButton(main_frame, text='Upload', command=lambda: upload(self.z_entry))
        upload_y = customtkinter.CTkButton(main_frame, text='Upload', command=lambda: upload(self.y_entry))
        contour_button = customtkinter.CTkButton(self, text='make contourf', command=self.make_contourf)
        title_title = customtkinter.CTkLabel(main_frame, text='title:', font=sub_title)
        title_entry = customtkinter.CTkEntry(main_frame)

        main_frame.grid(row=0, column=1)
        z_frame.grid(row=1, column=1)
        contour_button.grid(row=2, column=1, pady=10)

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0, padx=5)
        z_title.grid(row=2, column=1)
        y_title.grid(row=1, column=2, padx=5)
        self.x_entry.grid(row=2, column=0, padx=5)
        self.z_entry.grid(row=3, column=1)
        self.y_entry.grid(row=2, column=2, padx=5)
        upload_x.grid(row=3, column=0, pady=3, padx=5)
        upload_y.grid(row=3, column=2, pady=3, padx=5)

        self.z_entry2.grid(row=4, column=0, padx=5)
        self.z_entry3.grid(row=4, column=1)
        self.z_entry4.grid(row=4, column=2, padx=5)

        if middle_v:
            self.update()
            place_w_middle(self)

        if fun_numbers_v:
            entry_1_r = f'{randint(0, 10)} {randint(0, 10)}'
            entry_2_r = f'{randint(0, 10)} {randint(0, 10)}'
            self.x_entry.insert(END, entry_1_r)
            self.y_entry.insert(END, entry_2_r)
            self.z_entry.insert(END, randint(0, 10))
            self.z_entry2.insert(END, randint(0, 10))
            self.z_entry3.insert(END, randint(0, 10))
            self.z_entry4.insert(END, randint(0, 10))

        self.protocol('WM_DELETE_WINDOW', self.close_this)
        self.contourf_root = self
        opened_programs.append(self.contourf_root)

    def close_this(self):
        opened_programs.remove(self.contourf_root)
        self.destroy()

    def make_contourf(self):
        self.x_values = make_array(self.x_entry)
        # must be 2x2 - D array!!!
        self.z_values = tuple(array((self.z_entry.get().split(' '), self.z_entry2.get().split(' '),
                                           self.z_entry3.get().split(' '), self.z_entry4.get().split()), dtype='int32'
                                          ).reshape(2, 2))
        self.y_values = make_array(self.y_entry)
        plt.contourf(self.x_values, self.y_values, self.z_values)
        plt.show()


class ImShowMaker(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        global im_transparency
        self.title('Egon  Imshow maker')
        if not (resize_v):
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
        self.cmap_var = customtkinter.StringVar()
        self.interpolation_var = customtkinter.StringVar()
        self.cmap_var.set('Accent')
        self.interpolation_var.set('none')

        title = customtkinter.CTkLabel(self, text='Graphical user interface for ImageShow',
                                       font=main_title)
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         font=sub_title)
        title_title = customtkinter.CTkLabel(self, text='add title:',
                                             font=sub_title)
        tr_title = customtkinter.CTkLabel(self, text='transparency:',
                                          font=sub_title)
        # self.x_entry = customtkinter.CTkEntry(self)
        self.title_entry = customtkinter.CTkEntry(self)
        im_transparency = customtkinter.CTkSlider(self, from_=0, to=100)
        im_transparency.set(100)
        upload_im = customtkinter.CTkButton(self, text='Upload (SG. png)', command=self.upload_image)
        upload_y = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))
        c_map_title = customtkinter.CTkLabel(self, text='cmap:', font=sub_title)
        cmap_combobox = customtkinter.CTkComboBox(self, variable=self.cmap_var, values=self.cmap_values,
                                                  command=self.change_cmap,  state='readonly')
        interpolation_title = customtkinter.CTkLabel(self, text='interpolation:', font=sub_title)
        self.interpolation_c = customtkinter.CTkComboBox(self, values=interpolation_values,
                                                         variable=self.interpolation_var,  state='readonly'
                                                         )
        # title_title = customtkinter.CTkLabel(self, text='add title:', font=sub_title)
        # self.title_entry = customtkinter.CTkEntry(self)
        imshow_button = customtkinter.CTkButton(self, text='make imshow', command=self.make_imshow)

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0, padx=5)
        title_title.grid(row=1, column=1)
        tr_title.grid(row=1, column=2, padx=5)
        # self.x_entry.grid(row=2, column=0)
        upload_im.grid(row=2, column=0, padx=5)
        self.title_entry.grid(row=2, column=1)
        im_transparency.grid(row=2, column=2, padx=5)
        upload_y.grid(row=3, column=2, padx=5)
        c_map_title.grid(row=4, column=0, padx=5)
        interpolation_title.grid(row=4, column=2, padx=5)
        cmap_combobox.grid(row=5, column=0, padx=5)
        self.interpolation_c.grid(row=5, column=2, padx=5)
        imshow_button.grid(row=10, column=1, pady=10)

        if middle_v:
            self.update()
            place_w_middle(self)

        self.protocol('WM_DELETE_WINDOW', self.close_this)
        self.imshow_root = self
        opened_programs.append(self.imshow_root)

    def close_this(self):
        opened_programs.remove(self.imshow_root)
        self.destroy()

    def make_imshow(self):
        # self.x_values = numpy.array(self.x_entry.get().split(' '))
        if self.im_up:
            plt.clf()
            if title_condition(self.title_entry):
                plt.title(title_condition(self.title_entry))
            x = plt.imshow(self.frame, cmap=self.s_cmap, alpha=get_transparency(),
                           interpolation=self.get_interpolation(self.interpolation_c.get()))
            plt.colorbar(x)
            plt.show()
        else:
            messagebox.showinfo('', 'please upload image')

    def upload_image(self):
        image_name = filedialog.askopenfilename(title='Open file', filetypes=(('All', '*.*'), ('PNG', '*.png')))
        if image_name:
            image = Image.open(image_name)
            self.frame = numpy.asarray(image)
            messagebox.showinfo('', 'Successfully uploaded image')
            self.im_up = True
        else:
            messagebox.showinfo('', 'failed to upload image')
            self.im_up = False

    def change_cmap(self, ccmap):
        if ccmap:
            self.s_cmap = ccmap
        else:
            self.s_cmap = self.cmap_values[0]

    def get_interpolation(self, interpolation):
        if interpolation:
            return interpolation
        else:
            return 'none'


class ScatterPlotMaker(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        global sc_transparency
        self.title('Egon scatter plot maker')
        if not (resize_v):
            self.resizable(False, False)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for ScatterPlot',
                                       font=main_title)
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         font=sub_title)
        colors_title = customtkinter.CTkLabel(self, text='colors values:',
                                              font=sub_title)
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         font=sub_title)
        self.x_entry = customtkinter.CTkEntry(self)
        self.colors_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        upload_y = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))
        upload_x = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
        styles_title = customtkinter.CTkLabel(self, text='Styles:', font=med_bold_title)
        transparency_title = customtkinter.CTkLabel(self, text='transparency:',
                                                    font=sub_title)
        size_title = customtkinter.CTkLabel(self, text='sizes:',
                                            font=sub_title)
        sc_transparency = customtkinter.CTkSlider(self, from_=0, to=100)
        sc_transparency.set(100)
        self.size = customtkinter.CTkEntry(self)

        color_maps_values = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
        color_maps_v = customtkinter.StringVar()
        color_maps_v.set('viridis')
        self.color_map = customtkinter.CTkComboBox(self, values=color_maps_values, variable=color_maps_v,  state='readonly')

        self.make_scatter = customtkinter.CTkButton(self, command=self.make_scatter_plot, text='Make scatter plot')

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0, padx=5)
        colors_title.grid(row=1, column=1)
        y_title.grid(row=1, column=2, padx=5)
        self.x_entry.grid(row=2, column=0, padx=5)
        self.colors_entry.grid(row=2, column=1)
        self.y_entry.grid(row=2, column=2, padx=5)
        upload_x.grid(row=3, column=0, padx=5, pady=3)
        upload_y.grid(row=3, column=2, padx=5, pady=3)
        styles_title.grid(row=4, column=1)
        size_title.grid(row=5, column=0, padx=5)

        transparency_title.grid(row=5, column=2, padx=5)
        self.size.grid(row=6, column=0, padx=5)
        self.color_map.grid(row=6, column=1)
        sc_transparency.grid(row=6, column=2, padx=5)
        self.make_scatter.grid(row=10, column=1, pady=10)

        if middle_v:
            self.update()
            place_w_middle(self)

        if fun_numbers_v:
            entry_1_r = f'{randint(0, 20)} {randint(0, 20)} {randint(0, 20)} {randint(0, 20)}'
            entry_2_r = f'{randint(0, 20)} {randint(0, 20)} {randint(0, 20)} {randint(0, 20)}'
            self.x_entry.insert(END, entry_1_r)
            self.y_entry.insert(END, entry_2_r)

        self.protocol('WM_DELETE_WINDOW', self.close_this)
        self.scatterplot_root = self
        opened_programs.append(self.scatterplot_root)

    def close_this(self):
        opened_programs.remove(self.scatterplot_root)
        self.destroy()

    def make_scatter_plot(self):
        self.x_values = make_array(self.x_entry)
        self.y_values = make_array(self.y_entry)
        plt.clf()
        alp_value = get_transparency(class_='scatter')
        plt.scatter(self.x_values, self.y_values, cmap=self.color_m(self.color_map.get())
                    , alpha=alp_value, s=self.size_(), c=self.colors_())
        plt.colorbar()
        plt.show()

    def color_m(self, cm):
        if cm:
            return cm
        else:
            return 'inferno'

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
                colors_values.append(np_random.randint(1, 100))
            return colors_values


class StemMaker(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title('Egon stem maker')
        if not (resize_v):
            self.resizable(False, False)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Stem',
                                       font=main_title)
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         font=sub_title)
        bottom_title = customtkinter.CTkLabel(self, text='bottom value:',
                                              font=sub_title)
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         font=sub_title)
        self.x_entry = customtkinter.CTkEntry(self)
        self.bottom_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        upload_x = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
        upload_y = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))
        stem_button = customtkinter.CTkButton(self, text='Make a stem', command=self.make_stem)

        styles_title = customtkinter.CTkLabel(self, text='Styles:', font=med_bold_title)
        line_title = customtkinter.CTkLabel(self, text='lines format:', font=sub_title)
        marker_title = customtkinter.CTkLabel(self, text='marker format:', font=sub_title)

        line_values = ['-', '--', ':']
        marker_values = ['ro', 'r-', 'g--', 'm:']
        line_var = customtkinter.StringVar()
        marker_var = customtkinter.StringVar()
        line_var.set('-')
        marker_var.set('ro')
        self.line = customtkinter.CTkComboBox(self, values=line_values, variable=line_var,  state='readonly')
        self.marker = customtkinter.CTkComboBox(self, values=marker_values, variable=marker_var,  state='readonly')

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0, padx=5)
        bottom_title.grid(row=1, column=1)
        y_title.grid(row=1, column=2, padx=5)
        self.x_entry.grid(row=2, column=0, padx=5)
        self.bottom_entry.grid(row=2, column=1)
        self.y_entry.grid(row=2, column=2, padx=5)
        upload_x.grid(row=3, column=0, padx=5, pady=3)
        upload_y.grid(row=3, column=2, padx=5, pady=3)
        styles_title.grid(row=4, column=1)
        line_title.grid(row=5, column=0, padx=5)
        marker_title.grid(row=5, column=2, padx=5)
        self.line.grid(row=6, column=0, padx=5)
        self.marker.grid(row=6, column=2, padx=5)

        stem_button.grid(row=10, column=1, pady=10)

        if middle_v:
            self.update()
            place_w_middle(self)

        if fun_numbers_v:
            entry_1_r = f'{randint(0, 10)} {randint(0, 10)}'
            entry_2_r = f'{randint(0, 10)} {randint(0, 10)}'
            self.x_entry.insert(END, entry_1_r)
            self.y_entry.insert(END, entry_2_r)

        self.protocol('WM_DELETE_WINDOW', self.close_this)
        self.stemmaker_root = self
        opened_programs.append(self.stemmaker_root)

    def close_this(self):
        opened_programs.remove(self.stemmaker_root)
        self.destroy()

    def make_stem(self):
        x_values = make_array(self.x_entry)
        y_values = make_array(self.y_entry)
        plt.clf()
        plt.stem(x_values, y_values, bottom=self.bottom(), linefmt=change_line(self.line.get()),
                 markerfmt=change_marker(self.marker.get()))
        plt.show()

    def bottom(self):
        if self.bottom_entry.get():
            return self.bottom_entry.get()
        else:
            return 0



class PieMaker(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title('Egon pie-chart maker')
        if not (resize_v):
            self.resizable(False, False)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Pie-charts',
                                       font=main_title)
        percentage_title = customtkinter.CTkLabel(self, text='values:',
                                                  font=sub_title)
        self.percentage_entry = customtkinter.CTkEntry(self)
        names_title = customtkinter.CTkLabel(self, text='Names:',
                                             font=sub_title)
        self.names_entry = customtkinter.CTkEntry(self)

        self.s_var = IntVar()
        self.l_var = IntVar()
        styles_title = customtkinter.CTkLabel(self, text='Styles',
                                              font=med_bold_title)
        shadows = customtkinter.CTkCheckBox(self, text='Shadows', variable=self.s_var)
        sa_title = customtkinter.CTkLabel(self, text='start angle:',
                                          font=sub_title)
        self.start_angle = customtkinter.CTkEntry(self)
        legend_tt = customtkinter.CTkLabel(self, text='Legend title:',
                                           font=sub_title)
        legend_title = customtkinter.CTkLabel(self, text='Legend:',
                                              font=med_bold_title)
        legend = customtkinter.CTkCheckBox(self, text='Legend', variable=self.l_var)
        self.pie_legend_title = customtkinter.CTkEntry(self)
        explode_title = customtkinter.CTkLabel(self, text='Explode values:',
                                               font=sub_title)
        self.explode_entry = customtkinter.CTkEntry(self)

        pie_button = customtkinter.CTkButton(self, text='Make a pie-chart', command=self.pie_maker)

        title.grid(row=0, column=1)
        percentage_title.grid(row=1, column=0, padx=5)
        names_title.grid(row=1, column=2, padx=5)
        self.percentage_entry.grid(row=2, column=0, padx=5)
        self.names_entry.grid(row=2, column=2, padx=5)
        legend_title.grid(row=4, column=1)
        legend_tt.grid(row=5, column=2, padx=5)
        legend.grid(row=6, column=0, padx=5)
        self.pie_legend_title.grid(row=6, column=2, pady=10, padx=5)
        styles_title.grid(row=9, column=1)
        explode_title.grid(row=10, column=1)
        sa_title.grid(row=10, column=2, padx=5)
        shadows.grid(row=11, column=0, padx=5)
        self.explode_entry.grid(row=11, column=1)
        self.start_angle.grid(row=11, column=2, padx=5)

        pie_button.grid(row=12, column=1, pady=10)

        if middle_v:
            self.update()
            place_w_middle(self)

        if fun_numbers_v:
            characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            entry_1_r = f'{randint(0, 10)} {randint(0, 10)}'
            entry_2_r = f'{ran_choice(characters)} {ran_choice(characters)}'
            self.percentage_entry.insert(END, entry_1_r)
            self.names_entry.insert(END, entry_2_r)

        self.protocol('WM_DELETE_WINDOW', self.close_this)
        self.piemaker_root = self
        opened_programs.append(self.piemaker_root)

    def close_this(self):
        opened_programs.remove(self.piemaker_root)
        self.destroy()

    def pie_maker(self):
        percentages_values = make_array(self.percentage_entry)

        if self.labels():
            plt.pie(percentages_values, explode=self.explode(), labels=self.labels(), shadow=self.s_var.get(),
                    startangle=self.angle())
        else:
            plt.pie(percentages_values, explode=self.explode(), shadow=self.s_var.get(), startangle=self.angle())

        if self.l_var.get() == 1:
            plt.legend(title=get_legend(self.pie_legend_title.get()))
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


    def angle(self):
        if self.start_angle.get():
            return int(self.start_angle.get())
        else:
            return 0


class HistogramMaker(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title('Egon histogram maker')
        if not (resize_v):
            self.resizable(False, False)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Histograms',
                                       font=main_title)
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         font=sub_title)
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         font=sub_title)
        self.x_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        x_upload = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
        y_upload = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))

        # titles_title = customtkinter.CTkLabel(self, text='Change titles!',
        #                                       font=med_bold_title)

        titles_title = customtkinter.CTkLabel(self, text='Choose titles!',
                                              font=med_bold_title)
        main_title_ = customtkinter.CTkLabel(self, text='Write main title',
                                             font=sub_title)
        self.main_title_entry = customtkinter.CTkEntry(self)
        x_title_ = customtkinter.CTkLabel(self, text='Write x-label title',
                                          font=sub_title)
        self.x_title_entry = customtkinter.CTkEntry(self)
        y_title_ = customtkinter.CTkLabel(self, text='Write y-label title')
        self.y_title_entry = customtkinter.CTkEntry(self)

        grid_title = customtkinter.CTkLabel(self, text='Grid modes!', font=med_bold_title)
        self.g = customtkinter.IntVar(value=3)
        x_grid = customtkinter.CTkRadioButton(self, text='x', variable=self.g, value=1)
        y_grid = customtkinter.CTkRadioButton(self, text='y', variable=self.g, value=2)
        both_grid = customtkinter.CTkRadioButton(self, text='Both', variable=self.g, value=3)

        histogram_button = customtkinter.CTkButton(self, text='Make a histogram', command=self.make_histogram)

        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0, padx=5)
        y_title.grid(row=1, column=2, padx=5)
        self.x_entry.grid(row=2, column=0, padx=5)
        self.y_entry.grid(row=2, column=2, padx=5)
        x_upload.grid(row=3, column=0, padx=5, pady=3)
        y_upload.grid(row=3, column=2, padx=5, pady=3)
        titles_title.grid(row=4, column=1)
        x_title_.grid(row=5, column=0, padx=5)
        main_title_.grid(row=5, column=1)
        y_title_.grid(row=5, column=2, padx=5)
        self.x_title_entry.grid(row=6, column=0, padx=5)
        self.main_title_entry.grid(row=6, column=1)
        self.y_title_entry.grid(row=6, column=2, padx=5)
        grid_title.grid(row=7, column=1)
        x_grid.grid(row=8, column=0, padx=5)
        both_grid.grid(row=8, column=1)
        y_grid.grid(row=8, column=2, padx=5)
        histogram_button.grid(row=10, column=1, pady=10)

        if middle_v:
            self.update()
            place_w_middle(self)

        if fun_numbers_v:
            entry_1_r = f'{randint(0, 10)} {randint(0, 10)}'
            entry_2_r = f'{randint(0, 10)} {randint(0, 10)}'
            self.x_entry.insert(END, entry_1_r)
            self.y_entry.insert(END, entry_2_r)

        self.protocol('WM_DELETE_WINDOW', self.close_this)
        self.histomaker_root = self
        opened_programs.append(self.histomaker_root)

    def close_this(self):
        opened_programs.remove(self.histomaker_root)
        self.destroy()

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
            messagebox.showerror('error', 'y values must increase monotonically')

    def grid_modes(self):
        if self.g.get() == 1:
            return 'x'
        elif self.g.get() == 2:
            return 'y'
        else:
            return 'both'


class BarMaker(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title('Egon bar maker')
        if not (resize_v):
            self.resizable(False, False)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Bars',
                                       font=main_title)
        bar_name_title = customtkinter.CTkLabel(self, text='bar names:',
                                                font=sub_title)
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         font=sub_title)
        self.bar_name_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        y_upload = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.y_entry))
        graph_button = customtkinter.CTkButton(self, text='Make a bar', command=self.make_bar)

        self.change_width_title = customtkinter.CTkLabel(self, text='change bars app_width:',
                                                         font=sub_title)
        self.bar_width = customtkinter.CTkEntry(self)

        self.change_direction_title = customtkinter.CTkLabel(self, text='bars direction:',
                                                             font=med_bold_title)
        self.i2 = customtkinter.IntVar(value=1)
        horizontal = customtkinter.CTkRadioButton(self, text='horizontal', variable=self.i2, value=1)
        vertical = customtkinter.CTkRadioButton(self, text='vertical', variable=self.i2, value=2)

        self.l_var = IntVar()
        legend_tt = customtkinter.CTkLabel(self, text='Legend title:',
                                           font=sub_title)
        legend_title = customtkinter.CTkLabel(self, text='Legend:',
                                              font=med_bold_title)
        legend = customtkinter.CTkCheckBox(self, text='Legend', variable=self.l_var)
        self.bar_legend_title = customtkinter.CTkEntry(self)

        title.grid(row=0, column=1)
        bar_name_title.grid(row=1, column=0, padx=5)
        y_title.grid(row=1, column=2, padx=5)
        self.bar_name_entry.grid(row=2, column=0, padx=5)
        self.y_entry.grid(row=2, column=2, padx=5)
        y_upload.grid(row=3, column=2, padx=5, pady=3)
        self.change_width_title.grid(row=1, column=1)
        self.bar_width.grid(row=2, column=1)
        self.change_direction_title.grid(row=5, column=1)
        horizontal.grid(row=6, column=0, padx=5)
        vertical.grid(row=6, column=2, padx=5)
        legend_title.grid(row=7, column=1)
        legend_tt.grid(row=8, column=0, padx=5)
        legend.grid(row=9, column=2, padx=5)
        self.bar_legend_title.grid(row=9, column=0, padx=5)
        graph_button.grid(row=10, column=1, pady=10)

        if middle_v:
            self.update()
            place_w_middle(self)

        if fun_numbers_v:
            characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            entry_1_r = f'{randint(0, 10)} {randint(0, 10)}'
            entry_2_r = f'{ran_choice(characters)} {ran_choice(characters)}'
            self.y_entry.insert(END, entry_1_r)
            self.bar_name_entry.insert(END, entry_2_r)

        self.protocol('WM_DELETE_WINDOW', self.close_this)
        self.barmaker_root = self
        opened_programs.append(self.barmaker_root)

    def close_this(self):
        opened_programs.remove(self.barmaker_root)
        self.destroy()

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
                plt.legend(title=get_legend(self.bar_legend_title.get()))
            plt.show()
        except ValueError:
            messagebox.showerror('error', 'y values must increase monotonically')

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


# graph maker window creations
class GraphMaker(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        # customtkinter.set_appearance_mode('dark')
        # customtkinter.set_default_color_theme('dark-blue')
        # root = customtkinter.CTk()

        # create window
        self.title('Egon graph maker')
        if not (resize_v):
            self.resizable(False, False)
        # variables
        self.marker_var = customtkinter.StringVar()
        self.marker_v = ['o', '*', '.', ',', 'x', 'X', '+', 'P', 's', 'D', 'd', 'p', 'H', 'h', 'v', '^', '<', '>', '1',
                         '2',
                         '3', '4', '|', '_']
        self.marker_var.set(ran_choice(self.marker_v))
        self.line_var = customtkinter.StringVar()
        self.line_v = ['-', ':', '--', '-.']
        self.line_var.set('-')
        self.i = customtkinter.IntVar(value=3)
        # make ui components
        title = customtkinter.CTkLabel(self, text='Graphical user interface for Graphs',
                                       font=main_title)
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         font=sub_title)
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         font=sub_title)
        self.x_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        upload_x = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
        upload_y = customtkinter.CTkButton(self, text='Upload', command=lambda: upload(self.x_entry))
        graph_button = customtkinter.CTkButton(self, text='Make a graph', command=self.make_graph)
        styles_title = customtkinter.CTkLabel(self, text='Change styles!',
                                              font=med_bold_title)
        marker_title = customtkinter.CTkLabel(self, text='Choose marker',
                                              font=sub_title)
        self.marker_select = customtkinter.CTkComboBox(self, state='readonly', variable=self.marker_var,
                                                  values=self.marker_v)
        line_style_title = customtkinter.CTkLabel(self, text='Choose line style',
                                                  font=sub_title)
        self.line_select_style = customtkinter.CTkComboBox(self, state='readonly', variable=self.line_var, values=self.line_v)
        sizes_title = customtkinter.CTkLabel(self, text='Change sizes!',
                                             font=med_bold_title)
        dot_title = customtkinter.CTkLabel(self, text='Choose dot size',
                                           font=sub_title)
        self.dot_select = customtkinter.CTkEntry(self)
        line_title = customtkinter.CTkLabel(self, text='Choose line size',
                                            font=sub_title)
        self.line_select_entry = customtkinter.CTkEntry(self)
        titles_title = customtkinter.CTkLabel(self, text='Change titles!',
                                              font=med_bold_title)
        main_title_ = customtkinter.CTkLabel(self, text='Write main title',
                                             font=sub_title)
        self.main_title_entry = customtkinter.CTkEntry(self)
        x_title_ = customtkinter.CTkLabel(self, text='Write x-label title',
                                          font=sub_title)
        self.x_title_entry = customtkinter.CTkEntry(self)
        y_title_ = customtkinter.CTkLabel(self, text='Write y-label title',
                                          font=sub_title)
        self.y_title_entry = customtkinter.CTkEntry(self)
        grid_title = customtkinter.CTkLabel(self, text='Change grid modes!',
                                            font=med_bold_title)
        x_grid = customtkinter.CTkRadioButton(self, text='x', variable=self.i, value=1)
        y_grid = customtkinter.CTkRadioButton(self, text='y', variable=self.i, value=2)
        both_grid = customtkinter.CTkRadioButton(self, text='Both', variable=self.i, value=3)
        inf_line_title = customtkinter.CTkLabel(self, text='Make an infinite line!',
                                                font=med_bold_title)
        inf_line_x_title = customtkinter.CTkLabel(self, text='Write value',
                                                  font=sub_title)
        inf_line_y_title = customtkinter.CTkLabel(self, text='select mode',
                                                  font=sub_title)
        # inf_line_slope_t = customtkinter.CTkLabel(self, text='Write slope value',
        # font=sub_title)
        self.inf_line_value = customtkinter.CTkEntry(self)
        self.inf_line_v = customtkinter.StringVar()
        self.inf_line_v.set('vertical')
        self.sinf_line = ['vertical', 'horizontal']
        self.inf_line_mode = customtkinter.CTkComboBox(self, state='readonly', variable=self.inf_line_v,
                                                       values=self.sinf_line)
        # self.inf_line_slope = customtkinter.CTkEntry(self)
        # place ui components
        title.grid(row=0, column=1)
        x_title.grid(row=1, column=0, padx=5)
        y_title.grid(row=1, column=2, padx=5)
        self.x_entry.grid(row=2, column=0, padx=5)
        self.y_entry.grid(row=2, column=2, padx=5)
        upload_x.grid(row=3, column=0, padx=5)
        upload_y.grid(row=3, column=2, padx=5)
        styles_title.grid(row=4, column=1)
        marker_title.grid(row=5, column=0, padx=5)
        line_style_title.grid(row=5, column=2, padx=5)
        self.marker_select.grid(row=6, column=0, padx=5)
        self.line_select_style.grid(row=6, column=2, padx=5)
        sizes_title.grid(row=7, column=1)
        dot_title.grid(row=8, column=0, padx=5)
        line_title.grid(row=8, column=2, padx=5)
        self.dot_select.grid(row=9, column=0, padx=5)
        self.line_select_entry.grid(row=9, column=2, padx=5)
        titles_title.grid(row=10, column=1)
        main_title_.grid(row=11, column=1)
        x_title_.grid(row=11, column=0, padx=5)
        y_title_.grid(row=11, column=2, padx=5)
        self.x_title_entry.grid(row=12, column=0, padx=5)
        self.main_title_entry.grid(row=12, column=1)
        self.y_title_entry.grid(row=12, column=2, padx=5)
        grid_title.grid(row=13, column=1)
        x_grid.grid(row=14, column=0, padx=5)
        both_grid.grid(row=14, column=1)
        y_grid.grid(row=14, column=2, padx=5)
        inf_line_title.grid(row=15, column=1)
        inf_line_x_title.grid(row=16, column=0, padx=5)
        # inf_line_slope_t.grid(row=15, column=1)
        inf_line_y_title.grid(row=16, column=2, padx=5)
        self.inf_line_value.grid(row=17, column=0, padx=5)
        # self.inf_line_slope.grid(row=16, column=1)
        self.inf_line_mode.grid(row=17, column=2, padx=5)
        graph_button.grid(row=18, column=1, pady=10)

        if middle_v:
            self.update()
            place_w_middle(self)

        if fun_numbers_v:
            entry_1_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
            entry_2_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
            self.x_entry.insert(END, entry_1_r)
            self.y_entry.insert(END, entry_2_r)

        self.protocol('WM_DELETE_WINDOW', self.close_this)
        self.grpahmaker_root = self
        opened_programs.append(self.grpahmaker_root)

    def close_this(self):
        opened_programs.remove(self.grpahmaker_root)
        self.destroy()

    # create the graph:
    def make_graph(self):

        self.change_grid_modes()
        x_values = make_array(self.x_entry)
        y_values = make_array(self.y_entry)
        try:
            plt.clf()

            # infinite line set
            if self.inf_line():
                # if self.inf_line.split(' ') > 1

                if self.inf_line() == 'vertical':
                    for line in self.infv1.split(' '):
                        plt.axvline(x=line, linestyle='--')
                elif self.inf_line() == 'horizontal':
                    for line in self.infv1.split(' '):
                        plt.axhline(y=line, linestyle='--')

            plt.plot(x_values, y_values, marker=change_marker(self.marker_select.get(), 'graph'), ms=self.change_dot_size(),
                     linewidth=self.change_line_size(), linestyle=change_line(self.line_select_style.get()))
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
        except BaseException as e:
            messagebox.showerror('error', 'an error occurred')
            print(e)


    def change_dot_size(self):
        self.chosen_dot_size = self.dot_select.get()
        if str(self.chosen_dot_size).isdigit():
            self.dot_value = self.chosen_dot_size
            return self.dot_value
        else:
            self.dot_value = 10
            return self.dot_value

    def change_line_size(self):
        self.chosen_line_size = self.line_select_entry.get()
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
        if self.inf_line_value.get() and self.inf_line_mode.get():
            self.infv1 = self.inf_line_value.get()
            # if ' ' in str(self.infv1).split(' '):
            #     '''+ not working'''
            #     print('Working')
            #     self.infv1 = int(str(self.infv1).split(' '))
            #     print(self.infv1)
            return self.inf_line_mode.get()
        else:
            return False




if __name__ == '__main__':
    mm = MainMenu()
    mm.mainloop()
