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
    if not (chosen_legend):
        return ''
    else:
        return chosen_legend


def change_line(line):
    if line:
        return line
    else:
        return '-'


# global functions for common things
def ask_for_file(entries):
    file_name = filedialog.askopenfilename(title='Open file', filetypes=(('All', '*.*'), ('CSV', 'csv.*')))
    if file_name:
        file_data = pandas.read_csv(file_name)
        ask_for_columns(file_data, entries)


def ask_for_columns(file_data, entries):
    if file_data is None:
        return

    column_window = customtkinter.CTkToplevel()
    column_window.title('Choose Columns')
    column_window.geometry('400x300')

    label = customtkinter.CTkLabel(column_window, text='Select columns to use:')
    label.pack(pady=10)

    listbox = tkinter.Listbox(column_window, selectmode=tkinter.MULTIPLE)
    for col in file_data.columns:
        listbox.insert(tkinter.END, col)
    listbox.pack(pady=10, padx=10, fill='both', expand=True)

    def on_submit():
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showwarning('No Columns Selected', 'Please select at least one column.')
            return

        selected_columns = [file_data.columns[i] for i in selected_indices]

        for i, entry in enumerate(entries):
            if i < len(selected_columns):
                column_data = file_data[selected_columns[i]].to_string(index=False).replace('\n', ' ')
                entry.delete(0, END)
                entry.insert(0, column_data)

        column_window.destroy()

    submit_button = customtkinter.CTkButton(column_window, text='Submit', command=on_submit)
    submit_button.pack(pady=10)


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
        self.open_graphMaker = customtkinter.CTkButton(app_frame, text='Graph maker',
                                                       command=lambda: open_app(GraphMaker), text_color=button_fg)
        self.open_histogramMaker = customtkinter.CTkButton(app_frame, text='Histogram maker', command=lambda: open_app(
            HistogramMaker))
        self.open_barMaker = customtkinter.CTkButton(app_frame, text='Bar maker', command=lambda: open_app(BarMaker))
        self.open_pieMaker = customtkinter.CTkButton(app_frame, text='Pie maker', command=lambda: open_app(PieMaker))
        self.open_stemMaker = customtkinter.CTkButton(app_frame, text='Stem maker', command=lambda: open_app(StemMaker))
        self.open_scatterPlotMaker = customtkinter.CTkButton(app_frame, text='Scatter plot maker',
                                                             command=lambda: open_app(
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
        limit_sizes_check = customtkinter.CTkCheckBox(settings_frame, text='Limit window sizes',
                                                      variable=self.limit_sizes_v
                                                      , command=self.resize_op)
        fun_numbers_check = customtkinter.CTkCheckBox(settings_frame, text='Fun numbers', variable=self.fun_numbers_v,
                                                      command=self.fun_v_set)
        transparency_title = customtkinter.CTkLabel(settings_frame, text='Transparency:', font=sub_title)
        self.trans_progress = customtkinter.CTkSlider(settings_frame, from_=25, to=100, variable=self.tr_v,
                                                      command=self.change_tr)
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
        if not (initial):
            resize_v = not (self.limit_sizes_v.get())
        if not (resize_v):
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


class BasePlotMaker(customtkinter.CTk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        if not resize_v:
            self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.close_this)
        opened_programs.append(self)

    def finalize_setup(self):
        if middle_v:
            self.update()
            place_w_middle(self)
        if fun_numbers_v:
            self._setup_fun_numbers()

    def _setup_fun_numbers(self):
        pass

    def close_this(self):
        opened_programs.remove(self)
        self.destroy()


class BoxPlot(BasePlotMaker):

    def __init__(self):
        super().__init__('Egon Box plot')
        self.pa_var = IntVar()
        self.notch_var = IntVar()
        self.line_var = customtkinter.StringVar()
        ls_values = [' ', 'solid', 'dashed', 'dashdot', 'dotted']
        default_line_var = ran_choice(ls_values)
        self.line_var.set(default_line_var)

        title = customtkinter.CTkLabel(self, text='Graphical user interface for BoxPlots', font=main_title)
        title.pack(pady=10)

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(padx=5, pady=5, fill='both', expand=True)

        data_tab = tabview.add('Data')
        style_tab = tabview.add('Style')
        names_tab = tabview.add('Names')

        # --- Data Tab ---
        data_tab.grid_columnconfigure(0, weight=1)
        data_tab.grid_columnconfigure(1, weight=1)
        data_tab.grid_columnconfigure(2, weight=1)
        data_title = customtkinter.CTkLabel(data_tab, text='data values:', font=sub_title)
        self.data_entry1 = customtkinter.CTkEntry(data_tab)
        self.data_entry2 = customtkinter.CTkEntry(data_tab)
        self.data_entry3 = customtkinter.CTkEntry(data_tab)
        upload_button = customtkinter.CTkButton(data_tab, text='Upload Data', command=lambda: ask_for_file(
            [self.data_entry1, self.data_entry2, self.data_entry3]))

        data_title.grid(row=0, column=1, pady=5)
        self.data_entry1.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
        self.data_entry2.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        self.data_entry3.grid(row=1, column=2, padx=5, pady=2, sticky='ew')
        upload_button.grid(row=2, column=1, pady=10)

        # --- Style Tab ---
        style_tab.grid_columnconfigure(0, weight=1)
        style_tab.grid_columnconfigure(1, weight=1)
        patchA_checkbox = customtkinter.CTkCheckBox(style_tab, text='Patch artist', variable=self.pa_var)
        notch_checkbox = customtkinter.CTkCheckBox(style_tab, text='Notch', variable=self.notch_var)
        lines_title = customtkinter.CTkLabel(style_tab, text='Lines:', font=med_bold_title)
        line_width_title = customtkinter.CTkLabel(style_tab, text='line app_width:', font=sub_title)
        line_style_title = customtkinter.CTkLabel(style_tab, text='line style:', font=sub_title)
        self.line_width = customtkinter.CTkEntry(style_tab)
        self.line_style = customtkinter.CTkComboBox(style_tab, state='readonly', variable=self.line_var,
                                                    values=ls_values)

        patchA_checkbox.grid(row=0, column=0, padx=5, pady=5)
        notch_checkbox.grid(row=0, column=1, padx=5, pady=5)
        lines_title.grid(row=1, column=0, columnspan=2, pady=5)
        line_width_title.grid(row=2, column=0, padx=5, pady=2)
        self.line_width.grid(row=3, column=0, padx=5, pady=2, sticky='ew')
        line_style_title.grid(row=2, column=1, padx=5, pady=2)
        self.line_style.grid(row=3, column=1, padx=5, pady=2, sticky='ew')

        # --- Names Tab ---
        names_tab.grid_columnconfigure(0, weight=1)
        names_tab.grid_columnconfigure(1, weight=1)
        names_title = customtkinter.CTkLabel(names_tab, text='Names:', font=med_bold_title)
        title_title = customtkinter.CTkLabel(names_tab, text='main title:', font=sub_title)
        x_val_title = customtkinter.CTkLabel(names_tab, text='X-axis names:', font=sub_title)
        self.title_entry = customtkinter.CTkEntry(names_tab)
        x_values_names = customtkinter.CTkEntry(names_tab, state=DISABLED)

        names_title.grid(row=0, column=0, columnspan=2, pady=5)
        title_title.grid(row=1, column=0, padx=5, pady=2)
        self.title_entry.grid(row=2, column=0, padx=5, pady=2, sticky='ew')
        x_val_title.grid(row=1, column=1, padx=5, pady=2)
        x_values_names.grid(row=2, column=1, padx=5, pady=2, sticky='ew')

        # --- Make Boxplot Button ---
        boxplot_button = customtkinter.CTkButton(self, text='Make box plot', command=self.make_boxplot)
        boxplot_button.pack(pady=10)

        self.finalize_setup()

    def _setup_fun_numbers(self):
        entry_1_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
        entry_2_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
        entry_3_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
        self.data_entry1.insert(END, entry_1_r)
        self.data_entry2.insert(END, entry_2_r)
        self.data_entry3.insert(END, entry_3_r)

    def make_boxplot(self):
        plt.clf()
        x = plt.boxplot(self.data_values(), patch_artist=self.pa_var.get(), notch=self.notch_var.get())
        # lines management
        for whisker in x['whiskers']:
            whisker.set(linewidth=self.line_w(), linestyle=change_line(self.line_style.get()))
        if title_condition(self.title_entry):
            plt.title(title_condition(self.title_entry))
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


class ErrorBarMaker(BasePlotMaker):

    def __init__(self):
        super().__init__('Egon Error bar maker')
        self.u_var = IntVar()
        self.l_var = IntVar()

        title = customtkinter.CTkLabel(self, text='Graphical user interface for ErrorBars', font=main_title)
        title.pack(pady=10)

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(padx=5, pady=5, fill='both', expand=True)

        data_tab = tabview.add('Data')
        error_tab = tabview.add('Error Values')
        options_tab = tabview.add('Options')

        # --- Data Tab ---
        data_tab.grid_columnconfigure(0, weight=1)
        data_tab.grid_columnconfigure(1, weight=1)
        x_title = customtkinter.CTkLabel(data_tab, text='x values:', font=sub_title)
        y_title = customtkinter.CTkLabel(data_tab, text='y values:', font=sub_title)
        self.x_entry = customtkinter.CTkEntry(data_tab)
        self.y_entry = customtkinter.CTkEntry(data_tab)
        upload_button = customtkinter.CTkButton(data_tab, text='Upload Data',
                                                command=lambda: ask_for_file([self.x_entry, self.y_entry]))

        x_title.grid(row=0, column=0, padx=5, pady=2, sticky='ew')
        self.x_entry.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
        y_title.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        self.y_entry.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        upload_button.grid(row=2, column=0, columnspan=2, pady=10)

        # --- Error Values Tab ---
        error_tab.grid_columnconfigure(0, weight=1)
        error_tab.grid_columnconfigure(1, weight=1)
        xerr_title = customtkinter.CTkLabel(error_tab, text='xerr value:', font=sub_title)
        yerr_title = customtkinter.CTkLabel(error_tab, text='yerr value:', font=sub_title)
        self.xerr_entry = customtkinter.CTkEntry(error_tab)
        self.yerr_entry = customtkinter.CTkEntry(error_tab)

        xerr_title.grid(row=0, column=0, padx=5, pady=2, sticky='ew')
        self.xerr_entry.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
        yerr_title.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        self.yerr_entry.grid(row=1, column=1, padx=5, pady=2, sticky='ew')

        # --- Options Tab ---
        options_tab.grid_columnconfigure(0, weight=1)
        options_tab.grid_columnconfigure(1, weight=1)
        uplims_checkbox = customtkinter.CTkCheckBox(options_tab, text='upper limits', variable=self.u_var)
        lolims_checkbox = customtkinter.CTkCheckBox(options_tab, text='lower limits', variable=self.l_var)

        uplims_checkbox.grid(row=0, column=0, padx=5, pady=5)
        lolims_checkbox.grid(row=0, column=1, padx=5, pady=5)

        # --- Make Error Bar Button ---
        eb_button = customtkinter.CTkButton(self, text='make error bar', command=self.make_errorBar)
        eb_button.pack(pady=10)

        self.finalize_setup()

    def _setup_fun_numbers(self):
        entry_1_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
        entry_2_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
        self.x_entry.insert(END, entry_1_r)
        self.y_entry.insert(END, entry_2_r)

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


class ContourfMaker(BasePlotMaker):

    def __init__(self):
        super().__init__('Egon contourf Maker')
        title = customtkinter.CTkLabel(self, text='Graphical user interface for ContourF', font=main_title)
        title.pack(pady=10)

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(padx=5, pady=5, fill='both', expand=True)

        data_tab = tabview.add('Data')
        z_values_tab = tabview.add('Z Values')

        # --- Data Tab ---
        data_tab.grid_columnconfigure(0, weight=1)
        data_tab.grid_columnconfigure(1, weight=1)
        x_title = customtkinter.CTkLabel(data_tab, text='x values:', font=sub_title)
        y_title = customtkinter.CTkLabel(data_tab, text='y values:', font=sub_title)
        self.x_entry = customtkinter.CTkEntry(data_tab)
        self.y_entry = customtkinter.CTkEntry(data_tab)
        upload_button = customtkinter.CTkButton(data_tab, text='Upload Data',
                                                command=lambda: ask_for_file([self.x_entry, self.y_entry]))

        x_title.grid(row=0, column=0, padx=5, pady=2, sticky='ew')
        self.x_entry.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
        y_title.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        self.y_entry.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        upload_button.grid(row=2, column=0, columnspan=2, pady=10)

        # --- Z Values Tab ---
        z_values_tab.grid_columnconfigure(0, weight=1)
        z_values_tab.grid_columnconfigure(1, weight=1)
        z_title = customtkinter.CTkLabel(z_values_tab, text='z values:', font=sub_title)
        self.z_entry = customtkinter.CTkEntry(z_values_tab)
        self.z_entry2 = customtkinter.CTkEntry(z_values_tab)
        self.z_entry3 = customtkinter.CTkEntry(z_values_tab)
        self.z_entry4 = customtkinter.CTkEntry(z_values_tab)

        z_title.grid(row=0, column=0, columnspan=2, pady=5)
        self.z_entry.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
        self.z_entry2.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        self.z_entry3.grid(row=2, column=0, padx=5, pady=2, sticky='ew')
        self.z_entry4.grid(row=2, column=1, padx=5, pady=2, sticky='ew')

        # --- Make Contourf Button ---
        contour_button = customtkinter.CTkButton(self, text='make contourf', command=self.make_contourf)
        contour_button.pack(pady=10)

        self.finalize_setup()

    def _setup_fun_numbers(self):
        entry_1_r = f'{randint(0, 10)} {randint(0, 10)}'
        entry_2_r = f'{randint(0, 10)} {randint(0, 10)}'
        self.x_entry.insert(END, entry_1_r)
        self.y_entry.insert(END, entry_2_r)
        self.z_entry.insert(END, randint(0, 10))
        self.z_entry2.insert(END, randint(0, 10))
        self.z_entry3.insert(END, randint(0, 10))
        self.z_entry4.insert(END, randint(0, 10))

    def make_contourf(self):
        self.x_values = make_array(self.x_entry)
        # must be 2x2 - D array!!!
        self.z_values = tuple(array((self.z_entry.get().split(' '), self.z_entry2.get().split(' '),
                                     self.z_entry3.get().split(' '), self.z_entry4.get().split()), dtype='int32'
                                    ).reshape(2, 2))
        self.y_values = make_array(self.y_entry)
        plt.contourf(self.x_values, self.y_values, self.z_values)
        plt.show()


class ImShowMaker(BasePlotMaker):

    def __init__(self):
        super().__init__('Egon Imshow maker')
        global im_transparency
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

        title = customtkinter.CTkLabel(self, text='Graphical user interface for ImageShow', font=main_title)
        title.pack(pady=10)

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(padx=5, pady=5, fill='both', expand=True)

        image_tab = tabview.add('Image')
        style_tab = tabview.add('Style')

        # --- Image Tab ---
        image_tab.grid_columnconfigure(0, weight=1)
        upload_im = customtkinter.CTkButton(image_tab, text='Upload (SG. png)', command=self.upload_image)
        upload_im.pack(pady=10, padx=10, fill='x')

        # --- Style Tab ---
        style_tab.grid_columnconfigure(0, weight=1)
        style_tab.grid_columnconfigure(1, weight=1)
        title_title = customtkinter.CTkLabel(style_tab, text='add title:', font=sub_title)
        self.title_entry = customtkinter.CTkEntry(style_tab)
        tr_title = customtkinter.CTkLabel(style_tab, text='transparency:', font=sub_title)
        im_transparency = customtkinter.CTkSlider(style_tab, from_=0, to=100)
        im_transparency.set(100)
        c_map_title = customtkinter.CTkLabel(style_tab, text='cmap:', font=sub_title)
        cmap_combobox = customtkinter.CTkComboBox(style_tab, variable=self.cmap_var, values=self.cmap_values,
                                                  command=self.change_cmap, state='readonly')
        interpolation_title = customtkinter.CTkLabel(style_tab, text='interpolation:', font=sub_title)
        self.interpolation_c = customtkinter.CTkComboBox(style_tab, values=interpolation_values,
                                                         variable=self.interpolation_var, state='readonly')

        title_title.grid(row=0, column=0, padx=5, pady=2)
        self.title_entry.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
        tr_title.grid(row=0, column=1, padx=5, pady=2)
        im_transparency.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        c_map_title.grid(row=2, column=0, padx=5, pady=2)
        cmap_combobox.grid(row=3, column=0, padx=5, pady=2, sticky='ew')
        interpolation_title.grid(row=2, column=1, padx=5, pady=2)
        self.interpolation_c.grid(row=3, column=1, padx=5, pady=2, sticky='ew')

        # --- Make Imshow Button ---
        imshow_button = customtkinter.CTkButton(self, text='make imshow', command=self.make_imshow)
        imshow_button.pack(pady=10)

        self.finalize_setup()

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


class ScatterPlotMaker(BasePlotMaker):

    def __init__(self):
        super().__init__('Egon scatter plot maker')
        global sc_transparency

        title = customtkinter.CTkLabel(self, text='Graphical user interface for ScatterPlot', font=main_title)
        title.pack(pady=10)

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(padx=5, pady=5, fill='both', expand=True)

        data_tab = tabview.add('Data')
        style_tab = tabview.add('Style')

        # --- Data Tab ---
        data_tab.grid_columnconfigure(0, weight=1)
        data_tab.grid_columnconfigure(1, weight=1)
        x_title = customtkinter.CTkLabel(data_tab, text='x values:', font=sub_title)
        y_title = customtkinter.CTkLabel(data_tab, text='y values:', font=sub_title)
        self.x_entry = customtkinter.CTkEntry(data_tab)
        self.y_entry = customtkinter.CTkEntry(data_tab)
        upload_button = customtkinter.CTkButton(data_tab, text='Upload Data',
                                                command=lambda: ask_for_file([self.x_entry, self.y_entry]))

        x_title.grid(row=0, column=0, padx=5, pady=2, sticky='ew')
        self.x_entry.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
        y_title.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        self.y_entry.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        upload_button.grid(row=2, column=0, columnspan=2, pady=10)

        # --- Style Tab ---
        style_tab.grid_columnconfigure(0, weight=1)
        style_tab.grid_columnconfigure(1, weight=1)
        colors_title = customtkinter.CTkLabel(style_tab, text='colors values:', font=sub_title)
        self.colors_entry = customtkinter.CTkEntry(style_tab)
        styles_title = customtkinter.CTkLabel(style_tab, text='Styles:', font=med_bold_title)
        transparency_title = customtkinter.CTkLabel(style_tab, text='transparency:', font=sub_title)
        size_title = customtkinter.CTkLabel(style_tab, text='sizes:', font=sub_title)
        sc_transparency = customtkinter.CTkSlider(style_tab, from_=0, to=100)
        sc_transparency.set(100)
        self.size = customtkinter.CTkEntry(style_tab)

        color_maps_values = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
        color_maps_v = customtkinter.StringVar()
        color_maps_v.set('viridis')
        self.color_map = customtkinter.CTkComboBox(style_tab, values=color_maps_values, variable=color_maps_v,
                                                   state='readonly')

        colors_title.grid(row=0, column=0, columnspan=2, pady=5)
        self.colors_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky='ew')
        styles_title.grid(row=2, column=0, columnspan=2, pady=5)
        size_title.grid(row=3, column=0, padx=5, pady=2)
        self.size.grid(row=4, column=0, padx=5, pady=2, sticky='ew')
        transparency_title.grid(row=3, column=1, padx=5, pady=2)
        sc_transparency.grid(row=4, column=1, padx=5, pady=2, sticky='ew')
        self.color_map.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        # --- Make Scatter Button ---
        self.make_scatter = customtkinter.CTkButton(self, command=self.make_scatter_plot, text='Make scatter plot')
        self.make_scatter.pack(pady=10)

        self.finalize_setup()

    def _setup_fun_numbers(self):
        entry_1_r = f'{randint(0, 20)} {randint(0, 20)} {randint(0, 20)} {randint(0, 20)}'
        entry_2_r = f'{randint(0, 20)} {randint(0, 20)} {randint(0, 20)} {randint(0, 20)}'
        self.x_entry.insert(END, entry_1_r)
        self.y_entry.insert(END, entry_2_r)

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


class StemMaker(BasePlotMaker):

    def __init__(self):
        super().__init__('Egon stem maker')

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Stem', font=main_title)
        title.pack(pady=10)

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(padx=5, pady=5, fill='both', expand=True)

        data_tab = tabview.add('Data')
        style_tab = tabview.add('Style')

        # --- Data Tab ---
        data_tab.grid_columnconfigure(0, weight=1)
        data_tab.grid_columnconfigure(1, weight=1)
        x_title = customtkinter.CTkLabel(data_tab, text='x values:', font=sub_title)
        y_title = customtkinter.CTkLabel(data_tab, text='y values:', font=sub_title)
        self.x_entry = customtkinter.CTkEntry(data_tab)
        self.y_entry = customtkinter.CTkEntry(data_tab)
        upload_button = customtkinter.CTkButton(data_tab, text='Upload Data',
                                                command=lambda: ask_for_file([self.x_entry, self.y_entry]))

        x_title.grid(row=0, column=0, padx=5, pady=2, sticky='ew')
        self.x_entry.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
        y_title.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        self.y_entry.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        upload_button.grid(row=2, column=0, columnspan=2, pady=10)

        # --- Style Tab ---
        style_tab.grid_columnconfigure(0, weight=1)
        style_tab.grid_columnconfigure(1, weight=1)
        bottom_title = customtkinter.CTkLabel(style_tab, text='bottom value:', font=sub_title)
        self.bottom_entry = customtkinter.CTkEntry(style_tab)
        styles_title = customtkinter.CTkLabel(style_tab, text='Styles:', font=med_bold_title)
        line_title = customtkinter.CTkLabel(style_tab, text='lines format:', font=sub_title)
        marker_title = customtkinter.CTkLabel(style_tab, text='marker format:', font=sub_title)

        line_values = ['-', '--', ':']
        marker_values = ['ro', 'r-', 'g--', 'm:']
        line_var = customtkinter.StringVar()
        marker_var = customtkinter.StringVar()
        line_var.set('-')
        marker_var.set('ro')
        self.line = customtkinter.CTkComboBox(style_tab, values=line_values, variable=line_var, state='readonly')
        self.marker = customtkinter.CTkComboBox(style_tab, values=marker_values, variable=marker_var, state='readonly')

        bottom_title.grid(row=0, column=0, columnspan=2, pady=5)
        self.bottom_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky='ew')
        styles_title.grid(row=2, column=0, columnspan=2, pady=5)
        line_title.grid(row=3, column=0, padx=5, pady=2)
        self.line.grid(row=4, column=0, padx=5, pady=2, sticky='ew')
        marker_title.grid(row=3, column=1, padx=5, pady=2)
        self.marker.grid(row=4, column=1, padx=5, pady=2, sticky='ew')

        # --- Make Stem Button ---
        stem_button = customtkinter.CTkButton(self, text='Make a stem', command=self.make_stem)
        stem_button.pack(pady=10)

        self.finalize_setup()

    def _setup_fun_numbers(self):
        entry_1_r = f'{randint(0, 10)} {randint(0, 10)}'
        entry_2_r = f'{randint(0, 10)} {randint(0, 10)}'
        self.x_entry.insert(END, entry_1_r)
        self.y_entry.insert(END, entry_2_r)

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


