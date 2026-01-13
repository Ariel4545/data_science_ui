import customtkinter
from customtkinter import *
import tkinter
from tkinter import filedialog, messagebox, ttk, simpledialog
import pandas, numpy, pyperclip, datetime
import matplotlib.pyplot as plt
import io
import json
import os
import threading

# Try importing optional dependencies for stats/ML
try:
    from scipy.stats import ttest_ind, chi2_contingency
except ImportError:
    ttest_ind, chi2_contingency = None, None

try:
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
except ImportError:
    LinearRegression, StandardScaler, OneHotEncoder = None, None, None


class StateManager:
    """Handles persistent state management for the application."""
    def __init__(self, filename="pandagui_state.json"):
        self.filename = filename
        self.default_state = {
            "view_mode": "Tabs",  # Options: "Tabs", "Phone", "MenuOnly"
            "show_menu": True,
            "theme": "Dark",
            "geometry": "900x600",
            "file_open_mode": "Dialog", # Options: "Dialog", "Buttons"
            "font_size": "Medium" # Options: "Small", "Medium", "Large"
        }
        self.state = self.default_state.copy()
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    self.state.update(data)
            except Exception as e:
                print(f"Failed to load state: {e}")

    def save(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self.state, f)
        except Exception as e:
            print(f"Failed to save state: {e}")

    def get(self, key):
        return self.state.get(key, self.default_state.get(key))

    def set(self, key, value):
        self.state[key] = value
        self.save()


