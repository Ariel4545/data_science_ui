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
            "theme": "Light"
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
        self.input_frame.grid_rowconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)

        # text boxes
        self.number_input = CTkTextbox(self.input_frame, wrap=tkinter.WORD)
        self.number_input.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        # Enable undo for the underlying tkinter Text widget
        self.number_input._textbox.config(undo=True)

        self.snumber_input = CTkTextbox(self.input_frame, wrap=tkinter.WORD, height=150)
        self.snumber_input.grid(row=1, column=0, sticky='nsew', pady=(5, 0))
        self.snumber_input._textbox.config(undo=True)

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
        else:
            customtkinter.set_appearance_mode('light')
            self.menu.configure(background='SystemButtonFace', foreground='black')
            for menu_ in self.menu_list:
                menu_.configure(background='SystemButtonFace', foreground='black')
            
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
        
        # Custom widgets for specific tabs
        if tab_name == 'Const':
            self.create_const_widgets(scrollable_frame, operations)
            return
        elif tab_name == 'Num Sys':
            self.create_num_sys_widgets(scrollable_frame, operations)
            return
        elif tab_name == 'Data':
            self.create_data_widgets(scrollable_frame, operations)
            return
        elif tab_name == 'Trig':
            self.create_trig_widgets(scrollable_frame, operations)
            return
        elif tab_name == 'Arithmetic':
            self.create_arithmetic_widgets(scrollable_frame, operations)
            return
        elif tab_name == 'Rounding':
            self.create_rounding_widgets(scrollable_frame, operations)
            return
        elif tab_name == 'Stats':
            self.create_stats_widgets(scrollable_frame, operations)
            return
        elif tab_name == 'Calculus':
            self.create_calculus_widgets(scrollable_frame, operations)
            return
        elif tab_name == 'Random':
            self.create_random_widgets(scrollable_frame, operations)
            return
        elif tab_name == 'Exponents':
            self.create_exponents_widgets(scrollable_frame, operations)
            return

        # Grid configuration for better layout
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        
        # Fallback for any other tabs
        for idx, op in enumerate(operations):
            # This part should ideally not be reached if all tabs are handled
            btn = CTkButton(scrollable_frame, text=op, height=32, font=("Arial", 12))
            btn.grid(row=idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")

    def create_const_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        
        label = CTkLabel(parent, text="Select Constant:", font=("Arial", 14, "bold"))
        label.grid(row=0, column=0, pady=(10, 5))
        
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
                
        btn = CTkButton(parent, text="Insert Value", command=insert_val)
        btn.grid(row=2, column=0, pady=20)

    def create_num_sys_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        
        label = CTkLabel(parent, text="Convert to System:", font=("Arial", 14, "bold"))
        label.grid(row=0, column=0, pady=(10, 5))
        
        self.num_sys_var = tkinter.StringVar(value=operations[0])
        seg_btn = CTkSegmentedButton(parent, values=operations, variable=self.num_sys_var)
        seg_btn.grid(row=1, column=0, pady=10)
        
        def convert():
            mode = self.num_sys_var.get()
            self.number_system(mode)
            
        btn = CTkButton(parent, text="Convert", command=convert)
        btn.grid(row=2, column=0, pady=20)

    def create_data_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)

        # Size Filter
        CTkLabel(parent, text="Filter by Size", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(5,0))
        self.data_size_entry = CTkEntry(parent, placeholder_text="Threshold")
        self.data_size_entry.grid(row=1, column=0, padx=2, pady=2)
        self.data_size_mode = CTkSegmentedButton(parent, values=[">", "<"])
        self.data_size_mode.set(">")
        self.data_size_mode.grid(row=1, column=1, padx=2, pady=2)
        CTkButton(parent, text="Apply", command=self.inline_size_filter, width=60).grid(row=1, column=2, padx=2, pady=2)

        # Parity Filter
        CTkLabel(parent, text="Filter by Parity", font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=3, pady=(10,0))
        self.data_parity_mode = CTkSegmentedButton(parent, values=["Even", "Odd"])
        self.data_parity_mode.set("Even")
        self.data_parity_mode.grid(row=3, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
        CTkButton(parent, text="Apply", command=self.inline_parity_filter, width=60).grid(row=3, column=2, padx=2, pady=2)

        # Search
        CTkLabel(parent, text="Search Value", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=3, pady=(10,0))
        self.data_search_entry = CTkEntry(parent, placeholder_text="Value")
        self.data_search_entry.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
        CTkButton(parent, text="Find", command=self.inline_search, width=60).grid(row=5, column=2, padx=2, pady=2)

        # Separator
        CTkLabel(parent, text="Operations", font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=3, pady=(15,5))

        # Other buttons
        handled = ['size', 'parity', 'search']
        others = [op for op in operations if op not in handled]
        
        btn_frame = CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=7, column=0, columnspan=3, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        
        for idx, op in enumerate(others):
            cmd = lambda o=op: self.data_operations(mode=o)
            btn = CTkButton(btn_frame, text=op, command=cmd, height=32)
            btn.grid(row=idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")

    def create_trig_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        groups = {
            "Standard": ['Sin', 'Cos', 'Tan'],
            "Conversion": ['d2r', 'r2d'],
            "Hyperbolic": ['sinh', 'cosh', 'tanh'],
            "Inverse Hyperbolic": ['arcsinh', 'arccosh', 'arctanh']
        }
        
        row = 0
        for group_name, ops in groups.items():
            CTkLabel(parent, text=group_name, font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=(10, 2))
            row += 1
            for idx, op in enumerate(ops):
                cmd = lambda o=op: self.trigonometry(o)
                btn = CTkButton(parent, text=op, command=cmd, height=32)
                r = row + idx // 2
                c = idx % 2
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="ew")
            row += (len(ops) + 1) // 2

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
        
        for idx, op in enumerate(calc_ops):
            if op in operations:
                cmd = lambda o=op: self.arithmetics(o)
                text = symbols.get(op, op)
                btn = CTkButton(parent, text=text, command=cmd, height=40, font=("Arial", 16, "bold"))
                btn.grid(row=idx // 4, column=idx % 4, padx=3, pady=3, sticky="ew")

    def create_rounding_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Rounding with decimals
        CTkLabel(parent, text="Rounding Precision", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(5,0))
        self.rounding_decimals_entry = CTkEntry(parent, placeholder_text="Decimals (default 0)")
        self.rounding_decimals_entry.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        CTkButton(parent, text="Round", command=lambda: self.round('Rounding')).grid(row=1, column=1, padx=2, pady=2, sticky="ew")
        
        # Other operations
        others = [op for op in operations if op != 'Rounding']
        CTkLabel(parent, text="Other Methods", font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=2, pady=(15,5))
        
        for idx, op in enumerate(others):
            cmd = lambda o=op: self.round(o)
            btn = CTkButton(parent, text=op, command=cmd, height=32)
            btn.grid(row=3 + idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")

    def create_stats_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        groups = {
            "Central Tendency": ['Mean', 'Median', 'Mode', 'Average'],
            "Extremes": ['Min', 'Max'],
            "Dispersion": ['Std', 'Ptp']
        }
        
        row = 0
        for group_name, ops in groups.items():
            CTkLabel(parent, text=group_name, font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=(10, 2))
            row += 1
            for idx, op in enumerate(ops):
                if op in operations:
                    cmd = lambda o=op: self.statistics(o)
                    btn = CTkButton(parent, text=op, command=cmd, height=32)
                    r = row + idx // 2
                    c = idx % 2
                    btn.grid(row=r, column=c, padx=5, pady=5, sticky="ew")
            row += (len(ops) + 1) // 2

    def create_calculus_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Linspace Generator
        CTkLabel(parent, text="Linspace Generator", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(5,0))
        
        self.linspace_start = CTkEntry(parent, placeholder_text="Start")
        self.linspace_start.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        self.linspace_stop = CTkEntry(parent, placeholder_text="Stop")
        self.linspace_stop.grid(row=1, column=1, padx=2, pady=2, sticky="ew")
        self.linspace_num = CTkEntry(parent, placeholder_text="Count (default 50)")
        self.linspace_num.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
        
        CTkButton(parent, text="Generate Linspace", command=self.inline_linspace).grid(row=3, column=0, columnspan=2, padx=2, pady=5, sticky="ew")
        
        # Other operations
        others = [op for op in operations if op != 'Line space']
        CTkLabel(parent, text="Operations", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=(15,5))
        
        for idx, op in enumerate(others):
            func = None
            if op == 'Integrate': func = scipy.integrate
            elif op == 'Integration sum': func = numpy.cumsum
            
            if func:
                cmd = lambda f=func: self.calculus(f)
                btn = CTkButton(parent, text=op, command=cmd, height=32)
                btn.grid(row=5 + idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")

    def create_random_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Random Integer Generator
        CTkLabel(parent, text="Generate Random Integers", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(5,0))
        self.randint_min = CTkEntry(parent, placeholder_text="Min")
        self.randint_min.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        self.randint_max = CTkEntry(parent, placeholder_text="Max")
        self.randint_max.grid(row=1, column=1, padx=2, pady=2, sticky="ew")
        self.randint_size = CTkEntry(parent, placeholder_text="Count (optional)")
        self.randint_size.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
        CTkButton(parent, text="Generate", command=self.inline_randint).grid(row=3, column=0, columnspan=2, padx=2, pady=5, sticky="ew")

        # Array Operations
        CTkLabel(parent, text="Array Operations", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=(15,5))
        array_ops = ['Choice', 'permutation', 'sample']
        for idx, op in enumerate(array_ops):
            if op in operations:
                cmd = lambda o=op: self.random(o)
                btn = CTkButton(parent, text=op, command=cmd, height=32)
                btn.grid(row=5 + idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")

        # Other
        CTkLabel(parent, text="Other", font=("Arial", 12, "bold")).grid(row=7, column=0, columnspan=2, pady=(15,5))
        if 'Generate unit interval' in operations:
            cmd = lambda: self.random('Generate unit interval')
            CTkButton(parent, text="Unit Interval (0-1)", command=cmd, height=32).grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def create_exponents_widgets(self, parent, operations):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Powers
        CTkLabel(parent, text="Exponential Functions", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(5,0))
        powers = ['exp', 'exp2', 'exp10', 'exp-1']
        for idx, op in enumerate(powers):
            if op in operations:
                cmd = lambda o=op: self.ex(o)
                btn = CTkButton(parent, text=op, command=cmd, height=32)
                btn.grid(row=1 + idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")

        # Logarithms
        CTkLabel(parent, text="Logarithmic Functions", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=(15,5))
        logs = ['log', 'log2']
        for idx, op in enumerate(logs):
            if op in operations:
                cmd = lambda o=op: self.ex(o)
                btn = CTkButton(parent, text=op, command=cmd, height=32)
                btn.grid(row=4 + idx // 2, column=idx % 2, padx=5, pady=5, sticky="ew")

        # Custom Base
        CTkLabel(parent, text="Custom Base", font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=2, pady=(15,5))
        self.custom_base_entry = CTkEntry(parent, placeholder_text="Base (e.g. 5)")
        self.custom_base_entry.grid(row=7, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
        
        CTkButton(parent, text="Log(Base)", command=lambda: self.inline_custom_base('log')).grid(row=8, column=0, padx=2, pady=5, sticky="ew")
        CTkButton(parent, text="Power(Base)", command=lambda: self.inline_custom_base('power')).grid(row=8, column=1, padx=2, pady=5, sticky="ew")

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
            pass

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
            pass

    def inline_linspace(self):
        try:
            start = float(self.linspace_start.get())
            stop = float(self.linspace_stop.get())
            num_str = self.linspace_num.get()
            num = int(num_str) if num_str else 50
            
            result = numpy.linspace(start, stop, num)
            self.result_page(result)
        except ValueError:
            pass

    def inline_randint(self):
        try:
            min_val = int(self.randint_min.get())
            max_val = int(self.randint_max.get())
            size_str = self.randint_size.get()
            size = int(size_str) if size_str else None
            
            result = numpy.random.randint(min_val, max_val, size)
            self.result_page(result)
        except ValueError:
            # Fallback to array based if inputs empty, or just pass
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
            pass

    def turn_into_array(self):
        self.content = self.number_input.get('1.0', 'end')
        self.list = self.content.split()
        
        try:
            self.array = numpy.array(self.list, dtype='int32')
        except ValueError:
             print("Error converting to array")
             self.array = numpy.array([])

        print(self.list)
        print(self.array)
        try:
            self.scontent = self.snumber_input.get('1.0', 'end')
            self.slist = self.scontent.split()
            self.sarray = numpy.array(self.slist, dtype='int32')
            return self.sarray
        except:
            pass
        return self.array

    def arithmetics(self, mode):
        self.turn_into_array()
        result = None
        if mode == 'Addition':
            result = (numpy.add(self.array, self.sarray))
        elif mode == 'Subtraction':
            result = numpy.subtract(self.array, self.sarray)
        elif mode == 'Multiplication':
            result = numpy.multiply(self.array, self.sarray)
        elif mode == 'Division':
            result = numpy.divide(self.array, self.sarray)
        elif mode == 'Power':
            result = numpy.power(self.array, self.sarray)
        elif mode == 'Remainder':
            result = numpy.remainder(self.array, self.sarray)
        elif mode == 'Absolute':
            result = numpy.abs(self.array)
        elif mode == 'square root':
            result = numpy.sqrt(self.array)
        elif mode == 'square':
            result = numpy.square(self.array)
        elif mode == 'Factorial':
            result = numpy.math.factorial(self.array)
        
        if result is not None:
             self.result_page(result)

    def round(self, mode):
        self.turn_into_array()
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

    def trigonometry(self, mode):
        self.turn_into_array()
        result = None
        if mode == 'Sin':
            result = numpy.sin(self.array)
        elif mode == 'Cos':
            result = numpy.cos(self.array)
        elif mode == 'Tan':
            result = numpy.tan(self.array)
        elif mode == 'd2r':
            result = numpy.deg2rad(self.array)
        elif mode == 'r2d':
            result = numpy.rad2deg(self.array)
        elif mode == 'sinh':
            result = numpy.sinh(self.array)
        elif mode == 'cosh':
            result = numpy.cosh(self.array)
        elif mode == 'tanh':
            result = numpy.tanh(self.array)
        elif mode == 'arcsinh':
            result = numpy.arcsinh(self.array)
        elif mode == 'arccosh':
            result = numpy.arccosh(self.array)
        elif mode == 'arctanh':
            result = numpy.arctanh(self.array)
        
        if result is not None:
            self.result_page(result)

    def statistics(self, mode):
        self.turn_into_array()
        result = None
        if mode == 'Median':
            result = numpy.median(self.array)
        elif mode == 'Average':
            result = numpy.average(self.array)
        elif mode == 'Mean':
            result = numpy.mean(self.array)
        elif mode == 'Min':
            result = numpy.min(self.array)
        elif mode == 'Max':
            result = numpy.max(self.array)
        elif mode == 'Std':
            result = numpy.std(self.array)
        elif mode == 'Ptp':
            result = numpy.ptp(self.array)
        elif mode == 'Mode':
            result = numpy.mod(self.array)
        
        if result is not None:
            self.result_page(result)

    def random(self, mode):
        self.turn_into_array()
        result = None
        if mode == 'Choice':
            result = numpy.random.choice(self.array)
        elif mode == 'Generate unit interval':
            result = numpy.random.rand()
        elif mode == 'Randint':
            result = numpy.random.randint(self.array, self.sarray)
        elif mode == 'sample':
            result = numpy.random.random_sample(self.array[0])
        elif mode == 'permutation':
            result = numpy.random.permutation(self.array)

        if result is not None:
            self.result_page(result)

    def data_operations(self, mode):
        self.turn_into_array()
        if mode == 'size':
            def change_condition():
                if self.size_con_value == '>':
                    self.size_con_value = '<'
                else:
                    self.size_con_value = '>'
                condition_button.configure(text=self.size_con_value)

            def enter():
                filter_array = []
                try:
                    conditional_number = int(condition_input.get())
                    for element in self.array:
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
                    result = self.array[filter_array]
                    self.result_page(result)
                except ValueError:
                    pass
                size_root.destroy()

            self.size_con_value = '>'
            size_root = CTkToplevel()
            size_root.title('filter by sizes')
            condition_input = CTkEntry(size_root)
            condition_button = CTkButton(size_root, text=self.size_con_value, command=change_condition)
            condition_label = CTkLabel(size_root, text='your Array')
            enter_button = CTkButton(size_root, text='Enter', command=enter)
            condition_input.grid(row=1, column=0)
            condition_button.grid(row=1, column=1)
            condition_label.grid(row=1, column=2)
            enter_button.grid(row=2, column=1)
        elif mode == 'parity':
            def change_condition():
                if self.parity_con_value == 'even':
                    self.parity_con_value = 'odd'
                else:
                    self.parity_con_value = 'even'
                condition_button.configure(text=self.parity_con_value)

            def enter():
                filter_array = []
                for element in self.array:
                    if self.parity_con_value == 'even':
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

            parity_root = CTkToplevel()
            self.parity_con_value = 'even'
            parity_root.title('filter by parity')
            condition_button = CTkButton(parity_root, text=self.parity_con_value, command=change_condition)
            condition_text = CTkLabel(parity_root, text='filter by:')
            enter_button = CTkButton(parity_root, text='Enter', command=enter)
            condition_text.grid(row=1, column=0)
            condition_button.grid(row=1, column=1)
            enter_button.grid(row=2, column=1)

        elif mode == 'sort':
            result = numpy.sort(self.array)
            self.result_page(result)

        elif mode == 'search':
            def enter():
                try:
                    searched_value = int(search_input.get())
                    result = numpy.where(self.array == searched_value)[0]
                    self.result_page(result)
                except ValueError:
                    pass

            search_root = CTkToplevel()
            search_root.title('search')
            search_input = CTkEntry(search_root)
            enter_button = CTkButton(search_root, text='Enter', command=enter)
            search_input.grid(row=1, column=1)
            enter_button.grid(row=2, column=1)

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

    def number_system(self, mode):
        self.turn_into_array()
        result = []
        for i in self.array:
            if mode == 'Binary':
                result.append(bin(i))
            elif mode == 'Hexadecimal':
                result.append(hex(i))
            elif mode == 'Octal':
                result.append(oct(i))
        
        if result:
            self.result_page(numpy.array(result))

    def ex(self, mode):
        self.turn_into_array()
        result = None
        if mode == 'exp':
            result = numpy.exp(self.array)
        elif mode == 'exp-1':
            result = numpy.expm1(self.array)
        elif mode == 'exp2':
            result = numpy.exp2(self.array)
        elif mode == 'exp10':
            result = scipy.special.exp10(self.array)
        elif mode == 'log':
            result = numpy.log10(self.array)
        elif mode == 'log2':
            result = numpy.log2(self.array)

        if result is not None:
            self.result_page(result)

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
                    for r in result_list:
                        custom_res += str(r)
                        if not(r == result_list[-1]):
                            custom_res += ' '
                except:
                    custom_res = str(result)

            if custom_res:
                pyperclip.copy(custom_res)

        def topmost():
            result_root.attributes('-topmost', self.tp.get())

        self.tp = BooleanVar()
        self.tp.set(True)
        result_root = tkinter.Toplevel()
        result_root.title('Numpy')
        frame = CTkFrame(result_root)
        title = CTkLabel(frame, text=f'Your result is:', font=('arial', 12, 'underline'))
        result_output = CTkLabel(frame, text=f'{result}')
        option_title = CTkLabel(frame, text='Options:', font=('arial', 12, 'underline'))
        topmost_checkbutton = CTkCheckBox(frame, text='TopMost', variable=self.tp, command=topmost)
        copy_b_array = CTkButton(frame, text='Copy array', command=lambda: copy_res('array'), width=10)
        copy_b_num = CTkButton(frame, text='Copy numbers', command=lambda: copy_res('numbers'), width=10)
        frame.pack(expand=True, fill=BOTH)
        title.pack(pady=2)
        result_output.pack(expand=True, fill=BOTH)
        option_title.pack(pady=2)
        topmost_checkbutton.pack(pady=2)
        copy_b_array.pack(pady=2)
        copy_b_num.pack(pady=2)

        result_root.update()
        win_w, win_h = result_root.winfo_width() + 100, result_root.winfo_height()
        enum_x, enum_y = (self.winfo_x()), (self.winfo_y())
        enum_w, enum_h = self.winfo_width(), self.winfo_height()
        mid_x, mid_y = (round(enum_x + (enum_w / 2) - (win_w / 2))), (round(enum_y + (enum_h / 2) - (win_h / 2)))
        if abs(mid_y - self.winfo_screenheight()) <= 80:
            mid_y = (self.winfo_screenheight() // 2)
            print(mid_y)
        result_root.geometry(f'{win_w}x{win_h}+{mid_x}+{mid_y}')

    def generate_op_num(self):
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

    def themes(self):
        # Deprecated, use toggle_theme
        self.toggle_theme()

    def calculus(self, command):
        self.turn_into_array()
        result = command(self.array)
        if result is not None:
            self.result_page(result)


if __name__ == '__main__':
    win = Window()
    win.mainloop()
