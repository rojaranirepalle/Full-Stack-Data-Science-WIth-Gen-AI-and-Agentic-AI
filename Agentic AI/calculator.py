"""Simple calculator GUI built with tkinter."""

import re
import tkinter as tk
from tkinter import font as tkfont


def safe_eval(expression: str) -> float:
    """Evaluate a math expression containing only digits and + - * / . ( )."""
    cleaned = expression.replace("×", "*").replace("÷", "/")
    if not re.fullmatch(r"[\d+\-*/().\s]+", cleaned):
        raise ValueError("invalid expression")
    if cleaned.count("(") != cleaned.count(")"):
        raise ValueError("mismatched parentheses")
    return eval(cleaned, {"__builtins__": {}}, {})


class Calculator(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")

        display_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
        button_font = tkfont.Font(family="Helvetica", size=16)

        self._expression = tk.StringVar(value="0")
        self._display = tk.Entry(
            self,
            textvariable=self._expression,
            font=display_font,
            justify="right",
            bd=0,
            readonlybackground="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            state="readonly",
        )
        self._display.grid(row=0, column=0, columnspan=4, padx=12, pady=(12, 8), sticky="nsew", ipady=16)

        buttons = [
            ("C", self._clear, "#f38ba8", "#11111b"),
            ("⌫", self._backspace, "#fab387", "#11111b"),
            ("(", lambda: self._append("("), "#585b70", "#cdd6f4"),
            (")", lambda: self._append(")"), "#585b70", "#cdd6f4"),
            ("7", lambda: self._append("7"), "#45475a", "#cdd6f4"),
            ("8", lambda: self._append("8"), "#45475a", "#cdd6f4"),
            ("9", lambda: self._append("9"), "#45475a", "#cdd6f4"),
            ("÷", lambda: self._append("÷"), "#89b4fa", "#11111b"),
            ("4", lambda: self._append("4"), "#45475a", "#cdd6f4"),
            ("5", lambda: self._append("5"), "#45475a", "#cdd6f4"),
            ("6", lambda: self._append("6"), "#45475a", "#cdd6f4"),
            ("×", lambda: self._append("×"), "#89b4fa", "#11111b"),
            ("1", lambda: self._append("1"), "#45475a", "#cdd6f4"),
            ("2", lambda: self._append("2"), "#45475a", "#cdd6f4"),
            ("3", lambda: self._append("3"), "#45475a", "#cdd6f4"),
            ("−", lambda: self._append("-"), "#89b4fa", "#11111b"),
            ("0", lambda: self._append("0"), "#45475a", "#cdd6f4"),
            (".", lambda: self._append("."), "#45475a", "#cdd6f4"),
            ("+", lambda: self._append("+"), "#89b4fa", "#11111b"),
            ("=", self._equals, "#a6e3a1", "#11111b"),
        ]

        row, col = 1, 0
        for label, command, bg, fg in buttons:
            width = 4 if label == "0" else (8 if label == "=" else 4)
            colspan = 2 if label == "0" else (4 if label == "=" else 1)
            btn = tk.Button(
                self,
                text=label,
                command=command,
                font=button_font,
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                relief="flat",
                width=width,
                height=2,
            )
            btn.grid(row=row, column=col, columnspan=colspan, padx=4, pady=4, sticky="nsew")
            col += colspan
            if col >= 4:
                col = 0
                row += 1

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        self.bind("<Key>", self._on_key)
        self.bind("<Return>", lambda _e: self._equals())
        self.bind("<Escape>", lambda _e: self._clear())

    def _set_expression(self, value: str) -> None:
        self._expression.set(value)

    def _current(self) -> str:
        return self._expression.get()

    def _append(self, char: str) -> None:
        current = self._current()
        if current == "0" and char not in "+−-×÷().":
            self._set_expression(char)
        elif current == "Error":
            self._set_expression(char if char not in "+−-×÷" else "0" + char)
        else:
            self._set_expression(current + char)

    def _clear(self) -> None:
        self._set_expression("0")

    def _backspace(self) -> None:
        current = self._current()
        if current in ("0", "Error"):
            return
        if len(current) == 1:
            self._set_expression("0")
        else:
            self._set_expression(current[:-1])

    def _equals(self) -> None:
        expr = self._current()
        if expr in ("0", "Error", ""):
            return
        try:
            result = safe_eval(expr)
            if result == int(result):
                self._set_expression(str(int(result)))
            else:
                self._set_expression(str(round(result, 10)).rstrip("0").rstrip("."))
        except ZeroDivisionError:
            self._set_expression("Error")
        except (ValueError, SyntaxError, TypeError, ArithmeticError):
            self._set_expression("Error")

    def _on_key(self, event: tk.Event) -> None:
        char = event.char
        keys = {
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            ".": ".",
            "+": "+",
            "-": "-",
            "*": "×",
            "/": "÷",
            "(": "(",
            ")": ")",
        }
        if char in keys:
            self._append(keys[char])
        elif event.keysym == "BackSpace":
            self._backspace()


def main() -> None:
    app = Calculator()
    app.mainloop()


if __name__ == "__main__":
    main()
