from customtkinter import *
import tkinter
from tkinter import filedialog, messagebox
import pandas


class Window(CTk):
    width = 340
    height = 430

    def __init__(self):
        super().__init__()
        self.geometry(f'{self.width}x{self.height}')
        self.title('PandasGui')
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.minsize(340, 430)
        self.maxsize(440, 630)

        self.open_file = CTkButton(self, text='open file', command=self.open)
        self.save_file = CTkButton(self, text='save file', command=self.save, state=DISABLED)
        self.clean_m = CTkButton(self, text='Clean empty', command=self.clean_empty, state=DISABLED)
        self.clean_d = CTkButton(self, text='Clean duplicates', command=self.clean_duplicates, state=DISABLED)
        self.info_ = CTkButton(self, text='Information ', command=self.info, state=DISABLED)
        self.open_file.pack(side=tkinter.BOTTOM)
        self.save_file.pack(side=tkinter.BOTTOM)
        self.clean_m.pack(side=tkinter.BOTTOM)
        self.clean_d.pack(side=tkinter.BOTTOM)
        self.info_.pack(side=tkinter.BOTTOM)

        pandas.options.display.max_rows = 9999

    def open(self):
        self.file_name = filedialog.askopenfilename(filetypes=(('CSV Files', '*.csv'), ('JSON FILES', '*.json'),
                                                               ('EXCEL Files', '*.xlsx')))
        # suffix = re.sub((r"(?:csv)$"))
        if self.file_name:
            if self.file_name.endswith('csv'):
                self.content = pandas.read_csv(self.file_name)
                self.suffix = '.csv'
            elif self.file_name.endswith('json'):
                self.suffix = '.json'
                self.content = pandas.read_json(self.file_name)
            elif self.file_name.endswith('xlsx'):
                self.content = pandas.read_excel(self.file_name)
                self.suffix = '.xlsx'

            self.data_frame = CTkFrame(self)
            self.scroll = tkinter.Scrollbar(self.data_frame)
            self.scroll.pack(side=RIGHT, fill=Y)
            self.data = tkinter.Text(self.data_frame, yscrollcommand=self.scroll, background='black', foreground='green')
            self.data.insert('1.0', self.content)
            self.data_frame.pack(side=tkinter.TOP)
            self.scroll.config(command=self.data.yview)
            self.data.pack(expand=True, fill=BOTH)

            self.data.configure(state=DISABLED)

            self.save_file.configure(state=ACTIVE)
            self.clean_m.configure(state=ACTIVE)
            self.clean_d.configure(state=ACTIVE)
            self.info_.configure(state=ACTIVE)

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
        self.data.delete('1.0', 'end')
        self.data.insert('1.0', self.content)

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

    def on_close(self):
        self.destroy()


if __name__ == '__main__':
    App = Window()
    App.mainloop()