class PieMaker(BasePlotMaker):

    def __init__(self):
        super().__init__('Egon pie-chart maker')

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Pie-charts', font=main_title)
        title.pack(pady=10)

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(padx=5, pady=5, fill='both', expand=True)

        data_tab = tabview.add('Data')
        style_tab = tabview.add('Style')
        legend_tab = tabview.add('Legend')

        # --- Data Tab ---
        data_tab.grid_columnconfigure(0, weight=1)
        data_tab.grid_columnconfigure(1, weight=1)
        percentage_title = customtkinter.CTkLabel(data_tab, text='values:', font=sub_title)
        self.percentage_entry = customtkinter.CTkEntry(data_tab)
        names_title = customtkinter.CTkLabel(data_tab, text='Names:', font=sub_title)
        self.names_entry = customtkinter.CTkEntry(data_tab)
        upload_button = customtkinter.CTkButton(data_tab, text='Upload Data',
                                                command=lambda: ask_for_file([self.percentage_entry, self.names_entry]))

        percentage_title.grid(row=0, column=0, padx=5, pady=2, sticky='ew')
        self.percentage_entry.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
        names_title.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        self.names_entry.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        upload_button.grid(row=2, column=0, columnspan=2, pady=10)

        # --- Style Tab ---
        style_tab.grid_columnconfigure(0, weight=1)
        style_tab.grid_columnconfigure(1, weight=1)
        self.s_var = IntVar()
        styles_title = customtkinter.CTkLabel(style_tab, text='Styles', font=med_bold_title)
        shadows = customtkinter.CTkCheckBox(style_tab, text='Shadows', variable=self.s_var)
        sa_title = customtkinter.CTkLabel(style_tab, text='start angle:', font=sub_title)
        self.start_angle = customtkinter.CTkEntry(style_tab)
        explode_title = customtkinter.CTkLabel(style_tab, text='Explode values:', font=sub_title)
        self.explode_entry = customtkinter.CTkEntry(style_tab)

        styles_title.grid(row=0, column=0, columnspan=2, pady=5)
        shadows.grid(row=1, column=0, padx=5, pady=5)
        sa_title.grid(row=2, column=0, padx=5, pady=2)
        self.start_angle.grid(row=3, column=0, padx=5, pady=2, sticky='ew')
        explode_title.grid(row=2, column=1, padx=5, pady=2)
        self.explode_entry.grid(row=3, column=1, padx=5, pady=2, sticky='ew')

        # --- Legend Tab ---
        legend_tab.grid_columnconfigure(0, weight=1)
        self.l_var = IntVar()
        legend_title = customtkinter.CTkLabel(legend_tab, text='Legend:', font=med_bold_title)
        legend = customtkinter.CTkCheckBox(legend_tab, text='Legend', variable=self.l_var)
        legend_tt = customtkinter.CTkLabel(legend_tab, text='Legend title:', font=sub_title)
        self.pie_legend_title = customtkinter.CTkEntry(legend_tab)

        legend_title.pack(pady=5)
        legend.pack(pady=5)
        legend_tt.pack(pady=2)
        self.pie_legend_title.pack(padx=5, pady=2, fill='x')

        # --- Make Pie Chart Button ---
        pie_button = customtkinter.CTkButton(self, text='Make a pie-chart', command=self.pie_maker)
        pie_button.pack(pady=10)

        self.finalize_setup()

    def _setup_fun_numbers(self):
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        entry_1_r = f'{randint(0, 10)} {randint(0, 10)}'
        entry_2_r = f'{ran_choice(characters)} {ran_choice(characters)}'
        self.percentage_entry.insert(END, entry_1_r)
        self.names_entry.insert(END, entry_2_r)

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


