import customtkinter
from customtkinter import *
import tkinter
from tkinter import filedialog, messagebox, ttk, simpledialog
import pandas, numpy, pyperclip, datetime
import matplotlib.pyplot as plt


class Window(CTk):
    app_width = 340
    app_height = 500
    b_height = 3
    b_width = 3
    def __init__(self):
        super().__init__()
        self.geometry(f'{self.app_width}x{self.app_height}')
        self.title('PandasGui')
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.minsize(340, 430)
        self.menu()
        self.changed = False
        self.upd_count = 0
        pandas.options.display.max_rows = 9999

        # for settings!

        self.buttons_frame = CTkFrame(self)
        self.open_file = CTkButton(self.buttons_frame, text='open file', command=self.open, height=self.b_height,
                                   width=self.b_width)
        self.save_file = CTkButton(self.buttons_frame, text='save file', command=self.save, state=DISABLED,
                                   height=self.b_height, width=self.b_width)
        self.clean_m = CTkButton(self.buttons_frame, text='Clean empty', command=self.clean_empty, state=DISABLED,
                                 height=self.b_height, width=self.b_width)
        self.clean_d = CTkButton(self.buttons_frame, text='Clean duplicates', command=self.clean_duplicates,
                                 state=DISABLED, height=self.b_height, width=self.b_width)
        self.info_ = CTkButton(self.buttons_frame, text='Information ', command=self.info, state=DISABLED,
                               height=self.b_height, width=self.b_width)
        self.desc_ = CTkButton(self.buttons_frame, text='Describe ', command=self.describe, state=DISABLED,
                               height=self.b_height, width=self.b_width)
        self.delete_ = CTkButton(self.buttons_frame, text='Drop ', command=self.delete, state=DISABLED,
                                 height=self.b_height, width=self.b_width)
        self.replace_ = CTkButton(self.buttons_frame, text='Replace ', command=self.replace, state=DISABLED,
                                  height=self.b_height, width=self.b_width)
        self.abs_ = CTkButton(self.buttons_frame, text='Abs ', command=self.abs, state=DISABLED,
                              height=self.b_height, width=self.b_width)
        self.pow_ = CTkButton(self.buttons_frame, text='Pow ', command=self.pow, state=DISABLED,
                              height=self.b_height, width=self.b_width)
        self.mode_ = CTkButton(self.buttons_frame, text='Mode ', command=self.mode, state=DISABLED,
                               height=self.b_height, width=self.b_width)
        # count , sum, mean, median, min max
        self.count_ = CTkButton(self.buttons_frame, text='Count', command=self.count, state=DISABLED,
                                height=self.b_height, width=self.b_width)
        self.sum_ = CTkButton(self.buttons_frame, text='Sum', command=self.sum, state=DISABLED, height=self.b_height,
                              width=self.b_width)
        self.mean_ = CTkButton(self.buttons_frame, text='Mean', command=self.mean, state=DISABLED, height=self.b_height,
                               width=self.b_width)
        self.median_ = CTkButton(self.buttons_frame, text='Median', command=self.median, state=DISABLED,
                                 height=self.b_height, width=self.b_width)
        self.min_ = CTkButton(self.buttons_frame, text='Min', command=self.min, state=DISABLED, height=self.b_height,
                              width=self.b_width)
        self.max_ = CTkButton(self.buttons_frame, text='Max', command=self.max, state=DISABLED, height=self.b_height,
                              width=self.b_width)
        self.rename_ = CTkButton(self.buttons_frame, text='Rename', command=self.rename, state=DISABLED, height=self.b_height,
                              width=self.b_width)
        self.nunique_ = CTkButton(self.buttons_frame, text='Nunique', command=self.nunique, state=DISABLED, height=self.b_height,
                              width=self.b_width)
        self.cumsum_ = CTkButton(self.buttons_frame, text='Cumsum', command=self.cumsum, state=DISABLED, height=self.b_height,
                              width=self.b_width)

        self.bind("<Control-o>", self.open), self.bind("<Control-O>", self.open)

    def clear(self):
        self.data.delete(*self.data.get_children())

    def open(self):
        def file_by(via):
            global fb
            if via == 'f':
                fb = 'file'
            else:
                fb = 'link'
            question_box.destroy()
            open_()
        question_box = CTkToplevel()
        question_box.title('File by')
        question_title = CTkLabel(question_box, text='What is the preferred way to open the file by')
        by_file = CTkButton(question_box, text='By (local) file', command=lambda: file_by('f'))
        by_link = CTkButton(question_box, text='By link', command=lambda: file_by('l'))
        question_title.grid(row=0, column=1)
        by_file.grid(row=1, column=0)
        by_link.grid(row=1, column=2)

        def open_():
            if fb == 'file':
                self.file_name = filedialog.askopenfilename(filetypes=(('CSV Files', '*.csv'), ('JSON FILES', '*.json'),
                                                                   ('EXCEL Files', '*.xlsx')))
            else:
                self.file_name = simpledialog.askstring('File link', 'enter the file link')
            # suffix = re.sub((r"(?:csv)$"))

            if self.file_name:
                try:
                    if self.file_name.endswith('csv'):
                        self.dataframe = pandas.read_csv(self.file_name)
                        self.suffix = '.csv'
                    elif self.file_name.endswith('json'):
                        self.suffix = '.json'
                        self.dataframe = pandas.read_json(self.file_name)
                    elif self.file_name.endswith('xlsx'):
                        self.dataframe = pandas.read_excel(self.file_name)
                        self.suffix = '.xlsx'
                except ValueError:
                    tkinter.messagebox.showerror('file could not be open!')
                except FileNotFoundError:
                    tkinter.messagebox.showerror('file could not be found!')

                # self.dataframe.plot()
                # plt.show()
                # self.data.configure(state=DISABLED)

                self.save_file.configure(state=ACTIVE), self.clean_m.configure(state=ACTIVE)
                self.clean_d.configure(state=ACTIVE), self.info_.configure(state=ACTIVE)
                self.desc_.configure(state=ACTIVE), self.delete_.configure(state=ACTIVE)
                self.replace_.configure(state=ACTIVE), self.count_.configure(state=ACTIVE)
                self.sum_.configure(state=ACTIVE), self.mean_.configure(state=ACTIVE)
                self.median_.configure(state=ACTIVE), self.min_.configure(state=ACTIVE)
                self.max_.configure(state=ACTIVE), self.abs_.configure(state=ACTIVE), self.pow_.configure(state=ACTIVE)
                self.mode_.configure(state=ACTIVE), self.rename_.configure(state=ACTIVE)
                self.nunique_.configure(state=ACTIVE), self.cumsum_.configure(state=ACTIVE)

                self.bind('<Control-Key-s>', self.save), self.bind('<Control-Key-S>', self.save)

                self.update_data()


    def save(self):
        if not (messagebox.askyesno('PandasGui', 'Would you like to replace the old data frame?')):
            self.save_file = filedialog.asksaveasfile(defaultextension=((f'{self.suffix}')))
            if self.save_file:
                save = open(self.save_file.name, 'w')
                save.write(self.dataframe.to_string())
                save.close()
        else:
            save = open(self.file_name, 'w')
            save.write(self.dataframe.to_string())
            save.close()

    def update_data(self):

        self.data_frame = CTkFrame(self)
        self.data_frame.pack(side=RIGHT, fill=Y)
        self.scroll = tkinter.Scrollbar(self.data_frame)
        self.scroll.pack(side=RIGHT, fill=Y)
        # self.data = tkinter.Text(self.data_frame, yscrollcommand=self.scroll, background='black',
        #                          foreground='green', font='arial 10')
        # self.data.insert('1.0', self.dataframe)

        self.data = ttk.Treeview(self, yscrollcommand=self.scroll.set)


        self.clear()

        self.data['column'] = list(self.dataframe.columns)
        self.data['show'] = 'headings'
        for cul in self.data['column']:
            self.data.heading(cul, text=cul)
        content_rows = self.dataframe.to_numpy().tolist()
        for row in content_rows:
            self.data.insert('', 'end', values=row)

        self.data.focus_set()
        self.data.pack(fill=BOTH, expand=True)
        self.scroll.config(command=self.data.yview)

        # self.cul = []
        # for index in range(len(self.dataframe)):
        #     pass
        #     self.cul.append((self.dataframe.iloc[index]))
        # self.cul = tuple(self.cul[0])

        self.upd_count += 1
        if self.upd_count >= 2:
            self.changed = True

    def clean_empty(self):
        self.dataframe.dropna(inplace=True)
        self.update_data()

    def clean_duplicates(self):
        self.dataframe.drop_duplicates(inplace=True)
        self.update_data()

    def info(self):
        # info_root = tkinter.Toplevel()
        # info_root.title('PandasGui df-info')
        information = self.dataframe.info()
        # info_label = CTkLabel(info_root, text=information)
        # info_label.pack()

    def describe(self):
        des_root = CTkToplevel()
        des_root.title('PandasGui - D.F description')
        self.description = self.dataframe.describe()
        des = CTkLabel(des_root, text=self.description)
        des.pack(expand=True)
        #des_root.resizable(False, False)

    def delete(self):
        def enter():
            try:
                self.dataframe.drop(columns=self.cul.get(), inplace=True)
            except KeyError:
                tkinter.messagebox.showerror('PandasGui', f'"{self.cul.get()}" was not found')
        drop_root = CTkToplevel()
        drop_root.title('PandasGui - drop')
        cul_title = CTkLabel(drop_root, text='Column')
        row_title = CTkLabel(drop_root, text='Row')
        self.cul = CTkEntry(drop_root)
        self.row = CTkEntry(drop_root, state=DISABLED)
        enter_button = CTkButton(drop_root, text='Enter', command=enter)
        cul_title.grid(row=0, column=0)
        row_title.grid(row=0, column=2)
        self.cul.grid(row=1, column=0)
        self.row.grid(row=1, column=2)
        enter_button.grid(row=2, column=1)

        #drop_root.resizable(False, False)
        self.update_data()

    def replace(self):
        def enter():
            try:
                self.dataframe.replace(self.old_value.get(), self.new_value.get())
            except KeyError:
                tkinter.messagebox.showerror('PandasGui', f'"{self.old_value.get()}" was not found')

        replace_root = CTkToplevel()
        replace_root.title('PandasGui - replace')
        oldv_title = CTkLabel(replace_root, text='Existing value')
        newv_title = CTkLabel(replace_root, text='New value')
        self.old_value = CTkEntry(replace_root)
        self.new_value = CTkEntry(replace_root)
        enter_button = CTkButton(replace_root, text='Enter', command=enter)
        oldv_title.grid(row=0, column=0)
        newv_title.grid(row=0, column=2)
        self.old_value.grid(row=1, column=0)
        self.new_value.grid(row=1, column=2)
        enter_button.grid(row=2, column=1)

    def rename(self):
        def enter():
            try:
                self.dataframe.rename(columns={self.oldc_value.get() : self.newc_value.get()})
            except KeyError:
                tkinter.messagebox.showerror('PandasGui', f'"{self.oldc_value.get()}" was not found')

        rename_root = CTkToplevel()
        rename_root.title('PandasGui - rename')
        oldv_title = CTkLabel(rename_root, text='Existing column name')
        newv_title = CTkLabel(rename_root, text='New column name')
        self.oldc_value = CTkEntry(rename_root)
        self.newc_value = CTkEntry(rename_root)
        enter_button = CTkButton(rename_root, text='Enter', command=enter)
        oldv_title.grid(row=0, column=0)
        newv_title.grid(row=0, column=2)
        self.oldc_value.grid(row=1, column=0)
        self.newc_value.grid(row=1, column=2)
        enter_button.grid(row=2, column=1)

    def count(self):
        count_info = self.dataframe.count()
        self.information_pop_msg(count_info, 'count')

    def sum(self):
        sum_info = self.dataframe.sum()
        self.information_pop_msg(sum_info, 'sum')

    def min(self):
        min_info = self.dataframe.min()
        self.information_pop_msg(min_info, 'min')

    def max(self):
        max_info = self.dataframe.max()
        self.information_pop_msg(max_info, 'max')

    def mean(self):
        mean_info = self.dataframe.mean()
        self.information_pop_msg(mean_info, 'mean')

    def median(self):
        median_info = self.dataframe.median()
        self.information_pop_msg(median_info, 'median')

    def abs(self):
        try:
            abs_info = self.dataframe.astype(int).abs()
            self.information_pop_msg(abs_info, 'abs')
        except:
            messagebox.showerror('error', 'enable to convert data frame to integer')

    def pow(self):
        try:
            pow_num = tkinter.simpledialog.askinteger('pow', 'please enter the amount of pow')
            pow_info = self.dataframe.pow(pow_num)
            self.information_pop_msg(pow_info, 'pow')
        except:
            messagebox.showerror('error', 'enable to convert data frame to integer')

    def mode(self):
        mode_info = self.dataframe.mode()
        self.information_pop_msg(mode_info, 'mode')

    def nunique(self):
        nun_info = self.dataframe.nunique()
        self.information_pop_msg(nun_info, 'nunique')

    def cumsum(self):
        cumsum_info = self.dataframe.cumsum()
        self.information_pop_msg(cumsum_info, 'cumsum')

    def information_pop_msg(self, result, operation_name):
        result_root = tkinter.Toplevel()
        time = datetime.datetime.now().strftime('%H:%M:%S')
        result_root.title(f'{operation_name} - {time}')
        result_output = CTkLabel(result_root, text=f'{result}', fg_color='black')
        copy_button = CTkButton(result_root, text='Copy', command=lambda: pyperclip.copy(str(result)), width=10)
        result_output.pack()
        copy_button.pack()

    def menu(self):
        self.menu_ = tkinter.Menu(self)
        self.config(menu=self.menu_)

        file_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open', command=self.open)
        file_menu.add_command(label='Save', command=self.save)

        statistics_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='Statistics', menu=statistics_menu)
        statistics_menu.add_command(label='Mode', command=self.mode)
        statistics_menu.add_command(label='Median', command=self.median)
        statistics_menu.add_command(label='Mean', command=self.mean)
        statistics_menu.add_command(label='Min', command=self.min)
        statistics_menu.add_command(label='Max', command=self.max)
        statistics_menu.add_command(label='Cumsum', command=self.cumsum)

        arithmetic_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='Arithmetics', menu=arithmetic_menu)
        arithmetic_menu.add_command(label='Sum', command=self.sum)
        arithmetic_menu.add_command(label='Pow', command=self.pow)
        arithmetic_menu.add_command(label='Abs', command=self.abs)

        cleaning_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='Cleaning', menu=cleaning_menu)
        cleaning_menu.add_command(label='Clean empty', command=self.clean_empty)
        cleaning_menu.add_command(label='Cleaning duplicates', command=self.clean_duplicates)
        cleaning_menu.add_command(label='Delete', command=self.delete)

        other_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='Other', menu=other_menu)
        other_menu.add_command(label='Replace', command=self.replace)
        other_menu.add_command(label='Info', command=self.info)
        other_menu.add_command(label='Describe', command=self.describe)
        other_menu.add_command(label='Count', command=self.describe)
        other_menu.add_command(label='Rename columns', command=self.rename)
        other_menu.add_command(label='nunique', command=self.nunique)

        self.menu_.add_cascade(label='Settings', command=self.settings)

    def settings(self):

        def buttons_grid():
            self.menu_.destroy()
            self.buttons_frame.pack(side=tkinter.BOTTOM, fill=X)
            self.open_file.grid(row=6, column=0, columnspan=1, padx=35, pady=2)
            self.save_file.grid(row=6, column=1, columnspan=1)
            self.info_.grid(row=6, column=2, columnspan=1)
            self.clean_m.grid(row=5, column=0, columnspan=1, pady=2)
            self.clean_d.grid(row=5, column=2, columnspan=1)
            self.desc_.grid(row=4, column=0, columnspan=1, pady=2)
            self.delete_.grid(row=4, column=1, columnspan=1)
            self.replace_.grid(row=4, column=2, columnspan=1)
            self.count_.grid(row=3, column=0, columnspan=1, pady=2)
            self.sum_.grid(row=3, column=1, columnspan=1)
            self.mean_.grid(row=3, column=2, columnspan=1)
            self.median_.grid(row=2, column=0, columnspan=1, pady=2)
            self.min_.grid(row=2, column=1, columnspan=1)
            self.max_.grid(row=2, column=2, columnspan=1)
            self.abs_.grid(row=1, column=0, columnspan=1, pady=2)
            self.pow_.grid(row=1, column=1, columnspan=1)
            self.mode_.grid(row=1, column=2, columnspan=1)
            self.rename_.grid(row=0, column=0, columnspan=1)
            self.nunique_.grid(row=0, column=1, columnspan=1)
            self.cumsum_.grid(row=0, column=2, columnspan=1)

            # self.open_file.pack(side=tkinter.LEFT)
            # self.save_file.pack(side=tkinter.LEFT)
            # self.info_.pack(side=tkinter.LEFT)
            # self.clean_m.pack(side=tkinter.LEFT)
            # self.clean_d.pack(side=tkinter.LEFT)
            # self.desc_.pack()

        def menus_():
            self.buttons_frame.pack_forget()
            self.menu()

        def dark_theme():
            customtkinter.set_appearance_mode('dark')

        def light_theme():
            customtkinter.set_appearance_mode('light')

        root = CTkToplevel()
        root.title('Settings')

        ui_style_title = CTkLabel(root, text='preferred UI')
        buttons_ui_button = CTkButton(root, text='By buttons', command=buttons_grid)
        menus_ui_button = CTkButton(root, text='By menus', command=menus_)

        themes_title = CTkLabel(root, text='preferred theme')
        dark_mode_button = CTkButton(root, text='Dark mode', command=dark_theme)
        light_mode_button = CTkButton(root, text='Light mode', command=light_theme)

        ui_style_title.grid(row=1, column=1)
        buttons_ui_button.grid(row=2, column=0)
        menus_ui_button.grid(row=2, column=2)
        themes_title.grid(row=3, column=1)
        dark_mode_button.grid(row=4, column=0)
        light_mode_button.grid(row=4, column=2)

    def on_close(self):
        if self.changed:
            if messagebox.askyesno('PandasGui', 'there is some unsaved progress are you sure you want to quit'):
                self.destroy()
        else:
            self.destroy()


if __name__ == '__main__':
    App = Window()
    set_appearance_mode('dark')
    App.mainloop()
