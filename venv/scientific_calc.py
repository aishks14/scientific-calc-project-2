import tkinter as tk
from tkinter import ttk
from math import sin, cos, tan, log, log10, sqrt, factorial, floor, ceil, pi, e, exp, radians
import constants

# --------------- Main Scientific Calculator Class ----------------
class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.expression = ""
        self.mod_first = None
        self.power_first = None
        self.just_evaluated = False
        self.overflowed = False

        style = ttk.Style()
        style.theme_use("clam")

        # ---------------- Displays ----------------
        self.total_var = tk.StringVar()
        self.display_var = tk.StringVar()

        self.total_label = tk.Label(root, textvariable=self.total_var,
                                    font=(constants.SEGOE_UI, 16), anchor="e",
                                    bg="#f9f9f9", fg="gray", height=3, pady=5)
        self.total_label.grid(row=0, column=0, columnspan=6, padx=10, pady=(10, 0), sticky="nsew")

        self.display = tk.Label(root, textvariable=self.display_var,
                                font=(constants.SEGOE_UI, 28), anchor="e",
                                bg="#f9f9f9", fg="black", height=2, pady=10)
        self.display.grid(row=1, column=0, columnspan=6, padx=10, pady=(0, 15), sticky="nsew")

        separator = tk.Frame(root, bg="#25265E", height=5)
        separator.grid(row=2, column=0, columnspan=6, sticky="ew", pady=(0, 8))
        separator.grid_propagate(False)

        for i in range(11):
            root.rowconfigure(i, weight=1)
        for j in range(6):
            root.columnconfigure(j, weight=1)

        # ---------------- Buttons that appear on the calculator ----------------
        buttons = [
            ("(", 3, 0, lambda: self.add("("), constants.CALC_BUTTON_STYLE, 1),
            (")", 3, 1, lambda: self.add(")"), constants.CALC_BUTTON_STYLE, 1),
            ("mod", 3, 2, lambda: self.show_mod(), constants.CALC_BUTTON_STYLE, 1),
            ("C", 3, 3, self.clear_all, constants.CLEAR_BUTTON_STYLE, 1),
            ("\u232B", 3, 4, self.clear_entry, constants.CLEAR_BUTTON_STYLE, 1),
            ("±", 3, 5, self.toggle_sign, constants.OPERATOR_STYLE, 1),

            ("/", 4, 5, lambda: self.add("/"), constants.OPERATOR_STYLE, 1),
            ("sin", 4, 0, self.calculate_sin, constants.CALC_BUTTON_STYLE, 1),
            ("cos", 4, 1, self.calculate_cos, constants.CALC_BUTTON_STYLE, 1),
            ("tan", 4, 2, self.calculate_tan, constants.CALC_BUTTON_STYLE, 1),
            ("log", 4, 3, self.calculate_log, constants.CALC_BUTTON_STYLE, 1),
            ("ln", 4, 4, self.calculate_ln, constants.CALC_BUTTON_STYLE, 1),

            ("x", 5, 5, lambda: self.add("*"), constants.OPERATOR_STYLE, 1),
            ("csc", 5, 0, self.calculate_csc, constants.CALC_BUTTON_STYLE, 1),
            ("sec", 5, 1, self.calculate_sec, constants.CALC_BUTTON_STYLE, 1),
            ("cot", 5, 2, self.calculate_cot, constants.CALC_BUTTON_STYLE, 1),
            ("exp", 5, 3, self.calculate_exp, constants.CALC_BUTTON_STYLE, 1),
            ("10ˣ", 5, 4, lambda: self.add("10**"), constants.CALC_BUTTON_STYLE, 1),

            ("-", 6, 5, lambda: self.add("-"), constants.OPERATOR_STYLE, 1),
            ("√", 6, 0, lambda: self.show_square_root(), constants.CALC_BUTTON_STYLE, 1),
            ("x\u00B2", 6, 1, self.show_square, constants.CALC_BUTTON_STYLE, 1),
            ("x\u00B3", 6, 2, lambda: self.show_cube(), constants.CALC_BUTTON_STYLE, 1),
            ("\u221B", 6, 3, lambda: self.show_cube_root(), constants.CALC_BUTTON_STYLE, 1),
            ("1/x", 6, 4, self.reciprocal, constants.CALC_BUTTON_STYLE, 1),

            ("+", 7, 5, lambda: self.add("+"), constants.OPERATOR_STYLE, 2),
            ("π", 7, 0, lambda: self.add(str(pi)), constants.CALC_BUTTON_STYLE, 1),
            ("e", 7, 1, lambda: self.add(str(e)), constants.CALC_BUTTON_STYLE, 1),
            ("7", 7, 2, lambda: self.add("7"), constants.NUMBER_BUTTON_STYLE, 1),
            ("8", 7, 3, lambda: self.add("8"), constants.NUMBER_BUTTON_STYLE, 1),
            ("9", 7, 4, lambda: self.add("9"), constants.NUMBER_BUTTON_STYLE, 1),

            ("n!", 8, 0, self.show_factorial, constants.CALC_BUTTON_STYLE, 1),
            ("^", 8, 1, self.show_power, constants.CALC_BUTTON_STYLE, 1),
            ("4", 8, 2, lambda: self.add("4"), constants.NUMBER_BUTTON_STYLE, 1),
            ("5", 8, 3, lambda: self.add("5"), constants.NUMBER_BUTTON_STYLE, 1),
            ("6", 8, 4, lambda: self.add("6"), constants.NUMBER_BUTTON_STYLE, 1),

            ("| x |", 10, 1, lambda: self.show_absolute(), constants.CALC_BUTTON_STYLE, 1),
            ("1", 9, 2, lambda: self.add("1"), constants.NUMBER_BUTTON_STYLE, 1),
            ("2", 9, 3, lambda: self.add("2"), constants.NUMBER_BUTTON_STYLE, 1),
            ("3", 9, 4, lambda: self.add("3"), constants.NUMBER_BUTTON_STYLE, 1),
            ("=", 9, 5, self.evaluate, constants.EQUAL_BUTTON_STYLE, 2),
            ("\u230Ax\u230B", 9, 0, self.calculate_floor, constants.CALC_BUTTON_STYLE, 1),
            ("\u2308x\u2309", 9, 1, self.calculate_ceil, constants.CALC_BUTTON_STYLE, 1),

            
            ("0", 10, 3, lambda: self.add("0"), constants.NUMBER_BUTTON_STYLE, 1),
            ("00", 10, 4, lambda: self.add("00"), constants.NUMBER_BUTTON_STYLE, 1),
            (".", 10, 2, lambda: self.add("."), constants.NUMBER_BUTTON_STYLE, 1),
        ]

        self.all_buttons = []
        for (text, r, c, cmd, style_name, rowspan) in buttons:
            b = ttk.Button(root, text=text, command=cmd, style=style_name)
            b.grid(row=r, column=c, rowspan=rowspan, sticky="nsew", padx=3, pady=3, ipadx=5, ipady=8)
            self.all_buttons.append((b, style_name))

        # ------------ Theme of toggle button ------------------
        self.theme_btn = ttk.Button(
            root,
            text = "\U0001F319",  # Moon initially
            command=self.toggle_theme,
            style=constants.CALC_BUTTON_STYLE
        )
        self.theme_btn.grid(row=10, column=0, sticky="nsew", padx=3, pady=3, ipadx=5, ipady=8)
        self.all_buttons.append((self.theme_btn, constants.CALC_BUTTON_STYLE))

        root.bind("<Key>", self.key_input)
        root.bind("<Return>", lambda event: self.evaluate())
        root.bind("<BackSpace>", lambda event: self.backspace())

        self.current_theme = "day"
        self.apply_theme("day")

    # ---------------- DAY and NIGHT THEMES ----------------
    def apply_theme(self, theme):
        style = ttk.Style()
        if theme == "day":
            bg_main = constants.BG_MAIN_DAY
            text_fg = constants.BLACK
            display_bg = constants.BG_MAIN_DAY
            total_fg = constants.TOTAL_FG_DAY

            style.configure(constants.NUMBER_BUTTON_STYLE, font=(constants.SEGOE_UI, 14), background="#ffffff", foreground=text_fg, padding=10)
            style.configure(constants.CALC_BUTTON_STYLE, font=(constants.SEGOE_UI, 13), background="#f3f3f3", foreground=text_fg, padding=10)
            style.configure(constants.OPERATOR_STYLE, font=(constants.SEGOE_UI, 14), background="#0078D7", foreground=constants.WHITE, padding=10)
            style.configure(constants.EQUAL_BUTTON_STYLE, font=(constants.SEGOE_UI, 14, "bold"), background="#0078D7", foreground=constants.WHITE, padding=10)
            style.configure(constants.CLEAR_BUTTON_STYLE, font=(constants.SEGOE_UI, 13), background="#ffd6d6", foreground=text_fg, padding=10)
        else:
            bg_main = constants.BG_MAIN_NIGHT
            text_fg = constants.WHITE
            display_bg = constants.DISPLAY_BG_NIGHT
            total_fg = constants.TOTAL_FG_NIGHT

            style.configure(constants.NUMBER_BUTTON_STYLE, font=(constants.SEGOE_UI, 14), background="#3c3c3c", foreground=text_fg, padding=10)
            style.configure(constants.CALC_BUTTON_STYLE, font=(constants.SEGOE_UI, 13), background="#101010", foreground=text_fg, padding=10)
            style.configure(constants.OPERATOR_STYLE, font=(constants.SEGOE_UI, 14), background="#005a9e", foreground=constants.WHITE, padding=10)
            style.configure(constants.EQUAL_BUTTON_STYLE, font=(constants.SEGOE_UI, 14, "bold"), background="#008080", foreground=constants.WHITE, padding=10)
            style.configure(constants.CLEAR_BUTTON_STYLE, font=(constants.SEGOE_UI, 13), background="#663333", foreground=text_fg, padding=10)

            style.map("TButton", foreground=[("active", "black")])

        self.root.configure(bg=bg_main)
        self.display.configure(bg=display_bg, fg=text_fg)
        self.total_label.configure(bg=display_bg, fg=total_fg)

    def toggle_theme(self):
        if self.current_theme == "day":
            self.current_theme = "night"
            self.theme_btn.config(text = "\u2600")
        else:
            self.current_theme = "day"
            self.theme_btn.config(text = "\U0001F319")
        self.apply_theme(self.current_theme)

    # ---------------- UTILITIES: Methods to help main functions ----------------
    def _convert_number(self, num):
        if isinstance(num, float) and num.is_integer():
            return int(num)
        return num

    def format_result(self, result):
        try:
            if isinstance(result, float) and result.is_integer():
                s = str(int(result))
            elif isinstance(result, (int,)):
                s = str(result)
            elif isinstance(result, float):
                absr = abs(result)
                if (absr != 0 and (absr >= 1e10 or absr < 1e-6)):
                    s = constants.SCIENTIFIC_NOTATION_FORMAT.format(result)
                else:
                    s = constants.SCIENTIFIC_NOTATION_FORMAT.format(result)
            else:
                s = str(result)
            if len(s) > constants.MAX_DISPLAY_CHARS:
                try:
                    s = constants.SCIENTIFIC_NOTATION_FORMAT.format(float(result))
                except Exception:
                    s = s[:constants.MAX_DISPLAY_CHARS-3] + "..."
            return s
        except Exception:
            return str(result)

    def fit_display_and_set(self, text):
        if isinstance(text, (int, float)):
            text = self.format_result(text)
        else:
            text = str(text)

        if len(text) > constants.MAX_DISPLAY_CHARS:
            try:
                f = float(text)
                text = self.format_result(f)
            except Exception:
                text = text[:constants.MAX_DISPLAY_CHARS-3] + "..."
        self.display_var.set(text)

    def safe_set_result(self, result):
        if self.overflowed:
            return

        try:
            result_str = str(result)

            if len(result_str) > 14:
                result_str = constants.RESULT_FORMAT_SCI.format(float(result))

            if len(result_str) > 20:
                self.display_var.set("Overflow")
                self.total_var.set("")
                self.expression = ""
                self.overflowed = True
                return

            self.display_var.set(result_str)
            self.expression = result_str

        except Exception:
            self.display_var.set("Overflow")
            self.total_var.set("")
            self.expression = ""
            self.overflowed = True
        
    # ---------------- CALCULATOR FUNCTIONS ----------------
    def add(self, value):
        if self.expression == "Error":
            self.expression = ""
        if self.overflowed:
            self.expression = ""
            self.overflowed = False
            self.total_var.set("")
            self.display_var.set("")
        if self.just_evaluated:
            if str(value).replace(".", "", 1).isdigit():    
                self.expression = "" 
            self.just_evaluated = False
        
        self.expression += str(value)
        self.display_var.set(self.expression)

    def clear_all(self):
        self.expression = ""
        self.mod_first = None
        self.power_first = None
        self.total_var.set("")
        self.display_var.set("")
        self.overflowed = False

    def clear_entry(self):
        self.expression = self.expression[:-1]
        self.display_var.set(self.expression)

    def backspace(self):
        self.clear_entry()

    def toggle_sign(self):
        if self.expression:
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.display_var.set(self.expression)

    def show_mod(self):
        try:
            if not self.expression.strip():
                self.display_var.set(constants.EMPTY_INPUT)
                return
            first = self._convert_number(eval(self.expression))
            self.mod_first = first
            self.total_var.set(f"{first} Mod")
            self.expression = ""
            self.display_var.set("")
        except Exception as e:
            print(f"Error occurred: {e}")
            self.display_var.set("Error")
            self.expression = ""
            self.mod_first = None

    def execute_mod(self):
        try:
            if self.mod_first is None:
                self.display_var.set("Error")
                return
            second = self._convert_number(eval(self.expression)) if self.expression.strip() else 0
            if second == 0:
                result = self.mod_first
            else:
                result = self.mod_first % second
            self.total_var.set(f"{self.mod_first} Mod {second}")
            self.fit_display_and_set(result)
            self.expression = str(result)
            self.mod_first = None
        except Exception as e:
            print(f"Error occurred: {e}")
            self.display_var.set("Error")
            self.expression = ""
            self.mod_first = None

    def calculate_floor(self):
        try:
            value = self.acquire_current_value()
            result = floor(value)
            self.total_var.set(f"floor({self._convert_number(value)})")
            self.fit_display_and_set(result)
            self.expression = str(result)
        except Exception:
            self.total_var.set("")
            self.display_var.set("Error")
            self.expression = ""

    def calculate_ceil(self):
        try:
            value = self.acquire_current_value()
            result = ceil(value)
            self.total_var.set(f"ceil({self._convert_number(value)})")
            self.fit_display_and_set(result)
            self.expression = str(result)
        except Exception:
            self.total_var.set("")
            self.display_var.set("Error")
            self.expression = ""
            
    # ---------- TRIGONOMETRIC FUNCTIONS ----------
    def acquire_current_value(self):
        try:
            if not self.expression.strip():
                return 0.0
            return float(eval(self.expression))
        except Exception:
            return 0.0

    def calculate_sin(self):
        try:
            value = self.acquire_current_value()
            result = round(sin(radians(value)), 10)
            self.total_var.set(f"sin({self._convert_number(value)})")
            self.fit_display_and_set(result)
            self.expression = str(result)
        except Exception:
            self.total_var.set("")
            self.display_var.set("Error")
            self.expression = ""

    def calculate_cos(self):
        try:
            value = self.acquire_current_value()
            result = round(cos(radians(value)), 10)
            self.total_var.set(f"cos({self._convert_number(value)})")
            self.fit_display_and_set(result)
            self.expression = str(result)
        except Exception:
            self.total_var.set("")
            self.display_var.set("Error")
            self.expression = ""

    def calculate_tan(self):
        try:
            value = self.acquire_current_value()
            result = round(tan(radians(value)), 10)
            self.total_var.set(f"tan({self._convert_number(value)})")
            self.fit_display_and_set(result)
            self.expression = str(result)
        except Exception:
            self.total_var.set("")
            self.display_var.set("Error")
            self.expression = ""
            
    def calculate_csc(self):
        try:
            value = self.acquire_current_value()
            rad = radians(value)
            if sin(rad) == 0:
                raise ZeroDivisionError
            result = round(1 / sin(rad), 10)
            self.total_var.set(f"cosec({self._convert_number(value)})")
            self.fit_display_and_set(result)
            self.expression = str(result)
        except ZeroDivisionError:
            self.total_var.set("")
            self.display_var.set(constants.ZERO_DIVISION)
            self.expression = ""
        except Exception:
            self.total_var.set("")
            self.display_var.set("Error")
            self.expression = ""

    def calculate_sec(self):
        try:
            value = self.acquire_current_value()
            rad = radians(value)
            self.total_var.set(f"sec({self._convert_number(value)})") 
            tolerance = 1e-10
            if abs(cos(rad)) < tolerance:
                raise ZeroDivisionError
            result = round(1 / cos(rad), 10)
            self.total_var.set(f"sec({self._convert_number(value)})")
            self.fit_display_and_set(result)
            self.expression = str(result)
        except ZeroDivisionError:
            self.total_var.set("")
            self.display_var.set(constants.ZERO_DIVISION)
            self.expression = ""
        except Exception:
            self.total_var.set("")
            self.display_var.set("Error")
            self.expression = ""

    def calculate_cot(self):
        try:
            value = self.acquire_current_value()
            rad = radians(value)
            if tan(rad) == 0:
                raise ZeroDivisionError
            result = round(1 / tan(rad), 10)
            self.total_var.set(f"cot({self._convert_number(value)})")
            self.fit_display_and_set(result)
            self.expression = str(result)
        except ZeroDivisionError:
            self.total_var.set("")
            self.display_var.set(constants.ZERO_DIVISION)
            self.expression = ""
        except Exception:
            self.total_var.set("")
            self.display_var.set("Error")
            self.expression = ""
    
    # ---------- LOGRITHMIC FUNCTIONS ------------
    
    def calculate_log(self):
        try:
            current_value = self.display_var.get().strip()

            if not current_value or float(current_value) == 0.0:
                self.display_var.set(constants.INVALID_INPUT)
                self.total_var.set("")
                self.expression = ""
                return

            value = float(current_value)
            result = log10(value)

            self.total_var.set(f"log10({value})")
            self.fit_display_and_set(result)
            self.expression = str(result)

        except Exception:
            self.display_var.set("Error")
            self.total_var.set("")
            self.expression = ""

    def calculate_ln(self):
        try:
            current_value = self.display_var.get().strip()

            if not current_value or float(current_value) == 0.0:
                self.display_var.set(constants.INVALID_INPUT)
                self.total_var.set("")
                self.expression = ""
                return

            value = float(current_value)
            result = log(value)

            self.total_var.set(f"ln({value})")
            self.fit_display_and_set(result)
            self.expression = str(result)

        except Exception:
            self.display_var.set("Error")
            self.total_var.set("")
            self.expression = ""
     
    # ---------- EXPONENTIAL FUNCTION ------------       
    def calculate_exp(self):
        try:
            current_value = self.display_var.get().strip()
            if not current_value:
                current_value = "0"
            exp_expr = f"{current_value}.e+0"
            self.display_var.set(exp_expr)
            self.expression = exp_expr
            self.total_var.set(f"exp({current_value})")
        except Exception:
            self.display_var.set("Error")
            self.total_var.set("")
            self.expression = ""

    # ---------- Evaluate ----------
    def evaluate(self):
        try:
            # finalize pending modes
            if hasattr(self, "cube_mode") and self.cube_mode:
                if self.total_var.get().startswith("cube("):
                    self.total_var.set(self.total_var.get() + " =")
                self.cube_mode = False
            if hasattr(self, "cuberoot_mode") and self.cuberoot_mode:
                if self.total_var.get().startswith("∛("):
                    self.total_var.set(self.total_var.get() + " =")
                self.cuberoot_mode = False
            if hasattr(self, "abs_mode") and self.abs_mode:
                if self.total_var.get().startswith("|"):
                    self.total_var.set(self.total_var.get() + " =")
                self.abs_mode = False

            if self.mod_first is not None:
                self.execute_mod()
                return

            if self.power_first is not None:
                a = float(self.power_first)
                b = float(self.expression) if self.expression.strip() else 0.0
                result = a ** b
                self.total_var.set(f"{a}^{b} =")
                self.fit_display_and_set(result)
                self.expression = str(result)
                self.power_first = None
                return

            # replace ^ with ** if user used caret
            expr = self.expression.replace("^", "**")

            # ensure sin/cos/tan take degrees (wrap arguments in radians)
            expr = expr.replace("sin(", "sin(radians(")
            expr = expr.replace("cos(", "cos(radians(")
            expr = expr.replace("tan(", "tan(radians(")

            allowed = {
                "sin": sin, "cos": cos, "tan": tan,
                "log": log, "log10": log10, "sqrt": sqrt,
                "factorial": factorial, "exp": exp,
                "pi": pi, "e": e, "radians": radians
            }

            # Evaluate safely
            result = eval(expr, {"__builtins__": None}, allowed)

            # Prefer showing the human-friendly expression if available
            display_expr = self.total_var.get().strip() or self.expression

            # Prevent multiple " ="
            if not display_expr.endswith("="):
                self.total_var.set(f"{display_expr} =")
            else:
                self.total_var.set(display_expr)

            self.fit_display_and_set(result)
            self.expression = str(result)
            self.just_evaluated = True 
        except Exception as ex:
            print(f"Evaluate error: {ex}")
            self.display_var.set("Error")
            self.expression = ""
            self.just_evaluated = False
            self.mod_first = None
            self.power_first = None

    # --------- Rest of scientific ops (unchanged) ---------
    def show_square_root(self):
        try:
            if not self.expression.strip():
                self.display_var.set(constants.EMPTY_INPUT)
                return
            value = self._convert_number(eval(self.expression))
            if value < 0:
                self.display_var.set(constants.INVALID_INPUT)
                return
            result = self._convert_number(sqrt(value))
            sqrt_expr = f"√({value})"
            self.total_var.set(sqrt_expr)
            self.fit_display_and_set(result)
            self.expression = str(result)
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def show_square(self):
        if self.overflowed:
            return

        try:
            if not self.expression.strip():
                self.display_var.set(constants.EMPTY_INPUT)
                return

            value = self._convert_number(eval(self.expression))
            result = self._convert_number(value ** 2)
            square_expr = f"({value})²"
            self.total_var.set(square_expr)

            result_str = str(result)
            if len(result_str) > constants.MAX_DISPLAY_CHARS * 2:
                self.display_var.set("Overflow")
                self.total_var.set("")
                self.expression = ""
                self.overflowed = True
                return

            self.safe_set_result(result)
            self.fit_display_and_set(result)
            self.expression = str(result)

        except Exception:
            self.display_var.set("Overflow")
            self.total_var.set("")
            self.expression = ""
            self.overflowed = True

    def show_cube(self):
        if self.overflowed:
            return

        try:
            if not self.expression.strip():
                self.display_var.set(constants.EMPTY_INPUT)
                return

            value = self._convert_number(eval(self.expression))
            result = self._convert_number(value ** 3)
            cube_expr = f"({value})³"
            self.total_var.set(cube_expr)

            result_str = str(result)
            if len(result_str) > constants.MAX_DISPLAY_CHARS * 2:
                self.display_var.set("Overflow")
                self.total_var.set("")
                self.expression = ""
                self.overflowed = True
                return

            self.safe_set_result(result)
            self.fit_display_and_set(result)
            self.expression = str(result)

        except Exception:
            self.display_var.set("Overflow")
            self.total_var.set("")
            self.expression = ""
            self.overflowed = True

    def show_cube_root(self):
        try:
            if not self.expression.strip():
                self.display_var.set(constants.EMPTY_INPUT)
                return
            value = self._convert_number(eval(self.expression))
            if value < 0:
                result = -((-value) ** (1/3))
            else:
                result = value ** (1/3)
            cbrt_expr = f"∛({value})"
            self.total_var.set(cbrt_expr)
            self.fit_display_and_set(self._convert_number(result))
            self.expression = str(result)
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def show_factorial(self):
        if hasattr(self, constants.OVERFLOWED) and self.overflowed:
            return

        try:
            if not self.expression.strip():
                self.display_var.set(constants.EMPTY_INPUT)
                return

            value = eval(self.expression)
            if not (isinstance(value, int) or (isinstance(value, float) and value.is_integer())) or value < 0:
                self.display_var.set(constants.INVALID_INPUT)
                return

            n = int(value)

            try:
                result = factorial(n)
            except (OverflowError, MemoryError):
                self.display_var.set("Overflow")
                self.total_var.set("")
                self.expression = ""
                self.overflowed = True
                return

            self.total_var.set(f"fact({n})")

            try:
                f_result = float(result)
                if f_result >= 1e10:
                    self.display_var.set("{:.10e}".format(f_result))
                else:
                    self.fit_display_and_set(result)
                self.expression = str(result)
            except (OverflowError, MemoryError, ValueError):
                self.display_var.set("Overflow")
                self.total_var.set("")
                self.expression = ""
                self.overflowed = True

        except Exception:
            self.display_var.set("Error")
            self.total_var.set("")
            self.expression = ""


    def show_power(self):
        if self.expression:
            self.power_first = self.expression
            self.expression = ""
            self.display_var.set(self.power_first)
            self.total_var.set(f"{self.power_first}^")

    def show_absolute(self):
        try:
            if not self.expression.strip():
                self.display_var.set(constants.EMPTY_INPUT)
                return
            value = eval(self.expression)
            if not isinstance(value, (int, float)):
                self.display_var.set(constants.INVALID_INPUT)
                return
            result = abs(value)
            abs_expr = f"|{value}|"
            self.total_var.set(abs_expr)
            self.fit_display_and_set(result)
            self.expression = str(result)
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def reciprocal(self):
        try:
            if not self.expression.strip():
                self.display_var.set(constants.EMPTY_INPUT)
                return
            value = float(eval(self.expression))
            if value == 0:
                self.display_var.set(constants.ZERO_DIVISION)
                return
            result = 1 / value
            reciprocal_expr = f"1/({value})"
            self.total_var.set(reciprocal_expr)
            self.fit_display_and_set(result)
            self.expression = str(result)
        except Exception as e:
            print(f"Error occurred: {e}")
            self.display_var.set("Error")
            self.expression = ""

    def key_input(self, event):
        key = event.char
        if key.isdigit() or key in ".+-*/()%":
            self.add(key)
        elif key == "^":
            self.show_power()
        elif key in ("e", "E"):
            self.add("e")
        elif key == "":
            self.evaluate()
        elif event.keysym == "BackSpace":
            self.backspace()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scientific Calculator")
    root.geometry("460x680")
    root.configure(bg="#f9f9f9")

    ScientificCalculator(root)
    root.configure(padx=10, pady=10)
    root.mainloop()
