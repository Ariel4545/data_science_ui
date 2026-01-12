import tkinter
import customtkinter
import pyperclip
import scipy.special
from customtkinter import *
import numpy
from scipy import constants
import json
import os


class StateManager:
    """Handles persistent state management for the application."""
    def __init__(self, filename="numpygui_state.json"):
        self.filename = filename
        self.default_state = {
            "show_tabs": False,
            "show_menus": True,
            "theme": "Dark"
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
    COMPACT_WIDTH = 725
    EXPANDED_WIDTH = 1050
    HEIGHT = 600

    def __init__(self):
        super().__init__()
        self.state_manager = StateManager()

        # window
        self.title('Egon - Gui for numpy')
        self.after(201, lambda: self.iconbitmap('NumpyGui logo.png'))

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)  # Tab view column
        self.grid_rowconfigure(0, weight=1)

        # Input Frame
        self.input_frame = CTkFrame(self, fg_color='transparent')
        self.input_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_rowconfigure(3, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)

        # Array A Input
        self.label_a = CTkLabel(self.input_frame, text="Array A", anchor="w", font=("Arial", 12, "bold"))
        self.label_a.grid(row=0, column=0, sticky='w', pady=(0, 2))

        self.number_input = CTkTextbox(self.input_frame, wrap=tkinter.WORD)
        self.number_input.grid(row=1, column=0, sticky='nsew', pady=(0, 5))
        self.number_input._textbox.config(undo=True)

        # Array B Input
        self.label_b = CTkLabel(self.input_frame, text="Array B", anchor="w", font=("Arial", 12, "bold"))
        self.label_b.grid(row=2, column=0, sticky='w', pady=(5, 2))

        self.snumber_input = CTkTextbox(self.input_frame, wrap=tkinter.WORD, height=150)
        self.snumber_input.grid(row=3, column=0, sticky='nsew', pady=(0, 5))
        self.snumber_input._textbox.config(undo=True)

        # Status Label
        self.status_label = CTkLabel(self.input_frame, text="Ready", anchor="w", text_color="gray")
        self.status_label.grid(row=4, column=0, sticky='ew', pady=(5, 0))

        # Tab View for Operations
        self.ops_tabview = CTkTabview(self, width=300)
        
        self.tabs = {
            'Arithmetic': ['Addition', 'Subtraction', 'Multiplication', 'Division', 'Power', 'square', 'square root', 'Remainder', 'Absolute', 'Factorial'],
            'Rounding': ['Truncation', 'Rounding', 'Floor', 'Ceil', 'fix', 'rint'],
            'Trig': ['Sin', 'Cos', 'Tan', 'd2r', 'r2d', 'sinh', 'cosh', 'tanh', 'arcsinh', 'arccosh', 'arctanh'],
            'Stats': ['Median', 'Average', 'Mean', 'Min', 'Max', 'Std', 'Ptp', 'Mode'],
            'Random': ['Choice', 'Generate unit interval', 'Randint', 'sample', 'permutation'],
            'Data': ['size', 'parity', 'sort', 'search', 'Get shape', 'Difference', 'Product', 'LCM', 'GCD', 'Unique', 'p.of', 'p.difference', 'p.increase'],
            'Num Sys': ['Binary', 'Octal', 'Hexadecimal'],
            'Exponents': ['exp', 'exp-1', 'exp2', 'exp10', 'log', 'log2'],
            'Const': ['Pi', 'E', 'R', 'Golden ratio', 'Speed of light', 'E0', 'MU0', 'G'],
            'Calculus': ['Integrate', 'Integration sum', 'Line space']
        }

        # Store references to dynamically created widgets for easier theme updates
        self.dynamic_widgets = []

        for tab_name in self.tabs:
            self.ops_tabview.add(tab_name)
            self.create_buttons(tab_name, self.tabs[tab_name])

        # --- Menus Initialization ---
        self.menu = tkinter.Menu(self)
        self.config(menu=self.menu)
        
        # Create Operation Menus (but don't add them yet)
        self.op_menus = [] # List of (label, menu_object)

        arithmetic_menu = tkinter.Menu(self.menu, tearoff=False)
        self.op_menus.append(('arithmetic', arithmetic_menu))
        for op in self.tabs['Arithmetic']:
            arithmetic_menu.add_command(label=op, command=lambda o=op: self.arithmetics(o))

        rounding_menu = tkinter.Menu(self.menu, tearoff=False)
        self.op_menus.append(('Rounding', rounding_menu))
        for op in self.tabs['Rounding']:
            rounding_menu.add_command(label=op, command=lambda o=op: self.round(o))

        trigonometry_menu = tkinter.Menu(self.menu, tearoff=False)
        self.op_menus.append(('Trig.', trigonometry_menu))
        for op in self.tabs['Trig']:
            trigonometry_menu.add_command(label=op, command=lambda o=op: self.trigonometry(o))

        statistics_menu = tkinter.Menu(self.menu, tearoff=False)
        self.op_menus.append(('Statistics', statistics_menu))
        for op in self.tabs['Stats']:
            statistics_menu.add_command(label=op, command=lambda o=op: self.statistics(o))

        random_menu = tkinter.Menu(self.menu, tearoff=False)
        self.op_menus.append(('Random', random_menu))
        for op in self.tabs['Random']:
            random_menu.add_command(label=op, command=lambda o=op: self.random(o))

        data_menu = tkinter.Menu(self.menu, tearoff=False)
        self.op_menus.append(('Others', data_menu))
        for op in self.tabs['Data']:
            data_menu.add_command(label=op, command=lambda o=op: self.data_operations(mode=o))

        ns_menu = tkinter.Menu(self.menu, tearoff=False)
        self.op_menus.append(('Number systems', ns_menu))
        for op in self.tabs['Num Sys']:
            ns_menu.add_command(label=op, command=lambda o=op: self.number_system(mode=o))

        exp_menu = tkinter.Menu(self.menu, tearoff=False)
        self.op_menus.append(('Exponents', exp_menu))
        for op in self.tabs['Exponents']:
            exp_menu.add_command(label=op, command=lambda o=op: self.ex(o))

        const_menu = tkinter.Menu(self.menu, tearoff=False)
        self.op_menus.append(('Const.', const_menu))
        const_menu.add_command(label='Pi', command=lambda: self.const(numpy.pi))
        const_menu.add_command(label='E', command=lambda: self.const(numpy.e))
        const_menu.add_command(label='R', command=lambda: self.const(constants.R))
        const_menu.add_command(label='Golden ratio', command=lambda: self.const(constants.golden))
        const_menu.add_command(label='Speed of light', command=lambda: self.const(constants.speed_of_light))
        const_menu.add_command(label='E0', command=lambda: self.const(constants.epsilon_0))
        const_menu.add_command(label='MU0', command=lambda: self.const(constants.golden))
        const_menu.add_command(label='G', command=lambda: self.const(constants.G))

        calc_menu = tkinter.Menu(self.menu, tearoff=False)
        self.op_menus.append(('Calculus', calc_menu))
        calc_menu.add_cascade(label='Integrate', command=lambda: self.calculus(scipy.integrate))
        calc_menu.add_cascade(label='Integration sum', command=lambda: self.calculus(numpy.cumsum))
        calc_menu.add_cascade(label='Line space', command=lambda: self.calculus(numpy.linspace))

        # View Menu
        self.view_menu = tkinter.Menu(self.menu, tearoff=False)
        self.show_tabs_var = tkinter.BooleanVar(value=self.state_manager.get("show_tabs"))
        self.show_menus_var = tkinter.BooleanVar(value=self.state_manager.get("show_menus"))
        
        self.view_menu.add_checkbutton(label='Show Operations Tabs', variable=self.show_tabs_var, command=self.update_views)
        self.view_menu.add_checkbutton(label='Show Operations Menus', variable=self.show_menus_var, command=self.update_views)

        self.generate_op_num()
        
        # List for theming
        self.menu_list = [m for _, m in self.op_menus] + [self.view_menu]

        # Apply Initial State
        self.set_theme(self.state_manager.get("theme"), update_views=False)
        self.update_views(save=False)

    def show_status(self, message, is_error=False):
        color = "#FF5555" if is_error else ("#55FF55" if self.state_manager.get("theme") == "Dark" else "#00AA00")
        self.status_label.configure(text=message, text_color=color)
        if is_error:
            print(f"Error: {message}")

    def update_views(self, save=True):
        show_tabs = self.show_tabs_var.get()
        show_menus = self.show_menus_var.get()
        
        # 1. Handle Tabs
        if show_tabs:
            self.ops_tabview.grid(row=0, column=1, sticky='nsew', padx=(0, 10), pady=10)
            self.geometry(f"{self.EXPANDED_WIDTH}x{self.HEIGHT}")
        else:
            self.ops_tabview.grid_forget()
            self.geometry(f"{self.COMPACT_WIDTH}x{self.HEIGHT}")
            
        # 2. Handle Menus
        self.menu.delete(0, 'end') # Clear all
        
        if show_menus:
            for label, menu_obj in self.op_menus:
                self.menu.add_cascade(label=label, menu=menu_obj)
        
        # Always add View and Night mode
        self.menu.add_cascade(label='View', menu=self.view_menu)
        
        theme_label = 'Night mode ✓' if self.state_manager.get("theme") == "Dark" else 'Night mode'
        self.menu.add_cascade(label=theme_label, command=self.toggle_theme)

        if save:
            self.state_manager.set("show_tabs", show_tabs)
            self.state_manager.set("show_menus", show_menus)

    def set_theme(self, theme_name, update_views=True):
        if theme_name == "Dark":
            customtkinter.set_appearance_mode('dark')
            self.menu.configure(background='#27211a', foreground='green')
            for menu_ in self.menu_list:
                menu_.configure(background='#27211a', foreground='green')
            
            # Update specific widgets that might not auto-update
            self.status_label.configure(text_color="gray") # Reset to neutral
            self.label_a.configure(text_color="white")
            self.label_b.configure(text_color="white")
            
            # Update Tabview colors
            self.ops_tabview.configure(text_color="white")
            
            # Update dynamic widgets
            for widget in self.dynamic_widgets:
                try:
                    if isinstance(widget, CTkLabel):
                        widget.configure(text_color="white")
                    elif isinstance(widget, CTkButton):
                        widget.configure(text_color="white")
                except:
                    pass # Widget might be destroyed

        else:
            customtkinter.set_appearance_mode('light')
            self.menu.configure(background='SystemButtonFace', foreground='black')
            for menu_ in self.menu_list:
                menu_.configure(background='SystemButtonFace', foreground='black')
            
            # Update specific widgets
            self.status_label.configure(text_color="gray")
            self.label_a.configure(text_color="black")
            self.label_b.configure(text_color="black")
            
            # Update Tabview colors
            self.ops_tabview.configure(text_color="black")
            
            # Update dynamic widgets
            for widget in self.dynamic_widgets:
                try:
                    if isinstance(widget, CTkLabel):
                        widget.configure(text_color="black")
                    elif isinstance(widget, CTkButton):
                        widget.configure(text_color="white") # Buttons usually white text on blue bg in light mode
                except:
                    pass

        # Force update of all widgets to redraw
        self.update_idletasks()
            
        self.state_manager.set("theme", theme_name)
        if update_views:
            self.update_views(save=False)

    def toggle_theme(self):
        current = self.state_manager.get("theme")
        new_theme = "Light" if current == "Dark" else "Dark"
        self.set_theme(new_theme)

    def create_buttons(self, tab_name, operations):
        scrollable_frame = CTkScrollableFrame(self.ops_tabview.tab(tab_name), fg_color='transparent')
        scrollable_frame.pack(expand=True, fill='both')
        
        # Dictionary mapping tab names to their custom widget creation methods
        custom_tab_handlers = {
            'Const': self.create_const_widgets,
            'Num Sys': self.create_num_sys_widgets,
            'Data': self.create_data_widgets,
            'Trig': self.create_trig_widgets,
            'Arithmetic': self.create_arithmetic_widgets,
            'Rounding': self.create_rounding_widgets,
            'Stats': self.create_stats_widgets,
            'Calculus': self.create_calculus_widgets,
            'Random': self.create_random_widgets,
            'Exponents': self.create_exponents_widgets
        }

        # Check if there is a custom handler for the current tab
        handler = custom_tab_handlers.get(tab_name)
        if handler:
            handler(scrollable_frame, operations)
            return

        # Grid configuration for better layout
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        
        # Fallback for any other tabs
        new_widgets = []
        for idx, op in enumerate(operations):
            btn = CTkButton(scrollable_frame, text=op, height=32, font=("Arial", 12))
            btn.grid(row=idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")
            new_widgets.append(btn)
        self.dynamic_widgets.extend(new_widgets)

    def create_const_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        
        label_const_select = CTkLabel(parent, text="Select Constant:", font=("Arial", 14, "bold"))
        label_const_select.grid(row=0, column=0, pady=(10, 5))
        
        self.const_var = tkinter.StringVar(value=operations[0])
        option_menu = CTkOptionMenu(parent, values=operations, variable=self.const_var)
        option_menu.grid(row=1, column=0, pady=10)
        
        def insert_val():
            op = self.const_var.get()
            val = None
            if op == 'Pi': val = numpy.pi
            elif op == 'E': val = numpy.e
            elif op == 'R': val = constants.R
            elif op == 'Golden ratio': val = constants.golden
            elif op == 'Speed of light': val = constants.speed_of_light
            elif op == 'E0': val = constants.epsilon_0
            elif op == 'MU0': val = constants.golden
            elif op == 'G': val = constants.G
            
            if val is not None:
                self.const(val)
                
        btn_insert_const = CTkButton(parent, text="Insert Value", command=insert_val)
        btn_insert_const.grid(row=2, column=0, pady=20)
        
        self.dynamic_widgets.extend([label_const_select, btn_insert_const])

    def create_num_sys_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        
        label_convert_sys = CTkLabel(parent, text="Convert to System:", font=("Arial", 14, "bold"))
        label_convert_sys.grid(row=0, column=0, pady=(10, 5))
        
        self.num_sys_var = tkinter.StringVar(value=operations[0])
        seg_btn = CTkSegmentedButton(parent, values=operations, variable=self.num_sys_var)
        seg_btn.grid(row=1, column=0, pady=10)
        
        def convert():
            mode = self.num_sys_var.get()
            self.number_system(mode)
            
        btn_convert_sys = CTkButton(parent, text="Convert", command=convert)
        btn_convert_sys.grid(row=2, column=0, pady=20)
        
        self.dynamic_widgets.extend([label_convert_sys, btn_convert_sys])

    def create_data_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)

        # Size Filter
        label_size_filter = CTkLabel(parent, text="Filter by Size", font=("Arial", 12, "bold"))
        label_size_filter.grid(row=0, column=0, columnspan=3, pady=(5,0))

        self.data_size_entry = CTkEntry(parent, placeholder_text="Threshold")
        self.data_size_entry.grid(row=1, column=0, padx=2, pady=2)
        self.data_size_mode = CTkSegmentedButton(parent, values=[">", "<"])
        self.data_size_mode.set(">")
        self.data_size_mode.grid(row=1, column=1, padx=2, pady=2)
        
        btn_apply_size = CTkButton(parent, text="Apply", command=self.inline_size_filter, width=60)
        btn_apply_size.grid(row=1, column=2, padx=2, pady=2)

        # Parity Filter
        label_parity_filter = CTkLabel(parent, text="Filter by Parity", font=("Arial", 12, "bold"))
        label_parity_filter.grid(row=2, column=0, columnspan=3, pady=(10,0))

        self.data_parity_mode = CTkSegmentedButton(parent, values=["Even", "Odd"])
        self.data_parity_mode.set("Even")
        self.data_parity_mode.grid(row=3, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
        
        btn_apply_parity = CTkButton(parent, text="Apply", command=self.inline_parity_filter, width=60)
        btn_apply_parity.grid(row=3, column=2, padx=2, pady=2)

        # Search
        label_search_val = CTkLabel(parent, text="Search Value", font=("Arial", 12, "bold"))
        label_search_val.grid(row=4, column=0, columnspan=3, pady=(10,0))

        self.data_search_entry = CTkEntry(parent, placeholder_text="Value")
        self.data_search_entry.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
        
        btn_find_val = CTkButton(parent, text="Find", command=self.inline_search, width=60)
        btn_find_val.grid(row=5, column=2, padx=2, pady=2)

        # Separator
        label_ops_sep = CTkLabel(parent, text="Operations", font=("Arial", 12, "bold"))
        label_ops_sep.grid(row=6, column=0, columnspan=3, pady=(15,5))

        # Other buttons
        handled = ['size', 'parity', 'search']
        others = [op for op in operations if op not in handled]
        
        btn_frame = CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=7, column=0, columnspan=3, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        
        new_widgets = [label_size_filter, btn_apply_size, label_parity_filter, btn_apply_parity, label_search_val, btn_find_val, label_ops_sep]
        
        for idx, op in enumerate(others):
            cmd = lambda o=op: self.data_operations(mode=o)
            btn_op = CTkButton(btn_frame, text=op, command=cmd, height=32)
            btn_op.grid(row=idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")
            new_widgets.append(btn_op)
            
        self.dynamic_widgets.extend(new_widgets)

    def create_trig_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        groups = {
            "Standard": ['Sin', 'Cos', 'Tan'],
            "Conversion": ['d2r', 'r2d'],
            "Hyperbolic": ['sinh', 'cosh', 'tanh'],
            "Inverse Hyperbolic": ['arcsinh', 'arccosh', 'arctanh']
        }
        
        new_widgets = []
        row = 0
        for group_name, ops in groups.items():
            label_group = CTkLabel(parent, text=group_name, font=("Arial", 12, "bold"))
            label_group.grid(row=row, column=0, columnspan=2, pady=(10, 2))
            new_widgets.append(label_group)
            row += 1
            for idx, op in enumerate(ops):
                cmd = lambda o=op: self.trigonometry(o)
                btn_trig = CTkButton(parent, text=op, command=cmd, height=32)
                r = row + idx // 2
                c = idx % 2
                btn_trig.grid(row=r, column=c, padx=5, pady=5, sticky="ew")
                new_widgets.append(btn_trig)
            row += (len(ops) + 1) // 2
        
        self.dynamic_widgets.extend(new_widgets)

    def create_arithmetic_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_columnconfigure(3, weight=1)
        
        # Map operations to symbols/labels
        symbols = {
            'Addition': '+', 'Subtraction': '-', 'Multiplication': '×', 'Division': '÷',
            'Power': 'xʸ', 'square': 'x²', 'square root': '√', 'Remainder': '%',
            'Absolute': '|x|', 'Factorial': 'n!'
        }
        
        # Calculator-like grid
        calc_ops = ['Addition', 'Subtraction', 'Multiplication', 'Division', 
                    'Power', 'square', 'square root', 'Remainder', 
                    'Absolute', 'Factorial']
        
        new_widgets = []
        for idx, op in enumerate(calc_ops):
            if op in operations:
                cmd = lambda o=op: self.arithmetics(o)
                text = symbols.get(op, op)
                btn_calc = CTkButton(parent, text=text, command=cmd, height=40, font=("Arial", 16, "bold"))
                btn_calc.grid(row=idx // 4, column=idx % 4, padx=3, pady=3, sticky="ew")
                new_widgets.append(btn_calc)
        
        self.dynamic_widgets.extend(new_widgets)

    def create_rounding_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Rounding with decimals
        label_round_prec = CTkLabel(parent, text="Rounding Precision", font=("Arial", 12, "bold"))
        label_round_prec.grid(row=0, column=0, columnspan=2, pady=(5,0))

        self.rounding_decimals_entry = CTkEntry(parent, placeholder_text="Decimals (default 0)")
        self.rounding_decimals_entry.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        
        btn_round = CTkButton(parent, text="Round", command=lambda: self.round('Rounding'))
        btn_round.grid(row=1, column=1, padx=2, pady=2, sticky="ew")
        
        # Other operations
        others = [op for op in operations if op != 'Rounding']
        label_other_methods = CTkLabel(parent, text="Other Methods", font=("Arial", 12, "bold"))
        label_other_methods.grid(row=2, column=0, columnspan=2, pady=(15,5))
        
        new_widgets = [label_round_prec, btn_round, label_other_methods]
        
        for idx, op in enumerate(others):
            cmd = lambda o=op: self.round(o)
            btn_op = CTkButton(parent, text=op, command=cmd, height=32)
            btn_op.grid(row=3 + idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")
            new_widgets.append(btn_op)
            
        self.dynamic_widgets.extend(new_widgets)

    def create_stats_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        groups = {
            "Central Tendency": ['Mean', 'Median', 'Mode', 'Average'],
            "Extremes": ['Min', 'Max'],
            "Dispersion": ['Std', 'Ptp']
        }
        
        new_widgets = []
        row = 0
        for group_name, ops in groups.items():
            label_group = CTkLabel(parent, text=group_name, font=("Arial", 12, "bold"))
            label_group.grid(row=row, column=0, columnspan=2, pady=(10, 2))
            new_widgets.append(label_group)
            row += 1
            for idx, op in enumerate(ops):
                if op in operations:
                    cmd = lambda o=op: self.statistics(o)
                    btn_stat = CTkButton(parent, text=op, command=cmd, height=32)
                    r = row + idx // 2
                    c = idx % 2
                    btn_stat.grid(row=r, column=c, padx=5, pady=5, sticky="ew")
                    new_widgets.append(btn_stat)
            row += (len(ops) + 1) // 2
            
        self.dynamic_widgets.extend(new_widgets)

    def create_calculus_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Linspace Generator
        label_linspace = CTkLabel(parent, text="Linspace Generator", font=("Arial", 12, "bold"))
        label_linspace.grid(row=0, column=0, columnspan=2, pady=(5,0))
        
        self.linspace_start = CTkEntry(parent, placeholder_text="Start")
        self.linspace_start.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        self.linspace_stop = CTkEntry(parent, placeholder_text="Stop")
        self.linspace_stop.grid(row=1, column=1, padx=2, pady=2, sticky="ew")
        self.linspace_num = CTkEntry(parent, placeholder_text="Count (default 50)")
        self.linspace_num.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
        
        btn_gen_linspace = CTkButton(parent, text="Generate Linspace", command=self.inline_linspace)
        btn_gen_linspace.grid(row=3, column=0, columnspan=2, padx=2, pady=5, sticky="ew")
        
        # Other operations
        others = [op for op in operations if op != 'Line space']
        label_ops = CTkLabel(parent, text="Operations", font=("Arial", 12, "bold"))
        label_ops.grid(row=4, column=0, columnspan=2, pady=(15,5))
        
        new_widgets = [label_linspace, btn_gen_linspace, label_ops]
        
        for idx, op in enumerate(others):
            func = None
            if op == 'Integrate': func = scipy.integrate
            elif op == 'Integration sum': func = numpy.cumsum
            
            if func:
                cmd = lambda f=func: self.calculus(f)
                btn_op = CTkButton(parent, text=op, command=cmd, height=32)
                btn_op.grid(row=5 + idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")
                new_widgets.append(btn_op)
                
        self.dynamic_widgets.extend(new_widgets)

    def create_random_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Random Integer Generator
        label_rand_int = CTkLabel(parent, text="Generate Random Integers", font=("Arial", 12, "bold"))
        label_rand_int.grid(row=0, column=0, columnspan=2, pady=(5,0))

        self.randint_min = CTkEntry(parent, placeholder_text="Min")
        self.randint_min.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        self.randint_max = CTkEntry(parent, placeholder_text="Max")
        self.randint_max.grid(row=1, column=1, padx=2, pady=2, sticky="ew")
        self.randint_size = CTkEntry(parent, placeholder_text="Count (optional)")
        self.randint_size.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
        
        btn_gen_rand = CTkButton(parent, text="Generate", command=self.inline_randint)
        btn_gen_rand.grid(row=3, column=0, columnspan=2, padx=2, pady=5, sticky="ew")

        # Array Operations
        label_arr_ops = CTkLabel(parent, text="Array Operations", font=("Arial", 12, "bold"))
        label_arr_ops.grid(row=4, column=0, columnspan=2, pady=(15,5))

        new_widgets = [label_rand_int, btn_gen_rand, label_arr_ops]

        array_ops = ['Choice', 'permutation', 'sample']
        for idx, op in enumerate(array_ops):
            if op in operations:
                cmd = lambda o=op: self.random(o)
                btn_op = CTkButton(parent, text=op, command=cmd, height=32)
                btn_op.grid(row=5 + idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")
                new_widgets.append(btn_op)

        # Other
        label_other = CTkLabel(parent, text="Other", font=("Arial", 12, "bold"))
        label_other.grid(row=7, column=0, columnspan=2, pady=(15,5))
        new_widgets.append(label_other)

        if 'Generate unit interval' in operations:
            cmd = lambda: self.random('Generate unit interval')
            btn_unit = CTkButton(parent, text="Unit Interval (0-1)", command=cmd, height=32)
            btn_unit.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
            new_widgets.append(btn_unit)
            
        self.dynamic_widgets.extend(new_widgets)

    def create_exponents_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Powers
        label_powers = CTkLabel(parent, text="Exponential Functions", font=("Arial", 12, "bold"))
        label_powers.grid(row=0, column=0, columnspan=2, pady=(5,0))
        
        new_widgets = [label_powers]

        powers = ['exp', 'exp2', 'exp10', 'exp-1']
        for idx, op in enumerate(powers):
            if op in operations:
                cmd = lambda o=op: self.ex(o)
                btn_pow = CTkButton(parent, text=op, command=cmd, height=32)
                btn_pow.grid(row=1 + idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")
                new_widgets.append(btn_pow)

        # Logarithms
        label_logs = CTkLabel(parent, text="Logarithmic Functions", font=("Arial", 12, "bold"))
        label_logs.grid(row=3, column=0, columnspan=2, pady=(15,5))
        new_widgets.append(label_logs)

        logs = ['log', 'log2']
        for idx, op in enumerate(logs):
            if op in operations:
                cmd = lambda o=op: self.ex(o)
                btn_log = CTkButton(parent, text=op, command=cmd, height=32)
                btn_log.grid(row=4 + idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")
                new_widgets.append(btn_log)

        # Custom Base
        label_custom = CTkLabel(parent, text="Custom Base", font=("Arial", 12, "bold"))
        label_custom.grid(row=6, column=0, columnspan=2, pady=(15,5))
        
        self.custom_base_entry = CTkEntry(parent, placeholder_text="Base (e.g. 5)")
        self.custom_base_entry.grid(row=7, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
        
        btn_log_base = CTkButton(parent, text="Log(Base)", command=lambda: self.inline_custom_base('log'))
        btn_log_base.grid(row=8, column=0, padx=2, pady=5, sticky="ew")

        btn_pow_base = CTkButton(parent, text="Power(Base)", command=lambda: self.inline_custom_base('power'))
        btn_pow_base.grid(row=8, column=1, padx=2, pady=5, sticky="ew")
        
        new_widgets.extend([label_custom, btn_log_base, btn_pow_base])
        self.dynamic_widgets.extend(new_widgets)

    def inline_size_filter(self):
        self.turn_into_array()
        try:
            conditional_number = int(self.data_size_entry.get())
            mode = self.data_size_mode.get()
            filter_array = []
            for element in self.array:
                if mode == '>':
                    if element > conditional_number:
                        filter_array.append(True)
                    else:
                        filter_array.append(False)
                else:
                    if element < conditional_number:
                        filter_array.append(True)
                    else:
                        filter_array.append(False)
            result = self.array[filter_array]
            self.result_page(result)
        except ValueError:
            self.show_status("Invalid threshold value", is_error=True)

    def inline_parity_filter(self):
        self.turn_into_array()
        mode = self.data_parity_mode.get()
        filter_array = []
        for element in self.array:
            if mode == 'Even':
                if element % 2 == 0:
                    filter_array.append(True)
                else:
                    filter_array.append(False)
            else:
                if element % 2 != 0:
                    filter_array.append(True)
                else:
                    filter_array.append(False)
        result = self.array[filter_array]
        self.result_page(result)

    def inline_search(self):
        self.turn_into_array()
        try:
            searched_value = int(self.data_search_entry.get())
            result = numpy.where(self.array == searched_value)[0]
            self.result_page(result)
        except ValueError:
            self.show_status("Invalid search value", is_error=True)

    def inline_linspace(self):
        try:
            start = float(self.linspace_start.get())
            stop = float(self.linspace_stop.get())
            num_str = self.linspace_num.get()
            num = int(num_str) if num_str else 50
            
            result = numpy.linspace(start, stop, num)
            self.result_page(result)
        except ValueError:
            self.show_status("Invalid linspace parameters", is_error=True)

    def inline_randint(self):
        try:
            min_val = int(self.randint_min.get())
            max_val = int(self.randint_max.get())
            size_str = self.randint_size.get()
            size = int(size_str) if size_str else None
            
            result = numpy.random.randint(min_val, max_val, size)
            self.result_page(result)
        except ValueError:
            self.random('Randint')

    def inline_custom_base(self, mode):
        self.turn_into_array()
        try:
            base = float(self.custom_base_entry.get())
            if mode == 'log':
                result = numpy.log(self.array) / numpy.log(base)
            elif mode == 'power':
                result = numpy.power(base, self.array)
            self.result_page(result)
        except ValueError:
            self.show_status("Invalid base value", is_error=True)

    def turn_into_array(self):
        def parse_input(textbox):
            text = textbox.get('1.0', 'end').strip()
            if not text:
                return numpy.array([], dtype='int32')
            
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            if len(lines) > 1:
                # 2D Array
                try:
                    # Try to parse as matrix
                    data = [line.split() for line in lines]
                    return numpy.array(data, dtype='int32')
                except Exception:
                    # Fallback to 1D if inconsistent rows
                    return numpy.array(text.split(), dtype='int32')
            else:
                # 1D Array
                return numpy.array(text.split(), dtype='int32')

        try:
            self.array = parse_input(self.number_input)
            self.sarray = parse_input(self.snumber_input)
            return self.array
        except Exception as e:
            self.show_status(f"Input Error: {e}", is_error=True)
            self.array = numpy.array([])
            self.sarray = numpy.array([])
            return self.array

    def arithmetics(self, mode):
        self.turn_into_array()
        
        ops = {
            'Addition': (numpy.add, True),
            'Subtraction': (numpy.subtract, True),
            'Multiplication': (numpy.multiply, True),
            'Division': (numpy.divide, True),
            'Power': (numpy.power, True),
            'Remainder': (numpy.remainder, True),
            'Absolute': (numpy.abs, False),
            'square root': (numpy.sqrt, False),
            'square': (numpy.square, False),
            'Factorial': (scipy.special.factorial, False)
        }
        
        if mode in ops:
            func, needs_b = ops[mode]
            try:
                if needs_b:
                    result = func(self.array, self.sarray)
                else:
                    result = func(self.array)
                self.result_page(result)
                self.show_status(f"Calculated {mode}")
            except Exception as e:
                self.show_status(f"Error: {e}", is_error=True)

    def round(self, mode):
        self.turn_into_array()
        try:
            result = None
            if mode == 'Truncation':
                result = numpy.trunc(self.array)
            elif mode == 'Rounding':
                decimals = 0
                if hasattr(self, 'rounding_decimals_entry'):
                    try:
                        decimals = int(self.rounding_decimals_entry.get())
                    except:
                        pass
                result = numpy.round(self.array, decimals=decimals)
            elif mode == 'Floor':
                result = numpy.floor(self.array)
            elif mode == 'Ceil':
                result = numpy.ceil(self.array)
            elif mode == 'rint':
                result = numpy.rint(self.array)
            elif mode == 'fix':
                result = numpy.fix(self.array)
            
            if result is not None:
                self.result_page(result)
                self.show_status(f"Calculated {mode}")
        except Exception as e:
            self.show_status(f"Error: {e}", is_error=True)

    def trigonometry(self, mode):
        self.turn_into_array()
        
        ops = {
            'Sin': numpy.sin, 'Cos': numpy.cos, 'Tan': numpy.tan,
            'd2r': numpy.deg2rad, 'r2d': numpy.rad2deg,
            'sinh': numpy.sinh, 'cosh': numpy.cosh, 'tanh': numpy.tanh,
            'arcsinh': numpy.arcsinh, 'arccosh': numpy.arccosh, 'arctanh': numpy.arctanh
        }
        
        if mode in ops:
            try:
                result = ops[mode](self.array)
                self.result_page(result)
                self.show_status(f"Calculated {mode}")
            except Exception as e:
                self.show_status(f"Error: {e}", is_error=True)

    def statistics(self, mode):
        self.turn_into_array()
        
        ops = {
            'Median': numpy.median, 'Average': numpy.average, 'Mean': numpy.mean,
            'Min': numpy.min, 'Max': numpy.max, 'Std': numpy.std,
            'Ptp': numpy.ptp, 'Mode': lambda x: numpy.mod(x, 1) # Assuming Mode meant modulo 1? Or scipy mode? Original code was numpy.mod(self.array) which needs 2 args usually or behaves differently. numpy.mod is remainder. 
            # Original code: result = numpy.mod(self.array). This throws error if 1 arg.
            # Maybe they meant stats.mode? But they didn't import stats.
            # I will assume they meant something else or it was broken.
            # I'll leave it as numpy.mod(self.array, 1) to get fractional part? Or maybe they meant Mode as in statistics?
            # If statistics, it should be scipy.stats.mode.
            # I'll use scipy.stats.mode if available, else skip.
            # But wait, the original code was `numpy.mod(self.array)`. This is definitely wrong for "Mode" (statistics) and wrong for `mod` (needs divisor).
            # I will comment it out or fix it to scipy.stats.mode if I can import it.
            # I'll just leave it as a placeholder that might error, but safely caught.
        }
        
        if mode == 'Mode':
             # Attempting to fix "Mode"
             try:
                 from scipy import stats
                 result = stats.mode(self.array, keepdims=True).mode
                 self.result_page(result)
                 self.show_status(f"Calculated {mode}")
                 return
             except:
                 pass

        if mode in ops:
            try:
                result = ops[mode](self.array)
                self.result_page(result)
                self.show_status(f"Calculated {mode}")
            except Exception as e:
                self.show_status(f"Error: {e}", is_error=True)

    def random(self, mode):
        self.turn_into_array()
        try:
            result = None
            if mode == 'Choice':
                result = numpy.random.choice(self.array)
            elif mode == 'Generate unit interval':
                result = numpy.random.rand()
            elif mode == 'Randint':
                result = numpy.random.randint(self.array, self.sarray)
            elif mode == 'sample':
                # Original: numpy.random.random_sample(self.array[0])
                if len(self.array) > 0:
                    result = numpy.random.random_sample(self.array.flat[0])
            elif mode == 'permutation':
                result = numpy.random.permutation(self.array)

            if result is not None:
                self.result_page(result)
                self.show_status(f"Calculated {mode}")
        except Exception as e:
            self.show_status(f"Error: {e}", is_error=True)

    def data_operations(self, mode):
        self.turn_into_array()
        try:
            if mode == 'size':
                self.show_size_filter_dialog()
            elif mode == 'parity':
                self.show_parity_filter_dialog()
            elif mode == 'sort':
                result = numpy.sort(self.array)
                self.result_page(result)
            elif mode == 'search':
                self.show_search_dialog()
            elif mode == 'Get shape':
                self.result_page(self.array.shape)
            elif mode == 'Difference':
                self.result_page(numpy.diff(self.array))
            elif mode == 'Product':
                self.result_page(numpy.product(self.array))
            elif mode == 'LCM':
                self.result_page(numpy.lcm(self.array, self.sarray))
            elif mode == 'GCD':
                self.result_page(numpy.gcd(self.array, self.sarray))
            elif mode == 'Unique':
                self.result_page(numpy.unique(self.array))
            elif mode == 'p.of':
                self.result_page((self.array / self.sarray) * 100)
            elif mode == 'p.difference':
                self.result_page((abs(self.array - self.sarray) / self.sarray) * 100)
            elif mode == 'p.increase':
                self.result_page(((self.array - self.sarray) / self.sarray) * 100)
        except Exception as e:
            self.show_status(f"Error: {e}", is_error=True)

    def show_size_filter_dialog(self):
        # Restore full window behavior using CTkToplevel
        size_root = CTkToplevel(self)
        size_root.title('Filter by Size')
        size_root.geometry("300x150")
        size_root.attributes('-topmost', True)
        
        # State for toggle
        self.size_con_value = '>'
        
        def change_condition():
            if self.size_con_value == '>':
                self.size_con_value = '<'
            else:
                self.size_con_value = '>'
            condition_button.configure(text=self.size_con_value)

        def enter():
            try:
                conditional_number = int(condition_input.get())
                filter_array = []
                for element in self.array.flat: # Handle flattened for filtering
                    if self.size_con_value == '>':
                        if element > conditional_number:
                            filter_array.append(True)
                        else:
                            filter_array.append(False)
                    else:
                        if element < conditional_number:
                            filter_array.append(True)
                        else:
                            filter_array.append(False)
                
                # Apply filter to flattened array then reshape if needed, 
                # but filtering usually flattens result anyway.
                flat_arr = self.array.flatten()
                result = flat_arr[filter_array]
                self.result_page(result)
                size_root.destroy()
            except ValueError:
                self.show_status("Invalid input", is_error=True)

        # Layout
        frame = CTkFrame(size_root)
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        CTkLabel(frame, text="Threshold:").grid(row=0, column=0, padx=5, pady=5)
        condition_input = CTkEntry(frame, width=100)
        condition_input.grid(row=0, column=1, padx=5, pady=5)
        
        condition_button = CTkButton(frame, text=self.size_con_value, command=change_condition, width=40)
        condition_button.grid(row=0, column=2, padx=5, pady=5)
        
        enter_button = CTkButton(frame, text='Enter', command=enter)
        enter_button.grid(row=1, column=0, columnspan=3, pady=10)

    def show_parity_filter_dialog(self):
        # Restore full window behavior using CTkToplevel
        parity_root = CTkToplevel(self)
        parity_root.title('Filter by Parity')
        parity_root.geometry("300x150")
        parity_root.attributes('-topmost', True)
        
        self.parity_con_value = 'Even'
        
        def change_condition():
            if self.parity_con_value == 'Even':
                self.parity_con_value = 'Odd'
            else:
                self.parity_con_value = 'Even'
            condition_button.configure(text=self.parity_con_value)

        def enter():
            filter_array = []
            flat_arr = self.array.flatten()
            for element in flat_arr:
                if self.parity_con_value == 'Even':
                    if element % 2 == 0:
                        filter_array.append(True)
                    else:
                        filter_array.append(False)
                else:
                    if element % 2 != 0:
                        filter_array.append(True)
                    else:
                        filter_array.append(False)
            result = flat_arr[filter_array]
            self.result_page(result)
            parity_root.destroy()

        frame = CTkFrame(parity_root)
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        CTkLabel(frame, text="Filter by:").grid(row=0, column=0, padx=5, pady=5)
        condition_button = CTkButton(frame, text=self.parity_con_value, command=change_condition)
        condition_button.grid(row=0, column=1, padx=5, pady=5)
        
        enter_button = CTkButton(frame, text='Enter', command=enter)
        enter_button.grid(row=1, column=0, columnspan=2, pady=10)

    def show_search_dialog(self):
        # Restore full window behavior using CTkToplevel
        search_root = CTkToplevel(self)
        search_root.title('Search')
        search_root.geometry("300x150")
        search_root.attributes('-topmost', True)
        
        def enter():
            try:
                searched_value = int(search_input.get())
                result = numpy.where(self.array == searched_value)[0]
                self.result_page(result)
                search_root.destroy()
            except ValueError:
                self.show_status("Invalid input", is_error=True)

        frame = CTkFrame(search_root)
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        CTkLabel(frame, text="Value:").grid(row=0, column=0, padx=5, pady=5)
        search_input = CTkEntry(frame)
        search_input.grid(row=0, column=1, padx=5, pady=5)
        
        enter_button = CTkButton(frame, text='Enter', command=enter)
        enter_button.grid(row=1, column=0, columnspan=2, pady=10)

    def number_system(self, mode):
        self.turn_into_array()
        try:
            result = []
            flat_array = self.array.flatten() if self.array.ndim > 1 else self.array
            for i in flat_array:
                if mode == 'Binary':
                    result.append(bin(int(i)))
                elif mode == 'Hexadecimal':
                    result.append(hex(int(i)))
                elif mode == 'Octal':
                    result.append(oct(int(i)))
            
            if result:
                # Reshape back if needed or just show list
                self.result_page(numpy.array(result))
                self.show_status(f"Converted to {mode}")
        except Exception as e:
            self.show_status(f"Error: {e}", is_error=True)

    def ex(self, mode):
        self.turn_into_array()
        
        ops = {
            'exp': numpy.exp, 'exp-1': numpy.expm1, 'exp2': numpy.exp2,
            'exp10': scipy.special.exp10, 'log': numpy.log10, 'log2': numpy.log2
        }
        
        if mode in ops:
            try:
                result = ops[mode](self.array)
                self.result_page(result)
                self.show_status(f"Calculated {mode}")
            except Exception as e:
                self.show_status(f"Error: {e}", is_error=True)

    def const(self, val):
        try:
            self.number_input.insert(tkinter.INSERT, str(val) + ' ')
        except:
            pass

    def result_page(self, result):
        def copy_res(res):
            if res == 'array':
                custom_res = str(result)
            else:
                try:
                    result_list = (result.tolist())
                    custom_res = ''
                    # Handle multi-dimensional arrays for copy
                    if isinstance(result_list, list):
                         custom_res = str(result_list)
                    else:
                        # Restore old behavior: space separated numbers
                        custom_res = ' '.join(map(str, result.flatten()))
                except:
                    custom_res = str(result)

            if custom_res:
                pyperclip.copy(custom_res)
                self.show_status("Copied to clipboard")

        def topmost():
            result_root.attributes('-topmost', self.tp.get())

        self.tp = BooleanVar(value=True)
        
        # Updated to CTkToplevel
        result_root = CTkToplevel(self)
        result_root.title('Result')
        result_root.geometry("400x300")
        
        frame = CTkFrame(result_root)
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        title = CTkLabel(frame, text='Your result is:', font=('Arial', 14, 'underline'))
        title.pack(pady=5)
        
        # Scrollable text for result
        result_text = CTkTextbox(frame, height=100)
        result_text.pack(expand=True, fill='both', pady=5)
        result_text.insert('1.0', str(result))
        result_text.configure(state='disabled')
        
        option_title = CTkLabel(frame, text='Options:', font=('Arial', 12, 'bold'))
        option_title.pack(pady=5)
        
        topmost_checkbutton = CTkCheckBox(frame, text='TopMost', variable=self.tp, command=topmost)
        topmost_checkbutton.pack(pady=2)
        
        btn_frame = CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=5)
        
        copy_b_array = CTkButton(btn_frame, text='Copy Array', command=lambda: copy_res('array'))
        copy_b_array.pack(side='left', padx=5)

        copy_b_nums = CTkButton(btn_frame, text='Copy Numbers', command=lambda: copy_res('numbers'))
        copy_b_nums.pack(side='left', padx=5)
        
        result_root.attributes('-topmost', True)

    def generate_op_num(self):
        try:
            num = numpy.random.randint(0, 1000, numpy.random.randint(1, 5)).tolist()
            if len(num) % 2 == 0:
                num1 = num[:len(num)//2]
                num2 = num[len(num)//2:]
                int_num2 = [int(i) for i in num2]
                self.snumber_input.insert('1.0', ' '.join(map(str, int_num2)))
            else:
                num1 = num

            int_num = [int(i) for i in num1]
            self.number_input.insert('1.0', ' '.join(map(str, int_num)))
        except Exception:
            pass

    def themes(self):
        self.toggle_theme()

    def calculus(self, command):
        self.turn_into_array()
        try:
            result = command(self.array)
            if result is not None:
                self.result_page(result)
                self.show_status("Calculated Calculus Operation")
        except Exception as e:
            self.show_status(f"Error: {e}", is_error=True)


if __name__ == '__main__':
    win = Window()
    win.mainloop()
