from customtkinter import *
import tkinter
from tkinter import filedialog, messagebox, ttk
import pandas, numpy


class Window(CTk):
    width = 340
    height = 430
    b_height = 3
    b_width = 6
    def __init__(self):
        super().__init__()
        self.geometry(f'{self.width}x{self.height}')
        self.title('PandasGui')
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.minsize(340, 430)
        self.maxsize(1000, 630)

        self.buttons_frame = CTkFrame(self)
        self.open_file = CTkButton(self.buttons_frame, text='open file', command=self.open, height=self.b_height, width=self.b_width)
        self.save_file = CTkButton(self.buttons_frame, text='save file', command=self.save, state=DISABLED, height=self.b_height, width=self.b_width)
        self.clean_m = CTkButton(self.buttons_frame, text='Clean empty', command=self.clean_empty, state=DISABLED, height=self.b_height, width=self.b_width)
        self.clean_d = CTkButton(self.buttons_frame, text='Clean duplicates', command=self.clean_duplicates, state=DISABLED, height=self.b_height, width=self.b_width)
        self.info_ = CTkButton(self.buttons_frame, text='Information ', command=self.info, state=DISABLED, height=self.b_height, width=self.b_width)
        self.desc_ = CTkButton(self.buttons_frame, text='Describe ', command=self.describe, state=DISABLED, height=self.b_height, width=self.b_width)
        self.delete_ = CTkButton(self.buttons_frame, text='Drop ', command=self.delete, state=DISABLED, height=self.b_height, width=self.b_width)
        self.replace_ = CTkButton(self.buttons_frame, text='Replace ', command=self.replace, state=DISABLED, height=self.b_height, width=self.b_width)
        self.buttons_frame.pack(side=tkinter.BOTTOM)
        self.open_file.grid(row=6, column=0, padx=3)
        self.save_file.grid(row=6, column=1)
        self.info_.grid(row=6, column=2)
        self.clean_m.grid(row=5, column=0, padx=3)
        self.clean_d.grid(row=5, column=2)
        self.desc_.grid(row=4, column=0)
        self.delete_.grid(row=4, column=1)
        self.replace_.grid(row=4, column=2)

        pandas.options.display.max_rows = 9999

    def clear(self):
        self.data.delete(*self.data.get_children())

    def open(self):

        self.file_name = filedialog.askopenfilename(filetypes=(('CSV Files', '*.csv'), ('JSON FILES', '*.json'),
                                                               ('EXCEL Files', '*.xlsx')))
        # suffix = re.sub((r"(?:csv)$"))
        if self.file_name:
            try:
                if self.file_name.endswith('csv'):
                    self.content = pandas.read_csv(self.file_name)
                    self.suffix = '.csv'
                elif self.file_name.endswith('json'):
                    self.suffix = '.json'
                    self.content = pandas.read_json(self.file_name)
                elif self.file_name.endswith('xlsx'):
                    self.content = pandas.read_excel(self.file_name)
                    self.suffix = '.xlsx'
            except ValueError:
                tkinter.messagebox.showerror('file could not be open!')
            except FileNotFoundError:
                tkinter.messagebox.showerror('file could not be found!')


            self.update_data()

            # self.data.configure(state=DISABLED)

            self.save_file.configure(state=ACTIVE)
            self.clean_m.configure(state=ACTIVE)
            self.clean_d.configure(state=ACTIVE)
            self.info_.configure(state=ACTIVE)
            self.desc_.configure(state=ACTIVE)
            self.delete_.configure(state=ACTIVE)
            self.replace_.configure(state=ACTIVE)

    def save(self):
        if not (messagebox.askyesno('PandasGui', 'Would you like to replace the old data frame?')):
            self.save_file = filedialog.asksaveasfile(defaultextension=((f'{self.suffix}')))
            if self.save_file:
                save = open(self.save_file.name, 'w')
                save.write(self.content.to_string())
                save.close()
        else:
            save = open(self.file_name, 'w')
            save.write(self.content.to_string())
            save.close()

    def update_data(self):

        self.data_frame = CTkFrame(self)
        self.data_frame.pack(side=RIGHT, fill=Y)
        self.scroll = tkinter.Scrollbar(self.data_frame)
        self.scroll.pack(side=RIGHT, fill=Y)
        # self.data = tkinter.Text(self.data_frame, yscrollcommand=self.scroll, background='black',
        #                          foreground='green', font='arial 10')
        # self.data.insert('1.0', self.content)

        self.data = ttk.Treeview(self, yscrollcommand=self.scroll.set)


        self.clear()

        self.data['column'] = list(self.content.columns)
        self.data['show'] = 'headings'
        for cul in self.data['column']:
            self.data.heading(cul, text=cul)
        content_rows = self.content.to_numpy().tolist()
        for row in content_rows:
            self.data.insert('', 'end', values=row)

        self.data.focus_set()
        self.data.pack(fill=BOTH, expand=True)
        self.scroll.config(command=self.data.yview)

        # self.cul = []
        # for index in range(len(self.content)):
        #     pass
        #     self.cul.append((self.content.iloc[index]))
        # self.cul = tuple(self.cul[0])


    def clean_empty(self):
        self.content.dropna(inplace=True)
        self.update_data()

    def clean_duplicates(self):
        self.content.drop_duplicates(inplace=True)
        self.update_data()

    def info(self):
        # info_root = tkinter.Toplevel()
        # info_root.title('PandasGui df-info')
        information = self.content.info()
        # info_label = CTkLabel(info_root, text=information)
        # info_label.pack()

    def describe(self):
        des_root = CTkToplevel()
        des_root.title('PandasGui - D.F description')
        self.description = self.content.describe()
        des = CTkLabel(des_root, text=self.description)
        des.pack(expand=True)
        #des_root.resizable(False, False)

    def delete(self):
        def enter():
            try:
                self.content.drop(columns=self.cul.get(), inplace=True)
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
                self.content.replace(self.old_value.get(), self.new_value.get())
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

    def on_close(self):
        self.destroy()


if __name__ == '__main__':
    App = Window()
    set_appearance_mode('dark')
    App.mainloop()