class HistogramMaker(BasePlotMaker):

    def __init__(self):
        super().__init__('Egon histogram maker')

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Histograms',
                                       font=main_title)
        x_title = customtkinter.CTkLabel(self, text='x values:',
                                         font=sub_title)
        y_title = customtkinter.CTkLabel(self, text='y values:',
                                         font=sub_title)
        self.x_entry = customtkinter.CTkEntry(self)
        self.y_entry = customtkinter.CTkEntry(self)
        upload_button = customtkinter.CTkButton(self, text='Upload Data',
                                                command=lambda: ask_for_file([self.x_entry, self.y_entry]))

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
        upload_button.grid(row=3, column=1, pady=10)
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

        self.finalize_setup()

    def _setup_fun_numbers(self):
        entry_1_r = f'{randint(0, 10)} {randint(0, 10)}'
        entry_2_r = f'{randint(0, 10)} {randint(0, 10)}'
        self.x_entry.insert(END, entry_1_r)
        self.y_entry.insert(END, entry_2_r)

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


class BarMaker(BasePlotMaker):

    def __init__(self):
        super().__init__('Egon bar maker')

        title = customtkinter.CTkLabel(self, text='Graphical user interface for Bars', font=main_title)
        title.pack(pady=10)

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(padx=5, pady=5, fill='both', expand=True)

        data_tab = tabview.add('Data')
        style_tab = tabview.add('Style')
        legend_tab = tabview.add('Legend')

        # --- Data Tab ---
        data_tab.grid_columnconfigure(0, weight=1)
        data_tab.grid_columnconfigure(1, weight=1)
        bar_name_title = customtkinter.CTkLabel(data_tab, text='bar names:', font=sub_title)
        y_title = customtkinter.CTkLabel(data_tab, text='y values:', font=sub_title)
        self.bar_name_entry = customtkinter.CTkEntry(data_tab)
        self.y_entry = customtkinter.CTkEntry(data_tab)
        upload_button = customtkinter.CTkButton(data_tab, text='Upload Data',
                                                command=lambda: ask_for_file([self.bar_name_entry, self.y_entry]))

        bar_name_title.grid(row=0, column=0, padx=5, pady=2, sticky='ew')
        self.bar_name_entry.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
        y_title.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        self.y_entry.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        upload_button.grid(row=2, column=0, columnspan=2, pady=10)

        # --- Style Tab ---
        style_tab.grid_columnconfigure(0, weight=1)
        style_tab.grid_columnconfigure(1, weight=1)
        self.change_width_title = customtkinter.CTkLabel(style_tab, text='change bars app_width:', font=sub_title)
        self.bar_width = customtkinter.CTkEntry(style_tab)
        self.change_direction_title = customtkinter.CTkLabel(style_tab, text='bars direction:', font=med_bold_title)
        self.i2 = customtkinter.IntVar(value=1)
        horizontal = customtkinter.CTkRadioButton(style_tab, text='horizontal', variable=self.i2, value=1)
        vertical = customtkinter.CTkRadioButton(style_tab, text='vertical', variable=self.i2, value=2)

        self.change_width_title.grid(row=0, column=0, columnspan=2, pady=5)
        self.bar_width.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky='ew')
        self.change_direction_title.grid(row=2, column=0, columnspan=2, pady=5)
        horizontal.grid(row=3, column=0, padx=5, pady=2)
        vertical.grid(row=3, column=1, padx=5, pady=2)

        # --- Legend Tab ---
        legend_tab.grid_columnconfigure(0, weight=1)
        self.l_var = IntVar()
        legend_title = customtkinter.CTkLabel(legend_tab, text='Legend:', font=med_bold_title)
        legend = customtkinter.CTkCheckBox(legend_tab, text='Legend', variable=self.l_var)
        legend_tt = customtkinter.CTkLabel(legend_tab, text='Legend title:', font=sub_title)
        self.bar_legend_title = customtkinter.CTkEntry(legend_tab)

        legend_title.pack(pady=5)
        legend.pack(pady=5)
        legend_tt.pack(pady=2)
        self.bar_legend_title.pack(padx=5, pady=2, fill='x')

        # --- Make Bar Button ---
        graph_button = customtkinter.CTkButton(self, text='Make a bar', command=self.make_bar)
        graph_button.pack(pady=10)

        self.finalize_setup()

    def _setup_fun_numbers(self):
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        entry_1_r = f'{randint(0, 10)} {randint(0, 10)}'
        entry_2_r = f'{ran_choice(characters)} {ran_choice(characters)}'
        self.y_entry.insert(END, entry_1_r)
        self.bar_name_entry.insert(END, entry_2_r)

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
class GraphMaker(BasePlotMaker):

    def __init__(self):
        super().__init__('Egon graph maker')
        # customtkinter.set_appearance_mode('dark')
        # customtkinter.set_default_color_theme('dark-blue')
        # root = customtkinter.CTk()

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
        title.pack(pady=10)

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(padx=5, pady=5, fill='both', expand=True)

        data_tab = tabview.add('Data')
        style_tab = tabview.add('Style')
        titles_tab = tabview.add('Titles & Grid')
        advanced_tab = tabview.add('Advanced')

        # --- Data Tab ---
        data_tab.grid_columnconfigure(0, weight=1)
        data_tab.grid_columnconfigure(1, weight=1)
        x_title = customtkinter.CTkLabel(data_tab, text='x values:', font=sub_title)
        y_title = customtkinter.CTkLabel(data_tab, text='y values:', font=sub_title)
        self.x_entry = customtkinter.CTkEntry(data_tab)
        self.y_entry = customtkinter.CTkEntry(data_tab)
        upload_button = customtkinter.CTkButton(data_tab, text='Upload Data',
                                                command=lambda: ask_for_file([self.x_entry, self.y_entry]))

        x_title.grid(row=0, column=0, padx=5, pady=2, sticky='ew')
        self.x_entry.grid(row=1, column=0, padx=5, pady=2, sticky='ew')
        y_title.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        self.y_entry.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        upload_button.grid(row=2, column=0, columnspan=2, pady=10)

        # --- Style Tab ---
        style_tab.grid_columnconfigure(0, weight=1)
        style_tab.grid_columnconfigure(1, weight=1)
        styles_title = customtkinter.CTkLabel(style_tab, text='Change styles!', font=med_bold_title)
        marker_title = customtkinter.CTkLabel(style_tab, text='Choose marker', font=sub_title)
        self.marker_select = customtkinter.CTkComboBox(style_tab, state='readonly', variable=self.marker_var,
                                                       values=self.marker_v)
        line_style_title = customtkinter.CTkLabel(style_tab, text='Choose line style', font=sub_title)
        self.line_select_style = customtkinter.CTkComboBox(style_tab, state='readonly', variable=self.line_var,
                                                           values=self.line_v)

        sizes_title = customtkinter.CTkLabel(style_tab, text='Change sizes!', font=med_bold_title)
        dot_title = customtkinter.CTkLabel(style_tab, text='Choose dot size', font=sub_title)
        self.dot_select = customtkinter.CTkEntry(style_tab)
        line_title = customtkinter.CTkLabel(style_tab, text='Choose line size', font=sub_title)
        self.line_select_entry = customtkinter.CTkEntry(style_tab)

        styles_title.grid(row=0, column=0, columnspan=2, pady=5, sticky='n')
        marker_title.grid(row=1, column=0, padx=5, pady=2)
        self.marker_select.grid(row=2, column=0, padx=5, pady=2, sticky='ew')
        line_style_title.grid(row=1, column=1, padx=5, pady=2)
        self.line_select_style.grid(row=2, column=1, padx=5, pady=2, sticky='ew')
        sizes_title.grid(row=3, column=0, columnspan=2, pady=5)
        dot_title.grid(row=4, column=0, padx=5, pady=2)
        self.dot_select.grid(row=5, column=0, padx=5, pady=2, sticky='ew')
        line_title.grid(row=4, column=1, padx=5, pady=2)
        self.line_select_entry.grid(row=5, column=1, padx=5, pady=2, sticky='ew')

        # --- Titles & Grid Tab ---
        titles_tab.grid_columnconfigure(0, weight=1)
        titles_tab.grid_columnconfigure(1, weight=1)
        titles_tab.grid_columnconfigure(2, weight=1)
        titles_title = customtkinter.CTkLabel(titles_tab, text='Change titles!', font=med_bold_title)
        main_title_ = customtkinter.CTkLabel(titles_tab, text='Write main title', font=sub_title)
        self.main_title_entry = customtkinter.CTkEntry(titles_tab)
        x_title_ = customtkinter.CTkLabel(titles_tab, text='Write x-label title', font=sub_title)
        self.x_title_entry = customtkinter.CTkEntry(titles_tab)
        y_title_ = customtkinter.CTkLabel(titles_tab, text='Write y-label title', font=sub_title)
        self.y_title_entry = customtkinter.CTkEntry(titles_tab)

        grid_title = customtkinter.CTkLabel(titles_tab, text='Change grid modes!', font=med_bold_title)
        x_grid = customtkinter.CTkRadioButton(titles_tab, text='x', variable=self.i, value=1)
        y_grid = customtkinter.CTkRadioButton(titles_tab, text='y', variable=self.i, value=2)
        both_grid = customtkinter.CTkRadioButton(titles_tab, text='Both', variable=self.i, value=3)

        titles_title.grid(row=0, column=1, pady=5)
        main_title_.grid(row=1, column=1, padx=5, pady=2)
        self.main_title_entry.grid(row=2, column=1, padx=5, pady=2, sticky='ew')
        x_title_.grid(row=3, column=0, padx=5, pady=2)
        self.x_title_entry.grid(row=4, column=0, padx=5, pady=2, sticky='ew')
        y_title_.grid(row=3, column=2, padx=5, pady=2)
        self.y_title_entry.grid(row=4, column=2, padx=5, pady=2, sticky='ew')

        grid_title.grid(row=5, column=1, pady=5)
        x_grid.grid(row=6, column=0, padx=5, pady=2)
        both_grid.grid(row=6, column=1, padx=5, pady=2)
        y_grid.grid(row=6, column=2, padx=5, pady=2)

        # --- Advanced Tab ---
        advanced_tab.grid_columnconfigure(0, weight=1)
        advanced_tab.grid_columnconfigure(1, weight=1)
        inf_line_title = customtkinter.CTkLabel(advanced_tab, text='Make an infinite line!', font=med_bold_title)
        inf_line_x_title = customtkinter.CTkLabel(advanced_tab, text='Write value', font=sub_title)
        inf_line_y_title = customtkinter.CTkLabel(advanced_tab, text='select mode', font=sub_title)
        self.inf_line_value = customtkinter.CTkEntry(advanced_tab)
        self.inf_line_v = customtkinter.StringVar()
        self.inf_line_v.set('vertical')
        self.sinf_line = ['vertical', 'horizontal']
        self.inf_line_mode = customtkinter.CTkComboBox(advanced_tab, state='readonly', variable=self.inf_line_v,
                                                       values=self.sinf_line)

        inf_line_title.grid(row=0, column=0, columnspan=2, pady=5)
        inf_line_x_title.grid(row=1, column=0, padx=5, pady=2)
        self.inf_line_value.grid(row=2, column=0, padx=5, pady=2, sticky='ew')
        inf_line_y_title.grid(row=1, column=1, padx=5, pady=2)
        self.inf_line_mode.grid(row=2, column=1, padx=5, pady=2, sticky='ew')

        # --- Make Graph Button ---
        graph_button = customtkinter.CTkButton(self, text='Make a graph', command=self.make_graph)
        graph_button.pack(pady=10)

        self.finalize_setup()

    def _setup_fun_numbers(self):
        entry_1_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
        entry_2_r = f'{randint(0, 10)} {randint(0, 10)} {randint(0, 10)}'
        self.x_entry.insert(END, entry_1_r)
        self.y_entry.insert(END, entry_2_r)

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

            plt.plot(x_values, y_values, marker=change_marker(self.marker_select.get(), 'graph'),
                     ms=self.change_dot_size(),
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