class Window(CTk):
    def __init__(self):
        super().__init__()
        self.state_manager = StateManager()
        
        self.title('PandasGui')
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.minsize(340, 430)

        # Grid configuration
        self.grid_columnconfigure(0, weight=0)  # Sidebar/Tabs column
        self.grid_columnconfigure(1, weight=1)  # Data column
        self.grid_rowconfigure(0, weight=1)     # Data row
        self.grid_rowconfigure(1, weight=0)     # Phone layout row

        self.history = []
        self.history_index = -1
        self.changed = False
        self.upd_count = 0
        pandas.options.display.max_rows = 9999

        # Initialize UI components
        self.setup_menu()
        self.setup_tabs()
        self.setup_phone_layout()
        self.setup_data_view()

        # Apply initial state (Theme and Font Scaling FIRST)
        self.set_theme(self.state_manager.get("theme"))
        self.apply_font_scaling(self.state_manager.get("font_size"))
        self.update_view_mode()
        
        # Restore geometry AFTER scaling to prevent inflation
        # We use after_idle to ensure the window is ready to accept geometry
        self.after_idle(lambda: self.geometry(self.state_manager.get("geometry")))

        # Bindings
        self.bind("<Control-o>", lambda e: self.handle_open_command())
        self.bind("<Control-O>", lambda e: self.handle_open_command())
        self.bind('<Control-z>', lambda e: self.undo())
        self.bind('<Control-y>', lambda e: self.redo())
        self.bind('<Control-s>', lambda e: self.save())
        self.bind('<Control-S>', lambda e: self.save()) # Restored Shift+S binding

    def setup_data_view(self):
        self.data_frame = CTkFrame(self)
        # Grid position will be managed by update_view_mode
        
        self.data_frame.grid_columnconfigure(0, weight=1)
        self.data_frame.grid_rowconfigure(0, weight=1)

        self.scroll_y = tkinter.Scrollbar(self.data_frame, orient="vertical")
        self.scroll_x = tkinter.Scrollbar(self.data_frame, orient="horizontal")
        
        self.data = ttk.Treeview(self.data_frame, yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        
        self.scroll_y.config(command=self.data.yview)
        self.scroll_x.config(command=self.data.xview)
        
        self.data.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.data.heading("#0", text="No Data Loaded")

    def setup_tabs(self):
        self.tab_view = CTkTabview(self, width=250)
        # Grid position managed by update_view_mode
        
        self.tabs = {
            "File": self.create_file_tab,
            "Edit": self.create_edit_tab,
            "Stats": self.create_stats_tab,
            "Cleaning": self.create_cleaning_tab,
            "Plotting": self.create_plotting_tab,
            "ML": self.create_ml_tab
        }

        for name, creator in self.tabs.items():
            self.tab_view.add(name)
            creator(self.tab_view.tab(name))

    def setup_phone_layout(self):
        # Use a scrollable frame for the phone layout to make it slimmer/scrollable
        self.phone_frame = CTkScrollableFrame(self, height=200, orientation="vertical")
        # Grid position managed by update_view_mode
        
        # Configure grid for phone layout (3 columns)
        for i in range(3):
            self.phone_frame.grid_columnconfigure(i, weight=1)
        
        self.phone_buttons = {}
        
        layout = [
            (6, 0, 'Open', self.handle_open_command), (6, 1, 'Save', self.save), (6, 2, 'Info', self.info),
            (5, 0, 'Clean Empty', self.clean_empty), (5, 2, 'Clean Dups', self.clean_duplicates),
            (4, 0, 'Describe', self.describe), (4, 1, 'Drop', self.delete), (4, 2, 'Replace', self.replace),
            (3, 0, 'Count', self.count), (3, 1, 'Sum', self.sum), (3, 2, 'Mean', self.mean),
            (2, 0, 'Median', self.median), (2, 1, 'Min', self.min), (2, 2, 'Max', self.max),
            (1, 0, 'Abs', self.abs), (1, 1, 'Pow', self.pow), (1, 2, 'Mode', self.mode),
            (0, 0, 'Rename', self.rename), (0, 1, 'Nunique', self.nunique), (0, 2, 'Cumsum', self.cumsum)
        ]
        
        for r, c, text, cmd in layout:
            # Use threading for potentially heavy operations to prevent freezing
            if cmd in [self.save, self.info, self.describe, self.count, self.sum, self.mean, self.median, self.min, self.max, self.abs, self.pow, self.mode, self.nunique, self.cumsum]:
                 command = lambda c=cmd: self.run_async(c)
            else:
                 command = cmd

            btn = CTkButton(self.phone_frame, text=text, command=command, height=32)
            btn.grid(row=r, column=c, padx=2, pady=2, sticky="ew")
            self.phone_buttons[text] = btn

    def create_file_tab(self, parent):
        # Dynamic File Opening Buttons
        self.file_buttons_frame = CTkFrame(parent, fg_color="transparent")
        self.file_buttons_frame.pack(pady=5, fill="x")
        self.update_file_buttons()

        self.btn_save = CTkButton(parent, text="Save File", command=lambda: self.run_async(self.save), state=DISABLED)
        self.btn_save.pack(pady=5, fill="x")
        self.btn_info = CTkButton(parent, text="Info", command=lambda: self.run_async(self.info), state=DISABLED)
        self.btn_info.pack(pady=5, fill="x")
        self.btn_desc = CTkButton(parent, text="Describe", command=lambda: self.run_async(self.describe), state=DISABLED)
        self.btn_desc.pack(pady=5, fill="x")

    def update_file_buttons(self):
        # Clear existing
        for widget in self.file_buttons_frame.winfo_children():
            widget.destroy()

        mode = self.state_manager.get("file_open_mode")
        if mode == "Dialog":
            CTkButton(self.file_buttons_frame, text="Open...", command=self.open_dialog).pack(fill="x")
        else:
            CTkButton(self.file_buttons_frame, text="Open File", command=self.open_file).pack(pady=2, fill="x")
            CTkButton(self.file_buttons_frame, text="Open Link", command=self.open_link).pack(pady=2, fill="x")

    def create_edit_tab(self, parent):
        CTkButton(parent, text="Undo", command=self.undo).pack(pady=5, fill="x")
        CTkButton(parent, text="Redo", command=self.redo).pack(pady=5, fill="x")
        self.btn_rename = CTkButton(parent, text="Rename Column", command=self.rename, state=DISABLED)
        self.btn_rename.pack(pady=5, fill="x")
        self.btn_replace = CTkButton(parent, text="Replace Value", command=self.replace, state=DISABLED)
        self.btn_replace.pack(pady=5, fill="x")
        self.btn_drop = CTkButton(parent, text="Drop Data", command=self.delete, state=DISABLED)
        self.btn_drop.pack(pady=5, fill="x")

    def create_stats_tab(self, parent):
        scroll = CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(expand=True, fill="both")
        
        self.stats_buttons = []
        stats_ops = [
            ("Count", self.count), ("Sum", self.sum), ("Mean", self.mean),
            ("Median", self.median), ("Min", self.min), ("Max", self.max),
            ("Mode", self.mode), ("Nunique", self.nunique), ("Cumsum", self.cumsum),
            ("Abs", self.abs), ("Pow", self.pow), ("T-Test", self.perform_ttest),
            ("Chi-Squared", self.perform_chi2_test)
        ]
        
        for text, cmd in stats_ops:
            btn = CTkButton(scroll, text=text, command=lambda c=cmd: self.run_async(c), state=DISABLED)
            btn.pack(pady=2, fill="x")
            self.stats_buttons.append(btn)

    def create_cleaning_tab(self, parent):
        self.clean_buttons = []
        clean_ops = [
            ("Clean Empty", self.clean_empty),
            ("Clean Duplicates", self.clean_duplicates),
            ("Fill NA", self.fill_na),
            ("One-Hot Encode", self.one_hot_encode),
            ("Scale Data", self.scale_data)
        ]
        for text, cmd in clean_ops:
            btn = CTkButton(parent, text=text, command=lambda c=cmd: self.run_async(c), state=DISABLED)
            btn.pack(pady=5, fill="x")
            self.clean_buttons.append(btn)

    def create_plotting_tab(self, parent):
        self.plot_buttons = []
        plots = ["hist", "scatter", "line", "bar", "box"]
        for p in plots:
            btn = CTkButton(parent, text=f"{p.title()} Plot", command=lambda k=p: self.plot(k), state=DISABLED)
            btn.pack(pady=5, fill="x")
            self.plot_buttons.append(btn)

    def create_ml_tab(self, parent):
        self.ml_buttons = []
        self.btn_linreg = CTkButton(parent, text="Linear Regression", command=lambda: self.run_async(self.linear_regression), state=DISABLED)
        self.btn_linreg.pack(pady=5, fill="x")
        self.ml_buttons.append(self.btn_linreg)

    def run_async(self, func, *args):
        """Runs a function in a separate thread to prevent UI freezing."""
        threading.Thread(target=func, args=args, daemon=True).start()

    def update_view_mode(self):
        mode = self.state_manager.get("view_mode")
        show_menu = self.state_manager.get("show_menu")
        
        # 1. Handle Menu
        # If mode is MenuOnly, force menu to be shown regardless of toggle
        if mode == "MenuOnly" or show_menu:
            self.config(menu=self.menu_)
        else:
            self.config(menu=tkinter.Menu(self))

        # 2. Handle Layout
        self.tab_view.grid_forget()
        self.phone_frame.grid_forget()
        self.data_frame.grid_forget()
        
        if mode == "Tabs":
            self.tab_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.data_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=0)
            
        elif mode == "Phone":
            self.data_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
            self.phone_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
            # Give less weight to phone frame row, more to data
            self.grid_rowconfigure(0, weight=3)
            self.grid_rowconfigure(1, weight=1)
            
        elif mode == "MenuOnly":
            self.data_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=0)

    def update_button_states(self):
        state = NORMAL if hasattr(self, 'dataframe') and self.dataframe is not None else DISABLED
        
        # Tab Buttons
        self.btn_save.configure(state=state)
        self.btn_info.configure(state=state)
        self.btn_desc.configure(state=state)
        self.btn_rename.configure(state=state)
        self.btn_replace.configure(state=state)
        self.btn_drop.configure(state=state)
        
        for btn in self.stats_buttons + self.clean_buttons + self.plot_buttons + self.ml_buttons:
            btn.configure(state=state)
            
        # Phone Buttons
        for text, btn in self.phone_buttons.items():
            if text != 'Open': 
                btn.configure(state=state)

    def handle_open_command(self):
        mode = self.state_manager.get("file_open_mode")
        if mode == "Dialog":
            self.open_dialog()
        else:
            # Default to file open if buttons mode is active but triggered via shortcut
            self.open_file()

    def open_dialog(self):
        dialog = CTkToplevel(self)
        dialog.title('Open File')
        dialog.geometry("350x150")
        dialog.transient(self)
        dialog.grab_set()
        
        CTkLabel(dialog, text="How would you like to open the file?", font=("Arial", 14)).pack(pady=15)
        
        btn_frame = CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20)
        
        def by_file():
            dialog.destroy()
            self.open_file()
            
        def by_link():
            dialog.destroy()
            self.open_link()
            
        CTkButton(btn_frame, text="Local File", command=by_file).pack(side="left", expand=True, padx=5)
        CTkButton(btn_frame, text="URL / Link", command=by_link).pack(side="right", expand=True, padx=5)

    def open_file(self):
        self.file_name = filedialog.askopenfilename(filetypes=(('CSV Files', '*.csv'), ('JSON FILES', '*.json'),
                                                               ('EXCEL Files', '*.xlsx')))
        if self.file_name:
            self.load_file(self.file_name)

    def open_link(self):
        link = simpledialog.askstring('File link', 'Enter the file link (CSV/JSON):')
        if link:
            self.load_file(link, is_link=True)

    def load_file(self, path, is_link=False):
        try:
            if path.endswith('.csv') or is_link:
                self.dataframe = pandas.read_csv(path)
                self.suffix = '.csv'
            elif path.endswith('.json'):
                self.suffix = '.json'
                self.dataframe = pandas.read_json(path)
            elif path.endswith('.xlsx'):
                self.dataframe = pandas.read_excel(path)
                self.suffix = '.xlsx'
            else:
                self.dataframe = pandas.read_csv(path)
                self.suffix = '.csv'
                
            self.history = []
            self.history_index = -1
            self.add_to_history(self.dataframe)
            self.update_data()
            self.update_button_states()
            
        except Exception as e:
            messagebox.showerror('Error', f'Could not open file: {e}')

    def save(self):
        if not self._require_data(): return
        if not (messagebox.askyesno('PandasGui', 'Would you like to replace the old data frame?')):
            self.save_file_handle = filedialog.asksaveasfile(defaultextension=((f'{self.suffix}')))
            if self.save_file_handle:
                save = open(self.save_file_handle.name, 'w')
                save.write(self.dataframe.to_string())
                save.close()
        else:
            if hasattr(self, 'file_name') and os.path.exists(self.file_name):
                save = open(self.file_name, 'w')
                save.write(self.dataframe.to_string())
                save.close()
            else:
                self.save_file_handle = filedialog.asksaveasfile(defaultextension=((f'{self.suffix}')))
                if self.save_file_handle:
                    save = open(self.save_file_handle.name, 'w')
                    save.write(self.dataframe.to_string())
                    save.close()

    def update_data(self):
        # Must be run on main thread if called from async
        if threading.current_thread() is not threading.main_thread():
            self.after(0, self.update_data)
            return

        self.clear()
        
        self.data['column'] = list(self.dataframe.columns)
        self.data['show'] = 'headings'
        for cul in self.data['column']:
            self.data.heading(cul, text=cul)
        
        content_rows = self.dataframe.head(1000).to_numpy().tolist()
        for row in content_rows:
            self.data.insert('', 'end', values=row)

        self.data.focus_set() # Restored focus
        
        self.upd_count += 1
        if self.upd_count >= 2:
            self.changed = True

    def clear(self):
        self.data.delete(*self.data.get_children())

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
        if not self._require_data(): return
        
        # Run on main thread
        if threading.current_thread() is not threading.main_thread():
            self.after(0, self.describe)
            return

        des_root = CTkToplevel(self)
        des_root.title('PandasGui - D.F description')
        des_root.geometry("600x400")
        
        desc_text = CTkTextbox(des_root)
        desc_text.pack(expand=True, fill="both", padx=10, pady=10)
        desc_text.insert("1.0", self.dataframe.describe().to_string())
        desc_text.configure(state="disabled")

    def delete(self):
        if not self._require_data(): return
        
        dialog = CTkToplevel(self)
        dialog.title('Drop Data')
        dialog.geometry("350x250")
        dialog.transient(self)
        dialog.grab_set()

        # Mode selection
        mode_var = StringVar(value="Column")
        
        # Frames for content
        col_frame = CTkFrame(dialog, fg_color="transparent")
        row_frame = CTkFrame(dialog, fg_color="transparent")

        def update_mode(val):
            if val == "Column":
                col_frame.pack(pady=10, fill="x")
                row_frame.pack_forget()
            else:
                col_frame.pack_forget()
                row_frame.pack(pady=10, fill="x")

        seg = CTkSegmentedButton(dialog, values=["Column", "Row"], command=update_mode, variable=mode_var)
        seg.pack(pady=10)

        # Column Frame Content
        CTkLabel(col_frame, text="Select Column:").pack(pady=5)
        col_combobox = CTkComboBox(col_frame, values=self._get_columns())
        col_combobox.pack(pady=5)
        if self._get_columns(): col_combobox.set(self._get_columns()[0])
        col_frame.pack(pady=10, fill="x") # Initial pack

        # Row Frame Content
        CTkLabel(row_frame, text="Row Index (int):").pack(pady=5)
        row_entry = CTkEntry(row_frame, placeholder_text="e.g. 0")
        row_entry.pack(pady=5)

        def apply():
            if mode_var.get() == "Column":
                col = col_combobox.get()
                if col:
                    self._apply_op('Drop Column', lambda: self.dataframe.drop(columns=col))
            else:
                try:
                    idx = int(row_entry.get())
                    self._apply_op('Drop Row', lambda: self.dataframe.drop(index=idx))
                except Exception as e:
                    messagebox.showerror("Error", f"Invalid row index: {e}")
            dialog.destroy()

        CTkButton(dialog, text="Drop", command=apply, fg_color="red").pack(pady=10)

    def replace(self):
        if not self._require_data(): return
        
        dialog = CTkToplevel(self)
        dialog.title('Replace Value')
        dialog.geometry("300x200")
        
        CTkLabel(dialog, text="Old Value:").pack(pady=5)
        old_entry = CTkEntry(dialog)
        old_entry.pack(pady=5)
        
        CTkLabel(dialog, text="New Value:").pack(pady=5)
        new_entry = CTkEntry(dialog)
        new_entry.pack(pady=5)
        
        def apply():
            old_val = old_entry.get()
            new_val = new_entry.get()
            try: old_val = float(old_val)
            except: pass
            try: new_val = float(new_val)
            except: pass
            
            self._apply_op('Replace', lambda: self.dataframe.replace(old_val, new_val))
            dialog.destroy()
            
        CTkButton(dialog, text="Apply", command=apply).pack(pady=10)

    def rename(self):
        if not self._require_data(): return
        
        dialog = CTkToplevel(self)
        dialog.title('Rename Column')
        dialog.geometry("350x250")
        dialog.transient(self)
        dialog.grab_set()

        CTkLabel(dialog, text="Select Column:").pack(pady=5)
        col_combobox = CTkComboBox(dialog, values=self._get_columns())
        col_combobox.pack(pady=5)
        if self._get_columns(): col_combobox.set(self._get_columns()[0])

        CTkLabel(dialog, text="New Name:").pack(pady=5)
        new_name_entry = CTkEntry(dialog)
        new_name_entry.pack(pady=5)

        def apply():
            col = col_combobox.get()
            new_name = new_name_entry.get()
            if col and new_name:
                self._apply_op('Rename', lambda: self.dataframe.rename(columns={col: new_name}))
                dialog.destroy()

        CTkButton(dialog, text="Rename", command=apply).pack(pady=20)

    def count(self):
        if not self._require_data(): return
        count_info = self.dataframe.count()
        self.information_pop_msg(count_info, 'count')

    def information_pop_msg(self, result, operation_name):
        # Ensure UI updates happen on main thread
        if threading.current_thread() is not threading.main_thread():
            self.after(0, lambda: self.information_pop_msg(result, operation_name))
            return

        result_root = CTkToplevel(self)
        time = datetime.datetime.now().strftime('%H:%M:%S')
        result_root.title(f'{operation_name} - {time}')
        result_root.geometry("400x300")
        
        result_text = CTkTextbox(result_root)
        result_text.pack(expand=True, fill="both", padx=10, pady=10)
        result_text.insert("1.0", str(result))
        result_text.configure(state="disabled")
        
        CTkButton(result_root, text='Copy', command=lambda: pyperclip.copy(str(result))).pack(pady=5)

    def setup_menu(self):
        self.menu_ = tkinter.Menu(self)
        self.config(menu=self.menu_)

        file_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open', command=self.handle_open_command)
        file_menu.add_command(label='Save', command=lambda: self.run_async(self.save))
        file_menu.add_separator()
        file_menu.add_command(label='Info', command=lambda: self.run_async(self.info))
        file_menu.add_command(label='Describe', command=lambda: self.run_async(self.describe))

        edit_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Undo', command=self.undo)
        edit_menu.add_command(label='Redo', command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label='Rename Column', command=self.rename)
        edit_menu.add_command(label='Replace Value', command=self.replace)

        statistics_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='Statistics', menu=statistics_menu)
        statistics_menu.add_command(label='Count', command=lambda: self.run_async(self.count))
        statistics_menu.add_command(label='Nunique', command=lambda: self.run_async(self.nunique))
        statistics_menu.add_separator()
        statistics_menu.add_command(label='Mode', command=lambda: self.run_async(self.mode))
        statistics_menu.add_command(label='Median', command=lambda: self.run_async(self.median))
        statistics_menu.add_command(label='Mean', command=lambda: self.run_async(self.mean))
        statistics_menu.add_command(label='Min', command=lambda: self.run_async(self.min))
        statistics_menu.add_command(label='Max', command=lambda: self.run_async(self.max))
        statistics_menu.add_command(label='Cumsum', command=lambda: self.run_async(self.cumsum))
        statistics_menu.add_command(label='T-Test', command=lambda: self.run_async(self.perform_ttest))
        statistics_menu.add_command(label='Chi-Squared', command=lambda: self.run_async(self.perform_chi2_test))

        arithmetic_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='Arithmetics', menu=arithmetic_menu)
        arithmetic_menu.add_command(label='Sum', command=lambda: self.run_async(self.sum))
        arithmetic_menu.add_command(label='Pow', command=lambda: self.run_async(self.pow))
        arithmetic_menu.add_command(label='Abs', command=lambda: self.run_async(self.abs))

        cleaning_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='Cleaning', menu=cleaning_menu)
        cleaning_menu.add_command(label='Clean empty', command=lambda: self.run_async(self.clean_empty))
        cleaning_menu.add_command(label='Cleaning duplicates', command=lambda: self.run_async(self.clean_duplicates))
        cleaning_menu.add_command(label='Delete', command=self.delete)
        cleaning_menu.add_command(label='Fill NA', command=lambda: self.run_async(self.fill_na))
        cleaning_menu.add_command(label='One-Hot Encode', command=lambda: self.run_async(self.one_hot_encode))
        cleaning_menu.add_command(label='Scale Data', command=lambda: self.run_async(self.scale_data))

        plotting_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='Plotting', menu=plotting_menu)
        plotting_menu.add_command(label='Histogram', command=lambda: self.plot('hist'))
        plotting_menu.add_command(label='Scatter', command=lambda: self.plot('scatter'))
        plotting_menu.add_command(label='Line', command=lambda: self.plot('line'))
        plotting_menu.add_command(label='Bar', command=lambda: self.plot('bar'))
        plotting_menu.add_command(label='Box', command=lambda: self.plot('box'))

        ml_menu = tkinter.Menu(self.menu_, tearoff=False)
        self.menu_.add_cascade(label='ML', menu=ml_menu)
        ml_menu.add_command(label='Linear Regression', command=lambda: self.run_async(self.linear_regression))

        self.menu_.add_cascade(label='Settings', command=self.settings)

    def settings(self):
        root = CTkToplevel(self)
        root.title('Settings')
        root.geometry("400x500")
        root.transient(self)
        root.grab_set()

        # Layout Mode
        CTkLabel(root, text='Layout Mode', font=("Arial", 14, "bold")).pack(pady=(10, 5))
        
        mode_var = StringVar(value=self.state_manager.get("view_mode"))
        
        def change_mode(val):
            self.state_manager.set("view_mode", val)
            self.update_view_mode()
            
        seg_btn = CTkSegmentedButton(root, values=["Tabs", "Phone", "MenuOnly"],
                                     variable=mode_var, command=change_mode)
        seg_btn.pack(pady=5)

        # Menu Visibility
        CTkLabel(root, text='Visibility', font=("Arial", 14, "bold")).pack(pady=(15, 5))
        
        menu_var = BooleanVar(value=self.state_manager.get("show_menu"))
        
        def toggle_menu():
            val = menu_var.get()
            self.state_manager.set("show_menu", val)
            self.update_view_mode()
            
        CTkCheckBox(root, text="Show Menu Bar", variable=menu_var, command=toggle_menu).pack(pady=5)

        # File Open Preference
        CTkLabel(root, text='File Open Preference', font=("Arial", 14, "bold")).pack(pady=(15, 5))
        
        file_mode_var = StringVar(value=self.state_manager.get("file_open_mode"))
        
        def change_file_mode(val):
            self.state_manager.set("file_open_mode", val)
            self.update_file_buttons()
            
        file_seg_btn = CTkSegmentedButton(root, values=["Dialog", "Buttons"],
                                          variable=file_mode_var, command=change_file_mode)
        file_seg_btn.pack(pady=5)

        # Font Size
        CTkLabel(root, text='Font Size', font=("Arial", 14, "bold")).pack(pady=(15, 5))
        
        font_var = StringVar(value=self.state_manager.get("font_size"))
        
        def change_font(val):
            self.state_manager.set("font_size", val)
            self.apply_font_scaling(val)
            
        font_seg_btn = CTkSegmentedButton(root, values=["Small", "Medium", "Large"],
                                          variable=font_var, command=change_font)
        font_seg_btn.pack(pady=5)

        # Theme
        CTkLabel(root, text='Theme', font=("Arial", 14, "bold")).pack(pady=(15, 5))

        def set_dark():
            self.set_theme("Dark")

        def set_light():
            self.set_theme("Light")

        theme_frame = CTkFrame(root, fg_color="transparent")
        theme_frame.pack(pady=5)

        current_theme = self.state_manager.get("theme")
        
        btn_dark = CTkButton(theme_frame, text='Dark', command=set_dark, width=80,
                             fg_color="green" if current_theme == "Dark" else None)
        btn_dark.pack(side="left", padx=5)
        
        btn_light = CTkButton(theme_frame, text='Light', command=set_light, width=80,
                              fg_color="green" if current_theme == "Light" else None)
        btn_light.pack(side="left", padx=5)

    def set_theme(self, theme):
        if theme == "Dark":
            customtkinter.set_appearance_mode('dark')
        else:
            customtkinter.set_appearance_mode('light')
        self.state_manager.set("theme", theme)
        # Force update to prevent freeze
        self.update_idletasks()

        # Refresh settings window if open to update button colors
        # (Simple way: close and reopen, or just let user reopen.
        # Here we just rely on next open or manual refresh if we wanted to be fancy)

    def apply_font_scaling(self, size):
        scaling = 1.0
        if size == "Small": scaling = 0.8
        elif size == "Large": scaling = 1.2
        
        customtkinter.set_widget_scaling(scaling)
        customtkinter.set_window_scaling(scaling)

    def _require_data(self) -> bool:
        if getattr(self, "dataframe", None) is None:
            try:
                self.information_pop_msg("No data loaded", "Please open a data file first.")
            except Exception:
                pass
            return False
        return True

    def _get_numeric_columns(self):
        import numpy as _np
        if not self._require_data():
            return []
        try:
            return list(self.dataframe.select_dtypes(include=[_np.number]).columns)
        except Exception:
            return []

    def _get_columns(self, string_only=False):
        if not self._require_data(): return []
        if string_only:
            return list(self.dataframe.select_dtypes(include=['object']).columns)
        return list(self.dataframe.columns)

    def _apply_op(self, op_name: str, fn):
        if not self._require_data():
            return
        try:
            result = fn()
            if result is not None:
                new_df = result
            else:
                new_df = self.dataframe

            self.add_to_history(new_df)
            self.dataframe = new_df
            self.changed = True
            self.upd_count += 1
            try:
                self.update_data()
            except Exception as e:
                self.information_pop_msg(f"{op_name} - UI update failed", str(e))
        except Exception as e:
            try:
                self.information_pop_msg(f"{op_name} failed", str(e))
            except Exception:
                pass

    def _apply_numeric_unary(self, op_name: str, series_op):
        if not self._require_data():
            return
        cols = self._get_numeric_columns()
        if not cols:
            self.information_pop_msg(f"{op_name} - No numeric data", "No numeric columns found to apply operation.")
            return

        def _runner():
            df = self.dataframe.copy()
            for c in cols:
                try:
                    df[c] = series_op(df[c])
                except Exception as col_err:
                    raise type(col_err)(f"Column '{c}': {col_err}")
            return df

        self._apply_op(op_name, _runner)

    def _numeric_summary(self, op_name: str, reducer):
        if not self._require_data():
            return

        import numpy as _np
        df = self.dataframe
        num_df = df.select_dtypes(include=[_np.number])
        if num_df.shape[1] == 0:
            self.information_pop_msg(f"{op_name} - No numeric data", "No numeric columns found to summarize.")
            return

        try:
            result = reducer(num_df)
        except Exception as e:
            self.information_pop_msg(f"{op_name} failed", str(e))
            return

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

        lines = [f"{op_name} per column (numeric only):"]
        for k in result.index:
            try:
                v = result[k]
                if isinstance(v, float):
                    lines.append(f"- {k}: {v:.6g}")
                else:
                    lines.append(f"- {k}: {v}")
            except Exception:
                lines.append(f"- {k}: <unavailable>")
        msg = "\n".join(lines)
        self.information_pop_msg(f"{op_name} result", msg)

    def sum(self):
        self._numeric_summary("Sum", lambda df: df.sum(numeric_only=True))

    def min(self):
        self._numeric_summary("Min", lambda df: df.min(numeric_only=True))

    def max(self):
        self._numeric_summary("Max", lambda df: df.max(numeric_only=True))

    def mean(self):
        self._numeric_summary("Mean", lambda df: df.mean(numeric_only=True))

    def median(self):
        self._numeric_summary("Median", lambda df: df.median(numeric_only=True))

    def abs(self):
        self._apply_numeric_unary("Absolute", lambda s: s.abs())

    def cumsum(self):
        self._apply_numeric_unary("Cumulative sum", lambda s: s.cumsum(skipna=True))

    def pow(self):
        try:
            val = simpledialog.askfloat('Power', 'Enter exponent:', initialvalue=2.0)
            if val is None:
                return
            exp = val
        except Exception:
            return

        self._apply_numeric_unary(f"Power (**{exp})", lambda s: s.pow(exp))

    def mode(self):
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
            self.information_pop_msg("Mode result (numeric)", m.to_string())
        except Exception as e:
            self.information_pop_msg("Mode failed", str(e))

    def nunique(self):
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
        else:
            pass

    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.dataframe = self.history[self.history_index].copy()
            self.update_data()
        else:
            pass

    def _ask_column(self, title, columns):
        dialog = CTkToplevel(self)
        dialog.title('Select Column')
        dialog.geometry('300x150')
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

    def fill_na(self):
        val = simpledialog.askstring('Fill NA', 'Enter value (or mean/median/mode):', parent=self)
        if val:
            if val.lower() == 'mean':
                self._apply_op('Fill NA (Mean)', lambda: self.dataframe.fillna(self.dataframe.mean(numeric_only=True)))
                return
            elif val.lower() == 'median':
                self._apply_op('Fill NA (Median)',
                               lambda: self.dataframe.fillna(self.dataframe.median(numeric_only=True)))
                return
            elif val.lower() == 'mode':
                self._apply_op('Fill NA (Mode)', lambda: self.dataframe.fillna(self.dataframe.mode().iloc[0]))
                return

            try:
                val = float(val)
            except:
                pass
            self._apply_op('Fill NA', lambda: self.dataframe.fillna(val))

    def one_hot_encode(self):
        col = self._ask_column('Select column:', self._get_columns(string_only=True))
        if col:
            if self.dataframe[col].nunique() > 20:
                if not messagebox.askyesno('High Cardinality',
                                           f'Column "{col}" has {self.dataframe[col].nunique()} unique values.\nThis will create many columns. Continue?'):
                    return

            self._apply_op(f'One-hot {col}', lambda: pandas.concat(
                [self.dataframe.drop(col, axis=1), pandas.get_dummies(self.dataframe[col], prefix=col)], axis=1))

    def scale_data(self):
        if not StandardScaler:
            messagebox.showerror('Error', 'Sklearn not installed')
            return
        cols = self._get_numeric_columns()
        if cols:
            def _runner():
                df = self.dataframe.copy()
                df[cols] = StandardScaler().fit_transform(df[cols])
                return df

            self._apply_op('Scale Data', _runner)

    def perform_ttest(self):
        if not ttest_ind:
            messagebox.showerror('Error', 'Scipy not installed')
            return
        c1 = self._ask_column('Col 1:', self._get_numeric_columns())
        c2 = self._ask_column('Col 2:', self._get_numeric_columns())
        if c1 and c2:
            s, p = ttest_ind(self.dataframe[c1], self.dataframe[c2], nan_policy='omit')
            self.information_pop_msg(f'Stat: {s}, P-value: {p}', 'T-Test')

    def perform_chi2_test(self):
        if not chi2_contingency:
            messagebox.showerror('Error', 'Scipy not installed')
            return
        c1 = self._ask_column('Col 1:', self._get_columns(string_only=True))
        c2 = self._ask_column('Col 2:', self._get_columns(string_only=True))
        if c1 and c2:
            tab = pandas.crosstab(self.dataframe[c1], self.dataframe[c2])
            chi2, p, dof, ex = chi2_contingency(tab)
            self.information_pop_msg(f'Chi2: {chi2}, P: {p}', 'Chi2 Test')

    def linear_regression(self):
        if not LinearRegression:
            messagebox.showerror('Error', 'Sklearn not installed')
            return
        x_col = self._ask_column('X:', self._get_numeric_columns())
        y_col = self._ask_column('Y:', self._get_numeric_columns())
        if x_col and y_col:
            try:
                data = self.dataframe[[x_col, y_col]].dropna()
                if data.empty:
                    raise ValueError("No valid data points after dropping NaNs")

                X = data[[x_col]]
                y = data[y_col]

                model = LinearRegression().fit(X, y)
                self.information_pop_msg(
                    f'Coef: {model.coef_[0]:.4f}, Intercept: {model.intercept_:.4f}\nR2: {model.score(X, y):.4f}',
                    'Linear Regression')
            except Exception as e:
                messagebox.showerror('Error', str(e))

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
        # Save state before closing
        self.state_manager.set("geometry", self.geometry())
        
        if self.changed:
            if messagebox.askyesno('PandasGui', 'there is some unsaved progress are you sure you want to quit'):
                self.destroy()
        else:
            self.destroy()


if __name__ == '__main__':
    App = Window()
    App.mainloop()
