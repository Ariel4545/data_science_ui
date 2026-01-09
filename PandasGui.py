import customtkinter
from customtkinter import *
import tkinter
from tkinter import filedialog, messagebox, ttk, simpledialog
import pandas, numpy, pyperclip, datetime
import matplotlib.pyplot as plt
import io


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
        
        self.history = []
        self.history_index = -1
        
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
        self.bind('<Control-z>', lambda e: self.undo())
        self.bind('<Control-y>', lambda e: self.redo())

    def clear(self):
        self.data.delete(*self.data.get_children())
        return

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
                
                self.history = []
                self.history_index = -1
                self.add_to_history(self.dataframe)
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
        self._apply_op('Clean Empty', lambda: self.dataframe.dropna())

    def clean_duplicates(self):
        self._apply_op('Clean Duplicates', lambda: self.dataframe.drop_duplicates())

    def info(self):
        if not self._require_data(): return
        buffer = io.StringIO()
        self.dataframe.info(buf=buffer)
        self.information_pop_msg(buffer.getvalue(), 'DataFrame Info')

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
                # Use _apply_op to handle history
                self._apply_op('Drop', lambda: self.dataframe.drop(columns=self.cul.get()))
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
        # self.update_data() # Handled by _apply_op

    def replace(self):
        def enter():
            try:
                self._apply_op('Replace', lambda: self.dataframe.replace(self.old_value.get(), self.new_value.get()))
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
                self._apply_op('Rename', lambda: self.dataframe.rename(columns={self.oldc_value.get() : self.newc_value.get()}))
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
        
        edit_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Undo', command=self.undo)
        edit_menu.add_command(label='Redo', command=self.redo)

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
        
        plotting_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='Plotting', menu=plotting_menu)
        plotting_menu.add_command(label='Histogram', command=lambda: self.plot('hist'))
        plotting_menu.add_command(label='Scatter', command=lambda: self.plot('scatter'))
        plotting_menu.add_command(label='Line', command=lambda: self.plot('line'))
        plotting_menu.add_command(label='Bar', command=lambda: self.plot('bar'))
        plotting_menu.add_command(label='Box', command=lambda: self.plot('box'))

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

    def _require_data(self) -> bool:
        """
        Ensure a DataFrame is loaded before proceeding.
        Returns True if data is available, otherwise shows an info popup and returns False.
        """
        if getattr(self, "dataframe", None) is None:
            try:
                self.information_pop_msg("No data loaded", "Please open a data file first.")
            except Exception:
                pass
            return False
        return True

    def _get_numeric_columns(self):
        """
        Returns a list of numeric column names in the current DataFrame.
        If there are no numeric columns, returns an empty list.
        """
        import numpy as _np  # local import to avoid top-level dependency impacts
        if not self._require_data():
            return []
        try:
            return list(self.dataframe.select_dtypes(include=[_np.number]).columns)
        except Exception:
            return []
            
    def _get_columns(self):
        if not self._require_data(): return []
        return list(self.dataframe.columns)

    def _apply_op(self, op_name: str, fn):
        """
        Unified mutation pipeline:
        - Checks that data is loaded
        - Executes the provided function (which should mutate or return a new DataFrame)
        - Assigns back if a new DataFrame is returned
        - Marks 'changed', increments 'upd_count', and calls update_data() once
        - Handles and reports errors uniformly
        """
        if not self._require_data():
            return
        try:
            result = fn()
            if result is not None:
                # allow functional style: return a new df
                new_df = result
            else:
                # If fn modified in place (which we try to avoid now), assume self.dataframe is new state
                # But for history, we need to be careful.
                # Ideally fn returns the new dataframe.
                new_df = self.dataframe

            self.add_to_history(new_df)
            self.dataframe = new_df
            
            # mark changed and update views exactly once
            self.changed = True
            self.upd_count += 1
            try:
                self.update_data()
            except Exception as e:
                # Surface update errors but keep the data change
                self.information_pop_msg(f"{op_name} - UI update failed", str(e))
            else:
                # Optional: lightweight success status (avoid modal spam)
                pass
        except Exception as e:
            try:
                self.information_pop_msg(f"{op_name} failed", str(e))
            except Exception:
                pass


    def _apply_numeric_unary(self, op_name: str, series_op):
        """
        Apply an element-wise Series -> Series operation to all numeric columns.
        """
        if not self._require_data():
            return
        cols = self._get_numeric_columns()
        if not cols:
            self.information_pop_msg(f"{op_name} - No numeric data", "No numeric columns found to apply operation.")
            return

        def _runner():
            df = self.dataframe.copy()
            # Operate only on a view of numeric columns to avoid dtype regressions on other columns
            for c in cols:
                # Each column individually to better surface column-specific errors
                try:
                    df[c] = series_op(df[c])
                except Exception as col_err:
                    # best-effort: continue on others, then raise aggregated info
                    raise type(col_err)(f"Column '{c}': {col_err}")
            return df  # in-place change; return for consistency

        self._apply_op(op_name, _runner)

    def _numeric_summary(self, op_name: str, reducer):
        """
        Compute a per-column numeric summary without mutating the DataFrame.
        Shows a popup with the results and stores them on matching attributes when present.
        """
        if not self._require_data():
            return

        import numpy as _np
        df = self.dataframe
        num_df = df.select_dtypes(include=[_np.number])
        if num_df.shape[1] == 0:
            self.information_pop_msg(f"{op_name} - No numeric data", "No numeric columns found to summarize.")
            return

        try:
            # reducer should return a Series indexed by column names
            result = reducer(num_df)
        except Exception as e:
            self.information_pop_msg(f"{op_name} failed", str(e))
            return

        # Persist on attribute if available (sum_ / min_ / max_ / mean_ / median_)
        # Store as dict for easier later use; also render nicely for popup.
        result_dict = {str(k): result[k] for k in result.index}
        attr_name = {
            "Sum": "sum_",
            "Min": "min_",
            "Max": "max_",
            "Mean": "mean_",
            "Median": "median_",
        }.get(op_name)
        if attr_name and hasattr(self, attr_name):
            try:
                setattr(self, attr_name, result_dict)
            except Exception:
                pass

        # Compose a readable message
        lines = [f"{op_name} per column (numeric only):"]
        for k in result.index:
            try:
                v = result[k]
                # Compact formatting for floats
                if isinstance(v, float):
                    lines.append(f"- {k}: {v:.6g}")
                else:
                    lines.append(f"- {k}: {v}")
            except Exception:
                lines.append(f"- {k}: <unavailable>")
        msg = "\n".join(lines)
        self.information_pop_msg(f"{op_name} result", msg)

    def sum(self):
        """
        Show column-wise sum for numeric columns without mutating the DataFrame.
        Previous behavior that could coerce/mutate is replaced with a safe summary.
        """
        self._numeric_summary("Sum", lambda df: df.sum(numeric_only=True))

    def min(self):
        """
        Show column-wise min for numeric columns without mutating the DataFrame.
        """
        self._numeric_summary("Min", lambda df: df.min(numeric_only=True))

    def max(self):
        """
        Show column-wise max for numeric columns without mutating the DataFrame.
        """
        self._numeric_summary("Max", lambda df: df.max(numeric_only=True))

    def mean(self):
        """
        Show column-wise mean for numeric columns without mutating the DataFrame.
        """
        self._numeric_summary("Mean", lambda df: df.mean(numeric_only=True))

    def median(self):
        """
        Show column-wise median for numeric columns without mutating the DataFrame.
        """
        self._numeric_summary("Median", lambda df: df.median(numeric_only=True))

    def abs(self):
        """
        Element-wise absolute value on numeric columns only.
        """
        # before: unguarded operation across all columns could raise or coerce incorrectly
        self._apply_numeric_unary("Absolute", lambda s: s.abs())

    def cumsum(self):
        """
        Element-wise cumulative sum on numeric columns only (skip NaN).
        """
        self._apply_numeric_unary("Cumulative sum", lambda s: s.cumsum(skipna=True))

    def pow(self):
        """
        Element-wise power on numeric columns only.
        Asks user for exponent.
        """
        try:
            val = simpledialog.askfloat('Power', 'Enter exponent:', initialvalue=2.0)
            if val is None:
                return
            exp = val
        except Exception:
            return

        self._apply_numeric_unary(f"Power (**{exp})", lambda s: s.pow(exp))

    def mode(self):
        """
        Show column-wise mode for numeric columns without mutating the DataFrame.
        """
        # Mode can return multiple rows, so we handle it slightly differently than _numeric_summary
        if not self._require_data():
            return
        
        import numpy as _np
        df = self.dataframe
        num_df = df.select_dtypes(include=[_np.number])
        if num_df.empty:
             self.information_pop_msg("Mode - No numeric data", "No numeric columns found.")
             return

        try:
            m = num_df.mode()
            # Format for display
            self.information_pop_msg("Mode result (numeric)", m.to_string())
        except Exception as e:
            self.information_pop_msg("Mode failed", str(e))

    def nunique(self):
        """
        Show column-wise unique count for numeric columns.
        """
        self._numeric_summary("Nunique", lambda df: df.nunique())
        
    def add_to_history(self, df):
        self.history = self.history[:self.history_index + 1]
        self.history.append(df.copy())
        self.history_index += 1

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.dataframe = self.history[self.history_index].copy()
            self.update_data()
            # self.status_bar.configure(text='Undo successful.') # No status bar in l1 yet
        else:
            pass
            # self.status_bar.configure(text='Nothing to undo.')

    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.dataframe = self.history[self.history_index].copy()
            self.update_data()
            # self.status_bar.configure(text='Redo successful.')
        else:
            pass
            # self.status_bar.configure(text='Nothing to redo.')
            
    def _ask_column(self, title, columns):
        dialog = CTkToplevel(self)
        dialog.title('Select Column')
        dialog.geometry('300x150')
        
        # Make dialog modal
        dialog.transient(self)
        dialog.grab_set()

        label = CTkLabel(dialog, text=title)
        label.pack(pady=10)

        col_var = tkinter.StringVar()
        combobox = CTkComboBox(dialog, values=columns, variable=col_var)
        combobox.pack(pady=5, padx=20, fill='x')
        if columns:
            combobox.set(columns[0])

        def on_ok():
            dialog.destroy()
        
        ok_button = CTkButton(dialog, text='OK', command=on_ok)
        ok_button.pack(pady=10)

        self.wait_window(dialog)
        return col_var.get()
        
    def plot(self, kind):
        if not self._require_data(): return
        numeric_cols = self._get_numeric_columns()
        all_cols = self._get_columns()

        if kind in ['hist', 'box']:
            if not numeric_cols:
                messagebox.showinfo('No Numeric Data', f'No numeric columns available for a {kind} plot.')
                return
            col = self._ask_column(f'Select column for {kind} plot:', numeric_cols)
            if not col: return
            try:
                plt.figure(f'{kind.title()} Plot of {col}')
                self.dataframe[col].plot(kind=kind, title=f'{kind.title()} Plot of {col}')
                plt.xlabel(col)
                if kind == 'hist': plt.ylabel('Frequency')
                plt.grid(True)
                plt.show()
            except Exception as e:
                messagebox.showerror('Plotting Error', str(e))

        elif kind in ['line', 'bar']:
            x_col = self._ask_column('Select column for X-axis:', all_cols)
            if not x_col: return
            y_col = self._ask_column('Select column for Y-axis:', numeric_cols)
            if not y_col: return
            try:
                plt.figure(f'{kind.title()} Plot: {y_col} vs {x_col}')
                self.dataframe.plot(kind=kind, x=x_col, y=y_col, title=f'{y_col} vs {x_col}')
                plt.grid(True)
                plt.show()
            except Exception as e:
                messagebox.showerror('Plotting Error', str(e))

        elif kind == 'scatter':
            if len(numeric_cols) < 2:
                messagebox.showinfo('Not Enough Data', 'You need at least two numeric columns for a scatter plot.')
                return
            x_col = self._ask_column('Select column for X-axis:', numeric_cols)
            if not x_col: return
            y_col = self._ask_column('Select column for Y-axis:', numeric_cols)
            if not y_col: return
            try:
                plt.figure(f'Scatter: {y_col} vs {x_col}')
                self.dataframe.plot(kind='scatter', x=x_col, y=y_col, title=f'{y_col} vs {x_col}')
                plt.grid(True)
                plt.show()
            except Exception as e:
                messagebox.showerror('Plotting Error', str(e))

    # ---------- Non-shadowing convenience wrappers (backward compatible) ----------

    def compute_sum(self):
        """Non-shadowing wrapper around sum()."""
        return self.sum()

    def compute_min(self):
        """Non-shadowing wrapper around min()."""
        return self.min()

    def compute_max(self):
        """Non-shadowing wrapper around max()."""
        return self.max()

    def compute_mean(self):
        """Non-shadowing wrapper around mean()."""
        return self.mean()

    def compute_median(self):
        """Non-shadowing wrapper around median()."""
        return self.median()

    def compute_abs(self):
        """Non-shadowing wrapper around abs()."""
        return self.abs()

    def compute_pow(self):
        """Non-shadowing wrapper around pow()."""
        return self.pow()

    def compute_mode(self):
        """Non-shadowing wrapper around mode()."""
        return self.mode()

    def compute_nunique(self):
        """Non-shadowing wrapper around nunique()."""
        return self.nunique()

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
